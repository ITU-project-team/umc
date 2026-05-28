---
name: umc-argument-review-task
description: "UMC 서울 보고서의 논증 일관성과 결과 간 정합성을 검토할 때 사용한다. ITU UMC 이론, Part 1 자치구 지수, Part 2 HLM, Part 3 LLM/Bayesian 신호, 정책 권고, 결론이 과장 없이 하나의 증거 사슬을 이루는지 확인한다."
---

# UMC 논증 검토 태스크

## 목적

보고서가 Part 1, Part 2, Part 3 산출물을 단순 병렬 배치한 문서가 아니라, 초연결 도시에서 Universal and Meaningful Connectivity를 측정하는 하나의 통합 방법론으로 읽히는지 검토한다.

## 사용 시점

- 사용자가 UMC 프로젝트에서 논증 검토, 일관성 검토, 결과 정합성, 모순 점검을 요청할 때.
- DOCX 제출이나 재설계 전 품질 관리가 필요할 때.
- 새로운 Part 1, Part 2, Part 3 산출물이 보고서에 들어가 bridge 점검이 필요할 때.

## 출처 경계

- 구체 파일은 `config`의 프로젝트 경로 레지스트리로 해석한다.
- 활성 보고서: `paths.docs.active_report_docx`.
- 디자인 가이드: `paths.docs.design_guide`.
- Part 1 출처: `paths.analysis.part1.output`.
- Part 2 출처: `paths.analysis.part2.output`.
- Part 3 출처: `paths.analysis.part3.bayesian_output`, `paths.analysis.part3.inference`, 공개 가능한 집계 문서.
- 원문 플랫폼 텍스트, 비공개 텍스트, 게시물 ID, 비밀값, `.env`, 로컬 설정은 열람·인용·노출하지 않는다.

## 판단 단위

D1. 여섯 연결고리를 pass, weak, missing, overclaimed로 평가한다.

- problem -> UMC measurement gap.
- gap -> theory/metatheory.
- theory -> operational variables and units.
- Part 1 index -> Part 2 HLM interpretation.
- Part 2 HLM -> Part 3 platform-visible signal interpretation.
- integrated results -> policy recommendations and limitations.

D2. 문제 유형을 분리한다.

- 논리 문제: 논증 연결이 빠졌거나 모순됨.
- 증거 문제: 주장이 인용된 표, 그림, 모형, 진단보다 앞서 나감.
- 작성/디자인 문제: 논리는 유지되지만 보고서가 시각적·수사적으로 읽기 어려움.

D3. 결과 간 정합성을 점검한다.

- Part 1 자치구 격차를 개인 박탈의 인과 증거로 해석하지 않는다.
- Part 2 HLM은 인과 식별이 아니라 다층 연관성 분석으로 유지한다.
- 작은 ICC와 제한적인 Level 2 효과가 place-sensitive 정책 주장과 충돌하지 않아야 한다.
- Part 3 LLM 분석은 prevalence estimation이 아니라 구조화된 코딩과 플랫폼 가시 신호 탐지로 유지한다.
- Bayesian 업데이트는 확증적 박탈 측정이 아니라 탐색적 증거 통합으로 유지한다.
- Digital Desert 라벨은 결정론적 자치구 진단이 아니라 잠정적 타기팅 라벨로 유지한다.

## 절차

1. 절, 주요 주장, 증거 출처, 다음 연결문으로 논증 지도를 만든다.
2. 보고서의 주요 수치/결과 주장을 추출하고 가능한 최신 공개 집계 산출물과 대조한다.
3. 근거 부족 주장, 누락된 가정, 과잉 주장을 표시한다.
4. 약한 연결고리마다 구체적인 재작성 지시나 bridge sentence를 제안한다.
5. 우선순위가 있는 수정 목록을 만들고, 지금 DOCX에 반영할 항목과 검토 노트로 남길 항목을 구분한다.

## 검증

- 모든 주요 결과 주장은 이론, 자료, 모형, 그림, 표, 진단, 공개 가능한 집계 산출물 중 하나에 연결되어야 한다.
- 결론은 3장과 4장에 없는 주장을 새로 도입하지 않는다.
- 정책 절은 증거 위계를 따른다: 개인 취약성 중심 지원을 먼저 두고, place-sensitive 타기팅을 보조적으로 둔다.
- 보고서 문구는 개인정보 경계를 보존하고 원문 플랫폼 텍스트나 게시물 ID를 공개하지 않는다.

## 출력 계약

- 논증 지도.
- 연결고리 점수.
- 결과 간 정합성 findings.
- 최우선 수정 과제.
- 제안 bridge sentence 또는 DOCX 편집 지시.
