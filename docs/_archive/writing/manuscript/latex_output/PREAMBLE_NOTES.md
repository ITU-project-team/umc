# preamble.tex 설계 노트

UMC 디지털 연결성 분석 보고서용 LaTeX preamble의 설계 결정 요약. 변환·컴파일 작업자가 참고.

## 1. 엔진: 왜 XeLaTeX + kotex

- 한국어 본문 + 영문 인용/약어가 섞인 문서. pdfLaTeX는 한글 처리에 부적합.
- XeLaTeX은 시스템 OpenType 폰트 직접 사용 가능. macOS의 Apple SD Gothic Neo를 그대로 호출.
- LuaLaTeX도 후보이나 컴파일 속도와 표준 배포 호환성에서 XeLaTeX이 우위.
- `kotex`은 한국어 단어 끊기·문장부호 간격을 한국어 조판 규칙에 맞춰 처리.

## 2. 문서클래스 / 레이아웃

- `article` + `twocolumn` 10pt A4. 학회지 수준은 아니지만 학생 해커톤 학술 보고서이므로 2단으로 정보 밀도 확보.
- `geometry`: top 20mm / bottom 22mm / left·right 18mm / columnsep 6mm. 한글 본문에서 너무 빡빡하지 않은 균형.
- `setspace`의 `\setstretch{1.15}`로 한국어 가독성 보정. 한국어는 영문 기본 행간(1.0)이 좁게 느껴짐.

## 3. 폰트 전략

### 영문
- 본문: TeX Gyre Termes (Times 호환, serif). 학술 보고서 분위기.
- 제목·캡션: TeX Gyre Heros (Helvetica 호환, sans). titlesec·caption이 sans로 호출.
- 모노: TeX Gyre Cursor.
- TeX Gyre 계열은 TeX Live 표준 배포에 포함 → 어느 환경에서도 1차 fallback 보장.

### 한글 fallback 우선순위
1. **Apple SD Gothic Neo** (macOS 시스템 기본). 현재 활성화.
2. **Pretendard Variable**. 디자인 가이드 권고 1순위. 설치 후 주석 해제.
3. **Noto Serif/Sans CJK KR**. 크로스플랫폼 안전판.
4. **NanumMyeongjo / NanumGothic**. 한컴/리눅스 환경.

폰트 미설치 시 대응:
- macOS: `brew install --cask font-pretendard` (Pretendard) / `brew install --cask font-noto-sans-cjk-kr`
- Linux: `sudo apt install fonts-nanum fonts-noto-cjk` 후 `fc-cache -fv`
- Windows: NanumGothic·Pretendard 공식 페이지에서 ttf/otf 설치
- 폰트 변경 시 `preamble.tex` 상단 `\setmainhangulfont{...}` 한 줄만 교체.

## 4. 참고문헌: 왜 natbib + apalike

- 현재 References 섹션이 비정형 텍스트(단순 나열). 정식 `.bib` 파일이 아직 없음.
- biblatex(APA) + biber는 정식 `.bib` 엔트리와 별도 빌드 단계가 필수 → 초기 변환 비용 큼.
- natbib + apalike는:
  - 저자-연도 인용 (\citep, \citet) 지원
  - `.bbl`을 bibtex로 1회 생성 후 본문 직접 삽입도 가능
  - 향후 biblatex로 마이그레이션해도 인용 매크로 호환
- 추후 정식 `.bib` 생성 시 `bibliographystyle{apalike}` → `biblatex[style=apa,backend=biber]`로 1줄 교체 가능.

## 5. 색상 / 디자인 토큰

- `primary = #1A2332` (Deep Ocean Navy): 섹션 제목, 캡션 라벨, 본문 링크
- `accent  = #C97B3F` (Warm Terracotta): subsubsection, 핵심메시지 박스, 인용 링크
- `muted   = #5B6470`: 머리말 보조 텍스트
- `rule    = #D6D9DE`: 섹션 구분선
- `bgsoft  = #F5F2EC`: 박스 배경 (따뜻한 베이지)

WCAG AA 대비 충족. 흑백 인쇄 시에도 가독성 유지(색상은 의미 강조용, 정보 전달 단독 매체 아님).

## 6. 박스 환경 사용처

| 환경 | 용도 | 예시 |
|---|---|---|
| `metabox` | 이론적 배경, 개념 정의, 메타이론 노트 | "디지털 연결성의 다층적 정의 …" |
| `keymsg`  | 장/절 끝 핵심 결론 박스 | "강남·서초·송파 클러스터가 …" |
| `quoteblock` | 짧은 인용·요약 사이드바 | LLM 텍스트 분석 결과의 대표 인용 |

## 7. 그림·표 매크로

- `\fig{path}{caption}{label}`: 단(column) 폭. 일반 그림 21장 대부분에 사용.
- `\figfull{path}{caption}{label}`: 페이지 폭(figure*). 서울 지도, 다층모형 forest plot 등 가로 긴 시각화에.
- 표는 booktabs(`\toprule`/`\midrule`/`\bottomrule`)와 `tabularx` 조합 권장. 숫자 컬럼은 `siunitx`의 `S` 컬럼타입으로 소수점 정렬.

## 8. main.tex 구조 (권고)

```latex
\input{preamble}

\begin{document}
\twocolumn[
  \maketitle
  \begin{abstract}
    \noindent 본 보고서는 …
  \end{abstract}
  \vspace{1em}
]

\input{sections/ch1}
\input{sections/ch2}
\input{sections/ch3}
\input{sections/ch4}
\input{sections/ch5}

\bibliography{references}   % 정식 .bib 준비 후
% 또는 \input{sections/references} (수동 thebibliography 환경)

\end{document}
```

## 9. 컴파일 명령

표준 4-pass (참고문헌·교차참조 안정화):

```bash
cd /Users/ujunbin/project/umc/writing/manuscript/latex_output
xelatex -interaction=nonstopmode main.tex
bibtex main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

`latexmk` 사용 시:

```bash
latexmk -xelatex -interaction=nonstopmode main.tex
```

`.latexmkrc` 예시:

```perl
$pdf_mode = 5;          # xelatex
$xelatex = 'xelatex -interaction=nonstopmode -synctex=1 %O %S';
$bibtex_use = 2;
```

## 10. 향후 BibTeX 변환 가이드

현재 References 섹션이 자유 형식 텍스트 → 정식 `.bib`로 정리 필요.

권장 절차:
1. `raw_extract.md`의 References 블록을 `references.bib`로 분리
2. 각 엔트리를 BibTeX 포맷으로 수동 변환 (article / book / techreport / online)
3. 본문의 `(저자, 연도)` 표기는 `\citep{key}`로, "저자(연도)"는 `\citet{key}`로 일괄 치환
4. 변환 보조 도구: Zotero(자동 export), `anystyle` Ruby gem (텍스트 → BibTeX 추정), Google Scholar 개별 export
5. DOI/URL이 있는 항목은 `doi = {…}`, `url = {…}` 필드 추가 → hyperref가 자동 링크

엔트리 예시:

```bibtex
@article{kim2023digital,
  author  = {Kim, Y. and Park, S.},
  title   = {Digital Connectivity Across Seoul Districts},
  journal = {Urban Studies},
  year    = {2023},
  volume  = {60},
  number  = {4},
  pages   = {712--735},
  doi     = {10.1177/00420980231xxx}
}
```

## 11. 미지원/주의 사항

- `subfigure` 패키지(deprecated) 대신 `subcaption` 사용 → 본문에서 `\begin{subfigure}` 사용
- `\float`의 `[H]` 옵션은 가능한 한 자제. 2단 레이아웃에서 강제 배치 시 부동(float) 균형이 깨짐 → `[htbp]` 권장
- `figure*`(=`\figfull`)는 페이지 상단/하단에만 배치 가능. 위치 조절은 LaTeX float 알고리즘 신뢰 권고
- 한글 폰트가 `Script=Hangul` 옵션을 지원하지 않으면 해당 옵션 제거 후 컴파일
- `microtype`은 XeLaTeX에서 기능 일부만 작동(protrusion만 기본). 경고 무시 가능
