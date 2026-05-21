# UMC 보고서 LaTeX 빌드 가이드

서울 25개 자치구 디지털 연결성(UMC) 분석 보고서의 LaTeX 소스 트리.
원본 `UMC_report_kr_20260510_v2.docx` (1888 lines, 21 images)를 XeLaTeX + kotex 기반 2단 학술 보고서 스타일로 변환한 결과물.

## 디렉토리 구조

```
latex_output/
├── main.tex                  # 진입점. \input으로 preamble + sections 통합
├── preamble.tex              # XeLaTeX + kotex 패키지, 폰트, 색상, 박스 환경
├── sections/
│   ├── ch1_overview.tex      # 1장 개요 (1.1 이론적 이해, 1.2 분석 방법)
│   ├── ch2_theory.tex        # 2장 이론적 기반과 해석적 맥락
│   ├── ch3_analysis.tex      # 3장 분석 (UMC 측정 / HLM / LLM 텍스트 / 종합)
│   ├── ch4_policy.tex        # 4장 정책 제언
│   ├── ch5_conclusion.tex    # 5장 결론
│   └── references.tex        # 참고문헌 (thebibliography 환경)
├── media/                    # 그림 파일 (image1.png ~ image21.png/jpeg)
│   └── media/                # pandoc 추출 원본 (graphicspath로 둘 다 검색)
├── PREAMBLE_NOTES.md         # preamble 설계 의도 문서
├── STRUCTURE_REPORT.md       # 원본 docx 구조 분석 (변환 전 진단)
├── raw_extract.md            # pandoc으로 추출한 원본 마크다운 (참고용)
└── README.md                 # 이 문서
```

## 사전 요구 사항

### LaTeX 배포판
- **macOS**: MacTeX 2024+ 권장 (`brew install --cask mactex`)
- **Linux**: TeX Live 2024+ (`sudo apt install texlive-full texlive-xetex texlive-lang-korean`)
- 핵심 패키지: `kotex`, `fontspec`, `tcolorbox`, `booktabs`, `siunitx`, `natbib`, `hyperref`, `microtype`

### 한글 폰트
preamble은 macOS 시스템 폰트 `Apple SD Gothic Neo`를 기본으로 사용한다. 부재 시 대체:

| 우선순위 | 폰트 | 설치 명령 |
|---|---|---|
| 1 (macOS) | Apple SD Gothic Neo | 시스템 기본 |
| 2 | Pretendard | <https://github.com/orioncactus/pretendard> |
| 3 | Noto Sans/Serif CJK KR | `brew install --cask font-noto-sans-cjk-kr` |
| 4 | Nanum 시리즈 | `brew install --cask font-nanum-myeongjo` |

폰트 변경은 `preamble.tex` line 26~46의 `\setmainhangulfont` 부분을 수정한다. 주석으로 fallback 예시 포함.

## 컴파일

```bash
cd /Users/ujunbin/project/umc/writing/manuscript/latex_output

# 표준 4-pass (인용·교차참조·ToC 모두 해결)
xelatex -interaction=nonstopmode main.tex
bibtex main || true                # thebibliography 환경 사용 시 생략 가능
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

참고문헌을 `thebibliography` 환경(`references.tex`)으로 inline 정리했으므로 `bibtex` 단계는 선택적이다. 향후 `.bib` 파일로 분리하면 BibTeX 또는 biber 호출이 필수가 된다.

### latexmk 권장

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

## 알려진 이슈 / 작성자 보완 필요

원본 docx에서 이어받은 미완 항목. LaTeX 컴파일은 통과하나 콘텐츠 보강 필요:

| 위치 | 상태 | 보완 작업 |
|---|---|---|
| 본문 `\textbf{[인용 필요]}` 3건 (원본 L768, L1006, L1209) | 자리표시자 그대로 | 작성자가 적절한 인용 채우기 |
| image4 (그림 캡션 누락, ch2) | 추정 캡션 사용 | 작성자 검토 |
| image5 (그림 캡션 누락, ch2) | 추정 캡션 사용 | 작성자 검토 |
| 그림 번호 체계 (0-N 과 N 혼용) | LaTeX의 `\thefigure` 자동 번호로 통일됨 | 본문 cross-reference 검증 |
| 표 6 vs 표 7 본문 cross-ref | STRUCTURE_REPORT.md 표 인벤토리 참조 | 표 번호 일관성 검토 |
| image8 (Min-Max 수식 이미지) | LaTeX 수식 `\eqref{eq:minmax}`로 치환됨 | 추가 검토 불필요 |
| image20 (9.62in 폭 초과) | `\figfull` + `\textwidth`로 강제 축소 | 가독성 확인 |

## 변환 시 적용된 디자인 결정

1. **2단 학술 논문 레이아웃** (`twocolumn`, 10pt, A4): 데이터 핵 보고서의 밀도와 가독성을 균형. 큰 그림과 표는 `figure*`/`table*`로 페이지 폭 가로지르기.
2. **색상 토큰**: Deep Ocean Navy `#1A2332` (primary, 제목·링크), Warm Terracotta `#C97B3F` (accent, 인용·강조 박스).
3. **박스 환경 3종** (`tcolorbox`):
   - `quoteblock`: 챕터 표지 pull-quote
   - `metabox`: 메타이론/이론적 사이드바
   - `keymsg`: 핵심 메시지·정책 시사점 콜아웃
4. **참고문헌**: `natbib` (저자-연도, `apalike` 스타일). References가 비정형 텍스트라 BibTeX 외부 파일 대신 `thebibliography` inline 정리. 향후 `.bib` 변환 권장.
5. **헤더 오타 보정**: 원본의 6건 헤더 표기 오류(L17, L170, L417, L419, L682, L928) 모두 LaTeX 변환 시 보정. CHAPTER 5 라벨 누락도 보충.

## 추가 작업 가이드

### `.bib` 파일로 분리하기

`references.tex`의 각 `\bibitem`을 `references.bib`의 BibTeX 엔트리로 옮긴 뒤, `main.tex` 끝에서:

```latex
\bibliographystyle{apalike}
\bibliography{references}
```

으로 교체. `xelatex → bibtex → xelatex → xelatex` 사이클 필요.

### 단일 컬럼으로 전환

`preamble.tex` line 6의 `[10pt,a4paper,twocolumn]`에서 `twocolumn` 제거. 모든 `figure*`/`table*`도 `figure`/`table`로 변환.

### PDF 메타데이터 변경

`preamble.tex` line 192~197의 `\hypersetup`에서 `pdftitle`, `pdfauthor` 등 수정.

## 변환 파이프라인 기록

| 단계 | 도구 | 산출물 |
|---|---|---|
| 1. 추출 | pandoc 3.9.0.2 | `raw_extract.md` (1888 lines) + `media/media/*.png` (21개) |
| 2. 구조 분석 | 서브에이전트 A | `STRUCTURE_REPORT.md` (헤더·미디어·표·인용·위험 인벤토리) |
| 3. 템플릿 설계 | 서브에이전트 B | `preamble.tex`, `PREAMBLE_NOTES.md` |
| 4. 본문 변환 | 메인 + 서브에이전트 C/D 병렬 | `sections/ch1~ch5.tex`, `references.tex` |
| 5. 통합 | 메인 | `main.tex`, `README.md` |

원본: `/Users/ujunbin/project/umc/writing/manuscript/UMC_report_kr_20260510_v2.docx`
