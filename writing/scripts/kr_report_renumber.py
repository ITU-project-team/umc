"""KR 보고서 docx의 figure/table 캡션·본문 cross-reference를 캐노니컬 한글 번호로 정리.

- 모든 캡션 단락의 3중 run 중복 정리
- Figure → 그림, Table → 표 한글 라벨 통일
- 본문 cross-reference 일괄 치환 (run 보존)
- 잉여 Figure 8 캡션 제거
- 결과 docx와 변경 로그 저장
"""
from __future__ import annotations

import csv
import re
import sys
from copy import deepcopy
from pathlib import Path

import docx
from docx.oxml.ns import qn

# canonical mapping by table_idx → "표 N. 제목"
TABLE_CAPTIONS: dict[int, str] = {
    1: "표 1. UMC 차원별 측정 지표",
    4: "표 2. 분석 변수 설명",
    5: "표 3. 주요 변수의 기술통계량",
    6: "표 4. HLM 추정 결과",
    7: "표 5. 텍스트 분석 표본 추출 및 판정 절차",
    8: "표 6. 3.3절의 분석 단위와 해석 단위",
    9: "표 7. 자치구별 게시글 판정 결과",
    10: "표 8. 결여 유형별 가설 생성 결과 분포",
}

# original caption-paragraph index -> canonical full caption text
# (we identify caption paragraphs by 3-run-duplicate pattern)
PARAGRAPH_CAPTIONS_BY_OLD: dict[int, str] = {
    24: "그림 1. 프로젝트 개괄",
    88: "그림 4. UMC 차원별 점수",
    92: "그림 5. UMC 수준의 공간적 자기상관 (서울 25개 자치구)",
    136: "그림 6. 분류와 추론의 역할 구분",
    153: "그림 7. LLM 기반 텍스트 분석 파이프라인",
    172: "그림 8. 지역별 사전-사후 분포 차이",
}

# paragraphs to delete (redundant duplicate captions)
PARAGRAPHS_TO_DELETE: set[int] = {170}  # Figure 8 duplicate caption (no image)

# table label paragraphs to overwrite (these are the existing
# "<Table N> ..." paragraphs that sit immediately above each table)
TABLE_LABEL_PARA_OVERRIDES: dict[int, str] = {
    71: "표 1. UMC 차원별 측정 지표",
    106: "표 2. 분석 변수 설명",
    115: "표 3. 주요 변수의 기술통계량",
    117: "표 4. HLM 추정 결과",
    132: "표 5. 텍스트 분석 표본 추출 및 판정 절차",
    146: "표 6. 3.3절의 분석 단위와 해석 단위",
    165: "표 7. 자치구별 게시글 판정 결과",
    176: "표 8. 결여 유형별 가설 생성 결과 분포",
}

# In-table caption rows (Figure 2, 3 inside t#2)
T2_FIGURE_LABELS: dict[tuple[int, int, int], str] = {
    (2, 1, 0): "그림 2. 자치구별 UMC 종합점수",
    (2, 1, 1): "그림 3. UMC 차원별 점수 히트맵",
}

# Figure number cross-ref routing in body text: old_num → new label
# (use both English and 한글 forms; we replace "Figure N", "figure N",
# "<Figure N>", "그림 N" all to "그림 NEW")
FIGURE_REROUTE: dict[int, int] = {
    1: 1,
    2: 2,  # if any body ref existed
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 7,  # duplicate caption, route to 7
    9: 8,
}

TABLE_REROUTE: dict[int, int] = {n: n for n in range(1, 9)}


def _new_run_xml(text: str) -> "OxmlElement":
    from docx.oxml import OxmlElement
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    r.append(t)
    return r


from lxml.etree import _Element as _LxmlElement


def _set_raw_text(desc, value):
    """Set lxml-level .text on element, bypassing any subclass override."""
    try:
        _LxmlElement.text.fset(desc, value)
    except Exception:
        pass


def _scrub_text_attrs(elem) -> None:
    """The original docx has stray .text values set on w:p and w:r elements
    (probably from a broken export tool). lxml's iter() picks up those text
    attributes, which doubles/triples the visible text. Clear them on every
    element except w:t (where text genuinely lives)."""
    for desc in elem.iter():
        tlocal = desc.tag.split("}", 1)[-1] if isinstance(desc.tag, str) else ""
        if tlocal == "t":
            continue
        _set_raw_text(desc, None)


def replace_paragraph_text(p_elem, new_text: str) -> None:
    """Replace all run text in p with a single run carrying new_text."""
    runs = p_elem.findall(qn("w:r"))
    if not runs:
        p_elem.append(_new_run_xml(new_text))
        _scrub_text_attrs(p_elem)
        return
    first = runs[0]
    ts = first.findall(qn("w:t"))
    if not ts:
        new_t = first.makeelement(qn("w:t"), {qn("xml:space"): "preserve"})
        new_t.text = new_text
        first.append(new_t)
    else:
        first_t = ts[0]
        first_t.text = new_text
        first_t.set(qn("xml:space"), "preserve")
        for t in ts[1:]:
            t.getparent().remove(t)
    for r in runs[1:]:
        r.getparent().remove(r)
    _scrub_text_attrs(p_elem)


def runs_text_offsets(p_elem):
    """Return list of (run_elem, t_elem, abs_start, abs_end, text) for each w:t in paragraph order.

    Pre-scrub stray .text on non-t elements (w:p, w:r etc.) so that the
    visible character offsets align with the actual w:t leaf content.
    """
    _scrub_text_attrs(p_elem)
    out = []
    pos = 0
    for r in p_elem.findall(qn("w:r")):
        for t in r.findall(qn("w:t")):
            text = t.text or ""
            out.append((r, t, pos, pos + len(text), text))
            pos += len(text)
    return out, pos


def replace_in_runs(p_elem, replacements: list[tuple[int, int, str]]) -> int:
    """Apply (start,end,replacement) replacements to paragraph, preserving runs.

    replacements use absolute character offsets across all w:t elements,
    must be sorted ascending and non-overlapping.
    Returns number of replacements applied.
    """
    if not replacements:
        return 0
    # build mapping from current state
    info, total = runs_text_offsets(p_elem)
    # apply from the end so earlier offsets remain valid
    count = 0
    for start, end, repl in sorted(replacements, key=lambda x: x[0], reverse=True):
        if start < 0 or end > total or start >= end:
            continue
        # find affected w:t elements
        affected = [(r, t, s, e, txt) for (r, t, s, e, txt) in info if not (e <= start or s >= end)]
        if not affected:
            continue
        # within first affected w:t: keep prefix [s..start), then replacement
        # within last affected w:t: keep suffix [end..e)
        first = affected[0]
        last = affected[-1]
        first_text = first[4]
        last_text = last[4]
        prefix = first_text[: start - first[2]]
        suffix = last_text[end - last[2] :]
        # set first w:t to prefix + replacement
        first[1].text = prefix + repl
        first[1].set(qn("xml:space"), "preserve")
        # set last w:t to suffix (only if different element)
        if last is not first:
            last[1].text = suffix
            last[1].set(qn("xml:space"), "preserve")
            # clear all middle w:t
            for mid in affected[1:-1]:
                mid[1].text = ""
        else:
            # both prefix and suffix go in the single w:t along with replacement
            first[1].text = prefix + repl + suffix
        count += 1
        # rebuild offsets for next iteration
        info, total = runs_text_offsets(p_elem)
    return count


def is_caption_paragraph(p_elem) -> bool:
    """Detect a caption-style paragraph (has Figure N or Table N or 그림 N or 표 N or <Table N>)."""
    text = "".join(p_elem.itertext()).strip()
    if not text:
        return False
    return bool(re.match(r"^\s*[\[<]?\s*(Figure|Fig\.|figure|그림|Table|table|표)\s*\d+", text))


# ---------- main pipeline ----------

def collect_body_items(doc) -> list[dict]:
    """Return ordered list of body items with paragraph and table indices."""
    out = []
    seq = 0
    p_idx = 0
    t_idx = 0
    for child in doc.element.body.iterchildren():
        tag = child.tag.split("}", 1)[-1]
        if tag == "p":
            out.append({"seq": seq, "kind": "p", "elem": child, "idx": p_idx})
            p_idx += 1
        elif tag == "tbl":
            out.append({"seq": seq, "kind": "tbl", "elem": child, "idx": t_idx})
            t_idx += 1
        seq += 1
    return out


def fix_caption_paragraphs(doc, log) -> None:
    items = collect_body_items(doc)
    for it in items:
        if it["kind"] != "p":
            continue
        idx = it["idx"]
        elem = it["elem"]
        # Figure caption overrides
        if idx in PARAGRAPH_CAPTIONS_BY_OLD:
            new_text = PARAGRAPH_CAPTIONS_BY_OLD[idx]
            old = "".join(elem.itertext()).strip()
            replace_paragraph_text(elem, new_text)
            log.append(("caption_fig", idx, old[:80], new_text))
            continue
        # Table label paragraph overrides (existing <Table N> labels)
        if idx in TABLE_LABEL_PARA_OVERRIDES:
            new_text = TABLE_LABEL_PARA_OVERRIDES[idx]
            old = "".join(elem.itertext()).strip()
            replace_paragraph_text(elem, new_text)
            log.append(("caption_tbl", idx, old[:80], new_text))
            continue


def insert_intable_figure_labels(doc, log) -> None:
    """Replace duplicated Figure 2/3 cell text inside t#2 with canonical Korean labels."""
    items = collect_body_items(doc)
    table_items = [it for it in items if it["kind"] == "tbl"]
    for ti in table_items:
        t_idx = ti["idx"]
        if t_idx != 2:
            continue
        rows = ti["elem"].findall(qn("w:tr"))
        for ri, tr in enumerate(rows):
            cells = tr.findall(qn("w:tc"))
            for ci, tc in enumerate(cells):
                key = (t_idx, ri, ci)
                if key in T2_FIGURE_LABELS:
                    new_text = T2_FIGURE_LABELS[key]
                    # replace text of all paragraphs inside the cell with one paragraph carrying new_text
                    paragraphs = tc.findall(qn("w:p"))
                    if not paragraphs:
                        continue
                    first_p = paragraphs[0]
                    old = "".join(first_p.itertext()).strip()
                    replace_paragraph_text(first_p, new_text)
                    for p in paragraphs[1:]:
                        # remove extra paragraphs (they are duplicate caption text)
                        ptxt = "".join(p.itertext()).strip()
                        if ptxt and ("Figure" in ptxt or "그림" in ptxt):
                            p.getparent().remove(p)
                    log.append(("caption_intable", f"t#{t_idx} r{ri} c{ci}", old[:80], new_text))


def delete_redundant_paragraphs(doc, log) -> None:
    items = collect_body_items(doc)
    for it in items:
        if it["kind"] == "p" and it["idx"] in PARAGRAPHS_TO_DELETE:
            text = "".join(it["elem"].itertext()).strip()[:80]
            it["elem"].getparent().remove(it["elem"])
            log.append(("deleted_paragraph", it["idx"], text, ""))


def reroute_cross_refs(doc, log) -> None:
    """Replace body-text Figure/Table references with canonical Korean labels."""
    items = collect_body_items(doc)
    # patterns
    fig_re = re.compile(r"<?\s*(Figure|Fig\.|figure|그림)\s*(\d+)\s*>?")
    tbl_re = re.compile(r"<?\s*(Table|table|표)\s*(\d+)\s*>?")
    # also handle obvious 3x duplicates like "Figure 4Figure 4Figure 4"
    # we apply replacements per paragraph

    # figure-caption paragraphs we already replaced; skip those
    skip_ids = set(PARAGRAPH_CAPTIONS_BY_OLD.keys()) | set(TABLE_LABEL_PARA_OVERRIDES.keys())

    def process_paragraph(p_elem, label_for_log: str):
        if not list(p_elem.findall(qn("w:r"))):
            return
        text = "".join(p_elem.itertext())
        if not text.strip():
            return
        replacements: list[tuple[int, int, str]] = []
        # collect figure refs
        for m in fig_re.finditer(text):
            old_num = int(m.group(2))
            if old_num not in FIGURE_REROUTE:
                continue
            new_num = FIGURE_REROUTE[old_num]
            replacements.append((m.start(), m.end(), f"그림 {new_num}"))
        for m in tbl_re.finditer(text):
            old_num = int(m.group(2))
            if old_num not in TABLE_REROUTE:
                continue
            new_num = TABLE_REROUTE[old_num]
            replacements.append((m.start(), m.end(), f"표 {new_num}"))
        # remove overlaps (table_re may match 표 N inside figure label; unlikely but defend)
        # sort by start
        replacements.sort(key=lambda x: x[0])
        cleaned: list[tuple[int, int, str]] = []
        for r in replacements:
            if cleaned and r[0] < cleaned[-1][1]:
                continue
            cleaned.append(r)
        if not cleaned:
            return
        n = replace_in_runs(p_elem, cleaned)
        if n:
            log.append(("xref", label_for_log, text[:120], "applied"))

    for it in items:
        if it["kind"] == "p":
            if it["idx"] in skip_ids:
                continue
            # avoid touching pure caption paragraphs that we have not whitelisted
            # (e.g., those starting with <Table or 표 even after our fix-up happen below)
            text = "".join(it["elem"].itertext()).strip()
            if re.match(r"^\s*[\[<]?\s*(Figure|Fig\.|figure|그림|Table|table|표)\s*\d+\s*[\]>]?\s*[\.:]?", text) and len(text) < 200:
                continue
            process_paragraph(it["elem"], f"p#{it['idx']}")
        elif it["kind"] == "tbl":
            for tr in it["elem"].findall(qn("w:tr")):
                for tc in tr.findall(qn("w:tc")):
                    for p in tc.findall(qn("w:p")):
                        # skip the figure label cells we already overwrote
                        text = "".join(p.itertext()).strip()
                        if text.startswith("그림 ") or text.startswith("표 "):
                            continue
                        process_paragraph(p, f"t#{it['idx']}-cell")


def apply_caption_style(doc) -> None:
    """Apply 'Caption' built-in style to all caption paragraphs we touched."""
    items = collect_body_items(doc)
    target_ids = set(PARAGRAPH_CAPTIONS_BY_OLD.keys()) | set(TABLE_LABEL_PARA_OVERRIDES.keys())
    for it in items:
        if it["kind"] != "p":
            continue
        if it["idx"] not in target_ids:
            continue
        elem = it["elem"]
        pPr = elem.find(qn("w:pPr"))
        if pPr is None:
            from docx.oxml import OxmlElement
            pPr = OxmlElement("w:pPr")
            elem.insert(0, pPr)
        # remove existing pStyle
        for ps in pPr.findall(qn("w:pStyle")):
            pPr.remove(ps)
        from docx.oxml import OxmlElement
        ps = OxmlElement("w:pStyle")
        ps.set(qn("w:val"), "Caption")
        pPr.insert(0, ps)


def main(argv: list[str]) -> int:
    if len(argv) < 4:
        print("usage: kr_report_renumber.py <input.docx> <output.docx> <log.csv>")
        return 2
    src = Path(argv[1])
    dst = Path(argv[2])
    log_path = Path(argv[3])
    dst.parent.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    doc = docx.Document(str(src))
    log: list[tuple[str, object, str, str]] = []

    # Global scrub — the source docx has stray .text on w:p / w:r elements
    # that lxml replays as duplicate text. Clear them everywhere first so
    # downstream regex-based work sees clean character positions.
    for p in doc.element.body.iter(qn("w:p")):
        _scrub_text_attrs(p)
    for tbl in doc.element.body.iter(qn("w:tbl")):
        _scrub_text_attrs(tbl)
    log.append(("global_scrub", "all_paragraphs", "stray .text cleared", ""))

    fix_caption_paragraphs(doc, log)
    insert_intable_figure_labels(doc, log)
    delete_redundant_paragraphs(doc, log)
    reroute_cross_refs(doc, log)
    apply_caption_style(doc)

    doc.save(str(dst))

    with log_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["op", "ref", "before", "after"])
        for row in log:
            w.writerow([str(c) for c in row])

    print(f"saved: {dst}")
    print(f"log:   {log_path}")
    print(f"ops:   {len(log)}")
    for tag in {r[0] for r in log}:
        n = sum(1 for r in log if r[0] == tag)
        print(f"  {tag}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
