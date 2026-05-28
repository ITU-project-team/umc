---
name: umc-academic-table-formatting
description: UMC 보고서 DOCX 학술 표를 생성·편집·검토할 때 사용한다. 특히 Table 4 스타일 HLM/모형 결과표, compact evidence table, 부록 프롬프트/키워드 표에 적용한다.
allowed-tools: Read, Bash
---

# UMC 학술 표 포맷팅

활성 UMC 보고서의 보고서용 표에 사용한다.

## 경로 레지스트리

- 구체 파일은 `config`의 프로젝트 경로 레지스트리로 해석한다.
- 활성 보고서 DOCX는 `paths.docs.active_report_docx`를 사용한다.
- 일회성 렌더 파일은 `paths.tmp.root`를 사용한다.

사용자가 "Table 4" 같은 표를 요청하면 활성 보고서의 `Table 4. HLM Estimation Results`를 시각 기준으로 삼는다.

## 규칙

- 표는 증거 display이지 산문 container가 아니다.
- 행은 짧은 라벨, compact wording, 작은 글꼴, 문단 간격 0, 좁은 셀 여백으로 압축한다.
- 해석은 긴 표 셀 안이 아니라 본문, 각주, 표 노트에 둔다.
- 캡션은 formal하게 표와 붙여 둔다. 캡션이 쪽 하단에 고립되지 않게 한다.
- 중첩 표나 장식적 표를 쓰지 않는다.

## DOCX 기본값

- 밀도 높은 수치표와 Table 4 스타일 모형표: Arial `8 pt`; 짧은 설명 표: `9-9.5 pt`.
- 셀 문단: 앞/뒤 `0 pt`, single spacing.
- 세로 정렬: 짧은 셀과 수치 셀은 가운데, 불가피한 산문 셀만 위쪽.
- 셀 여백: 위/아래 `30-50 twips`, 좌/우 `60-90 twips`.
- 헤더 행: 굵게, compact, gray fill, high contrast, 빈 줄 없음.
- 고정된 큰 행 높이는 피하고 빈 셀 문단을 제거한다.

## Table 4 모형 결과 패턴

- HLM, regression, 비교 가능한 multi-model result table에 사용한다.
- 캡션: 가운데 정렬 `Caption` 스타일, italic report caption text, 표 바로 위.
- 표: 거의 full text width, 활성 DOCX에서는 `List Table 1 Light` 효과를 따른다.
- 열: `Variable`과 model columns. 네 모형이면 대략 `30% / 21% / 16% / 16% / 16%`.
- 헤더: gray fill, bold centered labels, double top/bottom rules.
- 본문: 첫 열 좌측 정렬, 모형 결과 열 중앙 정렬, Arial `8 pt`, 문단 간격 없음.
- 그룹 행: `Level 1: Individual characteristics`, `Level 2: District characteristics`, `Retained interactions`처럼 짧은 라벨을 쓴다. 모형 셀은 비우고 그룹 라벨은 굵게 처리한다.
- 테두리: 세로 구분선은 얇게 보이게 하고, 표 상단·헤더 아래·주요 그룹 위·표 하단에는 double horizontal rules를 둔다.
- 강조: 원천 표나 사용자가 명시한 경우에만 드문 yellow highlighting을 보존한다. 임의로 강조를 만들지 않는다.
- 노트: 기준범주, 모형 variant, 유의성 표시는 표 아래 compact `9 pt` note에 둔다.

## 너비 패턴

- 수치/통계 표: 좁은 수치 열과 넓은 라벨 열.
- Table 4 스타일 모형표: 첫 열 약 `30%`, 모형 열은 내용 길이에 맞게 분배.
- 프롬프트 표: label `25-30%`, content `70-75%`.
- 키워드 부록 표: count column은 최대 `10-12%`, representative terms가 가장 넓은 열.
- 셀이 시각적으로 세 줄을 넘으면 줄이거나 note/artifact로 옮긴다.

## 압축 내용

- 셀 안에서는 문장형 산문보다 명사구를 쓴다.
- `SD`, `Min`, `Max` 같은 짧은 헤더를 쓰고 노트에서 정의한다.
- 텍스트 열은 좌측 정렬, 짧은 범주 열은 중앙 정렬, 수치/모형 결과 열은 우측 또는 소수점 정렬한다.
- 진짜 헤더 행만 반복한다. 본문 행을 반복 헤더로 표시하지 않는다.
- 모든 본문 행에 `cantSplit`을 걸지 않는다. 헤더, 그룹 행, 매우 짧은 표에만 제한적으로 쓴다.

## 부록 규칙

- 프롬프트 표는 기본적으로 role/input/rule/output을 요약한다. 사용자가 "as-is", "verbatim", "그대로"를 명시하면 원천 프롬프트 텍스트를 부록에 넣고 줄바꿈, 출처 경로 키, 버전 메타데이터, compact font/table spacing을 유지한다.
- 키워드 표는 count와 representative terms만 보여준다.
- 전체 프롬프트와 사전은 경로/날짜/버전 메타데이터가 있는 유지관리 부록 산출물에 둔다.
- 원문 게시물, 게시물 ID, 게시물 수준 LLM 덤프, 로컬 원자료 경로, 비공개 자료는 보고서 표에 넣지 않는다.

## 페이지네이션 규칙

- 본문 순서로 표를 탐지한다. `Table N.` 또는 `Appendix Table A#.` 캡션 바로 뒤의 표를 보고서 표로 본다. 그림 레이아웃용 표는 건너뛴다.
- 캡션은 다음 표와 함께 유지한다.
- PDF 렌더 후 continuation page가 `<=3`행이거나 거의 빈 공간이면 표시한다.
- 고아 캡션이나 깨진 표를 막는 경우가 아니면 수동 페이지 나누기를 넣지 않는다.

## 검토

1. 캡션 번호와 제목을 확인한다.
2. 페이지 분할과 고아 캡션을 확인한다.
3. 산문, 반복 라벨, 빈 문단, 큰 글꼴 때문에 행이 길어진 부분을 찾는다.
4. PDF로 렌더해 시각적으로 확인한다.
5. 일회성 렌더 파일은 설정된 임시 출력 키 아래에 두고 보고 전 정리한다.
