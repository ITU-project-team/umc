# UMC Report Quality Review - 2026-04-24

## Scope

검토 대상은 기존 개정본과 UMC 프로젝트 폴더의 주요 산출물이다. 기존 작업물은 수정하지 않았고, 이 메모와 Word 표 가능성 테스트 파일만 별도 폴더에 생성했다.

- 원고: `/Users/ujunbin/project/umc/Writing/manuscript/output/doc/UMC_report_draft_kr_revised.docx`
- Part 1 UMC 지수: `/Users/ujunbin/project/umc/Analysis/Part 1/output/tables/seoul_umc_scores_v7_2024.csv`
- Part 2 Bayesian/text: `/Users/ujunbin/project/umc/Analysis/02. baysian/output`
- Part 2-4 LLM pilot: `/Users/ujunbin/project/umc/Analysis/Part 2-4/output/pilot/comparison_report.csv`
- Part 3 HLM: `/Users/ujunbin/project/umc/Analysis/Part 3/output/tables/hlm_model_comparison.csv`
- 작성 계획/방법론 메모: `/Users/ujunbin/project/umc/Writing/report_writing_plan.md`

## Executive Diagnosis

현재 보고서는 소재와 분석 자산이 강하다. UMC 지수, 공간 자기상관, HLM, 플랫폼 텍스트, Bayesian aggregation을 하나의 문제의식으로 묶는 설계는 해커톤 보고서 수준을 넘길 잠재력이 있다. 특히 "플랫폼 텍스트는 대표 표본이 아니라 표출 자료(expression data)"라는 방향은 매우 좋다.

다만 최종 원고의 주장 강도와 실제 산출물 상태가 아직 완전히 일치하지 않는다. 가장 큰 리스크는 두 가지다.

1. 최신 HLM 결과는 지역 상호작용 효과를 강한 핵심 발견으로 밀기 어렵다.
2. LLM 파트는 실제 실행된 분류/파일럿/추론 파이프라인이 섞여 있어, 검증이 끝난 결과처럼 읽히는 문장을 줄여야 한다.

따라서 보고서의 최고 전략은 "서울의 디지털 격차를 인과적으로 증명했다"가 아니라, "UMC 실측 지수, 개인 수준 회귀, 플랫폼 표출 자료를 결합해 도시 디지털 결핍을 감사 가능한 방식으로 측정하고 해석했다"로 잡는 것이다. 이 편이 더 단단하고, 더 새롭고, 공격받기 어렵다.

## Critical Findings

### 1. HLM 스토리는 최신 결과 기준으로 재정렬해야 한다

원고 결론부는 공공 WiFi x 고령, 연결성 x 저학력 상호작용을 유의한 핵심 발견처럼 서술한다. 그러나 최신 HLM 테이블 기준으로는 다음과 같다.

- `score_Infrastructure_n:elderly = 1.84, p = .312`
- `score_Available_for_Use_n:elderly = 1.31, p = .394`
- `score_Affordability_n:elderly = 3.23, p = .081`
- `score_Infrastructure_n:low_edu = 4.18, p = .215`

즉 지역 인프라가 취약계층에게 차별적으로 큰 혜택을 준다는 문장은 현재 산출물 기준으로 과하다. 더 정직하고 강한 서술은 다음과 같다.

> HLM 결과는 서울의 디지털 활용 격차가 주로 개인 수준 요인, 특히 교육과 연령에 의해 구조화됨을 보여준다. 자치구 수준 UMC 조건은 일부 방향성 있는 신호를 보이나, 25개 자치구라는 Level-2 표본 제약 때문에 교차수준 상호작용은 탐색적으로 해석해야 한다.

이렇게 낮춰 쓰면 오히려 보고서가 더 성숙해진다. "지역이 전부다"가 아니라 "사람 기반 요인이 압도적이지만, 장소 조건은 취약집단 정책 설계의 맥락을 제공한다"가 현재 데이터와 맞다.

### 2. LLM 파트는 실행 상태를 세 층으로 분리해야 한다

현재 원고에는 다음 세 흐름이 한 절 안에서 섞여 있다.

- Phase 03 단일 Claude Sonnet 분류 파이프라인
- Bayesian aggregation 결과
- Part 2-4의 세 독립 추론 에이전트/삼각검증 설계

문제는 세 번째가 완전히 완료된 최종 판정 체계처럼 읽힌다는 점이다. `comparison_report.csv`는 pilot round의 convergence/high-confidence/overall 조건이 `FAIL`로 남아 있고, 원고도 "100건 Phase 1, Phase 2 미완료"라고 제한을 적고 있다. 따라서 "3개의 독립 추론 에이전트가 388건의 결여 가설을 생성하였다"는 문장은 가능하더라도, "검증된 결여 분포"처럼 사용하면 위험하다.

권장 구조는 다음과 같다.

1. 목적과 범위: 플랫폼 텍스트는 prevalence가 아니라 expression data.
2. 데이터 흐름: raw posts -> accessible posts -> keyword candidates -> LLM-coded cases -> Bayesian district profiles.
3. 분류 온톨로지: UMC 6차원, Y/N/?, absence typology.
4. LLM 실행 세부: Claude Sonnet, batch size, prompt, output schema, temperature/model version, parser.
5. 검증: human benchmark, Cohen's kappa, precision/recall, negative controls, rerun stability.
6. 집계: Bayesian update as exploratory triangulation.
7. 결과: "pilot findings" 또는 "illustrative findings"로 제한.

### 3. "언어 비종속성"과 "LLM의 구조적 우월성"은 낮춰 써야 한다

LLM 사용의 논리는 좋다. 한국어 생활 텍스트의 비표준 표현, 맥락 의존성, 형태소 기반 사전의 한계를 우회한다는 주장은 설득력이 있다.

다만 "언어 비종속성"은 과하다. 지금 증거로 말할 수 있는 것은 "언어별 사전 구축 부담을 줄이고, 동일한 이론 스키마를 다른 언어에 이식할 가능성이 있다" 정도다. 실제 language independence를 주장하려면 영어/한국어/다른 언어의 cross-lingual validation이 필요하다.

또한 "LLM이 기존 방법보다 구조적으로 우월하다"보다 아래처럼 쓰는 편이 단단하다.

> 본 연구에서 LLM은 비정형 생활 텍스트를 UMC의 사전 정의된 이론 범주로 분류하기 위한 절차적 도구로 사용된다. LLM의 장점은 타당성을 자동으로 보장하는 데 있지 않고, 동일한 입력 형식, 판정 기준, 오분류 방지 규칙을 반복 적용할 수 있게 하는 데 있다.

### 4. 플랫폼 텍스트는 개인정보/대표성/선택 편향을 전면에 둬야 한다

당근 동네생활 데이터는 강력하지만 위험하다. 이미 플랫폼을 쓰는 사람의 흔적이므로 가장 심각한 디지털 소외층은 구조적으로 빠질 수 있다. 또한 raw 데이터에는 게시글 ID, 지역, 시간, 제목/본문 등 재식별 가능성이 있는 정보가 포함된다.

보고서에는 아래 문장을 명시하는 것이 좋다.

> 플랫폼 게시글은 서울 시민의 대표 표본이 아니라, 디지털 접근이 가능한 이용자가 문제를 공개적으로 표출한 흔적이다. 따라서 본 분석은 디지털 결핍의 발생률을 추정하지 않고, 공식 지표가 포착하지 못하는 문제 표출의 양식과 지역별 불일치 신호를 탐색한다. 모든 사례 인용은 식별 가능 정보를 제거하거나 요약·의역하여 제시하였다.

### 5. Bayesian aggregation은 차별점이지만 검증 논리가 필요하다

`bayesian_posterior_k20.csv`, shrinkage plot, rank comparison, uncertainty map, raw vs posterior map 등 Part 2 Bayesian output은 보고서의 가장 차별적인 자산이다.

다만 해석은 조심해야 한다.

- Bayesian update가 플랫폼 활동 편향을 "해결"한다고 쓰면 과하다.
- 더 정확히는 "UMC 실측 사전정보와 플랫폼 표출 우도를 비교하는 구조화된 regularization"이다.
- UMC 점수는 높을수록 양호하고, 텍스트의 Y는 결여 표출이므로 방향을 반드시 정렬해야 한다. 설계 문서처럼 `prior_mean = 1 - UMC score`로 결여 확률을 정의하는 방식이 맞다.
- UMC 점수로 만든 prior와 텍스트의 UMC 정합성을 다시 검증하면 순환 검증 위험이 생긴다. human-coded benchmark, negative cases, 또는 외부 사건/서비스 자료를 최소 하나 붙이면 훨씬 강해진다.

권장 표현:

> Bayesian aggregation does not make platform posts representative. It provides a disciplined way to compare expressed digital difficulties against measured UMC priors, while shrinking sparse district evidence toward the measured baseline.

### 6. 수치 감사표가 필요하다

최종 제출 전 한 페이지짜리 "analysis inventory" 표를 추가해야 한다. 최소 항목은 다음과 같다.

| Analysis block | Unit | N | File/source | Interpretation |
|---|---:|---:|---|---|
| UMC index | district-year | 25 x 2 | `seoul_umc_scores_v7_2024.csv` | district-level measured connectivity |
| HLM | individual | 10,000 | `hlm_model_comparison.csv` | model-based association |
| Platform text raw | post | verify final count | Part 2 raw folder | non-representative expression traces |
| LLM classified | post | 5,000 or final verified N | `umc_post_scores.csv` or final classified output | post-level expression coding |
| Bayesian posterior | district x dimension | 150 | `bayesian_posterior_k20.csv` | exploratory prior-likelihood comparison |
| Multi-agent pilot | post/case | pilot only | `comparison_report.csv` | hypothesis generation, not final validation |

이 표 하나가 있으면 심사자가 "그래서 무엇을 몇 건 분석했나"를 바로 파악한다.

## Word Tables

Word 표는 가능하다. 다만 현재 개정본은 안정적 렌더링을 위해 대부분의 데이터 표가 PNG로 바뀌어 있다. 확인 결과 현재 개정 DOCX에는 실제 Word table이 1개만 남아 있다. 즉 "Word가 불가능"한 것이 아니라 "기존 변환 스크립트가 표를 이미지로 대체"한 상태다.

복원 전략은 원본 표를 그대로 되살리는 방식이 아니라, 새 표를 깨끗한 OOXML로 다시 만드는 방식이어야 한다.

권장 규칙:

- `python-docx`로 새 `add_table()` 생성
- `table.autofit = False`
- `<w:tblLayout w:type="fixed"/>` 지정
- `<w:tblW w:type="dxa" w:w="9360"/>`처럼 정수 twips만 사용
- `tblGrid`와 각 cell의 `tcW` 합계를 일치
- 첫 행에만 `tblHeader` 적용
- 본문 행의 `cantSplit` 제거
- 긴 표는 이미지가 아니라 여러 개의 editable Word table로 분할
- 표 글자 크기 7-8 pt, cell margin 60-80 twips

별도 테스트 파일을 만들었다.

- `/Users/ujunbin/project/umc/Writing/manuscript/output/doc/quality_review_20260424/word_table_feasibility.docx`

이 파일은 실제 Word table을 포함하며, XML 기준으로 decimal width 없이 fixed layout과 header row가 정상 설정되어 있다. 다만 현재 환경에는 `soffice`가 없어 PDF/PNG 렌더링 검증은 수행하지 못했다.

## Recommended Rewrite Strategy

### Core thesis

> Seoul's digital divide is not primarily a map of disconnected places. It is a layered capability problem: individual resources shape most variation, district-level UMC conditions define opportunity contexts, and platform text reveals how measured connectivity becomes, or fails to become, meaningful use in everyday life.

한국어 버전:

> 서울의 디지털 격차는 단순히 연결되지 않은 장소의 지도가 아니라, 개인의 자원, 자치구의 UMC 조건, 생활세계에서 표출되는 문제 경험이 겹쳐 만들어지는 다층적 역량 문제다.

### Methods framing

- 3.1: District-level measurement, not causal explanation.
- 3.2: Regression-based multilevel association, not causal identification.
- 3.3: Non-representative expression data, not prevalence estimation.
- Integration: Triangulated interpretation, not proof of mechanism.

### Result hierarchy

1. Strongest finding: individual-level factors dominate digital use gaps.
2. Strong contextual finding: district UMC profiles identify where infrastructure and service conditions are uneven.
3. Exploratory but novel finding: platform text highlights where measured UMC and expressed difficulty diverge.
4. Policy implication: people-based targeting should be place-sensitive, not place-only.

### LLM section rewrite stance

LLM을 "창의적 해석자"보다 "감사 가능한 분류 및 가설 생성 장치"로 쓰는 편이 더 강하다. 참신성은 모델 자체가 아니라 다음 결합에서 나온다.

- UMC 이론 범주를 prompt schema로 고정
- 과분류 방지 규칙을 명시
- Y/N/? 이산 판정으로 인간 검증 가능성 확보
- 자치구 x 차원 집계 후 UMC 실측 prior와 비교
- 불일치 셀을 정책적 조사 대상으로 삼음

이 구조가 사회과학적으로 더 세다. 허무맹랑한 "AI가 숨은 원인을 발견했다"가 아니라, "AI를 사용해 도시의 비정형 표출 자료를 검증 가능한 측정 파이프라인에 올렸다"가 된다.

## Immediate Fix Checklist

- [ ] 결론부의 `공공 WiFi x 고령 +3.03`, `연결성 x 저학력 +10.94` 주장을 최신 HLM 결과로 교체
- [ ] Figure 8 중복 번호 수정
- [ ] LLM section에서 "3개 독립 추론 에이전트가 최종 검증"처럼 읽히는 문장 완화
- [ ] 3.3 결과의 `정보부재 63%`, `복합 결여 88%`를 pilot/illustrative result로 라벨링
- [ ] platform text data의 sampling, user bias, terms/privacy 문단 추가
- [ ] analysis inventory 표 추가
- [ ] Bayesian aggregation을 "bias 해결"이 아니라 "structured comparison/regularization"으로 표현
- [ ] Word 표를 원하는 경우 이미지 표 대체본과 별도로 editable-table DOCX variant 제작

