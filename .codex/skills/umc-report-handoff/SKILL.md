---
name: umc-report-handoff
description: "UMC Part 1, Part 2, Part 3 분석 워커 증거를 보고서에 안전하게 전달할 때 사용한다. 원자료, 비공개 텍스트, 게시물 ID, 로컬 원자료 경로를 노출하지 않고 DOCX comment, 각주, 표/그림 노트, 산문 브리프, 보고서 워커 지시로 변환한다."
---

# UMC 보고서 전달

분석 워커 findings를 보고서용 지시나 독자용 설명으로 바꿔야 할 때 사용한다. 기본 chain은 analysis worker -> leader/orchestrator -> report DOCX worker다. 분석 워커는 소유권이 명시적으로 재배정되지 않는 한 DOCX를 직접 편집하지 않는다.

## 경로 레지스트리

- 구체 파일은 `config`의 프로젝트 경로 레지스트리로 해석한다.
- 키가 있으면 워커 브리프에는 하드코딩 경로 대신 경로 키를 사용한다.

## 전달 구조

1. live cmux layout을 확인하고 워커 역할을 확정한다.
2. 분석 워커에는 담당 경계 안의 읽기 전용 증거 작업을 배정한다.
   - Part 1: UMC 지수, Table 1 지표, 3.1절 그림/표.
   - Part 2: HLM 산출물, 모형 점검, 3.2절 연관성 문구.
   - Part 3: 플랫폼 텍스트, Bayesian/inference workflow, 3.3절 경계.
3. 반환 형식은 압축한다. 제안 문구, 확인한 비원자료 파일, 금지해야 할 주장, 범위 caveat를 받는다.
4. 리더가 핵심 사실을 직접 검증한 뒤 보고서 표면으로 변환한다.
5. 적절한 표면을 선택한다.
   - 작성자 전용 지시: DOCX reviewer comment.
   - 독자용 출처·정의·범위 설명: 각주.
   - 표/그림 자체 설명: compact table/figure note.
   - 일반 산문 초안이 필요한 경우: `report-prose-writer` 브리프.
   - 방법론 설명, context gating, 3.1/3.2/3.3 연결 설명이 필요한 경우: `report-method-explainer` 브리프.
   - 주장 강도와 해석 한계 조정이 필요한 경우: `report-evidence-boundary-editor` 브리프.
   - 부록 프롬프트·키워드·재현성 표면 정리가 필요한 경우: `report-appendix-curator` 브리프.
   - DOCX 반영·렌더·한글 MD 동기화가 필요한 경우: `report-docx-manager` 브리프.
6. 보이는 레이아웃이 바뀌면 DOCX 또는 영향받은 렌더 쪽을 검증한다.
7. 보고서 DOCX 본문이나 각주를 의미 있게 바꾼 뒤에는 `paths.docs.korean_markdown_copy`에 한국어 읽기용 Markdown 전문 복사본을 간단한 구조로 갱신한다.
8. 기존 PDF와 대비해 달라지는 본문·표기·부록 연결 문구는 DOCX에서 파란색 run으로 표시한다.

## 작성 원칙

- 내부 작업 상태, 워커 이름, 검증 TODO는 독자용 각주에 넣지 않는다.
- 출처 설명은 짧고 재현 가능한 수준으로만 쓴다.
- 실질적 해석을 먼저 쓰고 숫자는 보조 근거로만 사용한다.
- 본문에서 부록 자료를 가리킬 때는 문장 안 설명 뒤에 `(Appendix 1)`처럼 괄호형 참조를 붙이고, 해당 부록 제목과 번호가 일치하는지 확인한다.
- Part 3 예시는 보고서에 이미 안전하게 일반화된 사례가 있는 경우를 제외하고 익명화·범주 수준으로 유지한다.
- 한국어 Markdown 읽기본은 사용자가 빠르게 검토하기 위한 보조본이다. 원문 DOCX를 대체하지 않으며, 표·그림은 간단한 Markdown 텍스트와 캡션 중심으로 옮긴다.

## 경계

- 원 설문 행, 비공개 플랫폼 텍스트, 게시물 ID, 로컬 원자료 경로, 비밀값, `.env`, 로컬 설정을 comment, 각주, handoff에 포함하지 않는다.
- 분석 저장소와 루트 보고서 저장소의 dirty 상태는 완료된 전달과 분리해 보고한다.
- 중첩 저장소 경고는 숨기지 말고 별도로 표시한다.
