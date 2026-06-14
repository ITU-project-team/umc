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


def save_fig(fig, name, tight_pad=0.15):
    out = FIG_DIR / name
    fig.savefig(out, bbox_inches="tight", pad_inches=tight_pad)
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
    W, H = 13.0, 5.8
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    # Left region: Restricted layer (I_R)
    IR_X, IR_Y = 0.20, 0.30
    IR_W, IR_H = 5.60, H - 0.55
    dbox(ax, IR_X, IR_Y, IR_W, IR_H, ec=BLUE, fc=IR_FILL, lw=1.4)
    ax.text(IR_X + 0.22, IR_Y + IR_H - 0.10,
            "Restricted layer", ha="left", va="top",
            fontsize=11.5, fontweight="bold", color=BLUE)
    ax.text(IR_X + 0.22, IR_Y + IR_H - 0.44,
            r"$I_R$  restricted input",
            ha="left", va="top", fontsize=9.5, style="italic", color=BLUE)

    # Right region: Synthesis layer (I_J)
    IJ_X, IJ_Y = 6.10, 0.30
    IJ_W, IJ_H = W - 6.10 - 0.20, H - 0.55
    dbox(ax, IJ_X, IJ_Y, IJ_W, IJ_H, ec=ORANGE, fc=IJ_FILL, lw=1.4)
    ax.text(IJ_X + 0.22, IJ_Y + IJ_H - 0.10,
            "Synthesis layer", ha="left", va="top",
            fontsize=11.5, fontweight="bold", color=ORANGE)
    ax.text(IJ_X + 0.22, IJ_Y + IJ_H - 0.44,
            r"$I_J$  expanded judgment set",
            ha="left", va="top", fontsize=9.5, style="italic", color=ORANGE)

    # Boundary dashed line
    BND_X = 5.88
    ax.plot([BND_X, BND_X], [0.22, H - 0.22],
            color=ORANGE, linewidth=1.5, linestyle="--", alpha=0.6, zorder=2)
    ax.text(BND_X, 0.10, "boundary",
            ha="center", va="bottom", fontsize=8.5, color=ORANGE, style="italic")

    # Post input node
    PIN_X, PIN_Y = 0.52, H/2 - 0.55
    PIN_W, PIN_H = 1.45, 1.10
    outline_box(ax, PIN_X, PIN_Y, PIN_W, PIN_H,
                ec=GREY, fc=LIGHT,
                title="Post input",
                lines=("post text", "metadata", "codebook"),
                title_fs=9.5, body_fs=9.0)

    # Three lenses stacked vertically in I_R centre
    LENS_X = 2.50
    LENS_W, LENS_H = 1.90, 0.75
    # y-centres for three lenses
    LENS_CY = [H/2 + 0.72, H/2 - 0.02, H/2 - 0.76]
    LENS_LABELS = ["Abductive", "Forward", "Sequential"]
    for cy, lbl in zip(LENS_CY, LENS_LABELS):
        solid_box(ax, LENS_X, cy - LENS_H/2, LENS_W, LENS_H,
                  GREEN, 0.15, lbl, fs=11, weight="bold")

    # Fan-out from post input right edge to three lenses
    FAN_SRC_X = PIN_X + PIN_W
    FAN_SRC_Y = PIN_Y + PIN_H / 2
    for cy in LENS_CY:
        arr(ax, FAN_SRC_X, FAN_SRC_Y,
            LENS_X, cy,
            BLUE, lw=1.4, ms=13)

    # Additional context box (in I_J, upper-left)
    AI_X = IJ_X + 0.28
    AI_Y = H/2 - 0.02
    AI_W, AI_H = 2.10, 1.60
    outline_box(ax, AI_X, AI_Y, AI_W, AI_H,
                ec=ORANGE, fc="#FFF8EE",
                title="Additional context",
                lines=("district context",
                       "absence typology",
                       "active category set"),
                title_fs=9.2, body_fs=8.8)

    # Judgment synthesis box
    JS_X = IJ_X + 2.85
    JS_Y = H/2 - 0.60
    JS_W, JS_H = 2.05, 1.20
    solid_box(ax, JS_X, JS_Y, JS_W, JS_H,
              ORANGE, 0.14, "Judgment\nsynthesis", fs=11.5)

    # Fan-in: three lenses -> judgment synthesis (staggered y entry)
    JS_ENTRY_YS = [
        JS_Y + JS_H * 0.78,
        JS_Y + JS_H * 0.50,
        JS_Y + JS_H * 0.22,
    ]
    for cy, ey in zip(LENS_CY, JS_ENTRY_YS):
        arr(ax, LENS_X + LENS_W, cy,
            JS_X, ey,
            ORANGE, lw=1.4, ms=13)

    # Additional context -> judgment synthesis
    arr(ax, AI_X + AI_W, AI_Y + AI_H/2,
        JS_X, JS_Y + JS_H/2,
        ORANGE, lw=1.3, ms=12)

    # Bounded classification output
    BC_X = IJ_X + 3.15
    BC_Y = 0.55
    BC_W, BC_H = 1.95, 0.72
    outline_box(ax, BC_X, BC_Y, BC_W, BC_H,
                ec=DARK, fc=LIGHT,
                title="Bounded classification",
                title_fs=9.5, zorder=4)
    arr(ax, JS_X + JS_W/2, JS_Y,
        BC_X + BC_W/2, BC_Y + BC_H,
        DARK, lw=1.4, ms=13)

    return save_fig(fig, "figure08_information_sets_en.png")


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
    # Canvas
    W, H = 13.0, 12.0
    fig, ax = plt.subplots(figsize=(W, H))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    # -------------------------------------------------------------------
    # Column bounding boxes
    # Canvas H=12.0; both columns: bottom=0.20, height=11.60
    # -------------------------------------------------------------------
    C2_X, C2_Y = 0.20, 0.20
    C2_W = 5.00
    C2_H = H - 0.40    # 11.60
    dbox(ax, C2_X, C2_Y, C2_W, C2_H, ec=BLUE, fc=IR_FILL, lw=1.1)
    ax.text(C2_X + 0.20, C2_Y + C2_H - 0.10,
            "Stage 2 -- EB Shrinkage Rate Aggregation",
            ha="left", va="top", fontsize=10.5, fontweight="bold", color=BLUE)
    ax.text(C2_X + 0.20, C2_Y + C2_H - 0.44,
            "Unit of analysis: district x dimension cell",
            ha="left", va="top", fontsize=8.5, style="italic", color=MID)

    C3_X = C2_X + C2_W + 0.30   # 5.50
    C3_Y = C2_Y
    C3_W = W - C3_X - 0.20      # 7.30
    C3_H = C2_H                  # 11.60
    dbox(ax, C3_X, C3_Y, C3_W, C3_H, ec=GREEN, fc=S3_FILL, lw=1.1)
    ax.text(C3_X + 0.20, C3_Y + C3_H - 0.10,
            "Stage 3 -- Agent-Based Post Interpretation",
            ha="left", va="top", fontsize=10.5, fontweight="bold", color=GREEN)
    ax.text(C3_X + 0.20, C3_Y + C3_H - 0.44,
            "Unit of analysis: individual post",
            ha="left", va="top", fontsize=8.5, style="italic", color=MID)

    # -------------------------------------------------------------------
    # Stage 2: vertical EB cascade (7 nodes)
    # First node top at y_top2=10.00, clearing subtitle (~11.10) by 0.40".
    # -------------------------------------------------------------------
    BW2, BH2 = 2.20, 0.70
    GAP2  = 0.28
    STEP2 = BH2 + GAP2   # 0.98

    EB_NODES = [
        ("Classified-post base\n(from Stage 1)", GREY, 0.18, ""),
        ("Administrative-dong\nlinkage",           BLUE, 0.13, ""),
        ("Living-population\nexposure",            BLUE, 0.13, "hourly person-time"),
        ("Observed post rate",                      BLUE, 0.13, ""),
        ("EB shrinkage",                            BLUE, 0.13,
         "prior = Part 1 deficiency\nposterior = precision-weighted mean"),
        ("Posterior rate\n(per 100k person-years)", BLUE, 0.13, ""),
        ("Within-dimension\nz_shift",               BLUE, 0.13, ""),
    ]
    N2 = len(EB_NODES)

    CX2    = C2_X + C2_W / 2           # 2.70
    y_top2 = 10.00                      # first node: [10.00, 10.70], subtitle ~11.10 -> gap 0.40
    eb_tops = [y_top2 - i * STEP2 for i in range(N2)]

    for i, ((lbl, col, a, sub), ty) in enumerate(zip(EB_NODES, eb_tops)):
        solid_box(ax, CX2 - BW2/2, ty, BW2, BH2, col, alpha=a,
                  label=lbl, fs=8.8, sublabel=sub, subfs=7.5)
        if i > 0:
            arr(ax, CX2, eb_tops[i-1],
                CX2, ty + BH2,
                col, ms=10)

    # ZSHIFT_MID: vertical mid of the last cascade node (Within-dimension z_shift)
    ZSHIFT_BOT = eb_tops[-1]           # 4.12
    ZSHIFT_MID = ZSHIFT_BOT + BH2 / 2  # 4.47

    # -------------------------------------------------------------------
    # OC2 box -- placed BELOW z_shift node, inside C2 column.
    # Arrow: from z_shift node bottom-centre down to OC2 top-centre.
    # Width spans most of C2 inner width for readable two-line text.
    # -------------------------------------------------------------------
    OC2_W, OC2_H = 2.40, 0.80
    OC2_GAP = 0.18
    OC2_X = C2_X + (C2_W - OC2_W) / 2   # horizontally centred in C2
    OC2_Y = ZSHIFT_BOT - OC2_GAP - OC2_H   # 3.14

    outline_box(ax, OC2_X, OC2_Y, OC2_W, OC2_H,
                ec=ORANGE, fc="#FFF8EE",
                title="High-z_shift outlier cells",
                lines=("district x dimension",),
                title_fs=9.0, body_fs=8.2, zorder=4)
    # Arrow: z_shift bottom -> OC2 top (short vertical drop)
    arr(ax, CX2, ZSHIFT_BOT,
        CX2, OC2_Y + OC2_H,
        ORANGE, ms=11, lw=1.5)

    # Handoff start: OC2 right-centre
    OC2_MID_Y  = OC2_Y + OC2_H / 2    # 3.54

    # -------------------------------------------------------------------
    # Stage 3 horizontal sub-layout geometry
    # S3_IN: inner region of Stage 3 column, inside the green dbox.
    # I_R: left ~43% for Post(input) + three lenses.
    # I_J: right ~55% for Judgment synthesizer + cascade.
    # -------------------------------------------------------------------
    S3_PAD_X  = 0.28
    S3_PAD_Y  = 0.22
    S3_IN_X   = C3_X + S3_PAD_X                # 5.78
    S3_IN_W   = C3_W - 2 * S3_PAD_X            # 6.74
    S3_IN_Y   = C3_Y + S3_PAD_Y                # 0.42
    # S3_IN_TOP is capped below the Stage 3 column header/subtitle
    # to prevent I_R / I_J sub-region header labels from overlapping Stage 3 title text.
    # Stage 3 subtitle is at C3_Y+C3_H-0.44=11.36; set sub-box top 0.45" below that.
    S3_IN_TOP = (C3_Y + C3_H - 0.44) - 0.45   # 10.91
    S3_IN_H   = S3_IN_TOP - S3_IN_Y            # 10.49

    IR9_W   = S3_IN_W * 0.43    # 2.90
    IJ9_GAP = 0.22
    IJ9_X   = S3_IN_X + IR9_W + IJ9_GAP       # 8.90
    IJ9_W   = S3_IN_X + S3_IN_W - IJ9_X        # 3.62

    # I_R sub-region dbox (extends full height of S3_IN)
    dbox(ax, S3_IN_X, S3_IN_Y, IR9_W, S3_IN_H,
         ec=BLUE, fc=IR_FILL, lw=1.0)
    ax.text(S3_IN_X + 0.10, S3_IN_TOP - 0.08,
            r"$I_R$: post text + metadata + codebook",
            ha="left", va="top", fontsize=7.5, style="italic", color=BLUE)
    ax.text(S3_IN_X + 0.10, S3_IN_TOP - 0.32,
            "three lenses independent",
            ha="left", va="top", fontsize=7.5, style="italic", color=BLUE)

    # I_J sub-region dbox
    dbox(ax, IJ9_X, S3_IN_Y, IJ9_W, S3_IN_H,
         ec=ORANGE, fc=IJ_FILL, lw=1.0)
    ax.text(IJ9_X + 0.10, S3_IN_TOP - 0.08,
            r"$I_J$: hypotheses + district context",
            ha="left", va="top", fontsize=7.5, style="italic", color=ORANGE)
    ax.text(IJ9_X + 0.10, S3_IN_TOP - 0.32,
            "absence typology + active category set",
            ha="left", va="top", fontsize=7.5, style="italic", color=ORANGE)

    # -------------------------------------------------------------------
    # Post (input) node -- left edge of I_R, vertically centred at ZSHIFT_MID.
    # Handoff: OC2 right-mid -> Post left-mid (short angled arrow across gap).
    # -------------------------------------------------------------------
    PW, PH = 1.00, 0.68
    PX = S3_IN_X + 0.14                     # 5.92
    PY = ZSHIFT_MID - PH / 2               # 4.13 -- centred at ZSHIFT_MID=4.47
    PY = max(S3_IN_Y + 0.50, min(PY, S3_IN_TOP - PH - 0.50))

    solid_box(ax, PX, PY, PW, PH, GREY, 0.18, "Post\n(input)", fs=9.0)

    POST_MID_Y = PY + PH / 2               # 4.47

    # Handoff arrow: OC2 right-mid -> Post left-mid
    arr(ax, OC2_X + OC2_W, OC2_MID_Y,
        PX, POST_MID_Y,
        ORANGE, lw=1.7, ms=14, zorder=5)

    # Label placed just above the midpoint of the handoff arrow.
    # x-centre at arrow midpoint (between OC2 right edge and Post left edge),
    # y slightly above the arrow midpoint -- stays clear of all box borders.
    ARROW_MID_X = (OC2_X + OC2_W + PX) / 2
    ARROW_MID_Y = (OC2_MID_Y + POST_MID_Y) / 2
    LABEL_MID_X = ARROW_MID_X
    LABEL_Y     = ARROW_MID_Y + 0.22
    ax.text(LABEL_MID_X, LABEL_Y,
            "outlier-cell posts as input",
            ha="center", fontsize=7.8, style="italic", color=ORANGE)

    # -------------------------------------------------------------------
    # Three lenses -- stacked in I_R, right of Post node.
    # Centres at ZSHIFT_MID (+/- LENS_PITCH) so fan-out arrows are short.
    # -------------------------------------------------------------------
    LW9, LH9   = 1.35, 0.62
    LENS9_X    = PX + PW + 0.20             # 7.12
    LENS_PITCH = LH9 + 0.24                 # 0.86 between centres

    LENS9_CY = [
        ZSHIFT_MID + LENS_PITCH,            # top lens centre   5.33
        ZSHIFT_MID,                          # mid lens centre   4.47
        ZSHIFT_MID - LENS_PITCH,            # bot lens centre   3.61
    ]
    LENS_LABELS = ["Abductive\nlens", "Forward\nlens", "Sequential\nlens"]
    for cy, lbl in zip(LENS9_CY, LENS_LABELS):
        solid_box(ax, LENS9_X, cy - LH9/2, LW9, LH9,
                  GREEN, 0.15, lbl, fs=8.8, weight="bold")

    # Fan-out: Post right-mid -> each lens left-centre (short diagonals)
    FAN_SX = PX + PW
    FAN_SY = POST_MID_Y
    for cy in LENS9_CY:
        arr(ax, FAN_SX, FAN_SY,
            LENS9_X, cy,
            GREEN, lw=1.3, ms=10)

    # -------------------------------------------------------------------
    # Judgment synthesizer -- I_J left region, centred at ZSHIFT_MID.
    # Fan-in: each lens right-centre -> JS left, staggered y entries.
    # Hop distance ~0.61" (LENS9_X+LW9 to JS9_X).
    # -------------------------------------------------------------------
    JS9_W, JS9_H = 1.55, 0.72
    JS9_X = IJ9_X + 0.18                    # 9.08
    JS9_Y = ZSHIFT_MID - JS9_H / 2         # 4.11

    solid_box(ax, JS9_X, JS9_Y, JS9_W, JS9_H,
              ORANGE, 0.15, "Judgment\nsynthesizer", fs=9.2)

    JS9_ENTRY_YS = [
        JS9_Y + JS9_H * 0.78,
        JS9_Y + JS9_H * 0.50,
        JS9_Y + JS9_H * 0.22,
    ]
    for cy, ey in zip(LENS9_CY, JS9_ENTRY_YS):
        arr(ax, LENS9_X + LW9, cy,
            JS9_X, ey,
            ORANGE, lw=1.3, ms=10)

    # -------------------------------------------------------------------
    # 4-item cascade below Judgment synthesizer (vertical, inside I_J).
    # Bottom-up placement to guarantee containment inside S3_IN.
    # -------------------------------------------------------------------
    CSC9_W    = JS9_W
    CSC9_H    = 0.58
    CSC9_GAP  = 0.22
    CSC9_STEP = CSC9_H + CSC9_GAP
    N_CSC9    = 4

    CSC9_LAST_Y = S3_IN_Y + 0.35
    csc9_item_tops = [
        CSC9_LAST_Y + (N_CSC9 - 1 - i) * CSC9_STEP
        for i in range(N_CSC9)
    ]

    CASCADE9 = [
        ("Convergence /\ndisagreement check", ORANGE, 0.14),
        ("Non-structural\nalternatives",       GREY,   0.18),
        ("Final bounded\ncode",                GREY,   0.18),
        ("Audit trail",                        GREY,   0.18),
    ]
    CX9 = JS9_X + CSC9_W / 2

    for i, ((lbl, col, a), top_y) in enumerate(zip(CASCADE9, csc9_item_tops)):
        solid_box(ax, JS9_X, top_y, CSC9_W, CSC9_H, col, alpha=a,
                  label=lbl, fs=8.4)
        if i == 0:
            arr(ax, CX9, JS9_Y,
                CX9, top_y + CSC9_H,
                ORANGE, ms=11)
        else:
            arr(ax, CX9, csc9_item_tops[i-1],
                CX9, top_y + CSC9_H,
                DARK, ms=11)

    ax.text(CX9, csc9_item_tops[-1] - 0.14,
            "Output unit: post-level case",
            ha="center", fontsize=7.8, style="italic", color=GREY)

    return save_fig(fig, "figure09_sequential_eb_to_agent_en.png")


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
