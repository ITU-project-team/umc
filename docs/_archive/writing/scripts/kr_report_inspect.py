"""KR 보고서 docx의 paragraph/table/이미지/캡션/cross-ref 매핑을 JSON manifest로 추출."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import docx
from docx.oxml.ns import qn

FIG_RE = re.compile(r"(?<![A-Za-z])(Figure|Fig\.|figure|그림)\s*(\d+)")
TBL_RE = re.compile(r"(?<![A-Za-z])(Table|table|표)\s*(\d+)")
FIG_CAP_RE = re.compile(r"^\s*(?:\[?)\s*(Figure|Fig\.|그림)\s*(\d+)\s*[\].:]?\s*(.*?)\s*$")
TBL_CAP_RE = re.compile(r"^\s*(?:\[?)\s*(Table|표)\s*(\d+)\s*[\].:]?\s*(.*?)\s*$")
HEAD_NUM_RE = re.compile(r"^(\d+(?:\.\d+){0,2})\b\s*(.*)")


def extract_text(elem) -> str:
    """Sum only w:t leaf text. Avoid lxml's element.text caching artifact
    that makes Word XML appear duplicated when the parent w:p / w:r have
    stray .text values set."""
    parts = []
    for desc in elem.iter():
        tlocal = desc.tag.split("}", 1)[-1] if isinstance(desc.tag, str) else ""
        if tlocal == "t":
            parts.append(desc.text or "")
    return "".join(parts).strip()


def has_drawing(elem) -> bool:
    return bool(elem.findall(".//" + qn("w:drawing")))


def collect_runs(p_elem) -> list[dict]:
    runs = []
    for i, r in enumerate(p_elem.findall(qn("w:r"))):
        text = "".join(t.text or "" for t in r.findall(qn("w:t")))
        runs.append({"i": i, "text": text})
    return runs


def inspect(path: Path) -> dict:
    d = docx.Document(str(path))
    body = d.element.body

    items: list[dict] = []
    para_idx = 0
    table_idx = 0
    seq = 0
    for child in body.iterchildren():
        tag = child.tag.split("}", 1)[-1]
        if tag == "p":
            txt = extract_text(child)
            drawings = len(child.findall(".//" + qn("w:drawing")))
            style = None
            pPr = child.find(qn("w:pPr"))
            if pPr is not None:
                ps = pPr.find(qn("w:pStyle"))
                if ps is not None:
                    style = ps.get(qn("w:val"))
            entry = {
                "seq": seq,
                "kind": "p",
                "para_idx": para_idx,
                "style": style,
                "text": txt,
                "text_preview": txt[:160],
                "drawings": drawings,
                "runs": collect_runs(child),
            }
            # caption detection
            mfig = FIG_CAP_RE.match(txt)
            mtbl = TBL_CAP_RE.match(txt)
            if mfig and len(txt) < 600:
                entry["caption_kind"] = "FIG"
                entry["caption_old_num"] = int(mfig.group(2))
                entry["caption_title_raw"] = mfig.group(3)
            elif mtbl and len(txt) < 600:
                entry["caption_kind"] = "TBL"
                entry["caption_old_num"] = int(mtbl.group(2))
                entry["caption_title_raw"] = mtbl.group(3)
            # heading detection
            mh = HEAD_NUM_RE.match(txt)
            if mh and len(txt) < 80 and len(mh.group(1).split(".")) <= 3:
                entry["heading_num"] = mh.group(1)
                entry["heading_title"] = mh.group(2)
            # references in body text
            fig_refs = [(m.start(), m.end(), int(m.group(2)), m.group(0))
                        for m in FIG_RE.finditer(txt)]
            tbl_refs = [(m.start(), m.end(), int(m.group(2)), m.group(0))
                        for m in TBL_RE.finditer(txt)]
            if fig_refs:
                entry["fig_refs"] = fig_refs
            if tbl_refs:
                entry["tbl_refs"] = tbl_refs
            items.append(entry)
            para_idx += 1
        elif tag == "tbl":
            preview = extract_text(child).replace("\n", " / ")[:200]
            rows = len(child.findall(qn("w:tr")))
            # first row first cell preview
            first_tr = child.find(qn("w:tr"))
            header_cells = []
            if first_tr is not None:
                for tc in first_tr.findall(qn("w:tc")):
                    header_cells.append(extract_text(tc)[:80])
            # detect drawings inside table
            tbl_drawings = len(child.findall(".//" + qn("w:drawing")))
            items.append({
                "seq": seq,
                "kind": "tbl",
                "table_idx": table_idx,
                "rows": rows,
                "header_cells": header_cells,
                "preview": preview,
                "drawings_inside": tbl_drawings,
            })
            table_idx += 1
        elif tag == "sectPr":
            items.append({"seq": seq, "kind": "sectPr"})
        seq += 1

    # first body reference per number, in reading order
    first_fig_ref: dict[int, int] = {}
    first_tbl_ref: dict[int, int] = {}
    for it in items:
        if it["kind"] == "p":
            for ref in it.get("fig_refs", []):
                n = ref[2]
                if n not in first_fig_ref:
                    first_fig_ref[n] = it["seq"]
            for ref in it.get("tbl_refs", []):
                n = ref[2]
                if n not in first_tbl_ref:
                    first_tbl_ref[n] = it["seq"]

    return {
        "source": str(path),
        "paragraph_count": para_idx,
        "table_count": table_idx,
        "items": items,
        "first_fig_ref": first_fig_ref,
        "first_tbl_ref": first_tbl_ref,
    }


def summarize(manifest: dict) -> str:
    lines = []
    lines.append(f"# inspect summary: {manifest['source']}")
    lines.append(f"paragraphs={manifest['paragraph_count']}, tables={manifest['table_count']}")
    lines.append("")
    lines.append("## Figure captions / images / Table objects (in body order)")
    for it in manifest["items"]:
        if it["kind"] == "p":
            if it.get("caption_kind"):
                lines.append(f"  seq{it['seq']:>4} p#{it['para_idx']:>3} [{it.get('style')}] CAPTION {it['caption_kind']} old#{it['caption_old_num']} | {it['text_preview']}")
            elif it["drawings"]:
                lines.append(f"  seq{it['seq']:>4} p#{it['para_idx']:>3} IMG drawings={it['drawings']} text='{it['text_preview']}'")
        elif it["kind"] == "tbl":
            lines.append(f"  seq{it['seq']:>4} TABLE t#{it['table_idx']} rows={it['rows']} drawings={it['drawings_inside']} preview='{it['preview'][:140]}'")
    lines.append("")
    lines.append("## First body refs (number -> seq)")
    fig = manifest["first_fig_ref"]
    tbl = manifest["first_tbl_ref"]
    lines.append("  Figure refs: " + ", ".join(f"{n}@{s}" for n, s in sorted(fig.items(), key=lambda x: x[1])))
    lines.append("  Table refs: " + ", ".join(f"{n}@{s}" for n, s in sorted(tbl.items(), key=lambda x: x[1])))
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: kr_report_inspect.py <input.docx> <output.json> [<summary.txt>]")
        return 2
    src = Path(argv[1])
    dst = Path(argv[2])
    summary = Path(argv[3]) if len(argv) >= 4 else None
    manifest = inspect(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    text = summarize(manifest)
    if summary:
        summary.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
