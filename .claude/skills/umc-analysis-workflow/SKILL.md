---
name: umc-analysis-workflow
description: Part 1, Part 2, Part 3, text preprocessing, Bayesian aggregation, inference 산출물의 분석 스크립트, 결과, 해석 점검, 보고서 전달에 사용한다.
allowed-tools: Read, Bash
---

# UMC 분석 워크플로

## 트리거

UMC 분석 논리, 스크립트, 산출물, 검증, 보고서 전달, 루트 보고서 저장소와 중첩 분석 저장소의 발행 작업을 다룰 때 이 스킬을 사용한다.

## 경로 레지스트리

- 모든 구체 파일은 `config`의 프로젝트 경로 레지스트리를 통해 해석한다.
- 레지스트리 값은 루트 저장소 기준 GitHub 상대 경로다.
- 워커 브리프에는 가능하면 경로 키를 쓰고, 실행 시점에만 구체 경로로 해석한다.

주요 키:

| 키 | 역할 |
| --- | --- |
| `paths.root` | 루트 보고서/문서 저장소 |
| `paths.analysis.part1.repo` | Part 1 UMC 지수, 자치구 점수, 지도, 3.1절 그림 |
| `paths.analysis.part2.repo` | Part 2 HLM/다층분석과 3.2절 해석 |
| `paths.analysis.part3.repo` | Part 3 텍스트, Bayesian, 추론 통합 워크플로와 3.3절 |
| `paths.analysis.text_preprocessing.repo` | 레거시/참조 텍스트 전처리와 분류 지원 |
| `paths.analysis.legacy.*` | 레거시/참조 분석 작업공간 |

파일을 바꾸는 저장소 안에서 항상 `git status --short --branch`를 확인한다.

## 공통 규칙

- 분석 논리를 바꾸기 전 기존 스크립트, README, 산출물을 먼저 확인한다.
- 원자료, 비공개 입력, `.env` 파일을 덮어쓰지 않는다.
- 일회성 산출물은 `paths.tmp.root` 아래에, 내구 산출물은 소유 저장소의 설정된 산출물·문서·작성 경로 키 아래에 둔다.
- 분석 산출물이 보고서로 들어가면 분석 저장소와 루트 보고서 저장소의 변경을 분리해 관리한다.
- cmux 워커를 사용할 때는 `umc-worker-orchestration`과 함께 쓴다.
- 보이는 워커 패널에는 한국어 지시를 사용하되, 코드, 변수, 경로 키, 보고서 고유 용어는 원래 표기를 유지한다.
- 보고서 그림은 절제된 학술 스타일을 쓰고 해석은 그림 내부 푸터가 아니라 본문이나 정식 캡션에 둔다.
- HLM, LLM 플랫폼 텍스트 분석, Bayesian 업데이트, Digital Desert, 정책 권고를 해석할 때는 `umc-report-evidence-framing`을 함께 적용한다.

## Part 1: UMC 지수와 공간 그림

3.1절 지수, 자치구 순위, heatmap, composite map, 공간 자기상관 그림에는 Part 1을 사용한다.

자주 쓰는 키:

- `paths.analysis.part1.score_table_2024`
- `paths.analysis.part1.section31_figure_script`
- `paths.analysis.part1.report_refresh_figures`
- `paths.analysis.part1.seoul_gis`

기본 흐름:

1. 점수표와 자치구 코드를 확인한다.
2. 이미지를 손으로 고치지 말고 기존 스크립트로 그림을 재생성한다.
3. 절제된 색, 얇은 경계선, 읽을 수 있는 라벨, 최소 장식, 안정적인 DOCX 크기를 우선한다.
4. 공간 진단은 contiguity 규칙, Moran's I, permutation p-value, LISA 유의성 기준을 함께 보고한다.
5. 분석 산출물이 생성·확인된 뒤에만 루트 DOCX에 최종 그림을 다시 넣는다.

기본 점검:

```bash
python3 -m py_compile "$PART1_SECTION31_FIGURE_SCRIPT"
python3 "$PART1_SECTION31_FIGURE_SCRIPT"
git -C "$PART1_REPO" status --short --branch
```

## Part 2: HLM 다층분석

3.2절 개인 특성과 자치구 특성 분석에는 Part 2를 사용한다.

주요 스크립트 키:

- `paths.analysis.part2.scripts.data_prep`
- `paths.analysis.part2.scripts.eda`
- `paths.analysis.part2.scripts.hlm_modeling`
- `paths.analysis.part2.scripts.generate_report`
- `paths.analysis.part2.scripts.regenerate_codebook_euckr`

주요 자료/산출물 키:

- `paths.analysis.part2.data.analysis_csv`
- `paths.analysis.part2.data.analysis_parquet`
- `paths.analysis.part2.tables.hlm_model_comparison`
- `paths.analysis.part2.tables.hlm_fit_statistics`
- `paths.analysis.part2.tables.hlm_policy_simulation`
- `paths.analysis.part2.tables.hlm_sensitivity_summary`
- `paths.analysis.part2.reports.validity_check`

자료 준비 점검:

- 서울서베이 연도가 로드되고 조화되었는지 확인한다.
- 서울 25개 자치구가 모두 있는지 확인한다.
- `digital_use_score`가 의도한 서비스 이용 항목으로 구성되었는지 확인한다.
- Level 1 변수가 연도별로 일관되게 재코딩되었는지 확인한다.
- Level 2 UMC 점수가 자치구와 연도로 병합되었는지 확인한다.
- 중심화 정보가 기록되었는지 확인한다.
- 최종 행 수, 자치구 수, 연도 분포를 보고한다.

원 설문 입력은 바꾸지 않는다. 스크립트에 로컬 절대 경로가 있으면 필요한 경로를 문서화하거나 좁은 패치로 매개변수화한다.

EDA 점검:

- Level 1 기술통계표가 있고 보고서와 맞는지 확인한다.
- Level 2 기술통계표가 있고 자치구 단위를 쓰는지 확인한다.
- 종속변수 분포를 확인한다.
- 취약집단 비교가 보고되었는지 확인한다.
- HLM 모델링 전 상관 점검으로 높은 공선성 위험을 표시한다.

모형 순서:

1. Model 0: null random-intercept model.
2. Model 1: Level 1 individual characteristics.
3. Model 2: Level 1 plus district-level UMC dimensions.
4. Model 3: cross-level interaction model.

해석 규칙:

- ICC가 작아도 design effect가 다층모형을 정당화할 수 있다.
- 자치구 간 분산이 작을 때 Level 2 효과는 조심스럽게 해석한다.
- 개인 수준 차이와 자치구 수준 차이를 구분한다.
- 관측 연관성을 인과 주장으로 바꾸지 않는다.
- 모형 적합도, 분산 성분, Level 2 추가가 실질적으로 적합을 개선하는지 보고한다.

타당성 점검:

- 주요 명세의 Level 2 예측변수에 결과에서 만든 집계값이 우연히 들어가지 않았는지 확인한다.
- 자치구 수준 affordability 해석은 개인 소득을 통제한 맥락에서만 조심스럽게 다룬다.
- 자치구 25개라는 제약은 추정 가능한 Level 2 매개변수 수를 제한한다.
- 가능하면 L1/L2 잔차 가정을 점검한다.
- 표준화 계수는 의미 있는 단위로 풀어 쓴다.
- 정책 시뮬레이션은 관측 연관성 아래 예측 변화이지 인과 정책 효과가 아니다.

기본 점검:

```bash
python3 -m py_compile "$PART2_DATA_PREP" "$PART2_EDA" "$PART2_HLM_MODELING" "$PART2_GENERATE_REPORT"
```

## 텍스트 전처리와 UMC 분류

게시물 전처리와 UMC 분류 배치 준비에는 이 절을 사용한다.

대표 키:

- `paths.analysis.text_preprocessing.repo`
- `paths.analysis.part3.text_preprocessing`

공통 흐름:

1. 입력 배치를 준비한다.
2. 가능한 경우 분류 에이전트를 실행하거나 지시한다.
3. 분류기 응답을 파싱한다.
4. 최종 CSV 산출물을 병합한다.
5. 행 수, 인코딩, 실패 응답 사례를 확인한다.

3.3절 방법론, 에이전트 운용, 프롬프트 세부사항, 독자용 파이프라인 설명이 필요하면 전처리와 추론 계층을 모두 확인한다. 공개 가능한 부록 후보는 사용자가 하나씩 지명하지 않아도 기본 검토한다: 키워드 사전 요약, UMC 관련성/차원 분류 프롬프트, abductive prompt, forward prompt, sequential prompt, judgment-synthesizer prompt. 기본 형식은 role/input/rule/output 표다. 사용자가 프롬프트를 "as-is", "verbatim", "그대로" 요청하면 원천 프롬프트 파일을 사용하고 줄바꿈과 출처 경로 키를 보존한다.

원문 게시물, 게시물 수준 식별자, 로컬 원자료 경로, 전체 게시물 수준 LLM 덤프를 보고서에 붙여 넣지 않는다. 전체 키워드 목록이 필요하면 본문 DOCX를 혼잡하게 만들지 말고 counts와 representative terms만 넣고 유지관리되는 사전 키를 note로 남기거나 별도 부록 산출물을 제안한다.

## 추론 파이프라인

구조화된 게시물 수준 추론에는 다음 키를 사용한다.

- `paths.analysis.part3.inference`
- `paths.analysis.legacy.inference`
- `paths.analysis.legacy.part2_alt1`
- `paths.analysis.legacy.part2_alt2`

통합된 작업군:

- 배치 전처리: 원 게시물에서 필터링/점수 JSONL 생성.
- 가설 생성: 여러 reasoning agent가 후보 해석 생성.
- 게시물 판단: 가설과 문맥을 로드해 accepted classification 부여.
- 조정: 여러 파이프라인 산출물을 비교해 보수적 최종 분류 채택.
- 지식 갱신: 로컬 규칙 아래에서만 category knowledge 추가 또는 수정.
- 벤치마크/포화도: 재현성, 범주 안정성, coverage 평가.

핵심 가드레일:

- 가설 생성과 판단을 분리한다.
- 텍스트 전용이어야 하는 단계에 문맥 블록이 새어 들어가지 않게 한다.
- 직접 텍스트 증거와 메타데이터는 비공개 경계 안에서만 보존한다.
- 공개 보고서에는 집계 수준 요약, 방법 설명, 익명화된 범주 예시만 전달한다.

## 보고서 전달

1. 원천 산출물을 확인한다.
2. 필요한 경우 DOCX, 그림, 표, 문구를 갱신한다.
3. 레이아웃이 중요한 경우 DOCX를 렌더하거나 구조적으로 검사한다.
4. 참조와 캡션을 고친다.
5. 변경된 저장소 상태를 보고한다.
