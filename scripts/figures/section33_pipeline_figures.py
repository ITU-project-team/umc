#!/usr/bin/env python3
"""
Generate Figure 7, Figure 8, and Figure 9 for Section 3.3.2.

Section 3.3.2 framing: three SEQUENTIAL analytic components.
  Stage 1 (Classification): filtered candidate posts -> LLM relevance coding (Y/?/N)
           -> UMC dimension assignment -> Classified-post base.
  Stage 2 (EB aggregation): Classified-post base -> administrative-dong linkage
           -> living-population exposure -> observed post rate
           -> EB shrinkage (prior = Part 1 deficiency, posterior = precision-weighted mean)
           -> posterior rate (per 100k person-years) -> within-dimension z_shift
           -> HIGH-z_shift outlier cells (district x dimension).
  Stage 3 (Agent interpretation): outlier cells from Stage 2 as input
           -> three reasoning lenses under restricted I_R
           -> Judgment synthesizer under expanded I_J -> bounded post-level cases.

Output files (all 300 dpi, white background, saved to docs/figures/):
  figure07_sequential_pipeline_en.png   (Figure 7 replacement)
  figure08_information_sets_en.png      (Figure 8 replacement)
  figure09_sequential_eb_to_agent_en.png  (Figure 9 replacement)

Script is standalone: run from any directory.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "docs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Shared palette  (matches existing report figures)
# ---------------------------------------------------------------------------
BLUE   = "#2F80ED"   # processing / EB steps
CYAN   = "#56CCF2"   # secondary process
YELLOW = "#F2C94C"   # classification / LLM coding
GREEN  = "#27AE60"   # three reasoning lenses
ORANGE = "#F2994A"   # judgment synthesizer / synthesis
GREY   = "#9CA3AF"   # input / base nodes
DARK   = "#1F2937"   # text
MID    = "#6B7280"   # secondary text / arrows
EDGE   = "#CBD5E1"   # borders
LIGHT  = "#F7F9FB"   # fill background

# Dashed-box fills
IR_FILL = "#EBF4FF"   # restricted layer  (light blue)
IJ_FILL = "#FFF8EE"   # judgment layer    (light orange)
S2_FILL = "#EBF4FF"
S3_FILL = "#F0FAF4"   # Stage 3 green tint

plt.rcParams.update({
    "font.family":       "Arial",
    "font.sans-serif":   ["Arial", "Helvetica", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.dpi":        150,
    "savefig.dpi":       300,
    "figure.facecolor":  "white",
    "savefig.facecolor": "white",
    "pdf.fonttype":      42,
    "svg.fonttype":      "none",
    "text.color":        DARK,
})


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def rbox(ax, x, y, w, h, fc, ec=None, lw=1.3, alpha=1.0,
         radius=0.06, zorder=2, ls="solid"):
    """Rounded rectangle patch."""
    if ec is None:
        ec = fc
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.0,rounding_size={radius}",
        facecolor=fc, edgecolor=ec,
        linewidth=lw, linestyle=ls, alpha=alpha, zorder=zorder,
    )
    ax.add_patch(p)
    return p


def solid_box(ax, x, y, w, h, color, alpha=0.13, label="", fs=10,
              sublabel="", subfs=8.0, weight="bold", zorder=2):
    """Filled rounded box with centred main label + optional italic sublabel."""
    rbox(ax, x, y, w, h, fc=color, ec=color, alpha=alpha, radius=0.06, zorder=zorder)
    cx, cy = x + w / 2, y + h / 2
    shift = 0.10 if sublabel else 0.0
    ax.text(cx, cy + shift, label, ha="center", va="center",
            fontsize=fs, fontweight=weight, zorder=zorder + 1)
    if sublabel:
        ax.text(cx, cy - 0.16, sublabel, ha="center", va="center",
                fontsize=subfs, style="italic", color=MID, zorder=zorder + 1)


def outline_box(ax, x, y, w, h, ec, fc=LIGHT, lw=1.5,
                title="", lines=(), title_fs=9.5, body_fs=8.5,
                body_ls=1.35, zorder=3):
    """Outline rounded box: bold coloured title + body lines."""
    rbox(ax, x, y, w, h, fc=fc, ec=ec, lw=lw, radius=0.06, zorder=zorder)
    ax.text(x + 0.12, y + h - 0.15, title,
            ha="left", va="top",
            fontsize=title_fs, fontweight="bold", color=ec,
            zorder=zorder + 1)
    if lines:
        ax.text(x + 0.12, y + h - 0.15 - title_fs * 0.016,
                "\n".join(lines),
                ha="left", va="top",
                fontsize=body_fs, color=DARK, linespacing=body_ls,
                zorder=zorder + 1)


def dbox(ax, x, y, w, h, ec, fc, lw=1.2, zorder=1):
    """Dashed-border rounded rectangle (region background)."""
    rbox(ax, x, y, w, h, fc=fc, ec=ec, lw=lw, ls="--",
         alpha=1.0, radius=0.08, zorder=zorder)


def arr(ax, x1, y1, x2, y2, color=MID, lw=1.3, ms=11, rad=0.0, zorder=4):
    """Single clean arrow; avoid calling with identical endpoints."""
    if abs(x2 - x1) < 1e-6 and abs(y2 - y1) < 1e-6:
        return
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>",
        mutation_scale=ms,
        linewidth=lw,
        color=color,
        connectionstyle=f"arc3,rad={rad}",
        zorder=zorder,
    ))


def hline(ax, x1, x2, y, color=MID, lw=1.2, zorder=3):
    """Plain horizontal line (no arrowhead)."""
    ax.plot([x1, x2], [y, y], color=color, lw=lw, zorder=zorder)


def vline(ax, x, y1, y2, color=MID, lw=1.2, zorder=3):
    """Plain vertical line (no arrowhead)."""
    ax.plot([x, x], [y1, y2], color=color, lw=lw, zorder=zorder)


def save_fig(fig, name, tight_pad=0.15, save_svg=False, save_vector=False):
    out = FIG_DIR / name
    fig.savefig(out, bbox_inches="tight", pad_inches=tight_pad)
    vector_exts = []
    if save_vector:
        vector_exts = [".pdf", ".svg"]
    elif save_svg:
        vector_exts = [".svg"]
    for ext in vector_exts:
        vector_out = out.with_suffix(ext)
        fig.savefig(vector_out, bbox_inches="tight", pad_inches=tight_pad)
        print(f"Saved: {vector_out}")
    plt.close(fig)
    print(f"Saved: {out}")
    return out


# ===========================================================================
# FIGURE 7 -- Full sequential pipeline overview
#
# Layout strategy: three horizontal band rows, top-to-bottom.
#   Band 1 (top):    Stage 1 -- Classification
#   Band 2 (middle): Stage 2 -- EB Aggregation
#   Band 3 (bottom): Stage 3 -- Agent Interpretation
#
# Stage 1: horizontal linear flow (left->right)
# Stage 2: vertical cascade in left-centre + outlier-cell output box to the right
# Stage 3: I_R sub-region (post input + 3 lenses) on left, I_J on right
#
# Coordinate system: (0,0) at bottom-left.
# Canvas: 14 wide x 14 tall (inches)
# ===========================================================================

def make_figure07():
    """
    Figure 7: compact three-stage sequential pipeline overview.

    Rebuilt as three left-to-right panels so the analytic sequence is explicit
    and all inter-stage arrows are short, continuous, and aligned.
    """
    W, H = 15.5, 7.8
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    panel_y, panel_h = 0.35, 7.05
    p1 = (0.30, panel_y, 4.25, panel_h)
    p2 = (4.80, panel_y, 4.60, panel_h)
    p3 = (9.65, panel_y, 5.55, panel_h)

    def panel(box, color, fill, stage, title, unit):
        x, y, w, h = box
        rbox(ax, x, y, w, h, fc=fill, ec=color, lw=1.05, alpha=1.0,
             radius=0.08, zorder=0)
        rbox(ax, x + 0.12, y + h - 0.78, 0.10, 0.54,
             fc=color, ec=color, alpha=0.82, radius=0.025, zorder=1)
        ax.text(x + 0.33, y + h - 0.28, f"Stage {stage}",
                ha="left", va="top", fontsize=11.2,
                fontweight="bold", color=color, zorder=2)
        ax.text(x + 0.33, y + h - 0.62, title,
                ha="left", va="top", fontsize=8.8, color=MID, zorder=2)
        ax.text(x + w - 0.22, y + h - 0.35, unit,
                ha="right", va="top", fontsize=7.7, color=MID,
                style="italic", zorder=2)

    panel(p1, YELLOW, "#FFFBEC", 1, "Classification", "unit: post")
    panel(p2, BLUE,   "#F2F7FF", 2, "EB aggregation", "unit: district x dimension")
    panel(p3, GREEN,  "#F2FBF6", 3, "Agent interpretation", "unit: post-level case")

    def node(x, y, w, h, label, color, alpha=0.14, fs=8.8, sublabel=""):
        solid_box(ax, x, y, w, h, color, alpha=alpha, label=label,
                  fs=fs, sublabel=sublabel, subfs=7.1)

    def connect_vertical(cx, y_top_lower, y_bottom_upper, color, lw=1.25):
        arr(ax, cx, y_bottom_upper, cx, y_top_lower, color=color, lw=lw, ms=10)

    # ------------------------------------------------------------------
    # Stage 1: minimal classification chain
    # ------------------------------------------------------------------
    x1, y1, w1, h1 = p1
    bw1, bh1 = 2.35, 0.54
    cx1 = x1 + w1 / 2
    nx1 = cx1 - bw1 / 2
    s1_ys = [6.25, 5.39, 4.53, 3.67, 2.81, 1.95]
    s1_nodes = [
        ("Platform\nrecords", GREY, 0.17, ""),
        ("Rule + keyword\nscreen", GREY, 0.17, ""),
        ("Candidate\nposts", BLUE, 0.13, ""),
        ("Relevance\ncoding", YELLOW, 0.18, "Y / ? / N"),
        ("Dimension\ntagging", YELLOW, 0.18, "six UMC dimensions"),
        ("Classified\npost base", DARK, 0.06, ""),
    ]
    for (label, color, alpha, sub), y in zip(s1_nodes, s1_ys):
        if color == DARK:
            outline_box(ax, nx1, y, bw1, bh1, ec=DARK, fc=LIGHT,
                        title=label.replace("\n", " "),
                        title_fs=8.5, zorder=4)
        else:
            node(nx1, y, bw1, bh1, label, color, alpha=alpha)
    for i in range(len(s1_ys) - 1):
        connect_vertical(cx1, s1_ys[i + 1] + bh1, s1_ys[i], BLUE if i >= 1 else GREY)

    # ------------------------------------------------------------------
    # Stage 2: EB aggregation chain
    # ------------------------------------------------------------------
    x2, y2, w2, h2 = p2
    bw2, bh2 = 2.45, 0.50
    cx2 = x2 + w2 / 2
    nx2 = cx2 - bw2 / 2
    s2_ys = [6.10, 5.31, 4.52, 3.73, 2.94, 2.15, 1.36]
    s2_nodes = [
        ("Classified\npost base", GREY, 0.17, ""),
        ("Dong\nlinkage", BLUE, 0.13, ""),
        ("Exposure\ndenominator", BLUE, 0.13, "person-time"),
        ("Observed\npost rate", BLUE, 0.13, ""),
        ("EB\nshrinkage", BLUE, 0.13, "prior + observed rate"),
        ("Posterior\nrate", BLUE, 0.13, "per 100k person-years"),
        ("High-z_shift\noutlier cells", ORANGE, 0.14, ""),
    ]
    for (label, color, alpha, sub), y in zip(s2_nodes, s2_ys):
        node(nx2, y, bw2, bh2, label, color, alpha=alpha, sublabel=sub)
    for i in range(len(s2_ys) - 1):
        connect_vertical(cx2, s2_ys[i + 1] + bh2, s2_ys[i],
                         ORANGE if i == len(s2_ys) - 2 else BLUE)

    # Stage 1 -> Stage 2 connector
    arr(ax, nx1 + bw1, s1_ys[-1] + bh1 / 2,
        nx2, s2_ys[0] + bh2 / 2,
        color=DARK, lw=1.35, ms=12, zorder=5)
    ax.text((nx1 + bw1 + nx2) / 2, s1_ys[-1] + bh1 / 2 + 0.18,
            "classified base", ha="center", fontsize=7.6,
            color=DARK, style="italic")

    # ------------------------------------------------------------------
    # Stage 3: restricted reading layer -> judgment layer
    # ------------------------------------------------------------------
    x3, y3, w3, h3 = p3
    ir_x, ir_y, ir_w, ir_h = x3 + 0.25, y3 + 0.72, 2.85, 5.50
    ij_x, ij_y, ij_w, ij_h = x3 + 3.35, y3 + 0.72, 1.95, 5.50
    dbox(ax, ir_x, ir_y, ir_w, ir_h, ec=BLUE, fc=IR_FILL, lw=0.85)
    dbox(ax, ij_x, ij_y, ij_w, ij_h, ec=ORANGE, fc=IJ_FILL, lw=0.85)
    ax.text(ir_x + 0.12, ir_y + ir_h - 0.12,
            r"$I_R$: restricted reading set",
            ha="left", va="top", fontsize=7.6, style="italic", color=BLUE)
    ax.text(ij_x + 0.12, ij_y + ij_h - 0.12,
            r"$I_J$: judgment context",
            ha="left", va="top", fontsize=7.6, style="italic", color=ORANGE)

    post_w, post_h = 1.05, 0.58
    post_x, post_y = ir_x + 0.14, 3.35
    node(post_x, post_y, post_w, post_h, "Outlier\nposts", ORANGE, alpha=0.13)

    lens_w, lens_h = 1.05, 0.56
    lens_x = ir_x + 1.58
    lens_ys = [4.45, 3.35, 2.25]
    for label, ly in zip(["Abductive\nlens", "Forward\nlens", "Sequential\nlens"], lens_ys):
        node(lens_x, ly, lens_w, lens_h, label, GREEN, alpha=0.15, fs=8.4)
        arr(ax, post_x + post_w, post_y + post_h / 2,
            lens_x, ly + lens_h / 2,
            color=GREEN, lw=1.2, ms=10, zorder=5)

    js_w, js_h = 1.42, 0.70
    js_x, js_y = ij_x + 0.26, 3.29
    node(js_x, js_y, js_w, js_h, "Judgment\nsynthesis", ORANGE, alpha=0.15)
    js_entries = [js_y + js_h * 0.76, js_y + js_h * 0.50, js_y + js_h * 0.24]
    for ly, ey in zip(lens_ys, js_entries):
        arr(ax, lens_x + lens_w, ly + lens_h / 2,
            js_x, ey,
            color=ORANGE, lw=1.2, ms=10, zorder=5)

    out_w, out_h = js_w, 0.54
    out_y = 2.32
    node(js_x, out_y, out_w, out_h, "Bounded\ncase code", DARK, alpha=0.06, fs=8.3)
    arr(ax, js_x + js_w / 2, js_y,
        js_x + out_w / 2, out_y + out_h,
        color=DARK, lw=1.2, ms=10, zorder=5)
    ax.text(js_x + out_w / 2, out_y - 0.18,
            "audit trail retained",
            ha="center", fontsize=7.5, color=MID, style="italic")

    # Stage 2 -> Stage 3 connector
    arr(ax, nx2 + bw2, s2_ys[-1] + bh2 / 2,
        post_x, post_y + post_h / 2,
        color=ORANGE, lw=1.35, ms=12, zorder=6)
    ax.text((nx2 + bw2 + post_x) / 2, s2_ys[-1] + bh2 / 2 + 0.18,
            "outlier cells", ha="center", fontsize=7.6,
            color=ORANGE, style="italic")

    return save_fig(fig, "figure07_sequential_pipeline_en.png",
                    tight_pad=0.12, save_svg=True)


def _make_figure07_legacy():
    """
    Figure 7: Three-stage sequential pipeline overview.

    Layout (top -> bottom):
      Stage 1 (Classification):   horizontal linear flow row
      Stage 2 (EB Aggregation):   vertical cascade (left col) + outlier box (right)
      Stage 3 (Agent Interpret.): I_R sub-region left, I_J sub-region right

    Key design decisions:
    - Explicit pixel-level y coordinates so nothing overlaps
    - Stage 1 -> Stage 2 connector routed via a SIMPLE downward arrow from
      CPB box to first Stage 2 node (both share the same x-column)
    - Stage 2 -> Stage 3 connector: outlier box bottom -> drop -> Stage 3 post input
    - All cascade elements confirmed to fit within their enclosing band before draw
    """
    # Band heights verified by geometry script (see calculation in docstring above):
    #   S2BH=0.68, GAP2=0.22, 7 nodes -> S2_H=7.80
    #   S3 cascade (4 items h=0.52, gap=0.10) + JS (0.68) + lenses -> S3_H=4.47
    W = 14.0

    S3_BOT  = 0.15
    S3_TOP  = S3_BOT + 5.00      # 5.15  (extra 0.53 gives breathing room top/bot)
    GAP_23  = 0.25
    S2_BOT  = S3_TOP + GAP_23    # 5.40
    S2_TOP  = S2_BOT + 7.80      # 13.20
    GAP_12  = 0.25
    S1_BOT  = S2_TOP + GAP_12    # 13.45
    S1_TOP  = S1_BOT + 3.50      # 16.95
    H       = S1_TOP + 0.32      # 17.27

    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    BAND_LX = 0.15
    BAND_W  = W - 0.30

    # -- Draw band backgrounds ----------------------------------------------
    for (by, bh, col, fc_col) in [
        (S1_BOT, S1_TOP - S1_BOT, YELLOW, "#FFFBEC"),
        (S2_BOT, S2_TOP - S2_BOT, BLUE,   IR_FILL),
        (S3_BOT, S3_TOP - S3_BOT, GREEN,  S3_FILL),
    ]:
        dbox(ax, BAND_LX, by, BAND_W, bh, ec=col, fc=fc_col, lw=0.9)

    # -- Stage accent bars + labels -----------------------------------------
    def stage_label(by, bh, num, title, subtitle, col):
        bar_x = BAND_LX + 0.05
        rbox(ax, bar_x, by + 0.20, 0.09, bh - 0.40,
             fc=col, ec=col, alpha=0.75, radius=0.02, zorder=2)
        tx = bar_x + 0.24
        ty = by + bh / 2
        ax.text(tx, ty + 0.25, f"Stage {num}",
                ha="left", va="center", fontsize=12.5,
                fontweight="bold", color=col, zorder=3)
        ax.text(tx, ty + 0.00, title,
                ha="left", va="center", fontsize=9.5, color=MID, zorder=3)
        ax.text(tx, ty - 0.32, subtitle,
                ha="left", va="center", fontsize=8.0, color=MID,
                style="italic", zorder=3)

    stage_label(S1_BOT, S1_TOP - S1_BOT, 1, "Classification",
                "filtered posts -> LLM coding -> classified base", YELLOW)
    stage_label(S2_BOT, S2_TOP - S2_BOT, 2, "EB Aggregation",
                "classified-post base -> posterior rates -> z_shift outliers", BLUE)
    stage_label(S3_BOT, S3_TOP - S3_BOT, 3, "Agent Interpretation",
                "outlier-cell posts -> three reasoning lenses -> bounded cases", GREEN)

    # =======================================================================
    # STAGE 1 -- horizontal linear flow
    # x layout: stage label occupies 0.0-1.55; nodes from 1.65 rightward
    # y-centre of node row
    # =======================================================================
    CY1 = S1_BOT + (S1_TOP - S1_BOT) / 2 + 0.15   # slightly above midline
    BW1, BH1 = 1.55, 0.76
    DY = 0.62   # vertical offset for the fork nodes

    # x-left of each box
    X_RAW  = 1.65
    X_FORK = 3.45   # Deterministic excl (top) and Keyword dict (bottom) share this x
    X_CAND = 5.50   # Candidate posts
    X_LLM  = 7.30   # LLM relevance coding
    X_REL  = 9.10   # Relevant UMC posts
    X_DIM  = 10.90  # Dimension assignment

    EXCL_W, EXCL_H = 1.65, 0.68
    KW_W,   KW_H   = 1.65, 0.68

    # Draw Stage 1 nodes
    solid_box(ax, X_RAW,  CY1 - BH1/2, BW1, BH1, GREY,   0.18,
              "Raw platform\nrecords", fs=9.2)
    solid_box(ax, X_FORK, CY1 - EXCL_H/2 + DY, EXCL_W, EXCL_H, GREY, 0.18,
              "Deterministic\nexclusions", fs=9.2,
              sublabel="inacc . dup . ad", subfs=7.5)
    solid_box(ax, X_FORK, CY1 - KW_H/2 - DY, KW_W, KW_H, GREY, 0.18,
              "Keyword\ndictionary", fs=9.2,
              sublabel="expanded from seed list", subfs=7.5)
    solid_box(ax, X_CAND, CY1 - BH1/2, BW1, BH1, BLUE,   0.15,
              "Candidate\nposts", fs=9.2)
    solid_box(ax, X_LLM,  CY1 - BH1/2, BW1, BH1, YELLOW, 0.18,
              "LLM relevance\ncoding", fs=9.2,
              sublabel="Y / ? / N", subfs=8.0)
    solid_box(ax, X_REL,  CY1 - BH1/2, BW1, BH1, YELLOW, 0.18,
              "Relevant\nUMC posts", fs=9.2)
    solid_box(ax, X_DIM,  CY1 - BH1/2, BW1, BH1, YELLOW, 0.18,
              "Dimension\nassignment", fs=9.2,
              sublabel="six UMC dimensions", subfs=7.5)

    # Stage 1 arrows (separate departure / arrival to avoid arrowhead overlap)
    arr(ax, X_RAW + BW1, CY1 + 0.15, X_FORK, CY1 + DY, GREY, ms=10)
    arr(ax, X_RAW + BW1, CY1 - 0.15, X_FORK, CY1 - DY, GREY, ms=10)
    arr(ax, X_FORK + EXCL_W, CY1 + DY, X_CAND, CY1 + 0.16, GREY, ms=10)
    arr(ax, X_FORK + KW_W,   CY1 - DY, X_CAND, CY1 - 0.16, GREY, ms=10)
    arr(ax, X_CAND + BW1, CY1, X_LLM,  CY1, BLUE,   ms=11)
    arr(ax, X_LLM  + BW1, CY1, X_REL,  CY1, YELLOW, ms=11)
    arr(ax, X_REL  + BW1, CY1, X_DIM,  CY1, YELLOW, ms=11)

    # Classified-post base output box -- directly below Dim assignment
    CPB_W, CPB_H = 1.80, 0.62
    CPB_X = X_DIM + (BW1 - CPB_W) / 2   # horizontally centred under dim assign
    CPB_Y = S1_BOT + 0.28
    outline_box(ax, CPB_X, CPB_Y, CPB_W, CPB_H,
                ec=DARK, fc=LIGHT,
                title="Classified-post base",
                title_fs=8.8, zorder=4)
    # Dim assignment -> Classified-post base (straight down)
    arr(ax, CPB_X + CPB_W/2, CY1 - BH1/2,
        CPB_X + CPB_W/2, CPB_Y + CPB_H,
        DARK, ms=11)

    # =======================================================================
    # Stage 1 -> Stage 2 connector
    # CPB is near right margin. Route: right side of CPB ->
    # horizontal to right-margin channel -> drop to S2_TOP -> left to S2 cascade cx
    # S2 cascade is centred at x = 4.20 (computed below)
    # =======================================================================
    S2_CX   = 4.20          # x-centre of Stage 2 vertical cascade
    CONN_RX = W - 0.45      # right-side routing channel

    CPB_MID_Y = CPB_Y + CPB_H/2

    # CPB right -> routing channel (horizontal line)
    hline(ax, CPB_X + CPB_W, CONN_RX, CPB_MID_Y, DARK, lw=1.2)
    # Routing channel down to Stage 2 entry level
    S2_ENTRY_Y = S2_TOP - 0.50
    vline(ax, CONN_RX, CPB_MID_Y, S2_ENTRY_Y, DARK, lw=1.2)
    # Horizontal left to S2 cascade centre
    arr(ax, CONN_RX, S2_ENTRY_Y, S2_CX, S2_ENTRY_Y, DARK, ms=11)

    ax.text((S2_CX + CONN_RX) / 2, S2_ENTRY_Y + 0.18,
            "Classified-post base feeds Stage 2",
            ha="center", fontsize=8.0, style="italic", color=DARK)

    # =======================================================================
    # STAGE 2 -- vertical cascade (left of centre)
    # 7 nodes with S2BH=0.68, GAP2=0.22 -> step=0.90 per node
    # Verified to fit within band by geometry calculation above.
    # =======================================================================
    S2BW, S2BH = 2.30, 0.68
    S2X = S2_CX - S2BW/2   # left edge

    N2    = 7
    GAP2  = 0.22
    STEP2 = S2BH + GAP2   # 0.90 per node

    # First node top just below entry arrow
    s2_tops = [S2_ENTRY_Y - S2BH - i * STEP2 for i in range(N2)]

    S2_NODES = [
        ("Classified-post base\n(from Stage 1)", GREY, 0.18, ""),
        ("Administrative-dong\nlinkage",          BLUE, 0.13, ""),
        ("Living-population\nexposure",           BLUE, 0.13, "hourly person-time"),
        ("Observed post rate",                     BLUE, 0.13, ""),
        ("EB shrinkage",                           BLUE, 0.13,
         "prior = Part 1 deficiency\nposterior = precision-weighted mean"),
        ("Posterior rate\n(per 100k person-years)", BLUE, 0.13, ""),
        ("Within-dimension\nz_shift",              BLUE, 0.13, ""),
    ]

    for i, ((lbl, col, a, sub), ty) in enumerate(zip(S2_NODES, s2_tops)):
        solid_box(ax, S2X, ty, S2BW, S2BH, col, alpha=a,
                  label=lbl, fs=9.0, sublabel=sub, subfs=7.5)
        if i > 0:
            # Arrow from bottom of prev to top of current
            arr(ax, S2_CX, s2_tops[i-1], S2_CX, ty + S2BH, col, ms=11)

    # -- Outlier cells output box (right of z_shift, horizontally) ----------
    LAST_TOP = s2_tops[-1]
    OC_W, OC_H = 2.60, 0.78
    OC_X = S2X + S2BW + 0.55
    OC_Y = LAST_TOP + (S2BH - OC_H) / 2   # vertically centred on last node
    outline_box(ax, OC_X, OC_Y, OC_W, OC_H,
                ec=ORANGE, fc="#FFF8EE",
                title="High-z_shift outlier cells",
                lines=("district x dimension",),
                title_fs=9.0, body_fs=8.5, zorder=4)
    arr(ax, S2X + S2BW, LAST_TOP + S2BH/2,
        OC_X, OC_Y + OC_H/2,
        ORANGE, ms=11)
    ax.text(OC_X + OC_W/2, OC_Y - 0.18,
            "Output unit: district x dimension",
            ha="center", fontsize=7.8, style="italic", color=ORANGE)

    # =======================================================================
    # Stage 2 -> Stage 3 connector
    # Outlier box bottom -> drop to S3_TOP gap -> left to Stage 3 post input node
    # Stage 3 post input is at x-centre 3.40 (matches S2 cascade column)
    # =======================================================================
    S3_POST_CX = 3.40
    CONN23_X   = OC_X + OC_W/2
    CONN23_Y_START = OC_Y        # bottom of outlier box
    CONN23_Y_END   = S3_TOP - 0.28  # entry into Stage 3

    vline(ax, CONN23_X, CONN23_Y_START, CONN23_Y_END, ORANGE, lw=1.2)
    arr(ax, CONN23_X, CONN23_Y_END, S3_POST_CX, CONN23_Y_END, ORANGE, ms=11)

    ax.text((S3_POST_CX + CONN23_X) / 2, CONN23_Y_END + 0.16,
            "outlier-cell posts feed Stage 3",
            ha="center", fontsize=8.0, style="italic", color=ORANGE)

    # =======================================================================
    # STAGE 3 -- I_R (left) and I_J (right)
    # I_R: x from 1.65 to 7.15 (width 5.50)
    # I_J: x from 7.35 to 13.65 (width 6.30)
    # Both regions span full height of Stage 3 band (minus margins)
    # =======================================================================
    IR3_X, IR3_Y = 1.65, S3_BOT + 0.20
    IR3_W = 5.50
    IR3_H = S3_TOP - 0.30 - IR3_Y
    dbox(ax, IR3_X, IR3_Y, IR3_W, IR3_H, ec=BLUE, fc=IR_FILL, lw=1.0)
    ax.text(IR3_X + 0.14, IR3_Y + IR3_H - 0.10,
            r"$I_R$: post text + metadata + generic codebook only   |   three lenses independent",
            ha="left", va="top", fontsize=7.8, style="italic", color=BLUE)

    IJ3_X = 7.35
    IJ3_Y = S3_BOT + 0.20
    IJ3_W = W - 0.35 - IJ3_X
    IJ3_H = S3_TOP - 0.30 - IJ3_Y
    dbox(ax, IJ3_X, IJ3_Y, IJ3_W, IJ3_H, ec=ORANGE, fc=IJ_FILL, lw=1.0)
    ax.text(IJ3_X + 0.14, IJ3_Y + IJ3_H - 0.10,
            r"$I_J$: hypotheses + district context + absence typology + active category set",
            ha="left", va="top", fontsize=7.8, style="italic", color=ORANGE)

    # Outlier-cell post input node
    # Pre-compute JS3_Y and centre OCP vertically around JS mid
    _JS3_Y_pre = S3_BOT + 0.40 + 4 * (0.52 + 0.10)   # matches JS3_Y formula above
    _JS3_H_pre = 0.68
    _LENS_MID_Y = _JS3_Y_pre + _JS3_H_pre / 2
    OCP_W, OCP_H = 1.35, 0.65
    OCP_X = S3_POST_CX - OCP_W/2
    OCP_Y = _LENS_MID_Y - OCP_H/2   # vertically centred on lens midpoint
    solid_box(ax, OCP_X, OCP_Y, OCP_W, OCP_H,
              ORANGE, 0.15, "Outlier-cell\nposts", fs=9.2)
    # Drop arrow from connector into post input node
    arr(ax, S3_POST_CX, CONN23_Y_END,
        S3_POST_CX, OCP_Y + OCP_H,
        ORANGE, ms=11)

    # Three reasoning lenses (vertically stacked in I_R centre)
    # Centre lenses around JS3_Y + JS3_H/2 so fan-in arrows are roughly horizontal.
    # JS3_Y is set after JS3 computation below, but we place lenses here first
    # by pre-computing JS3_Y (same formula used below).
    LW3, LH3 = 1.55, 0.65
    LENS3_X = OCP_X + OCP_W + 0.42

    # JS3_Y pre-computed (same formula as used in Judgment synthesizer block below)
    CSC_W_PRE, CSC_H_PRE, CSC_GAP_PRE = 1.90, 0.52, 0.10
    JS3_Y_PRE = S3_BOT + 0.40 + 4 * (CSC_H_PRE + CSC_GAP_PRE)   # updated with S3 expansion
    JS3_H_PRE = 0.68
    LENS_MID_Y = JS3_Y_PRE + JS3_H_PRE / 2   # vertical midpoint of JS
    LENS_PITCH = LH3 + 0.16   # spacing between lens centres
    LC3 = [
        LENS_MID_Y + LENS_PITCH,            # top lens centre
        LENS_MID_Y,                          # middle lens centre (aligned with JS)
        LENS_MID_Y - LENS_PITCH,            # bottom lens centre
    ]
    # Convert from centre-y to bottom-of-box y
    LC3 = [cy - LH3/2 for cy in LC3]

    LC3_LABELS = ["Abductive\nlens", "Forward\nlens", "Sequential\nlens"]
    for cy, lbl in zip(LC3, LC3_LABELS):
        solid_box(ax, LENS3_X, cy, LW3, LH3, GREEN, 0.15, lbl, fs=9.2)

    # Fan-out: post input right -> three lenses (individual arrows from common source)
    FAN3_SX = OCP_X + OCP_W
    FAN3_SY = OCP_Y + OCP_H/2
    for cy in LC3:
        arr(ax, FAN3_SX, FAN3_SY,
            LENS3_X, cy + LH3/2,
            GREEN, lw=1.3, ms=10)

    # Judgment synthesizer in I_J region
    # JS3_Y placed so the full cascade below fits above S3_BOT + 0.35.
    # Cascade: 4 x (CSC_H=0.52 + CSC_GAP=0.10) = 2.48; output label 0.16 + margin 0.35
    JS3_W, JS3_H = 1.90, 0.68
    JS3_X = IJ3_X + 0.50
    CSC_W, CSC_H = JS3_W, 0.52
    CSC_GAP = 0.10
    N_CSC = 4
    # Bottom of last cascade sits at S3_BOT + 0.40
    # JS3_Y = S3_BOT + 0.40 + N_CSC*(CSC_H+CSC_GAP)
    JS3_Y = S3_BOT + 0.40 + N_CSC * (CSC_H + CSC_GAP)   # 2.63 with new S3
    solid_box(ax, JS3_X, JS3_Y, JS3_W, JS3_H,
              ORANGE, 0.15, "Judgment\nsynthesizer", fs=9.2)

    # Fan-in: three lenses -> judgment synthesizer (staggered y entry)
    JS3_ENTRY_YS = [
        JS3_Y + JS3_H * 0.78,
        JS3_Y + JS3_H * 0.50,
        JS3_Y + JS3_H * 0.22,
    ]
    for cy, ey in zip(LC3, JS3_ENTRY_YS):
        arr(ax, LENS3_X + LW3, cy + LH3/2,
            JS3_X, ey,
            ORANGE, lw=1.3, ms=10)

    # Cascade below JS3 (all within I_J region, verified in geometry calculation)
    CASCADE3 = [
        ("Convergence /\ndisagreement check", ORANGE, 0.14),
        ("Non-structural\nalternatives",       GREY,   0.18),
        ("Final bounded\ncode",                GREY,   0.18),
        ("Audit trail",                        GREY,   0.18),
    ]
    cy3 = JS3_Y
    for i, (lbl, col, a) in enumerate(CASCADE3):
        cy3 -= (CSC_H + CSC_GAP)
        solid_box(ax, JS3_X, cy3, CSC_W, CSC_H, col, alpha=a, label=lbl, fs=8.8)
        if i == 0:
            arr(ax, JS3_X + CSC_W/2, JS3_Y,
                JS3_X + CSC_W/2, cy3 + CSC_H,
                ORANGE, ms=11)
        else:
            arr(ax, JS3_X + CSC_W/2, cy3 + CSC_H + CSC_GAP,
                JS3_X + CSC_W/2, cy3 + CSC_H,
                DARK, ms=11)

    ax.text(JS3_X + CSC_W/2, cy3 - 0.16,
            "Output unit: post-level case",
            ha="center", fontsize=7.8, style="italic", color=GREY)

    return save_fig(fig, "figure07_sequential_pipeline_en.png")


# ===========================================================================
# FIGURE 8 -- Stage 3 information-set architecture (I_R / I_J)
# Two-column layout: left = Restricted layer, right = Synthesis layer.
# Clean fan-out (post -> 3 lenses) and staggered fan-in (3 lenses -> judgment).
# ===========================================================================

def make_figure08():
    W, H = 12.6, 5.2
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    # Left region: restricted information set
    IR_X, IR_Y = 0.25, 0.35
    IR_W, IR_H = 5.10, H - 0.70
    dbox(ax, IR_X, IR_Y, IR_W, IR_H, ec=BLUE, fc=IR_FILL, lw=1.4)
    ax.text(IR_X + 0.22, IR_Y + IR_H - 0.10,
            "Restricted information set", ha="left", va="top",
            fontsize=11.5, fontweight="bold", color=BLUE)
    ax.text(IR_X + 0.22, IR_Y + IR_H - 0.44,
            r"$I_R$: post text + metadata + codebook",
            ha="left", va="top", fontsize=9.5, style="italic", color=BLUE)

    # Right region: expanded judgment set
    IJ_X, IJ_Y = 5.85, 0.35
    IJ_W, IJ_H = W - IJ_X - 0.25, H - 0.70
    dbox(ax, IJ_X, IJ_Y, IJ_W, IJ_H, ec=ORANGE, fc=IJ_FILL, lw=1.4)
    ax.text(IJ_X + 0.22, IJ_Y + IJ_H - 0.10,
            "Expanded judgment set", ha="left", va="top",
            fontsize=11.5, fontweight="bold", color=ORANGE)
    ax.text(IJ_X + 0.22, IJ_Y + IJ_H - 0.44,
            r"$I_J$: lens hypotheses + district context",
            ha="left", va="top", fontsize=9.5, style="italic", color=ORANGE)

    # Boundary dashed line
    BND_X = 5.60
    ax.plot([BND_X, BND_X], [0.28, H - 0.28],
            color=ORANGE, linewidth=1.5, linestyle="--", alpha=0.6, zorder=2)
    ax.text(BND_X, 0.14, "information boundary",
            ha="center", va="bottom", fontsize=8.5, color=ORANGE, style="italic")

    # Post input node and restricted reasoning lenses
    PIN_X, PIN_Y = 0.82, 2.20
    PIN_W, PIN_H = 1.15, 0.78
    solid_box(ax, PIN_X, PIN_Y, PIN_W, PIN_H,
              GREY, 0.18, "Post\ninput", fs=9.4)

    LENS_X = 2.80
    LENS_W, LENS_H = 1.65, 0.62
    LENS_CY = [3.28, 2.60, 1.92]
    LENS_LABELS = ["Abductive", "Forward", "Sequential"]
    for cy, lbl in zip(LENS_CY, LENS_LABELS):
        solid_box(ax, LENS_X, cy - LENS_H/2, LENS_W, LENS_H,
                  GREEN, 0.15, lbl, fs=10.6, weight="bold")

    FAN_SRC_X = PIN_X + PIN_W
    FAN_SRC_Y = PIN_Y + PIN_H / 2
    for cy in LENS_CY:
        arr(ax, FAN_SRC_X, FAN_SRC_Y,
            LENS_X, cy, BLUE, lw=1.35, ms=12)

    # Synthesis layer: lens outputs and context are separated before judgment.
    HYP_X, HYP_Y = IJ_X + 0.42, 2.23
    HYP_W, HYP_H = 1.55, 0.74
    solid_box(ax, HYP_X, HYP_Y, HYP_W, HYP_H,
              GREEN, 0.12, "Lens\nhypotheses", fs=9.0)

    CTX_X, CTX_Y = HYP_X, 3.25
    CTX_W, CTX_H = HYP_W, 0.74
    solid_box(ax, CTX_X, CTX_Y, CTX_W, CTX_H,
              ORANGE, 0.12, "Context\nset", fs=9.0)

    JS_X = IJ_X + 3.00
    JS_Y = 2.10
    JS_W, JS_H = 2.05, 1.00
    solid_box(ax, JS_X, JS_Y, JS_W, JS_H,
              ORANGE, 0.14, "Judgment\nsynthesizer", fs=10.8)

    HYP_ENTRY_YS = [
        HYP_Y + HYP_H * 0.78,
        HYP_Y + HYP_H * 0.50,
        HYP_Y + HYP_H * 0.22,
    ]
    for cy, ey in zip(LENS_CY, HYP_ENTRY_YS):
        arr(ax, LENS_X + LENS_W, cy,
            HYP_X, ey, GREEN, lw=1.25, ms=11)

    arr(ax, HYP_X + HYP_W, HYP_Y + HYP_H / 2,
        JS_X, JS_Y + JS_H * 0.38,
        ORANGE, lw=1.35, ms=12)
    arr(ax, CTX_X + CTX_W, CTX_Y + CTX_H / 2,
        JS_X, JS_Y + JS_H * 0.72,
        ORANGE, lw=1.35, ms=12)

    # Bounded classification output
    BC_X = JS_X + 0.12
    BC_Y = 0.82
    BC_W, BC_H = 1.82, 0.64
    solid_box(ax, BC_X, BC_Y, BC_W, BC_H,
              GREY, 0.14, "Bounded\nclassification", fs=9.0)
    arr(ax, JS_X + JS_W/2, JS_Y,
        BC_X + BC_W/2, BC_Y + BC_H,
        DARK, lw=1.4, ms=13)

    return save_fig(fig, "figure08_information_sets_en.png", save_vector=True)


# ===========================================================================
# FIGURE 9 -- Stage 2 -> Stage 3 sequential handoff (detailed view)
#
# Layout:
#   Left column  (Stage 2, blue box): vertical EB cascade (7 nodes).
#                Outlier-cells (OC2) box to the RIGHT of z_shift node.
#                Handoff arrow: OC2 right edge -> Post(input) left edge, horizontal.
#   Right column (Stage 3, green box): LEFT/RIGHT split (not top/bottom).
#     I_R sub-region (left ~45%): Post(input) node + three stacked lenses.
#       Fan-out: Post right -> each lens left, short diagonal, well-separated.
#     I_J sub-region (right ~52%): Judgment synthesizer + 4-item cascade.
#       Fan-in: each lens right -> JS left, short near-horizontal, staggered.
#
# This LEFT/RIGHT Stage 3 layout makes fan-in arrows short and clean
# (same principle as Figure 8), eliminating the long diagonal bundle defect.
#
# Defects fixed vs. previous version:
#   1. OC2 box sized W=2.20, H=0.90 -- single-line title, body line, no overlap.
#   2. Handoff arrow is purely horizontal; no vertical drop -> no orphan line.
#   3. Lens->JS fan-in is short horizontal hops, not long panel-crossing diagonals.
#   4. Handoff label is placed above the arrow gap, clear of all box borders.
# ===========================================================================

def make_figure09():
    # Compact two-column layout with a horizontal Stage 2 -> Stage 3 handoff.
    W, H = 13.0, 9.8
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    # Column bounding boxes
    C2_X, C2_Y = 0.25, 0.25
    C2_W = 4.90
    C2_H = H - 0.50
    dbox(ax, C2_X, C2_Y, C2_W, C2_H, ec=BLUE, fc=IR_FILL, lw=1.1)
    ax.text(C2_X + 0.20, C2_Y + C2_H - 0.10,
            "Stage 2 -- EB Aggregation",
            ha="left", va="top", fontsize=10.5, fontweight="bold", color=BLUE)
    ax.text(C2_X + 0.20, C2_Y + C2_H - 0.44,
            "Unit of analysis: district x dimension cell",
            ha="left", va="top", fontsize=8.5, style="italic", color=MID)

    C3_X = C2_X + C2_W + 0.35
    C3_Y = C2_Y
    C3_W = W - C3_X - 0.25
    C3_H = C2_H
    dbox(ax, C3_X, C3_Y, C3_W, C3_H, ec=GREEN, fc=S3_FILL, lw=1.1)
    ax.text(C3_X + 0.20, C3_Y + C3_H - 0.10,
            "Stage 3 -- Agent-Based Post Interpretation",
            ha="left", va="top", fontsize=10.5, fontweight="bold", color=GREEN)
    ax.text(C3_X + 0.20, C3_Y + C3_H - 0.44,
            "Unit of analysis: individual post",
            ha="left", va="top", fontsize=8.5, style="italic", color=MID)

    # Stage 2: vertical EB cascade with compact labels.
    BW2, BH2 = 2.15, 0.54
    GAP2 = 0.20
    STEP2 = BH2 + GAP2

    EB_NODES = [
        ("Classified posts\n(Stage 1)", GREY, 0.18, ""),
        ("Admin-dong\nlinkage", BLUE, 0.13, ""),
        ("Population\nexposure", BLUE, 0.13, "hourly person-time"),
        ("Observed\npost rate", BLUE, 0.13, ""),
        ("EB shrinkage", BLUE, 0.13, "prior + observed rate"),
        ("Posterior rate\n(per 100k py)", BLUE, 0.13, ""),
        ("Within-dimension\nz_shift", BLUE, 0.13, ""),
    ]
    N2 = len(EB_NODES)

    CX2 = C2_X + 1.78
    y_top2 = 8.20
    eb_tops = [y_top2 - i * STEP2 for i in range(N2)]

    for i, ((lbl, col, a, sub), ty) in enumerate(zip(EB_NODES, eb_tops)):
        solid_box(ax, CX2 - BW2/2, ty, BW2, BH2, col, alpha=a,
                  label=lbl, fs=8.2, sublabel=sub, subfs=7.0)
        if i > 0:
            arr(ax, CX2, eb_tops[i-1],
                CX2, ty + BH2,
                col, ms=10)

    ZSHIFT_Y = eb_tops[-1]
    ZSHIFT_MID = ZSHIFT_Y + BH2 / 2

    # Outlier-cell handoff is aligned horizontally with z_shift.
    OC2_W, OC2_H = 1.42, 0.58
    OC2_X = C2_X + 3.30
    OC2_Y = ZSHIFT_MID - OC2_H / 2
    outline_box(ax, OC2_X, OC2_Y, OC2_W, OC2_H,
                ec=ORANGE, fc="#FFF8EE",
                title="Outlier cells",
                lines=("district x dimension",),
                title_fs=7.8, body_fs=6.8, zorder=4)
    arr(ax, CX2 + BW2 / 2, ZSHIFT_MID,
        OC2_X, ZSHIFT_MID,
        ORANGE, ms=10, lw=1.4)

    # Stage 3 sub-layout
    S3_IN_X = C3_X + 0.28
    S3_IN_W = C3_W - 0.56
    S3_IN_Y = C3_Y + 0.70
    S3_IN_TOP = C3_Y + C3_H - 1.55
    S3_IN_H = S3_IN_TOP - S3_IN_Y

    IR9_W = 2.82
    IJ9_GAP = 0.25
    IJ9_X = S3_IN_X + IR9_W + IJ9_GAP
    IJ9_W = S3_IN_X + S3_IN_W - IJ9_X

    dbox(ax, S3_IN_X, S3_IN_Y, IR9_W, S3_IN_H,
         ec=BLUE, fc=IR_FILL, lw=1.0)
    ax.text(S3_IN_X + 0.10, S3_IN_TOP - 0.08,
            r"$I_R$: restricted inputs",
            ha="left", va="top", fontsize=7.8, style="italic", color=BLUE)
    ax.text(S3_IN_X + 0.10, S3_IN_TOP - 0.32,
            "post + metadata + codebook",
            ha="left", va="top", fontsize=7.6, style="italic", color=BLUE)

    dbox(ax, IJ9_X, S3_IN_Y, IJ9_W, S3_IN_H,
         ec=ORANGE, fc=IJ_FILL, lw=1.0)
    ax.text(IJ9_X + 0.10, S3_IN_TOP - 0.08,
            r"$I_J$: expanded judgment set",
            ha="left", va="top", fontsize=7.8, style="italic", color=ORANGE)
    ax.text(IJ9_X + 0.10, S3_IN_TOP - 0.32,
            "hypotheses + context",
            ha="left", va="top", fontsize=7.6, style="italic", color=ORANGE)

    # Post input and reasoning lenses
    PW, PH = 0.82, 0.56
    PX = S3_IN_X + 0.22
    PY = ZSHIFT_MID - PH / 2
    solid_box(ax, PX, PY, PW, PH, GREY, 0.18, "Post", fs=8.8)

    POST_MID_Y = PY + PH / 2

    arr(ax, OC2_X + OC2_W, ZSHIFT_MID,
        PX, POST_MID_Y,
        ORANGE, lw=1.5, ms=12, zorder=5)

    ARROW_MID_X = (OC2_X + OC2_W + PX) / 2

    LW9, LH9 = 1.20, 0.54
    LENS9_X = PX + PW + 0.22
    LENS_PITCH = LH9 + 0.18

    LENS9_CY = [
        ZSHIFT_MID + LENS_PITCH,
        ZSHIFT_MID,
        ZSHIFT_MID - LENS_PITCH,
    ]
    LENS_LABELS = ["Abductive\nlens", "Forward\nlens", "Sequential\nlens"]
    for cy, lbl in zip(LENS9_CY, LENS_LABELS):
        solid_box(ax, LENS9_X, cy - LH9/2, LW9, LH9,
                  GREEN, 0.15, lbl, fs=7.8, weight="bold")

    FAN_SX = PX + PW
    FAN_SY = POST_MID_Y
    for cy in LENS9_CY:
        arr(ax, FAN_SX, FAN_SY,
            LENS9_X, cy,
            GREEN, lw=1.3, ms=10)

    # Judgment synthesizer and bounded-output checks
    JS9_W, JS9_H = 1.55, 0.64
    JS9_X = IJ9_X + 0.32
    JS9_Y = ZSHIFT_MID - JS9_H / 2

    solid_box(ax, JS9_X, JS9_Y, JS9_W, JS9_H,
              ORANGE, 0.15, "Judgment\nsynthesizer", fs=8.3)

    JS9_ENTRY_YS = [
        JS9_Y + JS9_H * 0.78,
        JS9_Y + JS9_H * 0.50,
        JS9_Y + JS9_H * 0.22,
    ]
    for cy, ey in zip(LENS9_CY, JS9_ENTRY_YS):
        arr(ax, LENS9_X + LW9, cy,
            JS9_X, ey,
            ORANGE, lw=1.3, ms=10)

    CSC9_W    = JS9_W
    CSC9_H    = 0.46
    CSC9_GAP  = 0.16
    CSC9_STEP = CSC9_H + CSC9_GAP
    N_CSC9    = 4

    csc9_item_tops = [
        JS9_Y - 0.28 - CSC9_H - i * CSC9_STEP
        for i in range(N_CSC9)
    ]

    CASCADE9 = [
        ("Convergence\ncheck", ORANGE, 0.14),
        ("Alternative\nexplanations", GREY, 0.18),
        ("Bounded\ncode", GREY, 0.18),
        ("Audit\ntrail", GREY, 0.18),
    ]
    CX9 = JS9_X + CSC9_W / 2

    for i, ((lbl, col, a), top_y) in enumerate(zip(CASCADE9, csc9_item_tops)):
        solid_box(ax, JS9_X, top_y, CSC9_W, CSC9_H, col, alpha=a,
                  label=lbl, fs=7.6)
        if i == 0:
            arr(ax, CX9, JS9_Y,
                CX9, top_y + CSC9_H + 0.03,
                ORANGE, ms=11)
        else:
            arr(ax, CX9, csc9_item_tops[i-1],
                CX9, top_y + CSC9_H + 0.03,
                DARK, ms=11)

    return save_fig(fig, "figure09_sequential_eb_to_agent_en.png", save_vector=True)


# ===========================================================================
# Main
# ===========================================================================

if __name__ == "__main__":
    import warnings
    # Suppress the harmless zero-length arrow head_dist warning from matplotlib
    warnings.filterwarnings("ignore", category=RuntimeWarning,
                            message="invalid value encountered in scalar divide")
    print("Generating Figure 7 ...")
    p7 = make_figure07()
    print("Generating Figure 8 ...")
    p8 = make_figure08()
    print("Generating Figure 9 ...")
    p9 = make_figure09()
    print("\nDone.")
    print(f"  Figure 7: {p7}")
    print(f"  Figure 8: {p8}")
    print(f"  Figure 9: {p9}")
