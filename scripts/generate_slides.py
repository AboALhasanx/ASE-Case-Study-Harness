#!/usr/bin/env python3
"""Build an editable 16:9 ASE case-study presentation from JSON or Markdown.

Inputs are structured content, not evidence validation: authors remain responsible
for checking claims, citations, and slide density before presenting the deck.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Inches, Pt
except ImportError as exc:  # pragma: no cover - exercised by CLI users
    raise SystemExit("Missing dependency: install python-pptx (pip install python-pptx)") from exc


WIDTH, HEIGHT = 13.333, 7.5
INK = "172B3A"
MUTED = "526574"
ACCENT = "176B73"
PALE = "EAF2F1"
RULE = "D5E1E0"
WHITE = "FFFFFF"
FONT = "Aptos"


def color(value: str) -> RGBColor:
    value = value.lstrip("#")
    if not re.fullmatch(r"[0-9A-Fa-f]{6}", value):
        raise ValueError(f"Invalid color {value!r}; expected a six-digit hex value")
    return RGBColor.from_string(value.upper())


def _clean_lines(value: Any, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
        raise ValueError(f"{field} must be an array of strings")
    return [x.strip() for x in value if x.strip()]


def validate_deck(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("The input must be an object with title and slides fields")
    title = data.get("title")
    slides = data.get("slides")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Deck title is required")
    if len(title.strip()) > 70:
        raise ValueError("Deck title must be 70 characters or fewer")
    subtitle = str(data.get("subtitle", "")).strip()
    if len(subtitle) > 150:
        raise ValueError("Subtitle must be 150 characters or fewer")
    if not isinstance(slides, list) or not slides:
        raise ValueError("At least one content slide is required")
    cover_notes = data.get("cover_notes", "")
    if not isinstance(cover_notes, str) or len(cover_notes) > 4000:
        raise ValueError("cover_notes must be a string of at most 4,000 characters")
    result = {"title": title.strip(), "subtitle": subtitle, "cover_notes": cover_notes.strip(), "slides": []}
    for number, item in enumerate(slides, 1):
        if not isinstance(item, dict) or not isinstance(item.get("title"), str) or not item["title"].strip():
            raise ValueError(f"Slide {number} needs a non-empty title")
        if len(item["title"].strip()) > 55:
            raise ValueError(f"Slide {number}: title must be 55 characters or fewer")
        kind = str(item.get("layout", "content")).lower()
        if kind not in {"content", "section"}:
            raise ValueError(f"Slide {number}: layout must be 'content' or 'section'")
        body = item.get("body", "")
        if not isinstance(body, str):
            raise ValueError(f"Slide {number}: body must be a string")
        body = body.strip()
        if len(body) > 240:
            raise ValueError(f"Slide {number}: body must be 240 characters or fewer; split it across slides")
        bullets = _clean_lines(item.get("bullets"), f"Slide {number} bullets")
        if len(bullets) > 5:
            raise ValueError(f"Slide {number}: use at most five bullets")
        if any(len(b) > 220 for b in bullets):
            raise ValueError(f"Slide {number}: each bullet must be 220 characters or fewer")
        estimated_bullet_lines = sum(max(1, (len(b) + 77) // 78) for b in bullets)
        if estimated_bullet_lines > 7:
            raise ValueError(f"Slide {number}: bullet text is too dense; shorten it or split it across slides")
        citations = item.get("citations", [])
        if isinstance(citations, str):
            citations = [citations]
        if not isinstance(citations, list) or any(not isinstance(c, str) for c in citations):
            raise ValueError(f"Slide {number}: citations must be a string or array of strings")
        citations = [c.strip() for c in citations if c.strip()]
        if len(citations) > 6 or sum(map(len, citations)) > 350:
            raise ValueError(f"Slide {number}: citations exceed the visible footer capacity; use up to six concise references")
        notes = str(item.get("notes", "")).strip()
        if len(notes) > 4000:
            raise ValueError(f"Slide {number}: speaker notes must be 4,000 characters or fewer")
        result["slides"].append({
            "title": item["title"].strip(), "layout": kind,
            "section": str(item.get("section", "")).strip(), "body": body.strip(),
            "bullets": bullets,
            "citations": citations,
            "notes": notes,
        })
    return result


def parse_markdown(text: str) -> dict[str, Any]:
    """Parse simple Markdown: H1 deck title, H2 slides, bullets, citations/notes."""
    lines = text.replace("\r\n", "\n").split("\n")
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), "")
    if not title:
        raise ValueError("Markdown needs a top-level '# Deck title' heading")
    subtitle = ""
    slide_blocks: list[tuple[str, list[str]]] = []
    current_title = None
    current_lines: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if current_title is not None:
                slide_blocks.append((current_title, current_lines))
            current_title, current_lines = line[3:].strip(), []
        elif current_title is not None:
            current_lines.append(line)
        elif line.strip() and not line.startswith("# ") and not line.startswith("<!--"):
            subtitle = line.strip()
    if current_title is not None:
        slide_blocks.append((current_title, current_lines))
    slides = []
    for heading, block in slide_blocks:
        bullets, body, citations, notes = [], [], [], []
        target = body
        for raw in block:
            line = raw.strip()
            if line.lower() in {"notes:", "speaker notes:"}:
                target = notes
            elif line.lower() in {"citations:", "sources:"}:
                target = citations
            elif re.match(r"^[-*+]\s+", line) and target is body:
                bullets.append(re.sub(r"^[-*+]\s+", "", line))
            elif line:
                if target is citations:
                    citations.append(line.removeprefix("- "))
                else:
                    target.append(line)
        slides.append({"title": heading, "body": "\n".join(body), "bullets": bullets,
                       "citations": citations, "notes": "\n".join(notes)})
    return validate_deck({"title": title, "subtitle": subtitle, "slides": slides})


def add_text(slide, x, y, w, h, text, *, size, fill=INK, bold=False, font=FONT,
             align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, margin=0):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    p.space_after = Pt(0)
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color(fill)
    return box


def add_notes(slide, notes: str, citations: list[str]) -> None:
    content = notes
    if citations:
        source_text = "Sources shown on slide: " + "; ".join(citations)
        content = (content + "\n\n" if content else "") + source_text
    if not content:
        return
    try:
        frame = slide.notes_slide.notes_text_frame
        frame.text = content
        # Arabic presenter narration reads right-to-left. The notes remain
        # editable in PowerPoint; Latin source identifiers remain unchanged.
        for paragraph in frame.paragraphs:
            if re.search(r"[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]", paragraph.text):
                paragraph._p.get_or_add_pPr().set("rtl", "1")
    except (AttributeError, NotImplementedError) as exc:
        raise ValueError("Speaker notes cannot be embedded by this python-pptx version; preserve the separate presenter script and upgrade python-pptx") from exc


def build_presentation(data: dict[str, Any], output: Path) -> None:
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(WIDTH), Inches(HEIGHT)
    blank = prs.slide_layouts[6]

    cover = prs.slides.add_slide(blank)
    cover.background.fill.solid()
    cover.background.fill.fore_color.rgb = color(PALE)
    # The narrow band is a structural brand marker; all text remains editable.
    band = cover.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.18), Inches(HEIGHT))
    band.fill.solid(); band.fill.fore_color.rgb = color(ACCENT); band.line.fill.background()
    add_text(cover, 0.85, 1.55, 11.0, 1.9, data["title"], size=38, bold=True)
    if data["subtitle"]:
        add_text(cover, 0.9, 3.7, 10.8, 0.9, data["subtitle"], size=20, fill=MUTED)
    add_text(cover, 0.9, 6.63, 10.8, 0.34, "ADVANCED SOFTWARE ENGINEERING  /  CASE STUDY", size=10,
             fill=ACCENT, bold=True)
    add_notes(cover, data.get("cover_notes", ""), [])

    count = len(data["slides"])
    for index, item in enumerate(data["slides"], 1):
        slide = prs.slides.add_slide(blank)
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = color(WHITE)
        if item["layout"] == "section":
            slide.background.fill.fore_color.rgb = color(PALE)
        label = item["section"] or f"CASE STUDY  /  {index:02d}"
        add_text(slide, 0.68, 0.44, 11.8, 0.32, label.upper(), size=10, fill=ACCENT, bold=True)
        add_text(slide, 0.68, 0.92, 12.0, 0.8, item["title"], size=30, bold=True)
        rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.68), Inches(1.82), Inches(0.72), Inches(0.055))
        rule.fill.solid(); rule.fill.fore_color.rgb = color(ACCENT); rule.line.fill.background()

        y = 2.18
        if item["body"]:
            body_lines = max(1, (len(item["body"]) + 85) // 86)
            body_h = min(1.25, max(0.54, body_lines * 0.31))
            add_text(slide, 0.72, y, 11.9, body_h, item["body"], size=18, fill=MUTED)
            y += body_h + (0.12 if item["bullets"] else 0)
        bullets = item["bullets"]
        if bullets:
            avg_lines = sum(max(1, (len(b) + 77) // 78) for b in bullets)
            gap = 0.12
            unit = 0.31
            for bullet in bullets:
                line_count = max(1, (len(bullet) + 77) // 78)
                height = unit * line_count
                box = slide.shapes.add_textbox(Inches(0.86), Inches(y), Inches(11.72), Inches(height))
                tf = box.text_frame
                tf.clear(); tf.word_wrap = True
                tf.margin_left = Inches(0); tf.margin_right = Inches(0)
                p = tf.paragraphs[0]
                p.text = bullet
                p.level = 0
                p.font.name = FONT; p.font.size = Pt(18); p.font.color.rgb = color(INK)
                p.space_after = Pt(0)
                pPr = p._p.get_or_add_pPr()
                from pptx.oxml.xmlchemy import OxmlElement
                from pptx.oxml.ns import qn
                bullet_el = OxmlElement("a:buChar"); bullet_el.set("char", "•")
                pPr.append(bullet_el)
                y += height + gap
        if item["citations"]:
            cite_text = "Sources: " + "  |  ".join(item["citations"])
            line_count = max(1, (len(cite_text) + 155) // 156)
            footer_h = min(0.68, 0.22 * line_count + 0.06)
            divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.68), Inches(6.72-footer_h), Inches(11.98), Inches(0.012))
            divider.fill.solid(); divider.fill.fore_color.rgb = color(RULE); divider.line.fill.background()
            add_text(slide, 0.7, 6.76-footer_h, 11.8, footer_h, cite_text, size=10, fill=MUTED)
        add_text(slide, 12.1, 7.13, 0.5, 0.22, f"{index:02d}", size=10, fill=MUTED, align=PP_ALIGN.RIGHT)
        add_notes(slide, item["notes"], item["citations"])
    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(output)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input .json or .md content file")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Destination .pptx")
    parser.add_argument("--force", action="store_true", help="Replace an existing output file")
    args = parser.parse_args(argv)
    try:
        text = args.input.read_text(encoding="utf-8")
        data = validate_deck(json.loads(text)) if args.input.suffix.lower() == ".json" else parse_markdown(text)
        if args.input.resolve() == args.output.resolve():
            raise ValueError("Input and output paths must be different")
        if args.output.exists() and not args.force:
            raise ValueError(f"Output already exists: {args.output}; pass --force to replace it")
        build_presentation(data, args.output)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(f"Created {args.output} ({len(data['slides']) + 1} slides)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
