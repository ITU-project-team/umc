#!/usr/bin/env python3
"""Regenerate report-facing UMC figures with a consistent compact style."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "docs" / "figures"
PART1_SCRIPT = ROOT / "analysis" / "part 1" / "scripts" / "generate_section31_figures.py"
PART1_TABLE = ROOT / "analysis" / "part 1" / "output" / "tables" / "seoul_umc_scores_v7_2024.csv"
BAYES_TABLE = ROOT / "analysis" / "part 3" / "02_bayesian" / "output" / "tables" / "bayesian_posterior_k20.csv"

BLUE = "#2F80ED"
CYAN = "#56CCF2"
ORANGE = "#F2994A"
RED = "#EB5757"
GREEN = "#27AE60"
PURPLE = "#9B51E0"
DARK = "#1F2937"
MID = "#6B7280"
GRID = "#E5E7EB"
LIGHT = "#F7F9FB"
EDGE = "#CBD5E1"

DIMENSIONS = [
    ("score_Infrastructure", "Connectivity"),
    ("score_Available_for_Use", "Available for Use"),
    ("score_Affordability", "Affordability"),
    ("score_Devices", "Devices"),
    ("score_Digital_Skills", "Digital Skills"),
    ("score_Safety", "Safety"),
]

BAYES_DIM_ORDER = [
    ("Connection Quality", "Connectivity"),
    ("Availability for Use", "Available for Use"),
    ("Affordability", "Affordability"),
    ("Devices", "Devices"),
    ("Digital Skills", "Digital Skills"),
    ("Safety & Security", "Safety"),
]

CLUSTER_COLORS = {
    "High-High": RED,
    "Low-Low": "#2D6A9F",
    "High-Low": ORANGE,
    "Low-High": "#7BC7C7",
    "Not significant": "#F3F4F6",
}

plt.rcParams.update(
    {
        "font.family": "Arial",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "figure.dpi": 160,
        "savefig.dpi": 300,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "axes.edgecolor": DARK,
        "axes.labelcolor": DARK,
        "xtick.color": DARK,
        "ytick.color": DARK,
        "text.color": DARK,
    }
)


def load_part1_module():
    spec = importlib.util.spec_from_file_location("section31_figures", PART1_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {PART1_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def save(fig: plt.Figure, name: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / name, bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)
    print(FIG_DIR / name)


def add_card(ax, x, y, w, h, text, color, fs=11, weight="bold", alpha=0.10):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.035",
        facecolor=color,
        edgecolor=color,
        linewidth=1.4,
        alpha=alpha,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight=weight, wrap=True)


def add_outline_card(ax, x, y, w, h, title, lines, color, fs=10.2):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.025,rounding_size=0.035",
        facecolor="white",
        edgecolor=color,
        linewidth=1.5,
        alpha=1.0,
    )
    ax.add_patch(patch)
    ax.text(x + 0.18, y + h - 0.30, title, ha="left", va="top", fontsize=fs + 0.6, weight="bold", color=color)
    ax.text(x + 0.18, y + h - 0.72, "\n".join(lines), ha="left", va="top", fontsize=fs, color=DARK, linespacing=1.35)


def arrow(ax, x1, y1, x2, y2, color=MID, rad=0.0):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.4,
            color=color,
            connectionstyle=f"arc3,rad={rad}",
        )
    )


def generate_project_overview():
    fig, ax = plt.subplots(figsize=(11.0, 6.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    add_card(ax, 0.3, 5.6, 2.4, 0.75, "Critical realism", BLUE, 11.5)
    add_card(ax, 3.1, 5.6, 3.1, 0.75, "ITU UMC", CYAN, 11.5)
    add_card(ax, 6.7, 5.6, 4.9, 0.75, "Capability-based connectivity", GREEN, 11.0)
    arrow(ax, 2.7, 5.98, 3.1, 5.98, BLUE)
    arrow(ax, 6.2, 5.98, 6.7, 5.98, GREEN)

    stages = [
        ("3.1", "Measure", "District UMC index", BLUE),
        ("3.2", "Explain", "Individual and place effects", GREEN),
        ("3.3", "Update", "Text evidence and Bayesian signal", ORANGE),
        ("4", "Interpret", "Place-sensitive policy", PURPLE),
    ]
    x0 = 0.6
    for i, (num, title, sub, color) in enumerate(stages):
        x = x0 + i * 2.85
        add_card(ax, x, 3.2, 2.25, 1.25, f"{num}\n{title}", color, 15, alpha=0.14)
        ax.text(x + 1.125, 2.85, sub, ha="center", va="top", fontsize=9.2, color=MID)
        if i < len(stages) - 1:
            arrow(ax, x + 2.25, 3.82, x + 2.82, 3.82, color)

    layers = [("Empirical", BLUE), ("Actual", GREEN), ("Real", ORANGE)]
    for i, (label, color) in enumerate(layers):
        add_card(ax, 1.25 + i * 3.3, 0.9, 2.35, 0.75, label, color, 10.5, alpha=0.11)
    save(fig, "fig_project_overview_en.png")


def generate_flow_diagrams():
    fig, ax = plt.subplots(figsize=(10.2, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    boxes = [
        (0.4, 4.8, 2.35, 0.9, "3.1 UMC index", BLUE),
        (3.85, 4.8, 2.35, 0.9, "3.2 HLM model", GREEN),
        (0.4, 2.45, 2.35, 0.9, "Text classification", ORANGE),
        (3.85, 2.45, 2.35, 0.9, "Bayesian update", PURPLE),
        (7.05, 2.45, 2.55, 0.9, "Policy interpretation", RED),
    ]
    for x, y, w, h, text, color in boxes:
        add_card(ax, x, y, w, h, text, color, 11, alpha=0.12)
    arrow(ax, 2.75, 5.25, 3.85, 5.25, BLUE)
    arrow(ax, 1.58, 4.8, 1.58, 3.35, BLUE)
    arrow(ax, 2.75, 2.9, 3.85, 2.9, ORANGE)
    arrow(ax, 6.2, 2.9, 7.05, 2.9, PURPLE)
    arrow(ax, 5.03, 4.8, 5.03, 3.35, GREEN)
    save(fig, "fig_analysis_flow_en.png")

    fig, ax = plt.subplots(figsize=(10.5, 4.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.axhline(2.5, color=EDGE, lw=1.2)
    ax.axvline(5.0, color=EDGE, lw=1.2)
    quadrants = [
        (0.7, 3.1, 3.6, 1.05, "Clear digital difficulty\nclassification: lower risk", BLUE),
        (5.7, 3.1, 3.6, 1.05, "Ambiguous digital reference\nclassification: Y / N / ?", ORANGE),
        (0.7, 0.85, 3.6, 1.05, "Non-digital local issue\nexclude from UMC coding", MID),
        (5.7, 0.85, 3.6, 1.05, "Mechanism interpretation\nonly after quantitative checks", GREEN),
    ]
    for x, y, w, h, text, color in quadrants:
        add_card(ax, x, y, w, h, text, color, 10.5, alpha=0.11)
    ax.text(5, 4.62, "Role Separation in Platform Text Analysis", ha="center", fontsize=12, weight="bold")
    ax.text(0.25, 2.55, "Evidence strength", rotation=90, va="center", fontsize=9, color=MID)
    ax.text(5.0, 0.25, "UMC explicitness", ha="center", fontsize=9, color=MID)
    save(fig, "fig_classification_inference_roles_en.png")

    fig, ax = plt.subplots(figsize=(10.8, 4.7))
    ax.set_xlim(0, 12)
    ax.set_ylim(1.1, 4.5)
    ax.axis("off")
    steps = [
        ("Candidate\nposts", BLUE),
        ("UMC\nfilter", CYAN),
        ("Bayesian\nscreen", ORANGE),
        ("Three\nreasoners", GREEN),
        ("Final\njudgment", PURPLE),
    ]
    for i, (label, color) in enumerate(steps):
        x = 0.45 + i * 2.3
        add_card(ax, x, 2.3, 1.75, 1.0, label, color, 11, alpha=0.12)
        if i < len(steps) - 1:
            arrow(ax, x + 1.75, 2.8, x + 2.25, 2.8, color)
    save(fig, "fig_agent_pipeline_en.png")

    fig, ax = plt.subplots(figsize=(11.2, 5.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.text(6, 5.55, "Context Control as Staged Information Sets", ha="center", fontsize=13, weight="bold")
    add_outline_card(
        ax,
        0.45,
        2.75,
        3.15,
        1.95,
        "Text-only reasoners",
        ["I_text = post text + metadata", "r in {abductive, forward, sequential}", "produce H_r under restricted input"],
        BLUE,
        8.9,
    )
    add_outline_card(
        ax,
        4.4,
        2.75,
        3.15,
        1.95,
        "Blocked at Phase 1",
        ["district context", "absence typology", "active categories", "other reasoner outputs"],
        RED,
        8.9,
    )
    add_outline_card(
        ax,
        8.35,
        2.75,
        3.15,
        1.95,
        "Judgment information set",
        ["I_judge = I_text + H_A + H_F + H_S", "+ district context", "+ typology and categories"],
        GREEN,
        8.9,
    )
    add_card(ax, 4.25, 0.70, 3.5, 0.82, "Synthesis target\nP(classification | I_judge)", PURPLE, 10.2, alpha=0.12)
    arrow(ax, 3.6, 3.72, 4.4, 3.72, BLUE)
    arrow(ax, 7.55, 3.72, 8.35, 3.72, GREEN)
    arrow(ax, 9.92, 2.75, 6.05, 1.52, PURPLE, rad=-0.14)
    save(fig, "fig_context_information_sets_en.png")

    fig, ax = plt.subplots(figsize=(12.0, 6.1))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.text(7, 7.45, "Section 3.3 Platform Text Analysis Pipeline", ha="center", fontsize=13, weight="bold")

    top_steps = [
        ("Stage 0", "CSV / Excel\nto JSONL", BLUE),
        ("Stage 1", "Deterministic\nfiltering", CYAN),
        ("Stage 2", "LLM relevance\nscoring", ORANGE),
    ]
    bottom_steps = [
        ("Phase 1", "Three reasoners\nparallel hypotheses", GREEN),
        ("Phase 2", "Judgment synthesizer\ntriangulation", PURPLE),
        ("Output", "District summary\nand saturation check", RED),
    ]

    for i, (stage, label, color) in enumerate(top_steps):
        x = 0.8 + i * 4.25
        add_card(ax, x, 5.3, 3.15, 1.05, f"{stage}\n{label}", color, 10.6, alpha=0.12)
        if i < len(top_steps) - 1:
            arrow(ax, x + 3.15, 5.82, x + 4.15, 5.82, color)

    for i, (stage, label, color) in enumerate(bottom_steps):
        x = 9.3 - i * 4.25
        add_card(ax, x, 2.55, 3.15, 1.05, f"{stage}\n{label}", color, 10.6, alpha=0.12)
        if i < len(bottom_steps) - 1:
            arrow(ax, x, 3.07, x - 1.10, 3.07, color)

    arrow(ax, 12.45, 5.3, 12.45, 3.6, ORANGE)
    labels = [
        (2.38, 4.65, "candidate construction"),
        (6.62, 4.65, "UMC Y / N / ?"),
        (10.88, 4.65, "screened evidence"),
        (10.88, 1.95, "post text only"),
        (6.62, 1.95, "context added at synthesis"),
        (2.38, 1.95, "aggregate signal"),
    ]
    for x, y, text in labels:
        ax.text(x, y, text, ha="center", va="center", fontsize=8.4, color=MID)
    save(fig, "fig_section33_pipeline_en.png")

    fig, ax = plt.subplots(figsize=(10.8, 4.7))
    ax.set_xlim(0, 12)
    ax.set_ylim(1.1, 4.6)
    ax.axis("off")
    add_card(ax, 0.6, 2.7, 3.0, 1.1, "Reasoners\npost text only", BLUE, 11.5, alpha=0.12)
    add_card(ax, 4.5, 2.7, 3.0, 1.1, "Judgment\nadds context", ORANGE, 11.5, alpha=0.12)
    add_card(ax, 8.4, 2.7, 3.0, 1.1, "Output\nbounded signal", GREEN, 11.5, alpha=0.12)
    arrow(ax, 3.6, 3.25, 4.5, 3.25, BLUE)
    arrow(ax, 7.5, 3.25, 8.4, 3.25, ORANGE)
    save(fig, "fig_context_control_en.png")


def generate_formula():
    fig, ax = plt.subplots(figsize=(8.2, 2.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")
    add_card(ax, 0.4, 1.55, 4.2, 0.75, r"Positive:  x* = (x - min) / (max - min)", BLUE, 11, alpha=0.09)
    add_card(ax, 5.2, 1.55, 4.4, 0.75, r"Reverse:  x* = (max - x) / (max - min)", ORANGE, 11, alpha=0.09)
    save(fig, "fig_normalization_formula_en.png")


def generate_part1_figures():
    mod = load_part1_module()
    df = pd.read_csv(PART1_TABLE).copy()
    df.loc[:, "district_code"] = df["district_code"].astype(int)
    geometry = mod.load_geometry()
    codes = df["district_code"].tolist()

    d = df.sort_values("station_density_4g", ascending=True)
    y = np.arange(len(d))
    fig, ax = plt.subplots(figsize=(7.2, 6.0))
    ax.barh(y - 0.18, d["station_density_4g"], height=0.34, color=BLUE, label="4G station density")
    ax.barh(y + 0.18, d["station_density_5g"], height=0.34, color=CYAN, label="5G station density")
    ax.set_yticks(y)
    ax.set_yticklabels([mod.GU_NAME[c] for c in d["district_code"]], fontsize=7.5)
    ax.set_xlabel("Stations per 1,000 daytime living population")
    ax.grid(axis="x", color=GRID, linewidth=0.7)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(loc="lower right", fontsize=8, frameon=False)
    save(fig, "fig_connectivity_inputs_2024.png")

    top_codes = set(df.nsmallest(5, "rank_UMC")["district_code"])
    desert_codes = mod.DIGITAL_DESERT_CODES
    d = df.sort_values("score_UMC", ascending=True)
    colors = [RED if c in desert_codes else BLUE if c in top_codes else "#B8C2CC" for c in d["district_code"]]
    fig, ax = plt.subplots(figsize=(5.4, 4.9))
    y = np.arange(len(d))
    ax.barh(y, d["score_UMC"], color=colors, edgecolor="white", linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels([mod.GU_NAME[c] for c in d["district_code"]], fontsize=7.4)
    ax.axvline(d["score_UMC"].mean(), color=DARK, linestyle="--", linewidth=1.0)
    ax.set_xlim(0.24, 0.72)
    ax.set_xlabel("UMC composite score (0-1)")
    ax.grid(axis="x", color=GRID, linewidth=0.7)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(
        handles=[
            Patch(facecolor=BLUE, label="Top five"),
            Patch(facecolor=RED, label="Digital deserts"),
            Patch(facecolor="#B8C2CC", label="Other districts"),
        ],
        loc="lower right",
        fontsize=7.4,
        frameon=False,
    )
    save(fig, "fig_umc_composite_scores_2024.png")

    d = df.sort_values("score_UMC", ascending=False)
    data = d[[c for c, _ in DIMENSIONS]].to_numpy()
    cmap = LinearSegmentedColormap.from_list("umc_blues", ["#F7FBFF", "#D6EAF8", "#85C1E9", "#2F80ED", "#1B4F72"])
    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    im = ax.imshow(data, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    ax.set_yticks(np.arange(len(d)))
    ax.set_yticklabels([mod.GU_NAME[c] for c in d["district_code"]], fontsize=7.2)
    ax.set_xticks(np.arange(len(DIMENSIONS)))
    ax.set_xticklabels([label.replace(" ", "\n") for _, label in DIMENSIONS], fontsize=7.0)
    ax.tick_params(length=0)
    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.025)
    cbar.ax.tick_params(labelsize=7)
    cbar.set_label("Score (0-1)", fontsize=8)
    save(fig, "fig_umc_dimension_heatmap_2024.png")

    values = dict(zip(df["district_code"], df["score_UMC"]))
    fig, ax = plt.subplots(figsize=(5.9, 4.5))
    collection = mod.plot_map(ax, geometry, codes, values, cmap="Blues", vmin=0.25, vmax=0.72, label_codes=top_codes | desert_codes, linewidth=0.55)
    colors = {code: (BLUE if code in top_codes else RED if code in desert_codes else "#F3F4F6") for code in codes}
    mod.plot_map(ax, geometry, codes, colors=colors, label_codes=top_codes | desert_codes, linewidth=0.6)
    ax.set_title("Seoul UMC composite index, 2024", fontsize=11, weight="bold", pad=6)
    handles = [Patch(facecolor=BLUE, label="Top five"), Patch(facecolor=RED, label="Digital deserts"), Patch(facecolor="#F3F4F6", edgecolor=EDGE, label="Other")]
    ax.legend(handles=handles, loc="lower left", fontsize=7.5, frameon=False)
    save(fig, "fig_context_seoul_map.png")
    save_map_only_composite(df, geometry, codes, values, mod)

    neighbors = mod.build_neighbors(geometry)
    w = mod.row_standardized_weights(sorted(codes), neighbors)
    indexed = df.set_index("district_code").loc[sorted(codes)]
    cluster_by_var = {}
    stats_rows = {}
    for var, label in DIMENSIONS:
        clusters, _local_i, _p_local, _lag = mod.lisa_clusters(indexed[var].to_numpy(float), w)
        moran_i, p_global = mod.global_moran(indexed[var].to_numpy(float), w)
        cluster_by_var[var] = dict(zip(sorted(codes), clusters))
        stats_rows[var] = (moran_i, p_global)

    fig, axes = plt.subplots(2, 3, figsize=(7.5, 4.8))
    for ax, (var, label) in zip(axes.ravel(), DIMENSIONS):
        colors = {code: CLUSTER_COLORS[cluster_by_var[var][code]] for code in sorted(codes)}
        sig = {code for code, cluster in cluster_by_var[var].items() if cluster != "Not significant"}
        mod.plot_map(ax, geometry, sorted(codes), colors=colors, label_codes=sig, linewidth=0.52)
        mi, pval = stats_rows[var]
        ax.set_title(f"{label}\nI={mi:.2f}, p={pval:.2f}", fontsize=8.2, pad=4)
    handles = [Patch(facecolor=color, edgecolor=DARK, label=label) for label, color in CLUSTER_COLORS.items()]
    fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=7.2, frameon=False, bbox_to_anchor=(0.5, 0.01))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.14, wspace=0.04, hspace=0.25)
    save(fig, "fig_lisa_dimensions_en.png")

    single_names = {
        "score_Infrastructure": "lisa_connectivity.png",
        "score_Available_for_Use": "lisa_available_for_use.png",
        "score_Affordability": "lisa_affordability.png",
        "score_Devices": "lisa_devices.png",
        "score_Digital_Skills": "lisa_digital_skills.png",
        "score_Safety": "lisa_safety.png",
    }
    for var, label in DIMENSIONS:
        fig, ax = plt.subplots(figsize=(4.8, 3.35))
        colors = {code: CLUSTER_COLORS[cluster_by_var[var][code]] for code in sorted(codes)}
        sig = {code for code, cluster in cluster_by_var[var].items() if cluster != "Not significant"}
        mod.plot_map(ax, geometry, sorted(codes), colors=colors, label_codes=sig, linewidth=0.55)
        ax.set_title(f"Local Spatial Association: {label}", fontsize=10.5, weight="bold")
        ax.legend(handles=handles, loc="lower left", fontsize=6.5, frameon=False)
        save(fig, single_names[var])


def save_map_only_composite(df, geometry, codes, values, mod):
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    collection = mod.plot_map(ax, geometry, codes, values, cmap="Blues", vmin=0.25, vmax=0.72, label_codes=set(), linewidth=0.55)
    cbar = fig.colorbar(collection, ax=ax, fraction=0.035, pad=0.02)
    cbar.set_label("UMC score", fontsize=8)
    cbar.ax.tick_params(labelsize=7)
    save(fig, "fig_umc_composite_map_2024.png")


def generate_bayesian_maps():
    mod = load_part1_module()
    geometry = mod.load_geometry()
    score_df = pd.read_csv(PART1_TABLE)
    code_by_gu = dict(zip(score_df["district"], score_df["district_code"].astype(int)))
    codes = sorted(code_by_gu.values())
    bayes = pd.read_csv(BAYES_TABLE)
    bayes.loc[:, "district_code"] = bayes["gu"].map(code_by_gu)

    vabs = float(bayes["shift"].abs().max())
    fig, axes = plt.subplots(2, 3, figsize=(7.8, 5.0))
    last = None
    for ax, (dim, label) in zip(axes.ravel(), BAYES_DIM_ORDER):
        sub = bayes[bayes["dimension"] == dim]
        values = dict(zip(sub["district_code"], sub["shift"]))
        last = mod.plot_map(ax, geometry, codes, values, cmap="RdBu_r", vmin=-vabs, vmax=vabs, label_codes=set(), linewidth=0.48)
        ax.set_title(label, fontsize=9.2, weight="bold", pad=4)
    cbar = fig.colorbar(last, ax=axes.ravel().tolist(), orientation="horizontal", fraction=0.045, pad=0.045)
    cbar.set_label("Posterior shift (posterior - prior)", fontsize=8.5)
    cbar.ax.tick_params(labelsize=7.2)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.91, bottom=0.12, wspace=0.03, hspace=0.20)
    save(fig, "fig_bayesian_shift_maps_en.png")

    score_df = score_df.copy()
    score_df.loc[:, "district_code"] = score_df["district_code"].astype(int)
    code_by_gu = dict(zip(score_df["district"], score_df["district_code"]))
    label_by_gu = {row["district"]: mod.GU_NAME[int(row["district_code"])] for _, row in score_df.iterrows()}
    ordered_gu = score_df.sort_values("score_UMC", ascending=True)["district"].tolist()
    heat = (
        bayes.pivot(index="gu", columns="dimension", values="shift")
        .reindex(index=ordered_gu, columns=[dim for dim, _label in BAYES_DIM_ORDER])
    )
    labels = [label_by_gu.get(gu, gu) for gu in heat.index]
    vmax = float(np.nanmax(np.abs(heat.to_numpy())))
    fig, ax = plt.subplots(figsize=(7.2, 7.4))
    im = ax.imshow(heat.to_numpy(), cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels, fontsize=7.6)
    ax.set_xticks(np.arange(len(BAYES_DIM_ORDER)))
    ax.set_xticklabels([label.replace(" ", "\n") for _dim, label in BAYES_DIM_ORDER], fontsize=7.5)
    ax.tick_params(length=0)
    ax.set_title("Posterior Shift by District and UMC Dimension", fontsize=11, weight="bold", pad=8)
    for i in range(heat.shape[0]):
        for j in range(heat.shape[1]):
            value = heat.iat[i, j]
            if pd.isna(value):
                continue
            ax.text(j, i, f"{value:+.3f}", ha="center", va="center", fontsize=5.5, color=DARK)
    for spine in ax.spines.values():
        spine.set_visible(False)
    cbar = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.025)
    cbar.set_label("Posterior shift", fontsize=8.5)
    cbar.ax.tick_params(labelsize=7.2)
    fig.subplots_adjust(left=0.22, right=0.94, top=0.92, bottom=0.11)
    save(fig, "fig_bayesian_shift_heatmap_en.png")

    fig, axes = plt.subplots(3, 4, figsize=(8.6, 6.6))
    cmap = "Blues"
    for idx, (dim, label) in enumerate(BAYES_DIM_ORDER):
        sub = bayes[bayes["dimension"] == dim]
        row = idx // 2
        col = (idx % 2) * 2
        prior_vals = dict(zip(sub["district_code"], sub["prior_mean"]))
        post_vals = dict(zip(sub["district_code"], sub["post_mean"]))
        vmin = min(prior_vals.values())
        vmax = max(post_vals.values())
        mod.plot_map(axes[row, col], geometry, codes, prior_vals, cmap=cmap, vmin=vmin, vmax=vmax, label_codes=set(), linewidth=0.42)
        mod.plot_map(axes[row, col + 1], geometry, codes, post_vals, cmap=cmap, vmin=vmin, vmax=vmax, label_codes=set(), linewidth=0.42)
        axes[row, col].set_title(f"{label} prior", fontsize=7.8)
        axes[row, col + 1].set_title(f"{label} posterior", fontsize=7.8)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.96, bottom=0.03, wspace=0.02, hspace=0.18)
    save(fig, "fig_prior_posterior_maps_en.png")


def main() -> None:
    generate_project_overview()
    generate_flow_diagrams()
    generate_formula()
    generate_part1_figures()
    generate_bayesian_maps()


if __name__ == "__main__":
    main()
