# UMC Codex 프로젝트 라우터

## 프로젝트 주제

An Integrated Methodology for Measuring Universal and Meaningful Connectivity (UMC) in a Hyper-Connected City

## 로컬 에이전트

- `report-docx-manager`: 보고서 DOCX 구조, 절 편집, 그림/표 배치, 레이아웃 위험을 담당한다.
- `report-figure-generator`: 보고서 그림 생성/수정, 원천 자료 확인, 학술적 스타일, DOCX 배치 검증을 담당한다.
- `part1-analysis-manager`: Part 1 UMC 지수 구축, 자치구 점수, 보고서용 그림/표, 3.1절 전달물을 담당한다.
- `part2-analysis-manager`: Part 2 HLM/다층모형 분석, 모형 산출물, 타당성 점검, 3.2절 전달물을 담당한다.
- `part3-analysis-manager`: Part 3 텍스트/Bayesian/추론 통합 워크플로와 데이터 경계 점검을 담당한다.
- `project-verifier`: 주장, 경로, Git 상태, 보호 대상 산출물 경계를 읽기 전용으로 검증한다.

각 워커의 담당 경계 안에서 서로 독립적인 보조 점검에는 제한된 병렬 서브에이전트를 사용할 수 있다. 워커 지시는 담당 주체를 명시해야 하며, 원자료, 비공개 플랫폼 텍스트, 게시물 ID, 비밀값, `.env`, 로컬 설정을 서브에이전트에 노출하면 안 된다.

## 프로젝트 규칙

- UMC 전용 Codex/Claude 스킬과 에이전트는 이 프로젝트 루트에 둔다.
- 중첩 분석 저장소는 좁은 실행 세부사항을 위해 자체 Claude 스킬과 에이전트를 둘 수 있다.
- 공유 프로젝트 설정은 `config`의 경로 레지스트리에 둔다. Codex와 Claude 라우터는 같은 경로 키를 참조해야 한다.
- 원자료, 기존 DOCX/PDF, 로컬 설정은 명시적 승인 없이 이동하거나 삭제하지 않는다.
- 역할 기반 워커 라벨과 압축된 워커 브리프를 사용한다.
- 생성된 점검/렌더 파일은 내구 산출물 경로가 지정되지 않은 한 `paths.tmp.root` 아래에 둔다.

## 활성 경로

구체 경로는 `config`의 프로젝트 경로 레지스트리에서 GitHub 상대 경로 값으로 해석한다.

- 활성 초안: `paths.docs.active_report_docx`
- 문헌 폴더: `paths.paper.literature`
- Part 1-3 저장소: `paths.analysis.part1.repo`, `paths.analysis.part2.repo`, `paths.analysis.part3.repo`
- 보고서 증거 서술 용어 사전: `paths.docs.evidence_terms`
- PPT 우선 원천증거 컴포넌트: `paths.docs.ppt_source_evidence`
- 보고서-분석 동기화 설정: `paths.config.report_analysis_lag`
