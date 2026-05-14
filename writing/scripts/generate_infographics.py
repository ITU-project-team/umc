"""KR 보고서용 인포그래픽 자산 생성.

생성물 (manuscript/output/doc/infographics/):
- umc_dimensions_hex.png : UMC 6개 차원 다이어그램 (헥사 형태)
- key_findings_card.png  : 핵심 발견 요약 카드
- analysis_pipeline.png  : 3단계 분석 파이프라인 인포그래픽
- digital_desert_summary.png : 디지털 사막 4개 자치구 요약
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Wedge, Circle, FancyArrowPatch
import numpy as np

# 한글 폰트 (macOS Apple SD Gothic Neo 사용)
matplotlib.rcParams["font.family"] = ["Apple SD Gothic Neo", "AppleGothic", "sans-serif"]
matplotlib.rcParams["axes.unicode_minus"] = False

NAVY = "#0E2A47"
NAVY_DARK = "#0A1F35"
NAVY_LIGHT = "#1E3A5F"
GOLD = "#B8860B"
GOLD_LIGHT = "#D4A82C"
TEAL = "#2C7A7B"
TEAL_SOFT = "#5BA3A4"
ACCENT_RED = "#C53030"
TEXT_BLACK = "#1A202C"
TEXT_GRAY = "#4A5568"
TEXT_GRAY_LIGHT = "#718096"
ZEBRA = "#F4F6F8"
LIGHT_GRAY = "#E2E8F0"
BG_NAVY_SOFT = "#EDF2F7"
BG_GOLD_SOFT = "#FFF8E6"
BG_TEAL_SOFT = "#E6F4F4"

OUT = Path("manuscript/output/doc/infographics")
OUT.mkdir(parents=True, exist_ok=True)


def _setup_axes(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def umc_dimensions_hex():
    """UMC 6개 차원 헥사 다이어그램."""
    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=200)
    _setup_axes(ax, (-1, 11), (-1, 7.5))
    fig.patch.set_facecolor("white")

    # 중앙 타이틀 영역
    title_box = FancyBboxPatch(
        (3.5, 5.7), 3, 1.0, boxstyle="round,pad=0.05,rounding_size=0.15",
        linewidth=0, facecolor=NAVY, edgecolor="none",
    )
    ax.add_patch(title_box)
    ax.text(5, 6.5, "UMC", color="white", fontsize=20, ha="center",
            va="center", fontweight="bold")
    ax.text(5, 5.95, "Universal Meaningful Connectivity",
            color=GOLD_LIGHT, fontsize=8.5, ha="center", va="center",
            fontweight="bold")

    # 6개 차원 (2 행 × 3 열)
    dims = [
        ("Connectivity", "연결성", "물리적 네트워크 인프라", NAVY, "◉"),
        ("Affordability", "경제적 접근성", "비용 부담 가능성", GOLD, "₩"),
        ("Devices", "기기 접근성", "기기 보유·이용 다양성", TEAL, "▣"),
        ("Digital Skills", "디지털 역량", "기초·응용·고급·사이버", NAVY_LIGHT, "✦"),
        ("Safety", "안전·보안", "보안 행동·인식", GOLD_LIGHT, "◈"),
        ("Avail. for Use", "이용 가능성", "공공 WiFi 등 가용성", TEAL_SOFT, "◎"),
    ]
    coords = [(0.6, 3.0), (3.7, 3.0), (6.8, 3.0),
              (0.6, 0.4), (3.7, 0.4), (6.8, 0.4)]
    for (en, ko, sub, color, icon), (x, y) in zip(dims, coords):
        # 박스
        box = FancyBboxPatch(
            (x, y), 2.5, 2.1, boxstyle="round,pad=0.05,rounding_size=0.1",
            linewidth=1.5, facecolor="white", edgecolor=color,
        )
        ax.add_patch(box)
        # 색상 헤더 띠
        header = FancyBboxPatch(
            (x, y + 1.6), 2.5, 0.5,
            boxstyle="round,pad=0,rounding_size=0.1",
            linewidth=0, facecolor=color, edgecolor="none",
        )
        ax.add_patch(header)
        # 한글 라벨 (헤더)
        ax.text(x + 1.25, y + 1.85, ko, color="white",
                fontsize=11, ha="center", va="center", fontweight="bold")
        # 영문 라벨
        ax.text(x + 1.25, y + 1.1, en, color=TEXT_BLACK,
                fontsize=10, ha="center", va="center", fontweight="bold")
        # 서브 라벨
        ax.text(x + 1.25, y + 0.55, sub, color=TEXT_GRAY,
                fontsize=8, ha="center", va="center")
        # 아이콘
        ax.text(x + 1.25, y + 0.2, icon, color=color,
                fontsize=12, ha="center", va="center")

    # 화살표: 중앙에서 6 차원으로
    for (x, y) in coords:
        cx, cy = 5.0, 5.6
        tx, ty = x + 1.25, y + 2.1
        # 단순 라인
        ax.plot([cx, tx], [cy, ty], color=LIGHT_GRAY, linewidth=0.7,
                linestyle="--", zorder=0)

    # 하단 캡션
    ax.text(5, -0.5, "ITU UMC 프레임 · 6개 차원 측정 체계 (ITU 2023 기반)",
            color=TEXT_GRAY_LIGHT, fontsize=8, ha="center", va="center",
            style="italic")

    plt.tight_layout()
    fig.savefig(OUT / "umc_dimensions_hex.png", dpi=200,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {OUT / 'umc_dimensions_hex.png'}")


def key_findings_card():
    """핵심 발견 4개 통계 카드."""
    fig, ax = plt.subplots(figsize=(9, 3.5), dpi=200)
    _setup_axes(ax, (0, 12), (0, 4))
    fig.patch.set_facecolor("white")

    # 좌측 strip 라벨
    strip = FancyBboxPatch(
        (0, 0), 0.3, 4, boxstyle="round,pad=0,rounding_size=0",
        linewidth=0, facecolor=NAVY,
    )
    ax.add_patch(strip)

    # 4개 KPI
    kpis = [
        ("0.279", "최하위 자치구\n(중랑구)", NAVY),
        ("0.695", "최상위 자치구\n(서초구)", GOLD),
        ("2.5×", "상·하위 격차", TEAL),
        ("4 개", "디지털 사막\n자치구", ACCENT_RED),
    ]
    x0 = 0.8
    width = 2.6
    gap = 0.2
    for i, (val, lbl, color) in enumerate(kpis):
        x = x0 + i * (width + gap)
        # 카드 배경
        card = FancyBboxPatch(
            (x, 0.2), width, 3.6,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            linewidth=1.2, facecolor="white",
            edgecolor=LIGHT_GRAY,
        )
        ax.add_patch(card)
        # 색상 액센트 바
        bar = FancyBboxPatch(
            (x, 3.3), width, 0.45,
            boxstyle="round,pad=0,rounding_size=0",
            linewidth=0, facecolor=color,
        )
        ax.add_patch(bar)
        ax.text(x + width / 2, 3.55, "KEY FINDING " + str(i + 1),
                color="white", fontsize=8, ha="center", va="center",
                fontweight="bold")
        # 큰 값
        ax.text(x + width / 2, 2.3, val, color=color,
                fontsize=30, ha="center", va="center", fontweight="bold")
        # 라벨
        ax.text(x + width / 2, 1.0, lbl, color=TEXT_BLACK,
                fontsize=9, ha="center", va="center", linespacing=1.4)

    plt.tight_layout()
    fig.savefig(OUT / "key_findings_card.png", dpi=200,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {OUT / 'key_findings_card.png'}")


def analysis_pipeline():
    """3단계 분석 파이프라인 인포그래픽."""
    fig, ax = plt.subplots(figsize=(9.5, 4.5), dpi=200)
    _setup_axes(ax, (0, 14), (0, 6))
    fig.patch.set_facecolor("white")

    # 타이틀
    ax.text(7, 5.4, "3단계 분석 파이프라인", color=NAVY,
            fontsize=14, ha="center", va="center", fontweight="bold")
    ax.text(7, 4.85, "Measure → Explain → Recover",
            color=GOLD, fontsize=10, ha="center", va="center",
            fontweight="bold", style="italic")

    stages = [
        ("§3.1", "측정 (Measure)", "UMC 6개 차원\n자치구별 격차 측정",
         "실증 영역\nEmpirical", NAVY),
        ("§3.2", "설명 (Explain)", "위계적 선형 모형\n개인-지역 기여 분리",
         "실재 영역\nActual", TEAL),
        ("§3.3", "복원 (Recover)", "텍스트 + 베이지안\n통합 추정",
         "실제 영역\nReal", GOLD),
    ]

    box_w = 3.4
    box_h = 3.0
    gap = 0.6
    x0 = 0.5

    for i, (sec, title, desc, strata, color) in enumerate(stages):
        x = x0 + i * (box_w + gap)
        # 박스
        box = FancyBboxPatch(
            (x, 0.5), box_w, box_h,
            boxstyle="round,pad=0.05,rounding_size=0.12",
            linewidth=2, facecolor="white", edgecolor=color,
        )
        ax.add_patch(box)
        # 색상 헤더
        header = FancyBboxPatch(
            (x, 0.5 + box_h - 0.7), box_w, 0.7,
            boxstyle="round,pad=0,rounding_size=0.12",
            linewidth=0, facecolor=color,
        )
        ax.add_patch(header)
        # 섹션 라벨 (좌측 상단)
        ax.text(x + 0.25, 0.5 + box_h - 0.35, sec,
                color="white", fontsize=9, ha="left", va="center",
                fontweight="bold")
        # 타이틀
        ax.text(x + box_w / 2, 0.5 + box_h - 0.35, title.split(" ")[0],
                color="white", fontsize=12, ha="center", va="center",
                fontweight="bold")
        # 영문 캡션
        ax.text(x + box_w - 0.15, 0.5 + box_h - 0.35,
                title.split(" ")[1].strip("()"), color=GOLD_LIGHT,
                fontsize=8, ha="right", va="center", style="italic")
        # 본문
        ax.text(x + box_w / 2, 0.5 + box_h - 1.5, desc,
                color=TEXT_BLACK, fontsize=9, ha="center", va="center",
                linespacing=1.5, fontweight="bold")
        # 하단 strata
        strata_box = FancyBboxPatch(
            (x + 0.3, 0.7), box_w - 0.6, 0.7,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            linewidth=0, facecolor=BG_NAVY_SOFT,
        )
        ax.add_patch(strata_box)
        ax.text(x + box_w / 2, 1.05, strata,
                color=color, fontsize=8.5, ha="center", va="center",
                linespacing=1.4, fontweight="bold")

        # 화살표 (마지막 제외)
        if i < len(stages) - 1:
            ax.annotate("", xy=(x + box_w + gap - 0.05, 0.5 + box_h / 2),
                        xytext=(x + box_w + 0.05, 0.5 + box_h / 2),
                        arrowprops=dict(arrowstyle="->", color=NAVY,
                                        lw=2.5, mutation_scale=20))

    # 하단 캡션
    ax.text(7, 0.15, "비판적 실재론(Bhaskar 1975)의 층화된 존재론에 정렬",
            color=TEXT_GRAY_LIGHT, fontsize=8, ha="center",
            va="center", style="italic")

    plt.tight_layout()
    fig.savefig(OUT / "analysis_pipeline.png", dpi=200,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {OUT / 'analysis_pipeline.png'}")


def digital_desert_summary():
    """디지털 사막 4개 자치구 요약 차트."""
    fig, ax = plt.subplots(figsize=(9, 4), dpi=200)
    _setup_axes(ax, (0, 12), (0, 4.5))
    fig.patch.set_facecolor("white")

    # 타이틀
    ax.text(0.3, 4.0, "디지털 사막 (Digital Desert)",
            color=NAVY, fontsize=13, ha="left", va="center",
            fontweight="bold")
    ax.text(0.3, 3.55, "종합지수 하위 4개 자치구 — 광역 거버넌스 우선순위",
            color=TEXT_GRAY, fontsize=9, ha="left", va="center",
            style="italic")

    deserts = [
        ("중랑구", "0.279", "최하위", "Devices·Safety 동반 결핍"),
        ("도봉구", "0.303", "하위", "Affordability 결핍 동반"),
        ("강북구", "0.380", "하위", "노인 인구 비율 26%"),
        ("노원구", "0.389", "하위", "북부 외곽 집중"),
    ]
    x0 = 0.3
    box_w = 2.7
    gap = 0.2
    for i, (gu, score, rank, note) in enumerate(deserts):
        x = x0 + i * (box_w + gap)
        # 카드
        card = FancyBboxPatch(
            (x, 0.3), box_w, 2.7,
            boxstyle="round,pad=0.03,rounding_size=0.1",
            linewidth=0, facecolor=BG_NAVY_SOFT,
        )
        ax.add_patch(card)
        # 좌측 strip
        strip = FancyBboxPatch(
            (x, 0.3), 0.1, 2.7,
            boxstyle="round,pad=0,rounding_size=0",
            linewidth=0, facecolor=ACCENT_RED,
        )
        ax.add_patch(strip)
        # 자치구명
        ax.text(x + 0.3, 2.55, gu, color=NAVY, fontsize=14,
                ha="left", va="center", fontweight="bold")
        # 점수
        ax.text(x + 0.3, 1.95, score, color=ACCENT_RED, fontsize=20,
                ha="left", va="center", fontweight="bold")
        ax.text(x + 1.6, 1.95, rank, color=TEXT_GRAY, fontsize=9,
                ha="left", va="center", style="italic")
        # 노트
        ax.text(x + 0.3, 0.95, note, color=TEXT_BLACK, fontsize=8.5,
                ha="left", va="center", linespacing=1.4)

    plt.tight_layout()
    fig.savefig(OUT / "digital_desert_summary.png", dpi=200,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {OUT / 'digital_desert_summary.png'}")


def chapter4_policy_summary():
    """4장 정책 제언 요약."""
    fig, ax = plt.subplots(figsize=(9, 5), dpi=200)
    _setup_axes(ax, (0, 12), (0, 6))
    fig.patch.set_facecolor("white")

    # 타이틀
    ax.text(6, 5.55, "장소민감적 정책 제언",
            color=NAVY, fontsize=15, ha="center", va="center",
            fontweight="bold")
    ax.text(6, 5.1, "Place-sensitive Policy Implications",
            color=GOLD, fontsize=10, ha="center", va="center",
            style="italic")

    items = [
        ("01", "디지털 사막 우선 개입",
         "중랑·도봉·강북·노원 4개 자치구 광역 거버넌스 체계 구축",
         NAVY),
        ("02", "차원별 차등 처방",
         "Devices/Safety 결핍 vs Connectivity 결핍 구분 처방",
         TEAL),
        ("03", "사람-장소 통합 접근",
         "개인 특성(고령·저학력·1인가구) × 자치구 인프라 교차 설계",
         GOLD),
        ("04", "정량+텍스트 모니터링",
         "분기별 텍스트 베이지안 신호로 잠재 격차 조기 감지",
         ACCENT_RED),
    ]
    box_w = 5.5
    box_h = 1.7
    gap = 0.15
    for i, (num, ttl, desc, color) in enumerate(items):
        col = i % 2
        row = i // 2
        x = 0.4 + col * (box_w + 0.4)
        y = 2.6 - row * (box_h + 0.25)
        # 카드
        card = FancyBboxPatch(
            (x, y), box_w, box_h,
            boxstyle="round,pad=0.03,rounding_size=0.1",
            linewidth=1.2, facecolor="white", edgecolor=LIGHT_GRAY,
        )
        ax.add_patch(card)
        # 좌측 number badge
        badge = FancyBboxPatch(
            (x + 0.1, y + 0.25), 1.1, box_h - 0.5,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            linewidth=0, facecolor=color,
        )
        ax.add_patch(badge)
        ax.text(x + 0.65, y + box_h / 2, num,
                color="white", fontsize=18, ha="center", va="center",
                fontweight="bold")
        # 타이틀
        ax.text(x + 1.4, y + box_h - 0.45, ttl,
                color=NAVY, fontsize=11, ha="left", va="center",
                fontweight="bold")
        # 본문
        ax.text(x + 1.4, y + 0.55, desc,
                color=TEXT_BLACK, fontsize=8.7, ha="left", va="center",
                linespacing=1.5)

    plt.tight_layout()
    fig.savefig(OUT / "chapter4_policy_summary.png", dpi=200,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {OUT / 'chapter4_policy_summary.png'}")


def cover_emblem():
    """표지에 들어갈 엠블럼/로고 마크 (광역 보조 그래픽)."""
    fig, ax = plt.subplots(figsize=(6, 1.6), dpi=200)
    _setup_axes(ax, (0, 12), (0, 3))
    fig.patch.set_facecolor(NAVY)

    # 좌측 ITU 마크
    ax.text(0.5, 1.5, "ITU·UMC", color="white", fontsize=18,
            ha="left", va="center", fontweight="bold")
    ax.text(0.5, 0.7, "DATA HACKATHON 2026", color=GOLD_LIGHT,
            fontsize=8, ha="left", va="center", fontweight="bold")
    # 중앙 라인
    ax.plot([4.6, 4.6], [0.4, 2.6], color=GOLD, linewidth=1.2)
    # 우측 팀 마크
    ax.text(5.0, 1.5, "TEAM HIGH-FIVE", color="white", fontsize=12,
            ha="left", va="center", fontweight="bold")
    ax.text(5.0, 0.7, "SEOUL · 25 DISTRICTS · MARCH 2026",
            color=GOLD_LIGHT, fontsize=8, ha="left", va="center",
            fontweight="bold")

    plt.tight_layout()
    fig.savefig(OUT / "cover_emblem.png", dpi=200,
                bbox_inches="tight", facecolor=NAVY)
    plt.close(fig)
    print(f"  ✓ {OUT / 'cover_emblem.png'}")


def chapter_divider(chap_num: int, title: str, kicker: str):
    """챕터 구분선 그래픽 (큰 챕터 번호 + 타이틀)."""
    fig, ax = plt.subplots(figsize=(9, 3), dpi=200)
    _setup_axes(ax, (0, 12), (0, 4))
    fig.patch.set_facecolor("white")

    # 좌측 큰 번호 영역
    big = FancyBboxPatch(
        (0.3, 0.4), 2.5, 3.2,
        boxstyle="round,pad=0.03,rounding_size=0.15",
        linewidth=0, facecolor=NAVY,
    )
    ax.add_patch(big)
    ax.text(1.55, 2.0, f"0{chap_num}", color=GOLD_LIGHT,
            fontsize=58, ha="center", va="center", fontweight="bold")
    ax.text(1.55, 0.7, "CHAPTER", color="white", fontsize=9,
            ha="center", va="center", fontweight="bold")

    # 우측 본문 영역
    ax.text(3.2, 3.0, title, color=NAVY, fontsize=22,
            ha="left", va="center", fontweight="bold")
    # 골드 언더라인
    ax.plot([3.2, 6.0], [2.5, 2.5], color=GOLD, linewidth=2)
    # 키커 박스
    ax.text(3.2, 1.7, kicker, color=TEXT_BLACK, fontsize=10,
            ha="left", va="center", linespacing=1.6)

    plt.tight_layout()
    fname = f"chapter_divider_{chap_num}.png"
    fig.savefig(OUT / fname, dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print(f"  ✓ {OUT / fname}")


def main():
    print(f"Generating infographics into {OUT}...")
    umc_dimensions_hex()
    key_findings_card()
    analysis_pipeline()
    digital_desert_summary()
    chapter4_policy_summary()
    cover_emblem()
    chapter_divider(1, "프로젝트 개괄",
                    "측정 → 설명 → 복원의 3단계 분석 체계")
    chapter_divider(2, "이론적 기반과 해석적 맥락",
                    "사람 기반과 장소 기반 접근의 통합")
    chapter_divider(3, "분석 결과",
                    "UMC 측정 · HLM 추정 · 베이지안 통합")
    chapter_divider(4, "정책 제언",
                    "장소민감적 처방과 외적 타당성")
    print("Done.")


if __name__ == "__main__":
    main()
