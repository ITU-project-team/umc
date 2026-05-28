---
name: umc-report-theory
description: 설정된 활성 DOCX와 문헌 출처 폴더를 사용해 UMC 보고서 2장 이론적 배경을 검토하거나 초안 작성할 때 사용한다.
allowed-tools: Read, Bash
---

# UMC 보고서 이론

2장 이론적 배경과 문헌 통합에 사용한다.

## 활성 입력

구체 파일은 `config`의 프로젝트 경로 레지스트리로 해석한다.

- 활성 초안: `paths.docs.active_report_docx`
- 문헌 폴더: `paths.paper.literature`
- 보고서 증거 서술 용어 사전: `paths.docs.evidence_terms`
- 현재 이론 대상:
  - `2.1 Universal Meaningful Connectivity`
  - `2.2.4 Bayesian Framework` 또는 이에 해당하는 Bayesian-updating 절
  - UMC dimensions와 보고서 장 전반의 용어 일관성

## 워크플로

1. DOCX에서 현재 2장 구조를 추출한다.
2. 작성 전 설정된 문헌 폴더의 사용 가능한 문헌을 확인한다.
3. 절별 gap을 식별한다.
   - UMC 정의와 차원 framework 누락.
   - people-based, place-based, place-sensitive 접근과 정책 이론 정렬.
   - 측정 지표와 텍스트 증거 사이의 bridge로서 Bayesian 업데이트.
   - 서울 맥락과 제도 배경.
4. 보고서 언어에 맞춘 간결한 학술 문장을 작성한다.
5. 인용은 사람이 읽을 수 있게 유지하고 placeholder token을 남기지 않는다.
6. 명시적 편집 지시 없이 활성 DOCX를 덮어쓰지 않는다.

## 출력

편집 없이 보고할 때는 다음을 반환한다.

- 보강이 필요한 절.
- 제안 thesis.
- 근거 또는 인용 후보.
- 차원명 불일치나 heading 오탈자 같은 정확한 wording risk.
