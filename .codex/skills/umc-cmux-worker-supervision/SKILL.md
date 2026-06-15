---
name: umc-cmux-worker-supervision
description: "UMC 프로젝트 작업을 cmux 워커 패널로 조율할 때 사용한다. 보고서, Part 1, Part 2, text preprocessing, git, 문서 검증 작업에서 리더가 워커 역할, 맥락, 산출물, 저장소 경계를 명확히 유지해야 할 때 적용한다."
---

# UMC cmux 워커 감독

이 스킬은 Codex 측 cmux 이벤트 감독, 워커 패널 배정표, Git 경계 점검에 초점을 둔다. Claude 측 대화형 워커 조율은 `umc-worker-orchestration`이 담당하며, 둘은 의도적으로 비대칭이다.

## 트리거

활성 루트가 UMC 프로젝트이고 다음 중 하나에 해당하면 이 스킬을 사용한다.

- 작업이 cmux 워커 패널로 나뉜다.
- 워커 패널의 이름 지정, 재지정, 갱신, 재배정이 필요하다.
- 보고서, DOCX, 그림, 표, 분석 산출물을 편집하거나 검증한다.
- Git 작업이 루트 UMC 저장소와 하나 이상의 중첩 분석 저장소에 걸친다.
- 임시 렌더, 백업, 보고서, 검증 산출물이 생성될 수 있다.

UMC 워커 조율과 무관한 작업이나 단일 명령 작업에는 사용하지 않는다.

## 첫 점검

1. 현재 루트가 설정된 UMC 프로젝트 루트인지 확인한다.
2. 워커에게 지시하기 전 live cmux layout을 확인한다.

```bash
cmux tree --workspace workspace:1
```

3. 편집이나 커밋 전 관련 Git 저장소를 확인한다.

```bash
git status --short --branch
git -C "$PART1_REPO" status --short --branch
git -C "$PART2_REPO" status --short --branch
git -C "$TEXT_PREPROCESSING_REPO" status --short --branch
```

4. 파일을 만들기 전 내구 산출물 위치를 정한다. 일회성 점검, 렌더, 백업에는 설정된 임시 출력 키를 사용한다.

## 경로 레지스트리

- 구체 파일은 `config`의 프로젝트 경로 레지스트리로 해석한다.
- 레지스트리 값은 루트 저장소 기준 GitHub 상대 경로다.
- 워커 브리프에는 가능하면 경로 키를 쓰고, 실행 시점에만 구체 경로로 해석한다.

## 워커 이름

기능적 역할 이름을 사용하고 장식적·성격 기반 이름을 쓰지 않는다.

권장 visible pane label:

- `보고서 DOCX 담당`
- `Part 1 분석 총괄`
- `Part 2 분석 총괄`
- `Part 3 분석 총괄`
- `Text preprocessing 담당`
- `Git/배포 담당`
- `검증 담당`

이름 변경:

```bash
cmux rename-tab --workspace workspace:1 --surface surface:<n> '<role label>'
```

변경 후 확인:

```bash
cmux tree --workspace workspace:1
```

## 기본 워커 배정

패널에 작업을 보내기 전 visible worker label을 명시적 agent name과 owning path에 매핑한다. surface ID는 달라질 수 있으므로, 역할 라벨과 agent name을 우선한다.

2026-05-28 기준 관측 배정이다. 실제 사용 전 live state를 다시 확인한다. leader surface는 배정 대상이 아니다.

| Visible worker label | Current surface | Assigned agent | Primary owning path | Primary skills/rules |
| --- | --- | --- | --- | --- |
| `검증 담당 · project-verifier` | `surface:1` | `project-verifier` | touched root or nested repo paths | read-only verification; findings first; no edits |
| `보고서 DOCX 담당 · report-docx-manager` | `surface:2` | `report-docx-manager` | `paths.docs.active_report_docx` | DOCX layout/execution, `umc-academic-table-formatting`, `umc-report-handoff`, `doc` |
| `방법론 설명 담당 · report-method-explainer` | 새 패널 배정 시 확인 | `report-method-explainer` | `paths.docs.active_report_docx`, Part 1/2/3 handoff | `umc-reader-first-method-writing`, `umc-report-handoff`, `umc-report-evidence-framing` |
| `증거 경계 담당 · report-evidence-boundary-editor` | 새 패널 배정 시 확인 | `report-evidence-boundary-editor` | report prose and interpretation sections | `umc-report-evidence-framing`, `umc-report-handoff` |
| `부록 큐레이션 담당 · report-appendix-curator` | 새 패널 배정 시 확인 | `report-appendix-curator` | appendix prompt/keyword/reproducibility surfaces | `umc-report-handoff`, `umc-report-commenting`, `umc-academic-table-formatting` |
| `독자 이해 검증 담당 · reader-comprehension-verifier` | 새 패널 배정 시 확인 | `reader-comprehension-verifier` | touched report sections/render pages | read-only, `umc-reader-first-method-writing`, findings first |
| `Part 3 분석 총괄 · part3-analysis-manager` | `surface:3` | `part3-analysis-manager` | `paths.analysis.part3.repo` | `umc-analysis-workflow`, `umc-report-evidence-framing`; no raw/private text or post IDs |
| `Part 1 분석 총괄 · part1-analysis-manager` | `surface:4` | `part1-analysis-manager` | `paths.analysis.part1.repo` | `umc-analysis-workflow`, `umc-report-handoff`; protect raw data and Part 1 nested repo boundary |
| `Part 2 분석 총괄 · part2-analysis-manager` | `surface:6` | `part2-analysis-manager` | `paths.analysis.part2.repo` | `umc-analysis-workflow`, `umc-report-evidence-framing`, `umc-report-handoff`; HLM as association analysis |

패널 이름을 바꿀 때는 worker label과 assigned agent를 함께 넣는다.

```bash
cmux rename-tab --workspace workspace:1 --surface surface:<n> '<worker label> · <agent-name>'
```

워커 브리프의 첫 줄은 배정을 다시 확인한다.

```text
[역할 지정] 이 패널의 담당 agent는 `<agent-name>`입니다.
```

보고서 DOCX 편집을 분석 에이전트에게 맡기지 않는다. 방법론 설명, 증거 경계, 부록 범위, DOCX layout, 독자 검증을 한 역할에 몰아주지 않는다. 원자료, 비공개 텍스트, 게시물 수준 검토를 보고서나 검증 워커에게 맡기지 않는다.

## 병렬 서브에이전트

사용자나 리더가 금지하지 않는 한, 배정된 워커 경계 안에서 독립적인 보조 점검에는 제한된 병렬 서브에이전트를 기본 허용한다.

규칙:

- 워커는 결과 통합과 최종 판단 책임을 유지한다.
- 병렬 하위 작업은 파일, 절, 스크립트, 산출물, 읽기 전용 증거 대상이 서로 분리되어야 한다.
- 원자료, 비공개 플랫폼 텍스트, 게시물 ID, 비밀값, `.env`, 로컬 설정을 서브에이전트 프롬프트에 보내지 않는다.
- 쓰기 작업은 각 서브에이전트의 소유 파일 경로나 모듈을 지정하고 다른 워커의 변경을 되돌리거나 덮어쓰지 못하게 한다.
- 검증 작업은 읽기 전용으로 두고 findings first 형식과 정확한 파일, 명령, 렌더 쪽을 요구한다.
- 어떤 서브에이전트를 썼고, 각자 무엇을 점검·변경했으며, 워커가 직접 무엇을 재검증했는지 보고한다.

## 워커 브리프

브리프는 제한적으로 보낸다. 긴 대화 이력을 붙여 넣지 않는다.

모든 워커 지시에는 다음을 포함한다.

- 현재 파일 키 또는 해석된 저장소 경로.
- 점검할 정확한 절, 표, 그림, 스크립트, 산출물.
- 범위 경계: read-only, edit allowed, report-only.
- 증거 출처: 파일 키, 표, 렌더 쪽, 로그, 명령 출력.
- 기대 반환 형식: 간결한 findings와 확인한 파일/절.
- 이 특정 작업에서 금지하지 않는 한 독립 보조 점검을 위한 제한된 병렬 서브에이전트 허용 문구.

워커가 오래된 context를 들고 있거나 context 압박이 크면 새 작업 전 짧은 상태 메모 저장 또는 context 정리를 지시한다.

`cmux send` 뒤에는 반드시 Enter를 보낸다.

```bash
cmux send --workspace workspace:1 --surface surface:<n> '<brief>'
cmux send-key --workspace workspace:1 --surface surface:<n> Enter
```

작업 착수 여부가 중요하면 화면을 다시 읽는다.

```bash
cmux read-screen --workspace workspace:1 --surface surface:<n> --lines 40
```

## 리더 루프

리더는 작업이 닫힐 때까지 워크플로 책임을 가진다.

1. 제한된 작업을 배정한다.
2. 워커가 지시를 받았는지 확인한다.
3. 완료를 모니터링한다.
4. 워커 결과를 읽고 충분성을 판단한다.
5. 중요한 주장은 가능한 범위에서 직접 검증한다.
6. 다음 제한 작업을 보내거나 대기 상태로 둔다.

위임을 완료로 취급하지 않는다. 워커 결과를 검토하고 중요한 주장을 확인한 뒤에만 사용자에게 보고한다.

보고서/DOCX 작업에서 리더는 오케스트레이터이자 검증자다.

- 관련 분석 워커에게 원천 truth, 결과 표, 프롬프트 파일, 파이프라인 단계를 확인시킨다.
- 분석 워커 증거가 DOCX comment, 각주, 표/그림 노트, 산문 지시, report-worker brief로 바뀌어야 하면 `$umc-report-handoff`를 사용한다.
- `보고서 DOCX 담당` 또는 `검증 담당`에게 렌더 쪽, 그림 배치, 캡션, 부록 표, 페이지네이션을 점검시킨다.
- 프롬프트를 "as-is" 또는 "verbatim"으로 넣으라는 요청이 있으면 요약 표로 대체하지 말고 원천 프롬프트 텍스트를 부록에 보존한다.
- 보고서 그림 안이나 바로 아래에 문장형 설명 푸터를 추가하지 않는다.

## Git 경계

- 파일을 소유한 저장소에서 커밋한다.
- 루트 저장소와 중첩 분석 저장소 변경을 섞어 하나의 커밋으로 만들지 않는다.
- 원자료, 비공개 플랫폼 텍스트, `.env`, 로컬 설정이 staging에 들어가지 않았는지 확인한다.
- push 전 `project-verifier` 또는 직접 읽기 전용 점검으로 staged 범위를 확인한다.
