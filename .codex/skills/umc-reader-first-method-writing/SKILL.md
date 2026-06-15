---
name: umc-reader-first-method-writing
description: "UMC 보고서 방법론 문단을 독자가 처음 읽어도 이해할 수 있게 작성·검토할 때 사용한다. 특히 Part 3 LLM/Bayesian/inference, context gating, data-based verification, 3.1/3.2/3.3 연결 설명에 적용한다."
---

# UMC 독자 우선 방법론 작성

보고서 방법론은 내부 파이프라인 나열이 아니라 독자의 이해를 먼저 달성해야 한다. 새 용어와 단계명을 쓰기 전에 왜 필요한지, 무엇을 입력으로 받고, 무엇을 차단하며, 어떤 산출을 만들고, 해석 한계가 무엇인지 설명한다.

## 기본 원칙

- 독자가 처음 보는 상태를 기본값으로 둔다.
- 단계명보다 기능을 먼저 설명한다.
- 모든 방법론 문단은 `목적 -> 입력 -> 처리 -> 산출 -> 해석 한계` 흐름을 갖는다.
- 수치나 파일명보다 분석 단위와 판단 단위를 먼저 밝힌다.
- 내부 워커 이름, TODO, 로컬 경로, 원자료 위치, 게시물 ID, 비공개 플랫폼 텍스트를 독자용 문장에 넣지 않는다.

## Part 3 설명 기준

- Part 3-1 classification: 게시물 수준 signal base를 만든다. 이 층만으로 자치구 조건이나 유병률을 주장하지 않는다.
- Part 3-2 EB aggregation: 3.1절 자치구·차원 지표를 administrative prior로 사용하고, 생활인구 노출로 보정한 플랫폼 게시율과 비교해 district-dimension divergence를 찾는다.
- Part 3-3 inference: classification과 EB aggregation 이후에 시작한다. high-divergence cell의 게시물을 설명 후보로 읽되, 곧바로 결핍 유형을 확정하지 않는다.
- Section 3.2 HLM: 해석의 guardrail이다. 자치구 수준 조건의 일반적 인과효과를 주장하지 않고, 개인 취약성이 더 큰 설명력을 가진다는 경계를 유지한다.
- Stage B reasoners: post text, metadata, dim codes, codebook만 사용한다. 3.1 지수값, 3.2 결과, EB outlier label, district profile, external indicators, other agent outputs는 차단한다.
- Stage C/D/E: Stage C는 필요한 변수를 명세하고, Stage D는 registered data로 deterministic evidence를 만들며, Stage E는 supported/refuted/undetermined verdict만 부여한다.

## 역할 라우팅

- 방법론 산문 초안: `report-method-explainer`.
- 주장 강도와 한계 문구: `report-evidence-boundary-editor`.
- DOCX 반영, 파란색 run, 렌더 검증: `report-docx-manager`의 layout/execution 책임.
- 부록 프롬프트와 재현성 표면: `report-appendix-curator`.
- 독자 이해 검증: `reader-comprehension-verifier`.
