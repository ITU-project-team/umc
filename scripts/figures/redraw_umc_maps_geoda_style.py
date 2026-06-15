#!/usr/bin/env python3
"""Redraw UMC map figures from the Part 1 source table and Seoul boundary."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Patch
from matplotlib.patches import Polygon as MplPolygon
import numpy as np
import pandas as pd


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "figures"

DEFAULT_PART1_ROOTS = [
    WORKSPACE_ROOT / "analysis" / "part 1",
    Path("/Users/ujunbin/project/umc/analysis/part 1"),
]

DIMENSIONS = [
    ("score_Infrastructure", "Connectivity"),
    ("score_Available_for_Use", "Available for Use"),
    ("score_Affordability", "Affordability"),
    ("score_Devices", "Devices"),
    ("score_Digital_Skills", "Digital Skills"),
    ("score_Safety", "Safety"),
]

DIMENSION_SLUGS = {
    "score_Infrastructure": "connectivity",
    "score_Available_for_Use": "available_for_use",
    "score_Affordability": "affordability",
    "score_Devices": "devices",
    "score_Digital_Skills": "digital_skills",
    "score_Safety": "safety",
}

QUINTILE_COLORS = ["#d73027", "#fc8d59", "#fee08b", "#91cf60", "#1a9850"]
GEODA_CLUSTER_COLORS = {
    "High-High": "#e31a1c",
    "Low-Low": "#1f78b4",
    "High-Low": "#fdbf6f",
    "Low-High": "#a6cee3",
    "Not significant": "#f7f7f7",
}
EDGE = "#5f5f5f"
INK = "#1f2933"
GRID = "#d7d7d7"

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.dpi": 300,
    }
)


def resolve_part1_root() -> Path:
    env_root = os.environ.get("UMC_PART1_ROOT")
    roots = [Path(env_root)] if env_root else []
    roots.extend(DEFAULT_PART1_ROOTS)
    for root in roots:
        if (
            (root / "scripts" / "generate_section31_figures.py").is_file()
            and (root / "output" / "tables" / "seoul_umc_scores_v7_2024.csv").is_file()
        ):
            return root
    raise FileNotFoundError("Could not find Part 1 script and 2024 score table.")


def load_part1_module(part1_root: Path):
    script = part1_root / "scripts" / "generate_section31_figures.py"
    spec = importlib.util.spec_from_file_location("section31_figures", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_patches(geometry: dict[int, dict[str, object]], codes: list[int]) -> tuple[list[MplPolygon], list[int]]:
    patches: list[MplPolygon] = []
    patch_codes: list[int] = []
    for code in codes:
        for ring in geometry[code]["rings"]:
            patches.append(MplPolygon(ring, closed=True))
            patch_codes.append(code)
    return patches, patch_codes


def set_map_limits(ax, geometry: dict[int, dict[str, object]]) -> None:
    bounds = np.array([item["bounds"] for item in geometry.values()], dtype=float)
    x0, y0 = bounds[:, 0].min(), bounds[:, 1].min()
    x1, y1 = bounds[:, 2].max(), bounds[:, 3].max()
    pad_x = (x1 - x0) * 0.04
    pad_y = (y1 - y0) * 0.04
    ax.set_xlim(x0 - pad_x, x1 + pad_x)
    ax.set_ylim(y0 - pad_y, y1 + pad_y)
    ax.set_aspect("equal")
    ax.axis("off")


def draw_map(
    ax,
    geometry: dict[int, dict[str, object]],
    codes: list[int],
    colors: dict[int, str],
    *,
    label_codes: set[int] | None = None,
    gu_name: dict[int, str],
    linewidth: float = 0.75,
) -> PatchCollection:
    patches, patch_codes = make_patches(geometry, codes)
    collection = PatchCollection(
        patches,
        facecolor=[colors[code] for code in patch_codes],
        edgecolor=EDGE,
        linewidth=linewidth,
    )
    ax.add_collection(collection)
    set_map_limits(ax, geometry)
    for code in sorted(label_codes or set()):
        x, y = geometry[code]["centroid"]
        ax.text(
            x,
            y,
            gu_name[code],
            ha="center",
            va="center",
            fontsize=7.2,
            color=INK,
            path_effects=[pe.withStroke(linewidth=2.4, foreground="white")],
        )
    return collection


def load_score_table(part1_root: Path, year: int) -> pd.DataFrame:
    path = part1_root / "output" / "tables" / f"seoul_umc_scores_v7_{year}.csv"
    df = pd.read_csv(path, encoding="utf-8-sig").copy()
    return df.assign(district_code=df["district_code"].astype(int))


def save_quintile_choropleth(
    df: pd.DataFrame,
    geometry: dict[int, dict[str, object]],
    mod,
    *,
    year: int,
) -> Path:
    d = df.sort_values("score_UMC", ascending=True).reset_index(drop=True)
    d["quintile_group"] = (np.arange(len(d)) // 5) + 1
    group_by_code = dict(zip(d["district_code"].astype(int), d["quintile_group"].astype(int)))
    colors = {code: QUINTILE_COLORS[group_by_code[code] - 1] for code in d["district_code"].astype(int)}
    codes = sorted(d["district_code"].astype(int).tolist())
    label_codes = set(d.head(5)["district_code"].astype(int)) | set(d.tail(5)["district_code"].astype(int))

    fig, ax = plt.subplots(figsize=(9.2, 5.9))
    draw_map(ax, geometry, codes, colors, label_codes=label_codes, gu_name=mod.GU_NAME, linewidth=0.78)
    ax.set_title(f"UMC Composite Score, {year}: Five-District Step Groups", fontsize=13, pad=10)

    handles = []
    for group in range(1, 6):
        sub = d[d["quintile_group"] == group]
        label = f"G{group}: {sub['score_UMC'].min():.3f}-{sub['score_UMC'].max():.3f}"
        if group == 1:
            label += " (lowest)"
        if group == 5:
            label += " (highest)"
        handles.append(Patch(facecolor=QUINTILE_COLORS[group - 1], edgecolor=EDGE, label=label))
    ax.legend(
        handles=handles,
        loc="center left",
        bbox_to_anchor=(1.015, 0.5),
        ncol=1,
        frameon=False,
        fontsize=8.7,
        handlelength=1.6,
        borderaxespad=0.0,
    )
    fig.text(
        0.5,
        0.018,
        "Classes are rank-based groups of five districts; lower UMC scores are red and higher scores are green.",
        ha="center",
        fontsize=8.5,
        color="#555555",
    )
    fig.subplots_adjust(right=0.72, bottom=0.085)
    out = OUTPUT_DIR / f"fig_umc_composite_map_{year}_5district_red_green.png"
    fig.savefig(out, bbox_inches="tight", pad_inches=0.13, dpi=300)
    plt.close(fig)

    assignment = d[["district_code", "district", "score_UMC", "rank_UMC", "quintile_group"]]
    assignment.to_csv(OUTPUT_DIR / f"fig_umc_composite_map_{year}_5district_groups.csv", index=False, encoding="utf-8-sig")
    return out


def save_lisa_dimension_maps(
    df: pd.DataFrame,
    geometry: dict[int, dict[str, object]],
    mod,
    *,
    year: int,
) -> list[Path]:
    codes = sorted(df["district_code"].astype(int).tolist())
    indexed = df.assign(district_code=df["district_code"].astype(int)).set_index("district_code").loc[codes]
    neighbors = mod.build_neighbors(geometry)
    w = mod.row_standardized_weights(codes, neighbors)
    handles = [Patch(facecolor=color, edgecolor=INK, label=label) for label, color in GEODA_CLUSTER_COLORS.items()]
    outputs: list[Path] = []

    for var, label in DIMENSIONS:
        x = indexed[var].to_numpy(float)
        moran_i, p_global = mod.global_moran(x, w)
        clusters, _local_i, _p_local, _lag = mod.lisa_clusters(x, w, alpha=0.10)
        cluster_by_code = dict(zip(codes, clusters))
        colors_by_code = {code: GEODA_CLUSTER_COLORS[cluster_by_code[code]] for code in codes}
        sig_codes = {code for code, cluster in cluster_by_code.items() if cluster != "Not significant"}

        fig, ax = plt.subplots(figsize=(7.8, 4.65))
        draw_map(ax, geometry, codes, colors_by_code, label_codes=sig_codes, gu_name=mod.GU_NAME, linewidth=0.72)
        ax.set_title(f"{label} LISA Cluster Map, {year}\nI={moran_i:.2f}, p={p_global:.2f}", fontsize=12, pad=9)
        ax.legend(
            handles=handles,
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            frameon=False,
            fontsize=8.8,
            borderaxespad=0.0,
        )
        fig.text(
            0.5,
            0.025,
            "Queen contiguity weights; local clusters use 999 random permutations and alpha = 0.10.",
            ha="center",
            fontsize=8.1,
            color="#555555",
        )
        fig.subplots_adjust(right=0.74, bottom=0.10)
        out = OUTPUT_DIR / f"fig_lisa_{DIMENSION_SLUGS[var]}_{year}_geoda_map.png"
        fig.savefig(out, bbox_inches="tight", pad_inches=0.13, dpi=300)
        plt.close(fig)
        outputs.append(out)
    return outputs


def save_geoda_autocorrelation(df: pd.DataFrame, geometry: dict[int, dict[str, object]], mod) -> Path:
    codes = sorted(df["district_code"].astype(int).tolist())
    indexed = df.assign(district_code=df["district_code"].astype(int)).set_index("district_code").loc[codes]
    neighbors = mod.build_neighbors(geometry)
    w = mod.row_standardized_weights(codes, neighbors)

    fig, axes = plt.subplots(
        6,
        2,
        figsize=(10.8, 14.4),
        gridspec_kw={"width_ratios": [1.0, 1.15], "hspace": 0.42, "wspace": 0.08},
    )

    for row, (var, label) in enumerate(DIMENSIONS):
        x = indexed[var].to_numpy(float)
        moran_i, p_global = mod.global_moran(x, w)
        clusters, _local_i, p_local, lag = mod.lisa_clusters(x, w, alpha=0.10)
        z = (x - x.mean()) / x.std(ddof=0)
        cluster_by_code = dict(zip(codes, clusters))
        colors_by_code = {code: GEODA_CLUSTER_COLORS[cluster_by_code[code]] for code in codes}
        point_colors = [GEODA_CLUSTER_COLORS[c] for c in clusters]

        ax_s = axes[row, 0]
        ax_m = axes[row, 1]

        ax_s.scatter(z, lag, c=point_colors, edgecolor=INK, s=38, linewidth=0.55, zorder=3)
        xs = np.linspace(min(z) - 0.25, max(z) + 0.25, 100)
        ax_s.plot(xs, moran_i * xs, color=INK, linewidth=1.15)
        ax_s.axhline(0, color="#777777", linewidth=0.8)
        ax_s.axvline(0, color="#777777", linewidth=0.8)
        ax_s.grid(color=GRID, linewidth=0.45, alpha=0.75)
        ax_s.set_title(f"{label}: Moran Scatterplot", fontsize=10.2, pad=6)
        ax_s.set_xlabel("Standardized value", fontsize=8.5)
        ax_s.set_ylabel("Spatial lag", fontsize=8.5)
        ax_s.tick_params(labelsize=7.5)
        ax_s.text(
            0.03,
            0.97,
            f"I = {moran_i:.2f}\np = {p_global:.2f}",
            transform=ax_s.transAxes,
            ha="left",
            va="top",
            fontsize=8.1,
            bbox={"facecolor": "white", "edgecolor": "#bcbcbc", "boxstyle": "square,pad=0.25"},
        )
        sig_codes = {code for code, cluster in cluster_by_code.items() if cluster != "Not significant"}
        draw_map(ax_m, geometry, codes, colors_by_code, label_codes=sig_codes, gu_name=mod.GU_NAME, linewidth=0.65)
        ax_m.set_title(f"{label}: LISA Cluster Map", fontsize=10.2, pad=6)

    handles = [Patch(facecolor=color, edgecolor=INK, label=label) for label, color in GEODA_CLUSTER_COLORS.items()]
    fig.subplots_adjust(top=0.965, bottom=0.065, left=0.07, right=0.985)
    fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, fontsize=9.0, bbox_to_anchor=(0.5, 0.018))
    fig.suptitle("GeoDa-Style Spatial Autocorrelation Diagnostics by UMC Dimension, 2024", fontsize=14, y=0.995)
    fig.text(
        0.5,
        0.005,
        "Queen contiguity weights; LISA clusters use 999 random permutations and alpha = 0.10.",
        ha="center",
        fontsize=8.5,
        color="#555555",
    )
    out = OUTPUT_DIR / "fig_lisa_dimensions_geoda_style.png"
    fig.savefig(out, bbox_inches="tight", pad_inches=0.16, dpi=300)
    plt.close(fig)
    return out


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    part1_root = resolve_part1_root()
    mod = load_part1_module(part1_root)
    geometry = mod.load_geometry()
    outputs: list[Path] = []
    for year in (2023, 2024):
        df = load_score_table(part1_root, year)
        outputs.append(save_quintile_choropleth(df, geometry, mod, year=year))
        if year == 2023:
            outputs.extend(save_lisa_dimension_maps(df, geometry, mod, year=year))
    for out in outputs:
        print(out)


if __name__ == "__main__":
    main()
