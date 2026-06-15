---
name: umc-reader-first-method-writing
description: UMC 보고서 방법론 문단을 독자가 처음 읽어도 이해할 수 있게 작성·검토할 때 사용한다. 특히 Part 3 LLM/Bayesian/inference, context gating, data-based verification, 3.1/3.2/3.3 연결 설명에 적용한다.
allowed-tools: Read, Bash
---

# UMC 독자 우선 방법론 작성

보고서 방법론은 내부 파이프라인 나열이 아니라 독자의 이해를 먼저 달성해야 한다. 새 용어와 단계명을 쓰기 전에 왜 필요한지, 무엇을 입력으로 받고, 무엇을 차단하며, 어떤 산출을 만들고, 해석 한계가 무엇인지 설명한다.

## 기본 원칙

- 독자가 처음 보는 상태를 기본값으로 둔다.
- 단계명보다 기능을 먼저 설명한다.
- 모든 방법론 문단은 `목적 -> 입력 -> 처리 -> 산출 -> 해석 한계` 흐름을 갖는다.
- 수치나 파일명보다 분석 단위와 판단 단위를 먼저 밝힌다.
- 방어 문장을 먼저 늘어놓지 않는다. 독자가 따라갈 수 있는 집계량과 해석 대상을 먼저 설명하고, 한계는 그 뒤에 짧고 정확하게 둔다.
- 분석 단위가 `개별 게시물 -> 자치구·차원 셀 -> 사례 해석`으로 바뀌는 지점을 명시한다.
- 내부 워커 이름, TODO, 로컬 경로, 원자료 위치, 게시물 ID, 비공개 플랫폼 텍스트를 독자용 문장에 넣지 않는다.

## Part 3 설명 기준

- Part 3-1 classification: 게시물 수준 signal base를 만든다. 이 층만으로 자치구 조건이나 유병률을 주장하지 않는다.
- Part 3-1 classification은 multi-label이다. 한 게시물이 여러 차원 셀에 각각 기여할 수 있고, 차원별 합은 전체 관련 게시물 수보다 클 수 있음을 밝힌다.
- Part 3-2 EB aggregation: 관측 단위는 자치구·차원 셀이다. `y_gk`는 해당 셀의 분류 게시 신호 수, `E_g`는 작성 시점 생활인구 person-years 노출, observed rate는 `y_gk/E_g`다.
- Part 3-2 EB aggregation: 3.1절 자치구·차원 점수는 결핍 방향으로 뒤집은 뒤 차원별 관측율 범위에 맞춰 administrative prior rate로 변환한다. UMC 점수 자체를 게시물의 직접 예측변수처럼 쓰지 않는다.
- Part 3-2 EB aggregation: posterior rate는 단순 보정 관측율이 아니라 prior rate와 observed rate의 EB 정밀도 가중평균이다. posterior shift는 posterior rate minus prior rate로 설명한다.
- Part 3-3 inference: classification과 EB aggregation 이후에 시작한다. high-divergence cell 또는 우선 검토 셀의 게시물을 설명 후보로 읽되, 곧바로 결핍 유형을 확정하지 않는다. 본문에서는 기준 없는 `outlier` 표현을 피한다.
- Section 3.2 HLM: 해석의 guardrail이다. 자치구 수준 조건의 일반적 인과효과를 주장하지 않고, 개인 취약성이 더 큰 설명력을 가진다는 경계를 유지한다.
- Stage B reasoners: post text, metadata, dim codes, codebook만 사용한다. 3.1 지수값, 3.2 결과, EB high-divergence label, district profile, external indicators, other agent outputs는 차단한다.
- Stage B 정보 차단의 이유를 먼저 쓴다: EB 결과를 알고 난 뒤 텍스트 해석을 사후적으로 맞추지 않기 위해서다.
- Stage C/D/E: Stage C는 필요한 변수를 명세하고, Stage D는 registered data로 규칙 기반 증거 묶음을 만들며, Stage E는 supported/refuted/undetermined verdict만 부여한다. 본문에서는 `evidence.json`, `deterministic evidence`, `data_spec` 같은 구현 용어를 필요한 경우에만 풀어서 쓴다.
- Prompt는 코드북 자체가 아니라 코드북 기준을 일관된 순서로 적용하게 하는 실행 지침으로 설명한다.

## 역할 라우팅

- 방법론 산문 초안: `report-method-explainer`.
- 주장 강도와 한계 문구: `report-evidence-boundary-editor`.
- DOCX 반영, 파란색 run, 렌더 검증: `report-docx-manager`의 layout/execution 책임.
- 부록 프롬프트와 재현성 표면: `report-appendix-curator`.
- 독자 이해 검증: `reader-comprehension-verifier`.
