---
name: umc-report-commenting
description: UMC 보고서의 DOCX reviewer comment, 각주, 표 노트, 그림 노트, 부록 노트, 검토 주석을 추가·검토·해결할 때 사용한다. 작성자용 지적과 독자용 설명을 구분한다.
allowed-tools: Read, Bash
---

# UMC 보고서 주석·각주 처리

UMC 보고서 워크플로에서 annotation 작업을 할 때 이 스킬을 사용한다.

## 경로 레지스트리

- 구체 파일은 `config`의 프로젝트 경로 레지스트리로 해석한다.
- 활성 초안은 `paths.docs.active_report_docx`를 사용한다.

## 노트 유형 선택

- 작성자나 편집자에게만 보일 지적은 DOCX reviewer comment로 남긴다.
- 독자가 읽어야 하는 출처, 정의, 범위 설명은 각주나 표/그림 노트로 옮긴다.
- 표 자체의 약어, 기준범주, 지표 정의, 유의성 표시는 표 아래 compact note로 둔다.
- 문단 흐름을 끊지만 출처·정의·범위 설명이 필요한 경우에만 각주를 사용한다.
- 스크래치 초안이거나 사용자가 명시적으로 요청한 경우에만 대괄호 인라인 노트를 사용한다.

## DOCX Reviewer Comment 규칙

- comment는 가장 작은 정확한 텍스트 범위, 표 셀, 캡션, 그림 참조에 앵커링한다.
- comment 하나에는 하나의 문제와 하나의 요청만 담는다.
- 필요하면 `Evidence:`, `Formatting:`, `Source:`, `Privacy:`, `Decision:` 같은 짧은 범주로 시작한다.
- 원문 게시물, 게시물 ID, 비공개 플랫폼 텍스트, 로컬 원자료 경로, `.env` 값, 비밀값은 comment나 note에 넣지 않는다.
- Part 3 예시와 민감 증거는 익명화된 paraphrase만 사용한다.
- 최종 해석을 comment에 보관하지 않는다. 채택된 해석은 본문, 각주, 표/그림 노트로 이동한다.

## 각주와 독자용 노트

- 독자용 정보 주석은 reviewer comment로 두지 말고 각주 또는 표/그림 노트로 변환한다.
- 각주는 출처, 정의, 범위 제한, 지표 산식의 짧은 설명에 한정한다.
- 같은 표의 여러 지표 설명은 각주보다 표 아래 compact note가 더 자연스러운지 먼저 판단한다.
- 각주 문장은 짧고 보고서 본문 톤을 따른다. 내부 작업 지시, 워커 이름, 검토 상태는 포함하지 않는다.
- 각주 번호 참조는 항상 윗첨자로 보이게 유지한다. OOXML을 직접 수정한 경우 `w:footnoteReference` 또는 `w:footnoteRef`가 있는 run에 `w:vertAlign w:val="superscript"`가 있는지 확인한다.
- PDF 렌더는 Word comment를 보통 보여주지 않는다. 각주, 표 노트, 그림 노트, 페이지네이션은 렌더로 확인한다.

## DOCX 작업 절차

- `python-docx` comment API가 가능하면 대상 paragraph/run을 찾고 필요한 경우 run을 분할한 뒤 `Document.add_comment(...)`를 사용한다.
- 각주가 필요하면 OOXML의 `footnotes.xml`, document relationship, content type을 함께 확인한다.
- 기존 comment를 각주로 바꿀 때는 작성자용 comment와 독자용 정보 comment를 분리한다.
- 각주 변환 후 DOCX를 다시 열어 comment 수, footnote reference 수, footnote text, 각주 참조 윗첨자 속성을 확인한다.
- 보이는 레이아웃이 바뀌면 DOCX를 PDF로 렌더하고 영향을 받은 쪽을 확인한다.

## 검토 순서

1. 사용자가 작성자용 comment를 원하는지, 독자에게 보이는 각주/노트를 원하는지 확인한다.
2. 정확한 대상 위치를 찾고 문서 전체에 넓게 annotation하지 않는다.
3. privacy-safe 문구로 comment, 각주, 표/그림 노트를 추가한다.
4. 필요에 따라 DOCX를 다시 열거나 렌더한다.
5. 추가·변환·남겨둔 comment와 각주 수, 위치, 잔여 위험을 보고한다.
