---
name: umc-report-evidence-framing
description: UMC 보고서에서 HLM, LLM 플랫폼 텍스트 분석, Bayesian 업데이트, Digital Desert, 정책 권고를 해석하는 문구를 편집할 때 사용한다. 주장을 증거 수준에 맞춘다.
allowed-tools: Read, Bash
---

# UMC 보고서 증거 서술

UMC 프로젝트의 보고서용 문구에 사용한다.

## 출처 기준

구체 파일은 `config`의 프로젝트 경로 레지스트리로 해석한다.

- 활성 초안: `paths.docs.active_report_docx`
- 용어 사전: `paths.docs.evidence_terms`
- HLM 원천 표: `paths.analysis.part2.tables.dir`
- Part 3 집계 출처: `paths.analysis.part3.bayesian_tables`, `paths.analysis.part3.inference`

## 핵심 서술 규칙

- ITU UMC framework, critical realism, multilayer design을 유지한다.
- HLM은 인과 식별이 아니라 hierarchical linear model 기반 다층 연관성 분석 또는 설명적 분해로 제시한다.
- 중심 메시지를 분명히 한다: 서울의 디지털 이용 격차는 개인 수준 취약성이 더 크게 설명하며, 자치구 수준 지표는 맥락 조건과 타기팅 보조 신호다.
- 정책에는 문헌 구분을 설명하는 경우를 제외하고 place-sensitive targeting 또는 place-sensitive intervention을 쓴다.
- LLM 분석은 platform-visible lived-experience signal detection으로 제시한다. LLM은 자율 증거원이 아니라 구조화된 코딩 보조자다.
- 프롬프트는 codebook-like classification criteria로 설명한다. 일관성을 높일 수 있지만 human validation을 대체하지 않는다.
- precision, recall, F1-score, Cohen's kappa, Krippendorff's alpha, robustness statistics, validation sample sizes를 지어내지 않는다.
- Bayesian 업데이트는 행정지표와 플랫폼 가시 신호 사이의 탐색적 증거 통합이지 deprivation prevalence의 확증적 추정이 아니다.
- Digital Desert는 잠정적이고 비결정론적인 타기팅 라벨로 유지한다. 자치구가 deprivation을 원인적으로 만든다는 인상을 주지 않는다.

## 최초 사용 설명

- HLM: hierarchical linear model, 중첩 자료에서 개인 수준과 자치구 수준 요인을 분리하는 모형.
- LLM: large language model, 여기서는 미리 정의된 기준으로 플랫폼 텍스트를 분류하는 구조화된 코딩 보조자.
- Bayesian updating: prior information을 새 증거로 갱신하는 방법. 여기서는 행정지표와 플랫폼 가시 신호를 탐색적으로 연결하는 데 사용한다.

## 권장 정책 구조

1. 개인 취약성 중심 지원: 저학력 고령층, 고령 1인 가구, 디지털 서비스 이용 경험이 낮은 집단, 오프라인 접근성이 낮은 주민.
2. Place-sensitive targeting: UMC composite index와 dimension scores로 취약 주민에게 더 효율적으로 도달할 위치를 찾되, 낮은 자치구 점수를 인과 증거로 보지 않는다.
3. Capability, safety, affordability support: 기기 접근, 디지털 서비스 훈련, 보안·사기 예방 역량, 통신비 부담 완화, 복잡한 공공 앱 이용 지원.
