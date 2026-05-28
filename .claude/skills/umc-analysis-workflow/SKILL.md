---
name: umc-analysis-workflow
description: Part 1, Part 2, Part 3, text preprocessing, Bayesian aggregation, inference 산출물의 분석 스크립트, 결과, 해석 점검, 보고서 전달에 사용한다.
allowed-tools: Read, Bash
---

# UMC 분석 워크플로

분석 스크립트, 산출물, 해석 점검, 보고서 전달에 사용한다.

## 경로 레지스트리

- 구체 파일은 `config`의 프로젝트 경로 레지스트리로 해석한다.
- 레지스트리 값은 루트 저장소 기준 GitHub 상대 경로다.
- 워커 브리프에는 가능하면 경로 키를 쓰고, 실행 시점에만 구체 경로로 해석한다.

## 저장소

- `paths.analysis.part1.repo`: UMC 지수, 자치구 점수, 지도, Moran/LISA, 3.1절 그림.
- `paths.analysis.part2.repo`: HLM/다층모형과 3.2절 해석.
- `paths.analysis.part3.repo`: 텍스트 전처리, Bayesian 업데이트, 구조화 추론, 3.3절 전달.
- `paths.analysis.text_preprocessing.repo`: 분류 지원과 레거시 전처리.
- `paths.analysis.legacy.*`: 레거시 또는 특수 추론 출처.

## 점검

- 분석 논리를 바꾸기 전 스크립트와 기존 산출물을 먼저 확인한다.
- 원자료와 비공개 자료는 추적하지 않는다.
- 보고서 주장은 원천 표, 그림, 스크립트, 검증 노트와 대조한다.
- 분석 파일과 보고서 파일이 모두 바뀌면 소유 저장소별 커밋을 분리한다.
- Part 3 공개/비공개 경계에서는 코드, 설정, 집계 표, 집계 그림, 자치구 수준 요약만 공개 가능 범위로 본다. 원자료와 게시물 수준 텍스트 출력은 제외한다.
- 보고서 그림은 절제된 학술 스타일을 쓰고 해석은 본문이나 정식 캡션에 둔다.
- HLM, LLM 플랫폼 텍스트 분석, Bayesian 업데이트, Digital Desert, 정책 권고를 해석할 때는 `umc-report-evidence-framing`을 함께 적용한다.

## 3.3절 부록 기본값

3.3절 방법론, 에이전트 운용, 프롬프트 설계, LLM 해석의 연구적 엄밀성을 설명하라는 요청이 있으면 다음 둘을 함께 확인한다.

- `paths.analysis.part3.text_preprocessing`
- `paths.analysis.part3.inference`

부록 후보는 사용자가 하나씩 지명하지 않아도 기본 검토한다: 키워드 사전 요약, UMC 관련성/차원 분류 프롬프트, abductive prompt, forward prompt, sequential prompt, judgment-synthesizer prompt. 기본 형식은 role/input/rule/output 표다.

사용자가 프롬프트를 "as-is", "verbatim", "그대로" 요청하면 원천 프롬프트 파일을 사용하고 줄바꿈과 출처 경로 키를 보존한다.

원문 게시물, 게시물 수준 식별자, 로컬 원자료 경로, 전체 게시물 수준 LLM 덤프는 노출하지 않는다. 전체 키워드 사전이 보고서에 너무 길면 DOCX에는 counts와 representative terms를 넣고 유지관리되는 사전 키를 note로 남긴다.

## 보고서 전달

1. 원천 산출물을 확인한다.
2. DOCX, 그림, 표, 산문을 갱신한다.
3. 레이아웃이 중요하면 DOCX를 렌더하거나 구조 검사한다.
4. 참조와 캡션을 고친다.
5. 변경된 저장소 상태를 보고한다.
