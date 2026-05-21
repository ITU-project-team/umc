# STRUCTURE_REPORT.md

UMC 보고서 `raw_extract.md`(총 1888 lines)의 구조·인벤토리·변환 위험 분석 리포트.
pandoc(docx→markdown) 변환 결과를 LaTeX로 재변환하기 위한 사전 진단 문서.

- 입력: `/Users/ujunbin/project/umc/writing/manuscript/latex_output/raw_extract.md`
- 미디어: `/Users/ujunbin/project/umc/writing/manuscript/latex_output/media/media/image1..21` (png 16 + jpeg 5)

---

## 1. 섹션 트리

원문 헤더를 라인 번호와 함께 트리로 나열한다. 오타·표기 오류는 그대로 보존한다.

```
# 1. 개요  ........................................................... L17  [단일 # + 두 칸 공백]
├── ## 1.1 이론적 이해  ............................................... L37
└── ## 1.2 분석 방법 이해  ........................................... L99

# 2. 이론적 기반과 해석적 맥락  ..................................... L170 [단일 # + 두 칸 공백]
├── ## 2.1 Policy  ................................................... L187
│   ├── ### 2.1.1 디지털 격차의 영향 요인: 개인 특성과 지역 조건  ... L198
│   ├── ### 2.1.2 정책적 구분: 사람 기반 / 장소 기반 / 장소민감적   . L222
│   └── ### 2.1.3 메타이론적 틀: 비판적 실재론의 층화된 존재론  ..... L249
└── ## 2.2 Seoul  ................................................... L265
    ├── ### 2.2.1 도시로서의 서울  .................................. L267
    └── ### 2.2.2 연결성 격차 현황과 관련 법령 및 정책 현황  ........ L301

# 3. 분석  .......................................................... L391
├── ## 3.1 서울의 UMC 지역 격차 [trailing space]  ................... L417
│   ├── ### 3.1.1 측정 지표 및 데이터 [trailing space]  ............. L419
│   ├── ### 3.1.2 측정 지표 지수화  ................................. L516
│   └── ### 3.1.3 지역별 UMC 지수 특성  ............................. L534
├── ## 3.2 개인 및 지역 특성과 디지털 연결성  ....................... L628
│   ├── ### 3.2.1 변수 구성  ........................................ L642
│   └── ### .2.2 분석 결과  ......................................... L682  ★ 오타: "### 3.2.2"여야 함
├── ### 3.3 플랫폼 텍스트 분석: LLM 기반 디지털 연결성 사례분석  .... L928  ★ 오타: ## 이어야 함 (### 3 깊이)
│   ├── ### 3.3.1 당근 플랫폼 특성  ................................. L944
│   ├── ### 3.3.2 왜 LLM인가: 기존 방법론의 한계와 LLM의 구조적 이점 L956
│   ├── ### 3.3.3 분석 구조  ........................................ L979
│   ├── ### 3.3.4 데이터와 적용 범위  ............................... L1107
│   └── ### 3.3.5 분석 결과  ........................................ L1137
└── ## 3.4 분석 결과 종합  ........................................... L1330

# 4. 정책 제언  ..................................................... L1411
├── ## 4.1 정책 제언의 이론적 프레임  ............................... L1433
├── ## 4.2 People-based 정책 제언  .................................. L1465
├── ## 4.3 Place-based 정책 제언  ................................... L1557
└── ## 4.4 통합적 정책 제언  ........................................ L1644

# 5. 결론  .......................................................... L1683
├── ## 5.1 요약  .................................................... L1685
└── ## 5.2 한계와 향후 과제  ........................................ L1726

# References  ...................................................... L1778
```

또한 line 613, 617, 621에 표 셀 내부에서 `## ![](...)` 형태로 **이미지가 H2 헤더 위치에 삽입되어 있다**. 이는 pandoc이 docx의 표 셀 안 그림 캡션 스타일을 `## `으로 잘못 변환한 결과이며, 실제 문서 구조에서 별도 섹션이 아니다.

### 1.1 헤더 표기 오류 보정 제안

| 라인 | 원문 (raw) | 추정 의도 | 보정 |
|---|---|---|---|
| L17 | `#  1. 개요` (두 칸 공백) | `# 1. 개요` | 공백 정규화 |
| L170 | `#  2. 이론적 기반과 해석적 맥락` | `# 2. ...` | 공백 정규화 |
| L417 | `## 3.1 서울의 UMC 지역 격차 ` (trailing space) | `## 3.1 ...` | trailing 공백 제거 |
| L419 | `### 3.1.1 측정 지표 및 데이터 ` (trailing space) | `### 3.1.1 ...` | trailing 공백 제거 |
| L682 | `### .2.2 분석 결과` | `### 3.2.2 분석 결과` | 누락된 "3" 보정 |
| L928 | `### 3.3 플랫폼 텍스트 분석: ...` | `## 3.3 플랫폼 텍스트 ...` | H3→H2 승격. 3.3.1~3.3.5와의 위계 정합 |
| L613/617/621 | 표 셀 내 `## ![image]` | 표 셀 안의 그림 캡션 | LaTeX에서는 H2 헤더가 아닌 `\subfloat` 또는 `tabular` 셀의 이미지로 처리 |
| 캡션 (그림 0-1 ~ 0-5) | `**그림 0-1.** ...` | 챕터 0 그림으로 표기되어 챕터-그림 번호 체계 불일치 (그림 1~8과 공존) | 통일 권장: 모두 챕터 번호 기반으로 (예: 그림 1-1, 1-2, 3-1...) 또는 모두 단일 시퀀스 (그림 1~13) |

---

## 2. 미디어 인벤토리 (image1 ~ image21)

총 21개 이미지(`image8.png`만 수식 렌더링 이미지, image12-17은 jpeg 6장).

| ID | 등장 라인 | 직후 캡션 (있는 경우) | width (in) | height (in) | 추정 타입 |
|---|---|---|---|---|---|
| image1.png | L27 | **그림 0-1. UMC 6개 차원 측정 체계** (L30) | 6.102 | 4.363 | figure (다이어그램) |
| image2.png | L32 | **그림 0-2. 3단계 분석 파이프라인** (L35) | 6.299 | 2.776 | figure (다이어그램) |
| image3.png | L165 | 그림 1. 프로젝트 개괄 (L168) | 8.259 | 6.194 | figure (대형 다이어그램) |
| image4.png | L285 | (캡션 없음, 서울 인구·자치구 관련 시각자료 추정) | 5.174 | 3.111 | figure (인포그래픽, 캡션 누락) |
| image5.png | L315 | (캡션 없음, 무선국 인프라 격차 관련 추정) | 5.301 | 3.022 | figure (캡션 누락) |
| image6.png | L400 | **그림 0-3. 핵심 발견 요약** (L403) | 6.299 | 2.195 | figure (요약 인포그래픽) |
| image7.png | L405 | **그림 0-4. 디지털 사막 — 종합지수 하위 4개 자치구** (L408) | 6.299 | 2.451 | figure (지도/인포그래픽) |
| image8.png | L521 | (식1.1) Min-Max 정규화 수식 — 본문 L519에서 (식1.1) 언급 | 2.028 | 0.375 | equation-as-image ★ |
| image9.png | L600 | 그림 2. 자치구별 UMC 종합점수 (L603) | 3.369 | 3.785 | figure (지도) |
| image10.png | L600 | 그림 3. UMC 차원별 점수 히트맵 (L603) | 2.889 | 3.785 | figure (히트맵) |
| image11.png | L607 | 그림 4. UMC 차원별 점수 (L610) | 7.522 | 5.719 | figure (대형 차원별 차트) |
| image12.jpeg | L613 | Connectivity (라벨, L615) | 3.458 | 1.849 | figure (LISA 지도, 2×3 grid의 1번) |
| image13.jpeg | L613 | Available for Use (L615) | 2.769 | 2.019 | figure (LISA 지도, 2번) |
| image14.jpeg | L617 | Affordability (L619) | 2.478 | 1.813 | figure (LISA 지도, 3번) |
| image15.jpeg | L617 | Devices (L619) | 2.601 | 1.899 | figure (LISA 지도, 4번) |
| image16.jpeg | L621 | Skills (L623) | 2.442 | 1.784 | figure (LISA 지도, 5번) |
| image17.jpeg | L621 | Safety (L623) | 2.426 | 1.770 | figure (LISA 지도, 6번). 그룹 캡션: 그림 5. UMC 수준의 공간적 자기상관 (L626) |
| image18.png | L1035 | 그림 6. 분류와 추론의 역할 구분 (L1038) | 6.198 | 4.100 | figure (다이어그램) |
| image19.png | L1132 | 그림 7. LLM 기반 텍스트 분석 파이프라인 (L1135) | 7.969 | 5.476 | figure (파이프라인 다이어그램) |
| image20.png | L1287 | 그림 8. 지역별 사전-사후 분포 차이 (L1290) | 9.619 | 4.405 | figure (대형 차트, 페이지 초과 위험) |
| image21.png | L1420 | **그림 0-5. 장소민감적 정책 제언 4대 축** (L1423) | 6.299 | 3.220 | figure (인포그래픽) |

**주의:**
- image8.png는 **수식을 이미지화한 것**으로, LaTeX 변환 시 원시 LaTeX 수식 `\frac{x_i - x_{min}}{x_{max} - x_{min}}` 으로 대체하는 것을 강력 권장.
- image4 (L285), image5 (L315)는 **캡션 라벨 자체가 누락**되어 있다. 본문 맥락상 image4는 서울 자치구 인구·구조 이미지, image5는 무선국 인프라 격차 이미지로 추정.
- image20은 9.62인치 폭으로 A4 세로(약 6.3in 안전 영역) 폭을 크게 초과 — `\begin{landscape}` 또는 `width=\linewidth`로 강제 축소 필요.
- image12~17은 2×3 grid 안에 배치된 6개 LISA 지도이며, 그룹 캡션은 L626의 "그림 5. UMC 수준의 공간적 자기상관 (서울 25개 자치구)"이다.

---

## 3. 표(Table) 인벤토리

마크다운 본문 내 모든 표(`+---|---+` multi-line 또는 `---|---|---` 단순 형식)를 나열. **L1~L15의 ASCII 표지(보고서 커버 박스)는 별도 처리**한다 (표가 아닌 박스 디자인).

| # | 라인 범위 | 형식 | 열 수 | 데이터 행 수 | 직전 캡션 | 직후 캡션 | 요약 |
|---|---|---|---|---|---|---|---|
| Cover | L1–L15 | ASCII pipe-border 박스 | 1 | 7 | — | — | 보고서 표지. 표가 아닌 디자인 박스. LaTeX에서는 `\maketitle` 또는 `titlepage` 환경으로 재구성 |
| T1 | L487–L514 | pandoc grid-table (multiline cells) | 4 | 6 | 표 1. UMC 차원별 측정 지표 (L485) | — | UMC 6개 차원별 측정 지표·데이터 소스·비고 |
| T2 (cell-image) | L612–L624 | pandoc multiline grid-table (그림 셀 포함) | 2 | 3 | — | 그림 5. UMC 수준의 공간적 자기상관 (L626) | LISA 지도 6장을 2×3 배치한 figure-grid. **표가 아닌 figure 배열**이므로 LaTeX에서는 `subfigure` 또는 `tabular` 안의 `\includegraphics`로 재구성 |
| T3 | L718–L761 | pandoc multiline grid-table | 5 | 12 | 표 2. 분석 변수 설명 (L716) | — | HLM 분석 변수 정의 (L1, L2 변수, 척도, 출처) |
| T4 | L793–L830 | pandoc multiline grid-table | 6 | 13 | 표 3. 주요 변수의 기술통계량 (L791) | — | 변수별 N·평균·SD·min·max |
| T5 | L840–L921 | pandoc grid-table | 4 | 23 | 표 4. HLM 추정 결과 (L838) | Note (L923–L926) | Model 1/2/3 회귀계수표. ★ 본 문서 최대·최복잡 표 |
| T6 | L1016–L1033 | pandoc multiline grid-table | 3 | 5 | 표 5. 텍스트 분석 표본 추출 및 판정 절차 (L1014) | — | 단계별 게시글 수 (1,287,761 → 26,742) |
| T7 | L1090–L1105 | pandoc multiline grid-table | 4 | 4 | 표 6. 3.3절의 분석 단위와 해석 단위 (L1088) | — | 분석 단위(개별·동·구·인과기제)별 의미 |
| T8 | L1232–L1285 | pandoc multiline grid-table | 5 | 25 | 표 7. 자치구별 게시글 판정 결과 (L1230) | — | 25개 자치구별 Y/N/? 판정 분포 |
| T9 | L1302–L1324 | pandoc multiline grid-table | 4 | 9 | 표 8. 결여 유형별 가설 생성 결과 분포 (L1300) | Note (L1326–L1328) | 결여 유형별 빈도·비율 |

**주의:**
- **표 번호 충돌**: 본문 L691에 "표 4는 순차적으로 다층 모형의 추정 결과를 나타낸 것이다"가 있으나 실제 표 4는 L838에 등장. 그 사이에 표 2 (L716), 표 3 (L791)이 끼어 있어 본문이 표보다 먼저 표 4를 참조. LaTeX에서 `\ref{tab:hlm}`로 처리하면 자동 해결.
- **표 6 라벨 중복**: L1086의 "그림 7과 같다"라는 본문 다음에 표 6(L1088)이 등장. 그러나 L1139의 본문에서 "텍스트 분류 결과는표 6과 같다"고 다시 표 6을 참조하는데, 이는 실제로는 표 7 (L1230)을 가리키는 것으로 추정됨 → **표 번호 검토 필요**.

---

## 4. 인용 패턴

### 4.1 본문 inline citation 샘플 (20개)

| # | 라인 | 인용 |
|---|---|---|
| 1 | L44 | (Allana & Clark, 2018) |
| 2 | L53 | (Dolowitz & Marsh, 2000) |
| 3 | L56 | (Greenhalgh & Russell, 2009) |
| 4 | L58 | (Head, 2010) |
| 5 | L85 | (Bhaskar, 1975) |
| 6 | L94 | (Bhaskar, 1975) |
| 7 | L194 | (Neumark & Simpson, 2015) |
| 8 | L202 | Hargittai(2010) ★ 한국식 저자(연도) 표기 (공백 없음) |
| 9 | L204 | Chipeva 등(2018) ★ "등" + 공백 없는 표기 |
| 10 | L207 | Borges 등(2020) |
| 11 | L209 | Hilbert(2011) |
| 12 | L213 | Mossberger 등(2006) |
| 13 | L216 | Crang 등(2006) |
| 14 | L218 | Hong 등(2017) |
| 15 | L229 | (Neumark & Simpson, 2015) |
| 16 | L234 | Hindman(2000) |
| 17 | L237 | van Dijk(2020) ★ 소문자 van + 공백 없는 표기 |
| 18 | L245 | (OECD, 2025) |
| 19 | L253 | Bhaskar(1975) ★ 표기 혼용 |
| 20 | L424 | (ITU, 2023) |

추가 표기 변형:
- ITU(2023) (L424, L466, L473), ITU(2024) (L454, L528, L1459)
- (Van Dijk, 2020) (L452), (Van Deursen & Helsper, 2015) (L470) — 대문자 Van vs 소문자 van 혼용
- OECD(2023) (L1457), European Commission(2025) (L1462)
- Age UK(2023) (L1485), UK DSIT(2025) (L1594), IMDA(2020), CSA Singapore(2023) (L1513)
- (ref) (L1006, L1209) — **미해결 자리표시자** ★ 인용 처리 필요
- (Ref) (L768) — 동일

### 4.2 References 섹션 진단 (L1778~L1888)

- **위치**: L1778 `# References` 헤더 이하
- **참고문헌 항목 수**: **약 29개**
  - L1780~L1802: 일반 단락 형식 5개 (Allana & Clark / Bhaskar / Dolowitz & Marsh / Greenhalgh & Russell / Head / Sayer)
  - L1804~L1888: blockquote (`> `) 형식 약 24개 (Age UK, Borges, Chipeva, Crang, European Commission, González 외, Hargittai, Hilbert, Hill O'Connor, Hindman, Hong, Hox 외, ITU 2023, ITU 2024, Mossberger, OECD 2025, PLACE 2025, Raudenbush & Bryk, Riley 2025, UK DSIT, van Deursen & Helsper, van Dijk)

- **형식 진단**: APA 7th 스타일에 가깝지만 **비일관**.
  - 일부 항목은 일반 단락 (L1780~L1802), 일부는 `>` blockquote (L1804~L1888) — pandoc이 docx의 다른 단락 스타일을 분리 처리한 결과로 추정. LaTeX 변환 시 `bibliography{}` 단일 환경으로 통합 필요.
  - URL을 `[[link]{.underline}](link)` 형식으로 이중 표기한 항목들 (L1784, L1791 등) — LaTeX `\url{}` 또는 BibTeX `url` 필드로 단순화 필요.
  - 본문 인용은 있으나 References에 누락된 항목이 있을 수 있음: Neumark & Simpson (2015), ITU IDI 2023 인용 등 검증 필요.
  - 본문 (ref) (L1006, L1209), (Ref) (L768)는 **미완 인용** — 작성자가 채워야 할 부분.

---

## 5. 특수 요소

### 5.1 인용블록 (`>` blockquote) 의도별 분류

본문 내 강조 박스 7개 (References의 blockquote 형식과 구분):

| 라인 | 헤더(굵게) | 의도 추정 |
|---|---|---|
| L21–L25 | "서울 25개 자치구의 디지털 격차를" | 챕터 1 표지 박스 (Chapter intro pull-quote) |
| L68–L73 | "메타이론 · 층화된 존재론 — 경험·실재·실제 영역" | 메타이론 박스 (theoretical sidebar) |
| L174–L177 | "사람 기반과 장소 기반 접근을 통합하는" | 챕터 2 표지 박스 |
| L395–L398 | "측정 → HLM → 베이지안 통합의" | 챕터 3 표지 박스 |
| L563–L567 | "핵심 발견 · 디지털 사막 4개 자치구" | 핵심 메시지 박스 (key finding callout) |
| L1415–L1418 | "관측·계수·텍스트의 3중 신호를 결합한" | 챕터 4 표지 박스 |
| L1638–L1642 | "정책 시사점 · 장소민감적 처방의 4대 축" | 정책 시사점 박스 |

LaTeX 변환 권고: `tcolorbox` 패키지로 두 가지 스타일 정의 — (a) chapter-intro pull-quote 박스 4종, (b) callout/sidebar 박스 3종.

### 5.2 굵은 라벨 ("CHAPTER N", "그림 N-N", "표 N-N") 일관성

| 라벨 | 라인 | 비고 |
|---|---|---|
| **CHAPTER 1** | L19 | 챕터 1 직후 |
| **CHAPTER 2** | L172 | |
| **CHAPTER 3** | L393 | |
| **CHAPTER 4** | L1413 | |
| CHAPTER 5 | — | ★ 누락 (L1683 `# 5. 결론` 다음에 **CHAPTER 5** 없음) |

그림 라벨 일관성:
- "그림 0-1" ~ "그림 0-5" (5개, 굵게, L30/L35/L403/L408/L1423) — 챕터 0 형식. 실제 챕터 1, 3, 4에 분산 등장 → **번호 체계 불일치**.
- "그림 1" ~ "그림 8" (8개, 굵음 없음, L168/L603/L610/L626/L1038/L1086/L1135/L1290) — 일련 번호 형식.
- 두 체계가 혼용되어 있으며 LaTeX 변환 시 통일 권고.

표 라벨: "표 1" ~ "표 8" 일관 (굵음 없음).

### 5.3 수식 사용 여부 (LaTeX/MathJax 검색)

| 라인 | 형식 | 내용 |
|---|---|---|
| L519 | 본문 참조 | "(식1.1)과 같이 산출한다" |
| L521 | image8.png | Min-Max 수식 이미지화 ★ |
| L1044–L1057 | inline `$...$` (pandoc LaTeX-in-math) | Beta 사전 분포, Binomial 우도, 사후 분포 수식 — 한국어 변수명(생활인구) 포함 |
| L1060 | display `$$...$$` | $\alpha_{jd} = \kappa \times s_{jd}$ |
| L1062 | display `$$...$$` | $\beta_{jd} = \kappa \times (1 - s_{jd})$ |
| L1064 | display `$$...$$` | $\theta_{jd} \mid y_{jd} \sim Beta(...)$ |
| L1066 | display `$$...$$` | $n_{jd}^{*} = n_{jd} \times (생활인구_j / 평균생활인구)$ |

★ pandoc이 수식 내 `=`을 `\text{=}`로 변환하는 등 비표준 표기. LaTeX 변환 시 수식 클린업 필수. 특히 L1066의 한국어 변수명은 `\text{생활인구}_j` 또는 영문(`pop_j`)으로 치환 권장.

### 5.4 영문 약어·고유명사 빈출 항목

| 약어/고유명사 | 출현 횟수 (대략) | 비고 |
|---|---|---|
| UMC | 70+ | Universal Meaningful Connectivity |
| ITU | 15+ | International Telecommunication Union |
| HLM | 10+ | Hierarchical Linear Model |
| LLM | 8+ | Large Language Model |
| ICC | 4+ | Intraclass Correlation Coefficient (급내상관계수) |
| OECD | 4+ | |
| EU / European Commission | 2+ | |
| ICT | 2+ | |
| IoT | 2+ | |
| SKT | 3+ | |
| LG U+ | 1 | |
| AI디지털배움터 | 3+ | |
| 서울온 (Seoul ON) | 2+ | |
| IMDA, CSA, Age UK, UK DSIT | 각 1~2회 | 정책 비교 사례 |
| 5G / 4G | 5+ | |
| WiFi / Wi-Fi | 다수 | 표기 혼용 가능 (검토 필요) |
| KLI, KOSIS, KISTEP | **검색 결과 0건** | 사용자가 예시로 들었으나 본문에 미등장 |

★ 약어는 LaTeX `\newacronym` (glossaries 패키지) 또는 단순 첫 등장 시 "UMC(Universal Meaningful Connectivity)" 풀이 패턴 사용 권장.

---

## 6. 변환 시 위험 지점 (pandoc → LaTeX)

| # | 위험 | 위치 | 영향 | 대응 권고 |
|---|---|---|---|---|
| 1 | **그림 width가 in 단위 절대값 (최대 9.62in)** | image20.png L1287 (9.619in), image19.png (7.969in), image11.png (7.522in), image3.png (8.259in) | A4 본문 영역(약 6.3in) 초과 → 페이지 깨짐 | 모든 `\includegraphics`를 `width=\linewidth` 또는 `width=\textwidth`로 통일. 가로폭이 진짜로 큰 figure는 `\begin{landscape}` 처리 |
| 2 | **수식이 이미지로 박힘 (image8.png)** | L521 | LaTeX의 강점 무력화, 폰트·크기 불일치 | image8를 원시 LaTeX 수식 `\[ x^* = \frac{x_i - x_{\min}}{x_{\max} - x_{\min}} \]`로 대체 |
| 3 | **헤더 깊이 오류 (### 3.3, ### .2.2)** | L928, L682 | 자동 ToC 생성 시 위계 망가짐 | L928 → `## 3.3 ...`, L682 → `### 3.2.2 ...`로 정정 후 변환 |
| 4 | **단일 # vs ## 혼용 (`#  1. 개요` 두 칸 공백)** | L17, L170 | pandoc은 허용하나 다른 변환기에서 오인 가능 | 공백 1칸으로 정규화 |
| 5 | **ASCII border 표지 박스** | L1–L15 | pandoc이 grid-table로 변환 → LaTeX `longtable`로 잘못 변환됨 | LaTeX의 `\titlepage` 환경 또는 `tcolorbox`로 재작성 |
| 6 | **multiline grid-table (특히 표 5 HLM)** | T5 L840–L921 | pandoc → LaTeX 변환 시 `longtable` + `\\` 줄바꿈 처리 복잡, 통계 유의도 표기 `^***^` (Pandoc superscript syntax) 깨질 위험 | `siunitx` + `booktabs` 기반으로 수동 재작성, 또는 별도 `.tex` 파일로 분리 |
| 7 | **표 셀 안의 이미지 grid (T2, image12~17)** | L612–L624 | pandoc은 셀에 `## ![](...)`를 H2 헤더로 변환 — LaTeX에서는 무효 | `subfigure` 또는 `tabular` + `\includegraphics`로 명시적 재작성 |
| 8 | **인용 표기 혼용 (Hargittai(2010) vs (Hargittai, 2010), 등 vs &)** | 본문 다수 | 자동 BibTeX 변환 곤란, `natbib`/`biblatex` 인식 실패 | 모든 inline citation을 `\citep{key, year}` 또는 `\citet{key}`로 수동 치환 |
| 9 | **미해결 자리표시자 (ref), (Ref)** | L768, L1006, L1209 | LaTeX 빌드 시 `\ref{}` 오류 또는 그대로 출력 | 작성자가 인용 채워야 함. 변환 시 `\todo{citation needed}` 마커 권장 |
| 10 | **수식 내 한국어 변수명 (`생활인구_j`)** | L1057, L1066 | LaTeX 기본 math mode는 한글 미지원 (kotex/xelatex 필요) | XeLaTeX + kotex 사용, 또는 변수명 영문화 (`pop_j`) |
| 11 | **그림 번호 체계 이중 (그림 0-N + 그림 N)** | L30/35/403/408/1423 (0-N) vs L168/603/610/626/1038/1135/1290 (N) | 본문 cross-reference 추적 곤란 | 챕터 기반 (그림 1.1, 3.1 등) 또는 단일 시퀀스로 통일 |
| 12 | **표지 헤더 trailing space (### 3.1 / 3.1.1)** | L417, L419 | pandoc은 허용하나 anchor id 생성에서 문제 가능 | 정규식으로 trailing space 일괄 제거 |
| 13 | **HLM 표(T5)의 통계 유의도 표기 `−22.618^***^`** | L851~L921 | Pandoc superscript markdown이 LaTeX `\textsuperscript{}`로 변환되며 마이너스 부호(`−` U+2212)는 그대로 — math mode와 충돌 | 표 전체를 LaTeX 수동 작성 시 `$-22.618^{***}$` 표기로 통일 |
| 14 | **CHAPTER 5 라벨 누락** | L1683 이후 | 챕터 표지 디자인 일관성 깨짐 | `**CHAPTER 5**` 라벨 보충 또는 LaTeX 템플릿에서 자동 생성 |

---

## 7. 권장 섹션 분할

### 7.1 권장: **분할 방식 (sections/ch1.tex ~ ch5.tex + references.tex)**

분할 권장 근거:

1. **본문 분량과 표의 복잡도**: raw_extract.md 1,888 라인 중 표만 5개가 30라인 이상 (T5는 82라인). 단일 `main.tex`로 만들면 1,500라인을 넘어 편집·diff·리뷰가 어려워진다.
2. **챕터 간 독립성이 높음**: 챕터 1 (개요), 챕터 2 (이론·서울 맥락), 챕터 3 (분석), 챕터 4 (정책 제언), 챕터 5 (결론)이 각각 자기완결적. 챕터 3은 분석 코드·표가 집중되어 별도 빌드/디버깅 단위로 유리.
3. **수식·그림 밀도 분포의 비대칭성**: 챕터 3에 수식 5개, 그림 11개, 표 7개가 집중. 챕터별 figure/table 카운터를 독립 관리하면 본문 작성 시 충돌 회피.
4. **검토자별 분담 작업 적합**: SSOT·Tier 리뷰 (Writing Integrity Gate W8) 절차에서 챕터 단위로 reviewer 컨텍스트를 분리하기에 파일 분할이 자연스러움.
5. **References 분리의 표준성**: BibTeX/biblatex 도입 시 `references.bib` 별도 파일이 사실상 표준.

### 7.2 권장 파일 구조

```
latex_output/
├── main.tex                  # \documentclass, preamble, \include 호출
├── preamble/
│   ├── packages.tex          # 패키지 로드 (kotex, booktabs, tcolorbox, graphicx, longtable, hyperref, biblatex)
│   ├── commands.tex          # \newcommand (callout 박스, chapter pull-quote 등)
│   └── titlepage.tex         # L1–L15 표지 박스 재구성
├── sections/
│   ├── ch1_overview.tex      # L17–L169 (개요, 1.1, 1.2)
│   ├── ch2_theory.tex        # L170–L390 (이론·서울 맥락, 2.1.x, 2.2.x)
│   ├── ch3_analysis.tex      # L391–L1410 (분석. ★ 최대 분량, 추가로 ch3_1, ch3_2, ch3_3, ch3_4 sub-include 검토)
│   │   ├── ch3_1_measurement.tex
│   │   ├── ch3_2_hlm.tex
│   │   ├── ch3_3_text.tex
│   │   └── ch3_4_synthesis.tex
│   ├── ch4_policy.tex        # L1411–L1682
│   └── ch5_conclusion.tex    # L1683–L1777
├── references.bib            # L1778–L1888 → BibTeX 변환
├── figures/                  # latex_output/media/media/* 그대로 또는 심볼릭 링크
└── tables/                   # T1, T3~T9 별도 .tex (선택)
```

### 7.3 단일 `main.tex` 방식이 더 나은 경우

- 보고서가 최종본이고 향후 수정이 없을 때
- 단일 파일 제출이 요구되는 학술지 양식
- arXiv 등 단일 tex 제출 플랫폼

이 경우 본 보고서는 약 1,500~2,000라인 LaTeX이 될 것이며, 편집 가능하지만 권장하지 않는다.

### 7.4 변환 우선순위 권장

1. **표 T5 (HLM 추정 결과)**: 변환 위험 #6, #13의 집중점. 가장 먼저 수동 작성 후 검증.
2. **수식 (L1044~L1066, image8)**: 위험 #2, #10 해소.
3. **표지/챕터 표지 박스 (Cover, 7개 blockquote)**: 위험 #5 해소 및 디자인 일관성 확보.
4. **표 셀 내 이미지 grid (T2)**: 위험 #7 해소.
5. **References → references.bib 변환**: 위험 #8 해소.
6. **본문 (ref)/(Ref) 자리표시자 해결**: 위험 #9, 작성자 협의 필요.

---

## 8. 요약 체크리스트

- [ ] 헤더 오타 6건 정정 (L17, L170, L417, L419, L682, L928)
- [ ] 그림 캡션 누락 2건 보충 (image4 L285, image5 L315)
- [ ] CHAPTER 5 라벨 보충 (L1683 직후)
- [ ] (ref)/(Ref) 자리표시자 3건 해결 (L768, L1006, L1209)
- [ ] image8 → LaTeX 수식 치환
- [ ] image20 등 6.3in 초과 그림 폭 조정
- [ ] 표 T5 (HLM) 수동 재작성
- [ ] 표 6 / 표 7 본문 cross-reference 검증
- [ ] References blockquote 통합 + BibTeX 변환
- [ ] 챕터 0-N vs N 그림 번호 체계 통일
- [ ] WiFi/Wi-Fi, Van/van 표기 통일

---

*리포트 작성: LaTeX 변환 파이프라인 서브에이전트 A. 입력 파일 실측 라인 번호 기반 분석.*
