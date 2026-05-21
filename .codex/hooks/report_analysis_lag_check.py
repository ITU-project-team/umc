#!/usr/bin/env python3
"""Warning-only UMC report/analysis synchronization checker."""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONFIG_RELATIVE_PATH = Path(".codex/config/report_analysis_lag.json")
GIT_TIMEOUT_SECONDS = 8
LOG_SCAN_LIMIT = 200


@dataclass
class GitStatusEntry:
    status: str
    paths: list[str]


def run_git(repo: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    command = ["git", "-C", str(repo), *args]
    try:
        return subprocess.run(
            command,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(
            command,
            124,
            "",
            f"git command timed out after {GIT_TIMEOUT_SECONDS}s",
        )


def script_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip("/")


def matches_glob(path: str, pattern: str) -> bool:
    path = normalize_path(path)
    pattern = normalize_path(pattern)
    if not path or not pattern:
        return False
    if fnmatch.fnmatchcase(path, pattern):
        return True
    if pattern.startswith("**/"):
        return matches_glob(path, pattern[3:])
    if pattern.endswith("/**"):
        prefix = pattern[:-3].rstrip("/")
        return path == prefix or path.startswith(prefix + "/")
    return False


def path_is_included(path: str, include_globs: list[str], exclude_globs: list[str]) -> bool:
    path = normalize_path(path)
    if any(matches_glob(path, pattern) for pattern in exclude_globs):
        return False
    return any(matches_glob(path, pattern) for pattern in include_globs)


def parse_status_z(raw: str) -> list[GitStatusEntry]:
    parts = raw.split("\0")
    entries: list[GitStatusEntry] = []
    index = 0
    while index < len(parts):
        item = parts[index]
        if not item:
            index += 1
            continue

        status = item[:2]
        path = item[3:] if len(item) > 3 else ""
        paths = [normalize_path(path)] if path else []

        if ("R" in status or "C" in status) and index + 1 < len(parts):
            index += 1
            original_path = parts[index]
            if original_path:
                paths.append(normalize_path(original_path))

        entries.append(GitStatusEntry(status=status, paths=paths))
        index += 1
    return entries


def git_status_entries(repo: Path) -> tuple[list[GitStatusEntry], str | None]:
    result = run_git(repo, ["status", "--porcelain", "-z", "--untracked-files=all"])
    if result.returncode != 0:
        return [], result.stderr.strip() or "git status failed"
    return parse_status_z(result.stdout), None


def commit_result(value: str) -> dict[str, Any]:
    timestamp_text, _, commit = value.partition("|")
    try:
        timestamp = int(timestamp_text)
    except ValueError:
        return {"timestamp": None, "iso": None, "commit": commit or None, "error": "invalid timestamp"}

    iso = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    return {"timestamp": timestamp, "iso": iso, "commit": commit or None, "error": None}


def latest_commit(
    repo: Path,
    include_globs: list[str],
    exclude_globs: list[str],
    pathspecs: list[str],
) -> dict[str, Any]:
    if not pathspecs:
        return {"timestamp": None, "iso": None, "commit": None, "error": None}

    result = run_git(
        repo,
        [
            "log",
            f"--max-count={LOG_SCAN_LIMIT}",
            "--format=commit:%ct|%H",
            "--name-only",
            "--",
            *pathspecs,
        ],
    )
    if result.returncode != 0:
        return {"timestamp": None, "iso": None, "commit": None, "error": result.stderr.strip()}

    current_commit: str | None = None
    touched_paths: list[str] = []

    def current_commit_matches() -> bool:
        return any(path_is_included(path, include_globs, exclude_globs) for path in touched_paths)

    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("commit:"):
            if current_commit is not None and current_commit_matches():
                return commit_result(current_commit)
            current_commit = line.removeprefix("commit:")
            touched_paths = []
            continue
        touched_paths.append(normalize_path(line))

    if current_commit is not None and current_commit_matches():
        return commit_result(current_commit)

    return {"timestamp": None, "iso": None, "commit": None, "error": None}


def configured_repo_path(project_root: Path, configured_path: str) -> Path:
    raw_path = Path(configured_path)
    if raw_path.is_absolute():
        raise ValueError("absolute repo paths are not allowed")
    repo_path = (project_root / raw_path).resolve()
    if not is_relative_to(repo_path, project_root):
        raise ValueError("repo path escapes project root")
    return repo_path


def summarize_repo(
    project_root: Path,
    repo_config: dict[str, Any],
    exclude_globs: list[str],
    max_examples: int,
) -> dict[str, Any]:
    repo_path_text = str(repo_config["path"])
    summary: dict[str, Any] = {
        "id": repo_config.get("id"),
        "label": repo_config.get("label"),
        "path": repo_path_text,
        "exists": False,
        "git_status_ok": False,
        "relevant_dirty_count": 0,
        "relevant_dirty_path_examples": [],
        "latest_relevant_commit": {"timestamp": None, "iso": None, "commit": None, "error": None},
        "error": None,
    }

    try:
        repo_path = configured_repo_path(project_root, repo_path_text)
    except ValueError as exc:
        summary["error"] = str(exc)
        return summary

    summary["exists"] = repo_path.exists()

    if not repo_path.exists():
        summary["error"] = "path not found"
        return summary

    entries, status_error = git_status_entries(repo_path)
    if status_error is not None:
        summary["error"] = status_error
        return summary

    summary["git_status_ok"] = True
    include_globs = repo_config.get("include_globs", [])
    relevant_paths: list[str] = []
    for entry in entries:
        entry_paths = [
            path
            for path in entry.paths
            if path_is_included(path, include_globs, exclude_globs)
        ]
        if entry_paths:
            relevant_paths.extend(entry_paths)

    unique_paths = sorted(set(relevant_paths))
    summary["relevant_dirty_count"] = len(unique_paths)
    summary["relevant_dirty_path_examples"] = unique_paths[:max_examples]
    summary["latest_relevant_commit"] = latest_commit(
        repo_path,
        include_globs,
        exclude_globs,
        repo_config.get("commit_pathspecs", []),
    )
    return summary


def warning_context(summary: dict[str, Any]) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    dirty_analysis = [
        repo for repo in summary["analysis_repositories"] if repo["relevant_dirty_count"] > 0
    ]

    if summary["warning_policy"].get("warn_on_relevant_analysis_dirty", True) and dirty_analysis:
        repo_text = ", ".join(
            f"{repo['path']} ({repo['relevant_dirty_count']})" for repo in dirty_analysis
        )
        warnings.append(
            {
                "code": "analysis_dirty",
                "message": f"Report-relevant analysis worktree changes are present: {repo_text}.",
            }
        )

    latest_analysis = summary["latest_analysis_commit"]
    latest_root = summary["root_report_repository"]["latest_relevant_commit"]
    compare_enabled = summary["warning_policy"].get(
        "warn_when_latest_analysis_commit_is_newer_than_latest_root_report_commit",
        True,
    )
    if (
        compare_enabled
        and latest_analysis["timestamp"] is not None
        and (
            latest_root["timestamp"] is None
            or latest_analysis["timestamp"] > latest_root["timestamp"]
        )
    ):
        root_time = latest_root["iso"] or "none"
        root_dirty = summary["root_report_repository"]["relevant_dirty_count"]
        warnings.append(
            {
                "code": "analysis_commit_newer_than_report",
                "message": (
                    "Latest relevant analysis commit "
                    f"({latest_analysis['repo_path']} at {latest_analysis['iso']}) "
                    f"is newer than latest root report-facing commit ({root_time}); "
                    f"root report-facing dirty path count is {root_dirty}."
                ),
            }
        )

    return warnings


def build_summary(project_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    exclude_globs = config.get("privacy", {}).get("exclude_globs", [])
    policy = config.get("warning_policy", {})
    max_examples = int(policy.get("max_reported_path_examples_per_repo", 8))

    analysis_summaries = [
        summarize_repo(project_root, repo_config, exclude_globs, max_examples)
        for repo_config in config.get("analysis_repositories", [])
    ]
    root_summary = summarize_repo(
        project_root,
        {
            "id": "root_report",
            "label": "Root report repository",
            **config["root_report_repository"],
        },
        exclude_globs,
        max_examples,
    )

    latest_analysis = {"timestamp": None, "iso": None, "commit": None, "repo_path": None}
    for repo in analysis_summaries:
        commit = repo.get("latest_relevant_commit", {})
        timestamp = commit.get("timestamp")
        if timestamp is not None and (
            latest_analysis["timestamp"] is None or timestamp > latest_analysis["timestamp"]
        ):
            latest_analysis = {
                "timestamp": timestamp,
                "iso": commit.get("iso"),
                "commit": commit.get("commit"),
                "repo_path": repo["path"],
            }

    summary = {
        "status": "ok",
        "project_root": str(project_root),
        "privacy_rule": config.get("privacy", {}).get("output_rule"),
        "analysis_repositories": analysis_summaries,
        "root_report_repository": root_summary,
        "latest_analysis_commit": latest_analysis,
        "warning_policy": policy,
        "warnings": [],
    }
    summary["warnings"] = warning_context(summary)
    if summary["warnings"]:
        summary["status"] = "warning"
    return summary


def concise_warning(summary: dict[str, Any]) -> str:
    warnings = summary.get("warnings", [])
    if not warnings:
        return "UMC report-analysis lag check: no warnings."

    dirty_repo_count = sum(
        1 for repo in summary["analysis_repositories"] if repo["relevant_dirty_count"] > 0
    )
    dirty_path_count = sum(repo["relevant_dirty_count"] for repo in summary["analysis_repositories"])
    root_dirty = summary["root_report_repository"]["relevant_dirty_count"]
    parts = ["UMC report-analysis lag warning:"]
    if dirty_repo_count:
        parts.append(
            f"{dirty_repo_count} analysis repo(s) have {dirty_path_count} report-relevant dirty path(s)."
        )

    latest_analysis = summary["latest_analysis_commit"]
    latest_root = summary["root_report_repository"]["latest_relevant_commit"]
    if latest_analysis["timestamp"] is not None and (
        latest_root["timestamp"] is None
        or latest_analysis["timestamp"] > latest_root["timestamp"]
    ):
        parts.append(
            "Latest relevant analysis commit "
            f"({latest_analysis['repo_path']} at {latest_analysis['iso']}) "
            f"is newer than latest root report-facing commit ({latest_root['iso'] or 'none'})."
        )

    parts.append(f"Root report-facing dirty path count: {root_dirty}.")
    parts.append("Verify report handoff, update report-facing artifacts if needed, then commit analysis and root repos separately.")
    return " ".join(parts)


def print_human(summary: dict[str, Any]) -> None:
    print("UMC report-analysis lag check")
    print(f"Status: {summary['status'].upper()}")
    print(f"Project root: {summary['project_root']}")
    print()
    print("Analysis repositories:")
    for repo in summary["analysis_repositories"]:
        latest = repo["latest_relevant_commit"]["iso"] or "none"
        print(
            f"- {repo['path']}: {repo['relevant_dirty_count']} relevant dirty path(s); "
            f"latest relevant commit: {latest}"
        )
    root = summary["root_report_repository"]
    root_latest = root["latest_relevant_commit"]["iso"] or "none"
    print(
        f"- root report-facing paths: {root['relevant_dirty_count']} relevant dirty path(s); "
        f"latest relevant commit: {root_latest}"
    )
    print()
    if summary["warnings"]:
        print("Warnings:")
        for warning in summary["warnings"]:
            print(f"- {warning['message']}")
        print()
        print("Next: verify the analysis-to-report handoff, update report-facing root artifacts if needed, and keep nested analysis commits separate from root report commits.")
    else:
        print("No report-analysis lag warnings.")


def hook_output(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "continue": True,
        "systemMessage": concise_warning(summary),
    }


def print_hook_continue() -> None:
    print(json.dumps({"continue": True}, ensure_ascii=True, separators=(",", ":")))


def load_payload() -> dict[str, Any]:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def load_config(project_root: Path) -> dict[str, Any] | None:
    config_path = project_root / CONFIG_RELATIVE_PATH
    if not config_path.exists():
        return None
    return json.loads(config_path.read_text(encoding="utf-8"))


def project_markers_present(project_root: Path, config: dict[str, Any]) -> bool:
    markers = config.get("project", {}).get("root_marker_paths", [])
    return all((project_root / marker).exists() for marker in markers)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check UMC report-analysis synchronization lag.")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON summary")
    parser.add_argument("--hook", choices=["stop"], help="emit warning-only Stop-hook JSON")
    parser.add_argument("--strict", action="store_true", help="exit 1 when warnings exist")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    project_root = script_project_root()
    payload = load_payload() if args.hook else {}
    payload_cwd = payload.get("cwd")

    if args.hook:
        if not isinstance(payload_cwd, str) or not payload_cwd:
            print_hook_continue()
            return 0
        active_cwd = Path(payload_cwd).expanduser()
        if not active_cwd.is_absolute():
            print_hook_continue()
            return 0
    else:
        active_cwd = Path.cwd()

    outside_project = not is_relative_to(active_cwd, project_root)
    if args.hook and outside_project:
        return 0

    try:
        config = load_config(project_root)
    except Exception as exc:
        if args.hook:
            print_hook_continue()
            return 0
        print(f"Config read failed: {exc}", file=sys.stderr)
        return 2

    if config is None:
        if args.hook:
            print_hook_continue()
            return 0
        print(f"Config not found: {project_root / CONFIG_RELATIVE_PATH}", file=sys.stderr)
        return 2

    try:
        markers_present = project_markers_present(project_root, config)
    except Exception as exc:
        if args.hook:
            print_hook_continue()
            return 0
        print(f"Project marker check failed: {exc}", file=sys.stderr)
        return 2

    if args.hook and not markers_present:
        print_hook_continue()
        return 0

    try:
        summary = build_summary(project_root, config)
    except Exception as exc:
        if args.hook:
            print_hook_continue()
            return 0
        print(f"Summary build failed: {exc}", file=sys.stderr)
        return 2
    if outside_project:
        summary["skipped_current_workdir_outside_project"] = True

    if args.hook:
        if summary["warnings"]:
            print(json.dumps(hook_output(summary), ensure_ascii=True, separators=(",", ":")))
        else:
            print_hook_continue()
        return 0

    if args.json:
        print(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True))
    else:
        print_human(summary)

    if args.strict and summary["warnings"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
