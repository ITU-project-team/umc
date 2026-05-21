"""KR 보고서에 한국 정책연구원 양식의 디자인을 적용한다.

- A4 세로, 여백 28/25/25/22mm
- 본문 KoPubWorld Dotum Medium 10.5pt, 행간 17pt
- 헤딩 Pretendard (H1 22pt navy, H2 16pt navy, H3 13pt dark gray, H4 11.5pt gold)
- 컬러: navy #0E2A47, gold #B8860B, gray #4A5568
- 표 3선표 (navy 헤더, zebra striping)
- 표지·간지·헤더·푸터·페이지 번호
- 본문 2단 (snake column flow), 폭 큰 표 직전·직후로 1단 임시 전환
"""
from __future__ import annotations

import sys
from pathlib import Path

import docx
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt, RGBColor, Twips
from lxml.etree import _Element as _LxmlElement

# ---- design constants ----
NAVY = "0E2A47"
NAVY_DARK = "0A1F35"
GOLD = "B8860B"
TEAL = "2C7A7B"
TEXT_BLACK = "1A202C"
TEXT_GRAY = "4A5568"
TEXT_GRAY_LIGHT = "718096"
ZEBRA = "F4F6F8"
LIGHT_GRAY = "E2E8F0"

# Family name that fontconfig matches with the Latin-Hangul space and
# precomposed glyphs (avoids HarfBuzz/LibreOffice column-boundary bugs
# we observed with KoPubWorldDotum's jamo-decomposed glyphs).
# Single-file family that LibreOffice resolves cleanly on macOS.
BODY_FONT = "AppleGothic"
BODY_FONT_FALLBACK = "AppleGothic"
HEAD_FONT = "AppleGothic"
HEAD_FONT_FALLBACK = "AppleGothic"

# Every non-cover table is wrapped in a 1-col zone. With body text in
# 2-col flow and all tables/figures in 1-col, layout stays predictable.
WIDE_TABLE_INDICES = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

# tables that are figure containers (do NOT apply the 3-line table style;
# they hold images, not tabular data).
FIGURE_CONTAINER_INDICES = {0, 2, 3}  # cover title block, Figure 2/3 map pair, Figure 5 LISA grid

# tables that benefit from a smaller font size to fit the narrow column flow.
SMALL_FONT_TABLE_INDICES = {1, 4, 5, 6, 7, 9, 10}


# ---- helpers ----

def _set_raw_text(desc, value):
    try:
        _LxmlElement.text.fset(desc, value)
    except Exception:
        pass


def _scrub_text_attrs(elem) -> None:
    for desc in elem.iter():
        tlocal = desc.tag.split("}", 1)[-1] if isinstance(desc.tag, str) else ""
        if tlocal == "t":
            continue
        _set_raw_text(desc, None)


def _make(tag: str) -> OxmlElement:
    return OxmlElement(tag)


def _set_attr(elem, key: str, val: str) -> None:
    elem.set(qn(key), val)


def _ensure_pPr(p_elem):
    pPr = p_elem.find(qn("w:pPr"))
    if pPr is None:
        pPr = _make("w:pPr")
        p_elem.insert(0, pPr)
    return pPr


def _ensure_rPr_in_run(r_elem):
    rPr = r_elem.find(qn("w:rPr"))
    if rPr is None:
        rPr = _make("w:rPr")
        r_elem.insert(0, rPr)
    return rPr


# ---- style configuration ----

def _set_run_font(rPr, font_name: str, size_pt: float | None = None,
                  color_hex: str | None = None, bold: bool | None = None):
    # rFonts (also pin shaping hint to eastAsia so LibreOffice picks the
    # CJK shaper for Korean glyphs even within en-US lang runs)
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = _make("w:rFonts")
        rPr.insert(0, rFonts)
    for k in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(k), font_name)
    rFonts.set(qn("w:hint"), "eastAsia")
    # ensure w:lang declares Korean for eastAsia so the shaping path is CJK
    lang = rPr.find(qn("w:lang"))
    if lang is None:
        lang = _make("w:lang")
        rPr.append(lang)
    lang.set(qn("w:eastAsia"), "ko-KR")
    if not lang.get(qn("w:val")):
        lang.set(qn("w:val"), "ko-KR")
    if size_pt is not None:
        # w:sz is in half-points
        sz = rPr.find(qn("w:sz"))
        if sz is None:
            sz = _make("w:sz")
            rPr.append(sz)
        sz.set(qn("w:val"), str(int(size_pt * 2)))
        szCs = rPr.find(qn("w:szCs"))
        if szCs is None:
            szCs = _make("w:szCs")
            rPr.append(szCs)
        szCs.set(qn("w:val"), str(int(size_pt * 2)))
    if color_hex is not None:
        col = rPr.find(qn("w:color"))
        if col is None:
            col = _make("w:color")
            rPr.append(col)
        col.set(qn("w:val"), color_hex)
    if bold is True:
        b = rPr.find(qn("w:b"))
        if b is None:
            b = _make("w:b")
            rPr.append(b)
        bCs = rPr.find(qn("w:bCs"))
        if bCs is None:
            bCs = _make("w:bCs")
            rPr.append(bCs)
    elif bold is False:
        for tag in ("w:b", "w:bCs"):
            for el in rPr.findall(qn(tag)):
                rPr.remove(el)


def _set_paragraph_spacing(pPr, line_240ths: int = 320,
                           before_pt: float | None = None,
                           after_pt: float | None = None,
                           line_rule: str = "auto"):
    spacing = pPr.find(qn("w:spacing"))
    if spacing is None:
        spacing = _make("w:spacing")
        pPr.append(spacing)
    if before_pt is not None:
        spacing.set(qn("w:before"), str(int(before_pt * 20)))
    if after_pt is not None:
        spacing.set(qn("w:after"), str(int(after_pt * 20)))
    spacing.set(qn("w:line"), str(line_240ths))
    spacing.set(qn("w:lineRule"), line_rule)


def force_run_fonts(doc) -> None:
    """Override every w:r's rFonts with our body font, and every heading's
    runs with our heading font. Style-level definitions are not always
    honored when the source docx has direct run-level font overrides.

    Also enforce paragraph line spacing so KoPubWorldDotum's tall metrics
    do not collide between rows when font size is reduced.
    """
    body = doc.element.body
    HEAD_STYLES = {"Heading1", "Heading2", "Heading3", "Heading4",
                   "1", "2", "3", "4",
                   "Heading 1", "Heading 2", "Heading 3", "Heading 4",
                   "Title", "Subtitle"}
    for p in body.iter(qn("w:p")):
        pPr = p.find(qn("w:pPr"))
        is_heading = False
        is_caption = False
        if pPr is not None:
            ps = pPr.find(qn("w:pStyle"))
            if ps is not None:
                sid = ps.get(qn("w:val"))
                if sid in HEAD_STYLES:
                    is_heading = True
                if sid == "Caption":
                    is_caption = True
        # apply paragraph-level line spacing (use exact at-least so the
        # body font's line-height is fixed and rows do not crash)
        if not is_heading and not is_caption:
            pPr_w = _ensure_pPr(p)
            sp = pPr_w.find(qn("w:spacing"))
            if sp is None:
                sp = _make("w:spacing")
                pPr_w.append(sp)
            sp.set(qn("w:line"), "360")  # 18pt at lineRule=auto = ~1.5x
            sp.set(qn("w:lineRule"), "auto")
            # small space-after to separate paragraphs
            sp.set(qn("w:after"), "60")
            sp.set(qn("w:before"), "0")
        for r in p.findall(qn("w:r")):
            rPr = _ensure_rPr_in_run(r)
            for rf in rPr.findall(qn("w:rFonts")):
                rPr.remove(rf)
            for tag in ("w:sz", "w:szCs"):
                for el in rPr.findall(qn(tag)):
                    rPr.remove(el)
            if not is_heading and not is_caption:
                for c in rPr.findall(qn("w:color")):
                    rPr.remove(c)
                # also remove any character-level spacing/kern that might
                # have leaked from the source
                for tag in ("w:spacing", "w:kern", "w:position"):
                    for el in rPr.findall(qn(tag)):
                        rPr.remove(el)
            if is_heading:
                _set_run_font(rPr, HEAD_FONT, size_pt=None,
                              color_hex=None, bold=None)
            elif is_caption:
                _set_run_font(rPr, HEAD_FONT, size_pt=10,
                              color_hex=NAVY, bold=True)
            else:
                _set_run_font(rPr, BODY_FONT, size_pt=10.5,
                              color_hex=TEXT_BLACK, bold=False)


def configure_styles(doc) -> None:
    styles_root = doc.styles.element
    # iterate all styles
    for style in doc.styles:
        # we only update text styles
        try:
            xml = style.element
        except AttributeError:
            continue
        tag = xml.tag.split("}", 1)[-1]
        if tag != "style":
            continue
        sid = xml.get(qn("w:styleId"))
        if sid is None:
            continue
        rPr = xml.find(qn("w:rPr"))
        pPr = xml.find(qn("w:pPr"))
        if sid in ("Normal", "Default", "DefaultParagraphFont"):
            if rPr is None:
                rPr = _make("w:rPr")
                xml.append(rPr)
            _set_run_font(rPr, BODY_FONT_FALLBACK, size_pt=10.5,
                          color_hex=TEXT_BLACK, bold=False)
            if pPr is None:
                pPr = _make("w:pPr")
                xml.insert(0, pPr)
            _set_paragraph_spacing(pPr, line_240ths=336, before_pt=0, after_pt=4)
        elif sid in ("Heading1", "1", "Heading 1"):
            if rPr is None:
                rPr = _make("w:rPr")
                xml.append(rPr)
            _set_run_font(rPr, HEAD_FONT_FALLBACK, size_pt=22,
                          color_hex=NAVY, bold=True)
            if pPr is None:
                pPr = _make("w:pPr")
                xml.insert(0, pPr)
            _set_paragraph_spacing(pPr, line_240ths=320, before_pt=24, after_pt=12)
        elif sid in ("Heading2", "2", "Heading 2"):
            if rPr is None:
                rPr = _make("w:rPr")
                xml.append(rPr)
            _set_run_font(rPr, HEAD_FONT_FALLBACK, size_pt=16,
                          color_hex=NAVY, bold=True)
            if pPr is None:
                pPr = _make("w:pPr")
                xml.insert(0, pPr)
            _set_paragraph_spacing(pPr, line_240ths=300, before_pt=18, after_pt=8)
        elif sid in ("Heading3", "3", "Heading 3"):
            if rPr is None:
                rPr = _make("w:rPr")
                xml.append(rPr)
            _set_run_font(rPr, HEAD_FONT_FALLBACK, size_pt=13,
                          color_hex="2D3748", bold=True)
            if pPr is None:
                pPr = _make("w:pPr")
                xml.insert(0, pPr)
            _set_paragraph_spacing(pPr, line_240ths=300, before_pt=12, after_pt=4)
        elif sid in ("Heading4", "4", "Heading 4"):
            if rPr is None:
                rPr = _make("w:rPr")
                xml.append(rPr)
            _set_run_font(rPr, HEAD_FONT_FALLBACK, size_pt=11.5,
                          color_hex=GOLD, bold=True)
            if pPr is None:
                pPr = _make("w:pPr")
                xml.insert(0, pPr)
            _set_paragraph_spacing(pPr, line_240ths=300, before_pt=10, after_pt=4)
        elif sid in ("Caption",):
            if rPr is None:
                rPr = _make("w:rPr")
                xml.append(rPr)
            _set_run_font(rPr, HEAD_FONT_FALLBACK, size_pt=10,
                          color_hex=NAVY, bold=True)
            if pPr is None:
                pPr = _make("w:pPr")
                xml.insert(0, pPr)
            _set_paragraph_spacing(pPr, line_240ths=300, before_pt=8, after_pt=6)
            # center
            jc = pPr.find(qn("w:jc"))
            if jc is None:
                jc = _make("w:jc")
                pPr.append(jc)
            jc.set(qn("w:val"), "center")
            # keep with next so caption stays attached to its figure
            keepNext = pPr.find(qn("w:keepNext"))
            if keepNext is None:
                keepNext = _make("w:keepNext")
                pPr.append(keepNext)


# ---- page setup ----

def _twips_from_mm(mm: float) -> int:
    return int(mm / 25.4 * 1440)


def configure_sections(doc) -> None:
    """Set every section to A4 portrait with the standard margins.

    Insert continuous section breaks to switch between 1-col and 2-col
    around wide tables. The body section becomes 2-col by default.
    """
    A4_W = _twips_from_mm(210)
    A4_H = _twips_from_mm(297)
    margins = dict(
        top=_twips_from_mm(28),
        bottom=_twips_from_mm(25),
        left=_twips_from_mm(25),
        right=_twips_from_mm(22),
        header=_twips_from_mm(15),
        footer=_twips_from_mm(15),
    )
    for sec_idx, sec in enumerate(doc.sections):
        sectPr = sec._sectPr
        # page size
        pgSz = sectPr.find(qn("w:pgSz"))
        if pgSz is None:
            pgSz = _make("w:pgSz")
            sectPr.append(pgSz)
        # Force portrait A4 for the cover (sec_idx==0) and any plain body
        # section. Keep landscape only for sections that explicitly hold
        # wide tables — but since we are committing to single-column
        # layout, even those should be portrait now.
        pgSz.set(qn("w:w"), str(A4_W))
        pgSz.set(qn("w:h"), str(A4_H))
        if qn("w:orient") in pgSz.attrib:
            del pgSz.attrib[qn("w:orient")]
        # margins
        pgMar = sectPr.find(qn("w:pgMar"))
        if pgMar is None:
            pgMar = _make("w:pgMar")
            sectPr.append(pgMar)
        pgMar.set(qn("w:top"), str(margins["top"]))
        pgMar.set(qn("w:right"), str(margins["right"]))
        pgMar.set(qn("w:bottom"), str(margins["bottom"]))
        pgMar.set(qn("w:left"), str(margins["left"]))
        pgMar.set(qn("w:header"), str(margins["header"]))
        pgMar.set(qn("w:footer"), str(margins["footer"]))


def _set_section_columns(sectPr, num: int = 2, space_twips: int = 453,
                         separator: bool = False) -> None:
    """Set column count and explicit column widths.

    LibreOffice does not always honor pure equalWidth + num=2; we set
    equalWidth=0 and provide explicit <w:col w:w=... w:space=...> for
    each column so the renderer flows text into both columns.
    """
    cols = sectPr.find(qn("w:cols"))
    if cols is None:
        cols = _make("w:cols")
        sectPr.append(cols)
    # remove any prior child cols
    for child in list(cols):
        cols.remove(child)
    cols.set(qn("w:num"), str(num))
    cols.set(qn("w:space"), str(space_twips))
    if separator:
        cols.set(qn("w:sep"), "1")
    else:
        cols.attrib.pop(qn("w:sep"), None)
    if num <= 1:
        cols.set(qn("w:equalWidth"), "1")
        return
    # compute body width from page size and margins on this section
    pgSz = sectPr.find(qn("w:pgSz"))
    pgMar = sectPr.find(qn("w:pgMar"))
    if pgSz is None or pgMar is None:
        cols.set(qn("w:equalWidth"), "1")
        return
    page_w = int(pgSz.get(qn("w:w"), "11905"))
    left = int(pgMar.get(qn("w:left"), "1417"))
    right = int(pgMar.get(qn("w:right"), "1247"))
    body_w = page_w - left - right
    each = (body_w - space_twips * (num - 1)) // num
    cols.set(qn("w:equalWidth"), "0")
    for i in range(num):
        c = _make("w:col")
        c.set(qn("w:w"), str(each))
        if i < num - 1:
            c.set(qn("w:space"), str(space_twips))
        cols.append(c)


def _is_caption_paragraph(p_elem) -> bool:
    pPr = p_elem.find(qn("w:pPr"))
    if pPr is None:
        return False
    ps = pPr.find(qn("w:pStyle"))
    if ps is None:
        return False
    return ps.get(qn("w:val")) == "Caption"


_WRAP_MARKER = "umc-wrap"


_WRAP_MARKER_ATTR = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}umcWrap"


def _mark_break(p_elem, num_cols: int) -> None:
    """Tag a section-break paragraph with a custom attribute so we can
    later force its column count without confusing it with breaks the
    source docx originally contained."""
    pPr = p_elem.find(qn("w:pPr"))
    if pPr is None:
        return
    sp = pPr.find(qn("w:sectPr"))
    if sp is None:
        return
    # use the w: namespace so docx serializer keeps the attribute
    sp.set(_WRAP_MARKER_ATTR, str(num_cols))


def _wrap_wide_table_in_one_col(tbl_elem) -> None:
    """Insert continuous 1-col section break before tbl (and any
    immediately preceding caption), and a 2-col break after the next
    paragraph (which may be the table's caption-after-figure)."""
    parent = tbl_elem.getparent()
    siblings = list(parent.iterchildren())
    idx = siblings.index(tbl_elem)
    start_idx = idx
    for j in range(idx - 1, -1, -1):
        s = siblings[j]
        if s.tag.endswith("}p"):
            text = "".join(t.text or "" for t in s.iter(qn("w:t"))).strip()
            if text == "" or _is_caption_paragraph(s):
                start_idx = j
                continue
        break
    end_idx = idx
    if idx + 1 < len(siblings):
        nxt = siblings[idx + 1]
        if nxt.tag.endswith("}p") and _is_caption_paragraph(nxt):
            end_idx = idx + 1
    before = _make_section_break_paragraph(num_cols=1)
    _mark_break(before, 1)
    siblings[start_idx].addprevious(before)
    after = _make_section_break_paragraph(num_cols=2)
    _mark_break(after, 2)
    parent.insert(list(parent).index(siblings[end_idx]) + 1, after)


def _remove_all_inline_section_breaks(body) -> None:
    """Strip every inline section break paragraph (a paragraph whose only
    purpose is the embedded sectPr). This is idempotent so the script can
    be re-run without compounding leftover breaks from previous runs."""
    to_remove = []
    for p in body.findall(qn("w:p")):
        pPr = p.find(qn("w:pPr"))
        if pPr is None:
            continue
        sp = pPr.find(qn("w:sectPr"))
        if sp is None:
            continue
        # only remove if paragraph has no real text content
        text = "".join(t.text or "" for t in p.iter(qn("w:t"))).strip()
        if text:
            continue
        to_remove.append(p)
    for p in to_remove:
        p.getparent().remove(p)


def apply_two_column_layout(doc) -> None:
    """Convert main body sections to 2-column flow with snake-column flow.

    Wide tables and figure-container tables get wrapped in 1-col zones
    so they can use full width; caption paragraphs travel with the table
    so they do not orphan into the 2-col stream.
    """
    body = doc.element.body
    # Strip any leftover inline section breaks (those were the 2-col snake
    # column flow attempt). We are committing to a single-column body for
    # stability and Korean-policy-report convention.
    _remove_all_inline_section_breaks(body)
    # Force every section to a single column for layout stability.
    for sec in doc.sections:
        _set_section_columns(sec._sectPr, num=1, space_twips=453)


def _make_section_break_paragraph(num_cols: int = 2,
                                  space_twips: int = 453) -> _LxmlElement:
    """Build a paragraph element that carries an inline continuous sectPr."""
    p = _make("w:p")
    pPr = _make("w:pPr")
    p.append(pPr)
    sectPr = _make("w:sectPr")
    pPr.append(sectPr)
    typeEl = _make("w:type")
    typeEl.set(qn("w:val"), "continuous")
    sectPr.append(typeEl)
    cols = _make("w:cols")
    cols.set(qn("w:num"), str(num_cols))
    cols.set(qn("w:space"), str(space_twips))
    sectPr.append(cols)
    return p


# ---- 3-line tables ----

def style_tables(doc) -> None:
    body = doc.element.body
    # build map: tbl element -> table_idx in body order (top-level only)
    table_idx_map: dict = {}
    table_idx = 0
    for child in body.iterchildren():
        tag = child.tag.split("}", 1)[-1]
        if tag == "tbl":
            table_idx_map[id(child)] = table_idx
            table_idx += 1
    # iterate top-level tables only (skip nested tables)
    for tbl in [c for c in body.iterchildren() if c.tag.endswith("}tbl")]:
        rows = tbl.findall(qn("w:tr"))
        if not rows:
            continue
        idx = table_idx_map.get(id(tbl), -1)
        # Pin table width to 100% of body width (single-column layout).
        tblPr_pre = tbl.find(qn("w:tblPr"))
        if tblPr_pre is None:
            tblPr_pre = _make("w:tblPr")
            tbl.insert(0, tblPr_pre)
        for tw in tblPr_pre.findall(qn("w:tblW")):
            tblPr_pre.remove(tw)
        tblW = _make("w:tblW")
        tblW.set(qn("w:w"), "5000")  # 100% in pct units
        tblW.set(qn("w:type"), "pct")
        tblPr_pre.append(tblW)
        for tl in tblPr_pre.findall(qn("w:tblLayout")):
            tblPr_pre.remove(tl)
        layout = _make("w:tblLayout")
        layout.set(qn("w:type"), "autofit")
        tblPr_pre.append(layout)
        # Remove any explicit cell widths so layout=autofit can recompute.
        for tr in rows:
            for tc in tr.findall(qn("w:tc")):
                tcPr = tc.find(qn("w:tcPr"))
                if tcPr is None:
                    continue
                for tcW in tcPr.findall(qn("w:tcW")):
                    tcPr.remove(tcW)
        if idx in FIGURE_CONTAINER_INDICES:
            # figure container: keep transparent, no borders, no shading
            tblPr = tbl.find(qn("w:tblPr"))
            if tblPr is None:
                tblPr = _make("w:tblPr")
                tbl.insert(0, tblPr)
            for tb in tblPr.findall(qn("w:tblBorders")):
                tblPr.remove(tb)
            tblBorders = _make("w:tblBorders")
            for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
                b = _make(f"w:{side}")
                b.set(qn("w:val"), "nil")
                tblBorders.append(b)
            tblPr.append(tblBorders)
            for tr in rows:
                for tc in tr.findall(qn("w:tc")):
                    tcPr = tc.find(qn("w:tcPr"))
                    if tcPr is None:
                        tcPr = _make("w:tcPr")
                        tc.insert(0, tcPr)
                    for sh in tcPr.findall(qn("w:shd")):
                        tcPr.remove(sh)
                    # remove inner cell borders too
                    for tb in tcPr.findall(qn("w:tcBorders")):
                        tcPr.remove(tb)
                    tcBorders = _make("w:tcBorders")
                    for side in ("top", "left", "bottom", "right"):
                        b = _make(f"w:{side}")
                        b.set(qn("w:val"), "nil")
                        tcBorders.append(b)
                    tcPr.append(tcBorders)
            continue
        # set table-level borders to 3-line
        tblPr = tbl.find(qn("w:tblPr"))
        if tblPr is None:
            tblPr = _make("w:tblPr")
            tbl.insert(0, tblPr)
        # remove existing tblBorders
        for tb in tblPr.findall(qn("w:tblBorders")):
            tblPr.remove(tb)
        tblBorders = _make("w:tblBorders")
        tblPr.append(tblBorders)
        # top / bottom navy
        for side, sz in (("top", 12), ("bottom", 8)):
            b = _make(f"w:{side}")
            b.set(qn("w:val"), "single")
            b.set(qn("w:sz"), str(sz))
            b.set(qn("w:space"), "0")
            b.set(qn("w:color"), NAVY)
            tblBorders.append(b)
        for side in ("left", "right", "insideV"):
            b = _make(f"w:{side}")
            b.set(qn("w:val"), "nil")
            tblBorders.append(b)
        # insideH 0.5pt navy
        b = _make("w:insideH")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), NAVY)
        tblBorders.append(b)

        # zebra + header styling
        for ri, tr in enumerate(rows):
            cells = tr.findall(qn("w:tc"))
            for tc in cells:
                tcPr = tc.find(qn("w:tcPr"))
                if tcPr is None:
                    tcPr = _make("w:tcPr")
                    tc.insert(0, tcPr)
                # remove old shading
                for sh in tcPr.findall(qn("w:shd")):
                    tcPr.remove(sh)
                shd = _make("w:shd")
                shd.set(qn("w:val"), "clear")
                shd.set(qn("w:color"), "auto")
                if ri == 0:
                    shd.set(qn("w:fill"), NAVY)
                elif ri % 2 == 1:
                    shd.set(qn("w:fill"), ZEBRA)
                else:
                    shd.set(qn("w:fill"), "FFFFFF")
                tcPr.append(shd)
                # apply font color/weight per cell
                cell_font_size = 9.5 if idx in SMALL_FONT_TABLE_INDICES else 10
                for p in tc.findall(qn("w:p")):
                    for r in p.findall(qn("w:r")):
                        rPr = _ensure_rPr_in_run(r)
                        if ri == 0:
                            _set_run_font(rPr, HEAD_FONT_FALLBACK, size_pt=cell_font_size,
                                          color_hex="FFFFFF", bold=True)
                        else:
                            _set_run_font(rPr, BODY_FONT_FALLBACK, size_pt=cell_font_size,
                                          color_hex=TEXT_BLACK, bold=False)


# ---- header / footer ----

def add_headers_footers(doc) -> None:
    """For each section: add header (left=report name, right=chapter via PAGE field),
    footer with PAGE number on outer side."""
    for si, sec in enumerate(doc.sections):
        sec.different_first_page_header_footer = False
        # header
        header = sec.header
        # clear existing header paragraphs
        hdr_elem = header._element
        for p in hdr_elem.findall(qn("w:p")):
            hdr_elem.remove(p)
        new_p = _make("w:p")
        pPr = _make("w:pPr")
        new_p.append(pPr)
        # bottom border 0.5pt navy
        pBdr = _make("w:pBdr")
        bot = _make("w:bottom")
        bot.set(qn("w:val"), "single")
        bot.set(qn("w:sz"), "4")
        bot.set(qn("w:space"), "1")
        bot.set(qn("w:color"), NAVY)
        pBdr.append(bot)
        pPr.append(pBdr)
        r = _make("w:r")
        rPr = _make("w:rPr")
        r.append(rPr)
        _set_run_font(rPr, HEAD_FONT_FALLBACK, size_pt=8.5, color_hex=TEXT_GRAY_LIGHT)
        t = _make("w:t")
        t.text = "ITU UMC Data Hackathon 2026 · 서울 디지털 격차 분석"
        t.set(qn("xml:space"), "preserve")
        r.append(t)
        new_p.append(r)
        hdr_elem.append(new_p)

        # footer (centered page number)
        footer = sec.footer
        ftr_elem = footer._element
        for p in ftr_elem.findall(qn("w:p")):
            ftr_elem.remove(p)
        new_p = _make("w:p")
        pPr = _make("w:pPr")
        jc = _make("w:jc")
        jc.set(qn("w:val"), "center")
        pPr.append(jc)
        new_p.append(pPr)
        # PAGE field
        r1 = _make("w:r")
        rPr1 = _make("w:rPr")
        r1.append(rPr1)
        _set_run_font(rPr1, HEAD_FONT_FALLBACK, size_pt=9, color_hex=TEXT_GRAY)
        fldChar1 = _make("w:fldChar")
        fldChar1.set(qn("w:fldCharType"), "begin")
        r1.append(fldChar1)
        new_p.append(r1)

        r2 = _make("w:r")
        rPr2 = _make("w:rPr")
        r2.append(rPr2)
        _set_run_font(rPr2, HEAD_FONT_FALLBACK, size_pt=9, color_hex=TEXT_GRAY)
        instrText = _make("w:instrText")
        instrText.text = " PAGE   \\* MERGEFORMAT "
        instrText.set(qn("xml:space"), "preserve")
        r2.append(instrText)
        new_p.append(r2)

        r3 = _make("w:r")
        rPr3 = _make("w:rPr")
        r3.append(rPr3)
        _set_run_font(rPr3, HEAD_FONT_FALLBACK, size_pt=9, color_hex=TEXT_GRAY)
        fldChar3 = _make("w:fldChar")
        fldChar3.set(qn("w:fldCharType"), "end")
        r3.append(fldChar3)
        new_p.append(r3)

        ftr_elem.append(new_p)


# ---- cover page ----

def upgrade_cover(doc) -> None:
    """The original cover is t#0 (a 1x1 table containing the title).
    Upgrade by setting cell shading to navy and styling text as cover title.
    """
    body = doc.element.body
    tables = body.findall(qn("w:tbl"))
    if not tables:
        return
    cover = tables[0]
    # apply cell shading to first cell
    rows = cover.findall(qn("w:tr"))
    if not rows:
        return
    cells = rows[0].findall(qn("w:tc"))
    if not cells:
        return
    tc = cells[0]
    # set cell shading
    tcPr = tc.find(qn("w:tcPr"))
    if tcPr is None:
        tcPr = _make("w:tcPr")
        tc.insert(0, tcPr)
    for sh in tcPr.findall(qn("w:shd")):
        tcPr.remove(sh)
    shd = _make("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), NAVY)
    tcPr.append(shd)
    # remove vertical alignment etc.
    # style every paragraph inside cover cell
    for p in tc.findall(qn("w:p")):
        # center
        pPr = _ensure_pPr(p)
        jc = pPr.find(qn("w:jc"))
        if jc is None:
            jc = _make("w:jc")
            pPr.append(jc)
        jc.set(qn("w:val"), "center")
        for r in p.findall(qn("w:r")):
            rPr = _ensure_rPr_in_run(r)
            text = "".join((t.text or "") for t in r.findall(qn("w:t")))
            size = 28 if "Bridging" in text or "디지털" in text else 14
            color = "FFFFFF"
            _set_run_font(rPr, HEAD_FONT_FALLBACK, size_pt=size,
                          color_hex=color, bold=True)
    # remove cell borders inside cover cell (we use shading only)
    tcBorders = tcPr.find(qn("w:tcBorders"))
    if tcBorders is not None:
        tcPr.remove(tcBorders)
    tcBorders = _make("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        b = _make(f"w:{side}")
        b.set(qn("w:val"), "nil")
        tcBorders.append(b)
    tcPr.append(tcBorders)
    # also clear table borders
    tblPr = cover.find(qn("w:tblPr"))
    if tblPr is None:
        tblPr = _make("w:tblPr")
        cover.insert(0, tblPr)
    for tb in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(tb)
    tblBorders = _make("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = _make(f"w:{side}")
        b.set(qn("w:val"), "nil")
        tblBorders.append(b)
    tblPr.append(tblBorders)


# ---- main ----

def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: kr_report_redesign.py <input.docx> <output.docx>")
        return 2
    src = Path(argv[1])
    dst = Path(argv[2])
    dst.parent.mkdir(parents=True, exist_ok=True)

    doc = docx.Document(str(src))
    # global scrub once more in case redesign output is independent
    for p in doc.element.body.iter(qn("w:p")):
        _scrub_text_attrs(p)

    configure_styles(doc)
    force_run_fonts(doc)
    configure_sections(doc)
    apply_two_column_layout(doc)
    style_tables(doc)
    add_headers_footers(doc)
    upgrade_cover(doc)

    doc.save(str(dst))
    print(f"saved: {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
