# UMC 프로젝트 라우터

이 파일은 UMC 프로젝트의 루트 라우터로 사용한다.

## 프로젝트 주제

An Integrated Methodology for Measuring Universal and Meaningful Connectivity (UMC) in a Hyper-Connected City

보고서 목표물은 전체 보고서이며, 현재 초안은 아직 완성본이 아니다.

## 로컬 에이전트

- `report-docx-manager`: 보고서 DOCX 집행 — 절 구조, 산문 배치, 표/그림 삽입, 인용·각주 배치, 레이아웃·렌더(render-check) 하위역할, 한글 MD 동기화를 담당한다.
- `report-prose-writer`: 3.1~3.3절과 결과·정책 서술의 산문 초안을 분석 핸드오프 증거로부터 작성한다. DOCX 최종 편집·배치는 하지 않는다.
- `report-figure-generator`: 보고서 그림 생성/수정, 원천 자료 확인, 학술적 스타일, DOCX 배치 검증을 담당한다.
- `part1-analysis-manager`: Part 1 UMC 지수 구축, 자치구 점수, 보고서용 그림/표, 3.1절 전달물을 담당한다.
- `part2-analysis-manager`: Part 2 HLM/다층모형 분석, 모형 산출물, 타당성 점검, 3.2절 전달물을 담당한다.
- `part3-analysis-manager`: Part 3 텍스트/Bayesian/추론 통합 워크플로와 데이터 경계 점검을 담당한다.
- `project-verifier`: 경로·존재·tmp 경계, 보안 경계, Git staged 범위·커밋 분리, 인용·교차참조를 읽기 전용으로 검증한다.
- `numeric-fidelity-verifier`: 보고서 본문·표·캡션 수치가 Part 1/2/3 집계 표 산출과 일치하는지 읽기 전용으로 대조한다.

각 워커의 담당 경계 안에서 서로 독립적인 보조 점검에는 제한된 병렬 서브에이전트를 사용할 수 있다. 워커 지시는 담당 주체를 명시해야 하며, 원자료, 비공개 플랫폼 텍스트, 게시물 ID, 비밀값, `.env`, 로컬 설정을 서브에이전트에 노출하면 안 된다.

## 프로젝트 규칙

- UMC 전용 Claude/Codex 스킬과 에이전트는 이 프로젝트 루트에 둔다.
- 중첩 분석 저장소는 좁은 실행 세부사항을 위해 자체 Claude 스킬과 에이전트를 둘 수 있다.
- 공유 프로젝트 설정은 `config`의 경로 레지스트리에 둔다. Codex와 Claude 라우터는 같은 경로 키를 참조해야 한다.
- 원자료, 기존 DOCX/PDF, 로컬 설정은 명시적 승인 없이 이동하거나 삭제하지 않는다.
- 역할 기반 워커 라벨과 압축된 워커 브리프를 사용한다.
- 생성된 점검/렌더 파일은 내구 산출물 경로가 지정되지 않은 한 `paths.tmp.root` 아래에 둔다.

## 훅 활성화 정책

- 자동 훅으로 거는 것은 보고서-분석 동기화 lag 점검 하나뿐이다. 점검기는 `paths.hooks.report_analysis_lag_check`(`scripts/hooks/report_analysis_lag_check.py`)이며 Codex와 Claude가 같은 스크립트·같은 `paths.config.report_analysis_lag` 설정을 공유한다.
- Claude는 `.claude/settings.local.json`의 `SubagentStop` 훅으로 등록한다. matcher는 `report-docx-manager`, `report-prose-writer`, `report-figure-generator`, `part1/2/3-analysis-manager`다. Claude `Stop` 훅은 matcher를 무시하므로, 보고서·분석 워커가 끝날 때만 발동시키려면 `SubagentStop`을 쓴다. Codex는 `/Users/ujunbin/.codex/hooks.json`에 전역 등록한다.
- 이 훅은 warning-only이며 fail-open이다. 스크립트나 설정이 없거나 프로젝트 밖 cwd면 `{"continue": true}`만 반환하고 워커를 막지 않는다. 훅은 파일 내용을 읽지 않고 경로명·타임스탬프·집계 수치만 출력한다.
- 나머지 규칙(tmp 경로 규율, 무단 원자료 삭제 금지, 증거 수준 프레이밍, privacy 경계)은 산문으로 강제하고, `project-verifier`와 분할된 검증 역할이 사후 확인한다. 도구 권한 게이트(allowed-tools, Bash allow 목록)가 1차 가드다.

## 보고서 앞부분 및 결과 서술

- 앞부분 2쪽에는 사용자가 작성한 Problem Statement를, 3쪽에는 Key Results Summary를 둔다. 두 쪽은 장 번호 체계와 분리한다.
- 사용자가 다른 언어를 명시하지 않는 한 앞부분은 영어로 작성한다.
- 결과 요약은 숫자 대시보드가 아니라 실질적 해석을 우선한다. 배수, ICC, p값, 행 수 같은 고립된 수치로 문단을 시작하지 않는다.
- 증거가 보여주는 내용을 먼저 쓴다. 자치구 차이는 차원별로 다르며, HLM 결과는 자치구 수준 조건과 개인 디지털 이용 사이의 일반적 관계를 통계적으로 의미 있게 지지하지 않는다. 개인 취약성이 디지털 이용 격차를 더 많이 설명한다. 플랫폼 텍스트와 Bayesian 업데이트는 탐색적 증거 통합 신호이지, 유병률 추정이나 인과 증명이 아니다.
- 수치는 발견을 문장으로 먼저 말한 뒤 보조 근거로만 사용한다.

## 활성 경로

구체 경로는 `config`의 프로젝트 경로 레지스트리에서 GitHub 상대 경로 값으로 해석한다.

- 활성 초안: `paths.docs.active_report_docx`
- 문헌 폴더: `paths.paper.literature`
- Part 1-3 저장소: `paths.analysis.part1.repo`, `paths.analysis.part2.repo`, `paths.analysis.part3.repo`
- 보고서 증거 서술 용어 사전: `paths.docs.evidence_terms`
- PPT 우선 원천증거 컴포넌트: `paths.docs.ppt_source_evidence`
- 보고서-분석 동기화 설정: `paths.config.report_analysis_lag`
