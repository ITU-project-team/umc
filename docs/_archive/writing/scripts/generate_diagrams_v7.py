"""
UMC Report v7 — Diagram Generator (v2 rewrite)
Clean academic-style diagrams with proper spacing and readability.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

plt.rcParams.update({
    "font.family": "Malgun Gothic",
    "font.size": 10,
    "axes.unicode_minus": False,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.4,
})

BASE = Path(r"C:\woo\Project\umc\Writing\figures")

# Muted academic palette
C = {
    "blue":    "#3B7DD8",
    "green":   "#2D8659",
    "orange":  "#D97706",
    "red":     "#DC2626",
    "purple":  "#7C3AED",
    "gray":    "#6B7280",
    "darkgray":"#374151",
}


def box(ax, cx, cy, w, h, text, color, fs=9.5, bold=False):
    """Rounded rectangle with text. No overlap, no bleeding."""
    r = FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle="round,pad=0.12",
        facecolor=color, alpha=0.12,
        edgecolor=color, linewidth=1.8,
    )
    ax.add_patch(r)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color="#1F2937",
            linespacing=1.4)


def arrow(ax, x1, y1, x2, y2, color="#6B7280", lw=1.5, style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))


def label(ax, x, y, text, color="#6B7280", fs=8, ha="center", rotation=0):
    ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va="center",
            rotation=rotation,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))


# ════════════════════════════════════════════════════════════
# A: Analysis Data Flow — vertical layout, no overlap
# ════════════════════════════════════════════════════════════
def diagram_a():
    fig, ax = plt.subplots(figsize=(11, 9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    # no title on figure

    # Row 1: top
    box(ax, 2.5, 8.5, 3.8, 1.2,
        "3.1 UMC 종합지수\n(25 자치구 x 6 차원 매트릭스)", C["blue"], fs=10, bold=True)
    box(ax, 7.5, 8.5, 3.8, 1.2,
        "3.2 HLM 다수준 분석\n(교차수준 상호작용)", C["green"], fs=10, bold=True)

    # Row 2: middle
    box(ax, 2.5, 5.0, 3.8, 1.2,
        "3.3 텍스트 분류\n(Y / N / ? 판정)", C["orange"], fs=10, bold=True)
    box(ax, 7.5, 5.0, 3.8, 1.2,
        "3.3 베이지안 집계\n(Beta-Binomial 사후 추정)", C["purple"], fs=10, bold=True)

    # Row 3: bottom
    box(ax, 5.0, 1.5, 4.2, 1.2,
        "3.3 추론 메커니즘\n(조건부: 유의미한 이동 시에만)", C["red"], fs=10, bold=True)

    # Arrows: 3.1 → 3.2
    arrow(ax, 4.4, 8.5, 5.6, 8.5, C["blue"])
    label(ax, 5.0, 8.85, "L2 변수", C["blue"], fs=8.5)

    # 3.1 → 텍스트 분류 (왼쪽 세로)
    arrow(ax, 2.5, 7.9, 2.5, 5.6, C["blue"])
    label(ax, 1.55, 6.75, "사전 분포", C["blue"], fs=8.5)

    # 3.1 → 베이지안 (대각선)
    arrow(ax, 4.4, 7.95, 5.7, 5.6, C["blue"])
    label(ax, 5.5, 7.0, "검증: Spearman rho", C["blue"], fs=8)

    # 텍스트 분류 → 베이지안
    arrow(ax, 4.4, 5.0, 5.6, 5.0, C["orange"])
    label(ax, 5.0, 5.35, "우도", C["orange"], fs=8.5)

    # 3.2 → 추론 (오른쪽에서 아래)
    arrow(ax, 7.5, 7.9, 7.5, 5.6, C["green"])
    label(ax, 8.5, 6.75, "추론 범위 제한", C["green"], fs=8.5)

    # 베이지안 → 추론
    arrow(ax, 7.5, 4.4, 6.2, 2.1, C["purple"])
    label(ax, 7.3, 3.25, "이동 판정", C["purple"], fs=8.5)

    # 3.2 → 추론 직접
    arrow(ax, 7.5, 4.4, 5.8, 2.1, C["green"])

    out = BASE / "ch1" / "fig_data_flow.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    print(f"[A] saved -> {out}")


# ════════════════════════════════════════════════════════════
# B: Simple vs Bayesian — two-column with clear spacing
# ════════════════════════════════════════════════════════════
def diagram_b():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7.5))
    # no title on figure

    # ── Left: Simple frequency ──
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis("off")
    ax1.set_title("단순 빈도 집계", fontsize=12, fontweight="bold",
                  color=C["red"], pad=12)

    box(ax1, 5, 8.5, 8, 1.0,
        "게시글 수: 관악구 43건  /  도봉구 2건", C["gray"], fs=11)

    arrow(ax1, 5, 8.0, 5, 7.2, C["darkgray"], lw=2)

    box(ax1, 5, 6.5, 8, 1.0,
        "결론: 관악 >> 도봉 (21.5배 심각)", C["red"], fs=11, bold=True)

    arrow(ax1, 5, 6.0, 5, 5.2, C["darkgray"], lw=2)

    box(ax1, 5, 4.2, 8, 1.6,
        "그런데 UMC 실측 확인:\n관악구 Skills = 0.795 (서울 1위)\n도봉구 Skills = 하위권",
        C["blue"], fs=10)

    arrow(ax1, 5, 3.4, 5, 2.5, C["darkgray"], lw=2)

    box(ax1, 5, 1.5, 8, 1.4,
        "문제: 빈도와 실측이 정반대 방향\n=> 빈도는 UMC가 아니라\n   플랫폼 활성도를 반영",
        C["red"], fs=10, bold=True)

    # ── Right: Bayesian ──
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis("off")
    ax2.set_title("베이지안 집계", fontsize=12, fontweight="bold",
                  color=C["green"], pad=12)

    box(ax2, 5, 8.8, 8, 0.9,
        "사전: 3.1절 UMC 실측 (Skills 점수)", C["blue"], fs=10.5, bold=True)

    arrow(ax2, 5, 8.35, 5, 7.7, C["darkgray"], lw=2)
    label(ax2, 6.5, 8.0, "kappa = 20", C["gray"], fs=8)

    box(ax2, 5, 7.0, 8, 0.9,
        "우도: 게시글 분류 (생활인구 보정)", C["orange"], fs=10.5, bold=True)

    arrow(ax2, 5, 6.55, 5, 5.9, C["darkgray"], lw=2)

    box(ax2, 5, 5.2, 8, 1.2,
        "사후 (관악구):\n사전이 강하므로 43건이 사후를 크게 움직이지 않음\n=> 실측과 유사한 수준 유지",
        C["green"], fs=10)

    arrow(ax2, 5, 4.6, 5, 3.9, C["darkgray"], lw=2)

    box(ax2, 5, 3.1, 8, 1.2,
        "사후 (도봉구):\n2건만으로는 증거 부족\n=> 사전에서 거의 이동 없음 = 판단 유보",
        C["purple"], fs=10)

    arrow(ax2, 5, 2.5, 5, 1.8, C["darkgray"], lw=2)

    box(ax2, 5, 1.0, 8.5, 1.2,
        "핵심: 게시글은 직접 측정이 아니라\n기존 측정을 수정(update)하는 증거",
        C["green"], fs=10.5, bold=True)

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    out = BASE / "ch3_3" / "fig_bayesian_comparison.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    print(f"[B] saved -> {out}")


# ════════════════════════════════════════════════════════════
# C: Structure-Mechanism-Experience — clean 3-tier
# ════════════════════════════════════════════════════════════
def diagram_c():
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    # no title on figure

    bw, bh = 6.0, 1.6

    # Top: Structure
    box(ax, 5, 8.5, bw, bh,
        "구조 (Structure)\n3.1 UMC 지역 지표\n자치구 수준의 디지털 연결성 조건",
        C["blue"], fs=10.5, bold=True)

    # Middle: Mechanism
    box(ax, 5, 5.0, bw, 2.0,
        "메커니즘 (Mechanism)\n추론 단계: 구조가 개인에게 작용하는 경로\n\n예: 공공 접근점 부재 -> 과업 단절 -> 커뮤니티 의존\n* 3.2 HLM 결과가 허용하는 범위 내에서만 추론",
        C["green"], fs=10, bold=True)

    # Bottom: Experience
    box(ax, 5, 1.5, bw, bh,
        "경험 (Experience)\n게시글: 개인 수준의 경험적 사건\n디지털 연결성 문제의 일상적 발현",
        C["orange"], fs=10.5, bold=True)

    # Vertical arrows between layers
    arrow(ax, 5, 7.7, 5, 6.0, C["darkgray"], lw=2.5)
    label(ax, 5, 6.85, "(관찰되지 않는 메커니즘)", C["gray"], fs=9)

    arrow(ax, 5, 4.0, 5, 2.3, C["darkgray"], lw=2.5)

    # Right side: Bhaskar labels
    ax.text(8.8, 8.5, "Bhaskar:\n실재 (Real)", fontsize=9, ha="center",
            color=C["blue"], style="italic", fontweight="bold")
    ax.text(8.8, 5.0, "Bhaskar:\n현실 (Actual)", fontsize=9, ha="center",
            color=C["green"], style="italic", fontweight="bold")
    ax.text(8.8, 1.5, "Bhaskar:\n경험 (Empirical)", fontsize=9, ha="center",
            color=C["orange"], style="italic", fontweight="bold")

    # Left side: Bayesian bridge
    arrow(ax, 1.3, 7.7, 1.3, 2.3, C["purple"], lw=2.5, style="<->")
    ax.text(0.6, 5.0, "베이지안\n집계", fontsize=10, ha="center",
            color=C["purple"], fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="#F5F3FF", ec=C["purple"], lw=1.2))

    # Connection labels
    ax.text(1.3, 7.0, "사전\n분포", fontsize=8, ha="center", color=C["purple"])
    ax.text(1.3, 3.0, "우도", fontsize=8, ha="center", color=C["purple"])

    out = BASE / "ch3_3" / "fig_structure_mechanism_experience.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    print(f"[C] saved -> {out}")


if __name__ == "__main__":
    print("Generating diagrams v2...")
    diagram_a()
    diagram_b()
    diagram_c()
    print("Done.")
