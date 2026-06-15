---
name: umc-worker-orchestration
description: UMC cmux 워커를 조율한다. 역할 라벨, 압축 브리프, context reset, 결과 검토, 산출물 정리, Git 저장소 경계를 포함한다.
allowed-tools: Read, Bash
---

# UMC 워커 오케스트레이션

보이는 워커 패널로 UMC 작업을 나눌 때 사용한다. 이 스킬은 Claude 측 대화형 조율(역할 라벨, 압축 브리프, 결과 검토, context reset)에 초점을 둔다. Codex 측 cmux 이벤트 감독·배정표는 `umc-cmux-worker-supervision`이 담당하며, 둘은 의도적으로 비대칭이다.

## 절차

1. 워커 이름 지정이나 배정 전 현재 cmux layout을 확인한다.
2. `보고서 DOCX 담당`, `Part 1 분석 총괄`, `Part 2 분석 총괄`, `Part 3 분석 총괄`, `검증 담당` 같은 기능적 라벨을 사용한다.
3. 압축 브리프에는 다음을 넣는다.
   - 정확한 파일 또는 저장소 경로 키.
   - 대상 절, 표, 그림, 스크립트, 산출물.
   - 범위 경계: read-only, edit allowed, report-only.
   - 증거 출처.
   - 기대 반환 형식.
4. 워커 결과를 읽고 충분성을 판단하며, 중요한 주장은 가능한 범위에서 직접 검증한 뒤 다음 제한 지시를 보낸다.
5. 임시 렌더, 점검, 백업은 설정된 임시 출력 키 아래에 둔다.

## 경로 레지스트리

- 구체 파일은 `config`의 프로젝트 경로 레지스트리로 해석한다.
- 레지스트리 값은 루트 저장소 기준 GitHub 상대 경로다.
- 워커 브리프에는 가능하면 경로 키를 쓰고, 실행 시점에만 구체 경로로 해석한다.

## 기본 워커 배정

작업 배정 전 `cmux tree --workspace workspace:1`을 다시 확인한다. surface ID는 바뀔 수 있으므로 worker label과 agent name을 우선한다.

2026-05-28 기준 관측 배정이다. 실제 사용 전 live state를 다시 확인한다.

| Visible worker label | Current surface | Assigned agent | Owning path | Primary skills/rules |
| --- | --- | --- | --- | --- |
| `검증 담당 · project-verifier` | `surface:1` | `project-verifier` | touched root or nested repo paths | read-only verification; findings first |
| `보고서 DOCX 담당 · report-docx-manager` | `surface:2` | `report-docx-manager` | `paths.docs.active_report_docx` | DOCX layout/execution, `umc-academic-table-formatting`, `umc-report-handoff` |
| `방법론 설명 담당 · report-method-explainer` | 새 패널 배정 시 확인 | `report-method-explainer` | `paths.docs.active_report_docx`, Part 1/2/3 handoff | `umc-reader-first-method-writing`, `umc-report-handoff`, `umc-report-evidence-framing` |
| `증거 경계 담당 · report-evidence-boundary-editor` | 새 패널 배정 시 확인 | `report-evidence-boundary-editor` | report prose and interpretation sections | `umc-report-evidence-framing`, `umc-report-handoff` |
| `부록 큐레이션 담당 · report-appendix-curator` | 새 패널 배정 시 확인 | `report-appendix-curator` | appendix prompt/keyword/reproducibility surfaces | `umc-report-handoff`, `umc-report-commenting`, `umc-table-formatting` |
| `독자 이해 검증 담당 · reader-comprehension-verifier` | 새 패널 배정 시 확인 | `reader-comprehension-verifier` | touched report sections/render pages | read-only, `umc-reader-first-method-writing`, findings first |
| `Part 3 분석 총괄 · part3-analysis-manager` | `surface:3` | `part3-analysis-manager` | `paths.analysis.part3.repo` | `umc-analysis-workflow`, `umc-report-evidence-framing`; no raw/private text or post IDs |
| `Part 1 분석 총괄 · part1-analysis-manager` | `surface:4` | `part1-analysis-manager` | `paths.analysis.part1.repo` | `umc-analysis-workflow`, `umc-report-handoff`; protect raw data |
| `Part 2 분석 총괄 · part2-analysis-manager` | `surface:6` | `part2-analysis-manager` | `paths.analysis.part2.repo` | `umc-analysis-workflow`, `umc-report-evidence-framing`, `umc-report-handoff`; HLM as association analysis |

워커 브리프는 다음으로 시작한다.

```text
[역할 지정] 이 패널의 담당 agent는 `<agent-name>`입니다.
```

## 병렬 서브에이전트

리더가 금지하지 않는 한, 워커의 배정 경로와 범위 안에서 독립적인 보조 점검에는 제한된 병렬 서브에이전트를 기본 허용한다.

- 워커가 통합과 최종 판단을 책임진다.
- 파일, 절, 스크립트, 산출물, 읽기 전용 증거 대상이 분리될 때만 나눈다.
- 원자료, 비공개 플랫폼 텍스트, 게시물 ID, 비밀값, `.env`, 로컬 설정을 서브에이전트에 전달하지 않는다.
- 검증 서브에이전트는 읽기 전용으로 두고 정확한 파일이나 명령이 들어간 findings first 출력을 요구한다.
- 쓰기 하위 작업은 소유 파일 경로나 모듈을 지정하고 다른 워커 변경을 되돌리지 못하게 한다.
- 리더에게 돌아올 때 각 서브에이전트가 확인하거나 바꾼 내용을 보고한다.

## 보고서/DOCX 작업

- 관련 분석 워커에게 원천 파일, 결과 주장, 프롬프트 위치, 파이프라인 단계를 확인시킨다.
- 분석 워커 증거가 DOCX comment, 각주, 표 노트, 산문 지시, report-worker brief로 바뀌어야 하면 `umc-report-handoff`를 사용한다.
- `보고서 DOCX 담당` 또는 `검증 담당`에게 렌더 쪽, 그림 배치, 캡션, 부록 표, 페이지네이션을 점검시킨다.
- 중요한 파일 경로나 렌더 쪽을 직접 확인하기 전에는 워커 답변을 완료로 보지 않는다.
- 사용자가 프롬프트를 "as-is" 또는 "verbatim"으로 넣으라고 하면 요약 표가 아니라 원천 프롬프트 텍스트를 부록에 보존한다.
- 보고서 그림 내부나 그림 바로 아래에 문장형 설명 푸터를 추가하지 않는다.

## 경계

- 명시적 승인 없이 기존 사용자 파일을 삭제하거나 이동하지 않는다.
- 원자료, 비공개 플랫폼 텍스트, `.env`, 로컬 설정을 커밋하지 않는다.
- 변경 파일을 소유한 저장소에서 커밋한다.
