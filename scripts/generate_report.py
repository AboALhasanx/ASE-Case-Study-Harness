#!/usr/bin/env python3
"""Convert an academic case-study Markdown report to a formatted DOCX.

Supported Markdown: headings, paragraphs, emphasis, inline code, links, lists,
fenced code blocks, standalone local images, and simple pipe tables. This
intentionally avoids pretending to be a full CommonMark implementation.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

try:
    from docx import Document
    from docx.image.image import Image
    from docx.enum.section import WD_SECTION
    from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor
except ImportError:
    print("Missing dependency: python-docx. Install it with `python -m pip install python-docx`. ", file=sys.stderr)
    raise SystemExit(2)


def shade(cell, fill: str) -> None:
    properties = cell._tc.get_or_add_tcPr()
    element = OxmlElement("w:shd")
    element.set(qn("w:fill"), fill)
    properties.append(element)


def set_cell_borders(table) -> None:
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        item = OxmlElement(f"w:{edge}")
        item.set(qn("w:val"), "single")
        item.set(qn("w:sz"), "4")
        item.set(qn("w:color"), "B8C2CC")
        borders.append(item)
    table._tbl.tblPr.append(borders)


def add_page_field(paragraph) -> None:
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar"); begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText"); instruction.set(qn("xml:space"), "preserve"); instruction.text = " PAGE "
    separate = OxmlElement("w:fldChar"); separate.set(qn("w:fldCharType"), "separate")
    value = OxmlElement("w:t"); value.text = "1"
    end = OxmlElement("w:fldChar"); end.set(qn("w:fldCharType"), "end")
    for element in (begin, instruction, separate, value, end):
        run._r.append(element)


INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*]+\*|`[^`]+`|\[[^\]]+\]\([^)]+\))")
IMAGE_LINE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def add_inline(paragraph, text: str) -> None:
    position = 0
    for match in INLINE.finditer(text):
        if match.start() > position:
            paragraph.add_run(text[position:match.start()])
        token = match.group(0)
        if token.startswith("**"):
            run = paragraph.add_run(token[2:-2]); run.bold = True
        elif token.startswith("*"):
            run = paragraph.add_run(token[1:-1]); run.italic = True
        elif token.startswith("`"):
            run = paragraph.add_run(token[1:-1]); run.font.name = "Consolas"; run.font.size = Pt(9)
        else:
            label, url = re.match(r"\[([^\]]+)\]\(([^)]+)\)", token).groups()
            add_hyperlink(paragraph, label, url)
        position = match.end()
    if position < len(text):
        paragraph.add_run(text[position:])


def add_hyperlink(paragraph, label: str, url: str) -> None:
    rel = paragraph.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    link = OxmlElement("w:hyperlink"); link.set(qn("r:id"), rel)
    run = OxmlElement("w:r"); props = OxmlElement("w:rPr")
    color = OxmlElement("w:color"); color.set(qn("w:val"), "1F4E79"); props.append(color)
    underline = OxmlElement("w:u"); underline.set(qn("w:val"), "single"); props.append(underline)
    run.append(props); text = OxmlElement("w:t"); text.text = label; run.append(text); link.append(run)
    paragraph._p.append(link)


def pipe_cells(line: str) -> list[str]:
    """Split an outer-pipe table row without splitting escaped pipe characters.

    Markdown escapes ``\\|`` and ``\\\\`` are decoded while scanning so odd and
    even runs of backslashes before a pipe retain their intended meaning.
    """
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    cells: list[str] = []
    cell: list[str] = []
    last_was_separator = False
    i = 0
    while i < len(text):
        char = text[i]
        if char == "\\" and i + 1 < len(text) and text[i + 1] in "\\|":
            cell.append(text[i + 1])
            i += 2
            last_was_separator = False
            continue
        if char == "|":
            cells.append("".join(cell).strip())
            cell = []
            last_was_separator = True
        else:
            cell.append(char)
            last_was_separator = False
        i += 1
    if not last_was_separator:
        cells.append("".join(cell).strip())
    return cells


def is_separator(line: str) -> bool:
    cells = pipe_cells(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells)


def local_image(match: re.Match, base: Path, number: int) -> Path:
    """Resolve an image within the report directory without network access."""
    raw_path = match.group(2).strip()
    parsed = urlsplit(raw_path)
    candidate = Path(raw_path)
    if (parsed.scheme or parsed.netloc or candidate.is_absolute() or
            raw_path.startswith(("/", "\\"))):
        raise ValueError(f"line {number}: image must be a local path relative to the report directory")
    root = base.resolve()
    image_path = (root / candidate).resolve()
    if not image_path.is_relative_to(root):
        raise ValueError(f"line {number}: image must remain inside the report directory")
    if not image_path.is_file():
        raise ValueError(f"line {number}: image not found: {raw_path}")
    try:
        Image.from_file(str(image_path))
    except Exception as error:
        raise ValueError(f"line {number}: unsupported or unreadable image: {raw_path}") from error
    return image_path


def validate_markdown(lines: list[str], base: Path) -> None:
    """Reject constructs the deliberately small reader cannot represent safely."""
    in_fence = False
    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if "![" in line:
            image = IMAGE_LINE.fullmatch(stripped)
            if not image:
                raise ValueError(f"line {number}: images must use a standalone ![caption](relative/path) line")
            local_image(image, base, number)
        if re.search(r"\[\^[^\]]+\](?::)?", line):
            raise ValueError(f"line {number}: Markdown footnotes are unsupported; use an inline citation or add the footnote in Word after conversion")
        if re.match(r"^\s{2,}[-*+]\s+|^\s{2,}\d+[.)]\s+", line):
            raise ValueError(f"line {number}: nested lists are unsupported; flatten the list before generating DOCX")
        if re.match(r"^\s*>+", line):
            raise ValueError(f"line {number}: block quotes are unsupported; rewrite as a paragraph before generating DOCX")
        if re.search(r"<\/?[A-Za-z][^>]*>", line):
            raise ValueError(f"line {number}: embedded HTML is unsupported; use plain Markdown before generating DOCX")
        if stripped.startswith("|") and number < len(lines) and lines[number].strip().startswith("|") and is_separator(lines[number]):
            if any(":" in cell for cell in pipe_cells(lines[number])):
                raise ValueError(f"line {number + 1}: aligned pipe tables are unsupported; use a plain separator row")
            expected = len(pipe_cells(line))
            actual = len(pipe_cells(lines[number]))
            if actual != expected:
                raise ValueError(f"line {number + 1}: table separator has {actual} cells; expected {expected} from header")
            row_index = number + 1
            while row_index < len(lines) and lines[row_index].strip().startswith("|"):
                actual = len(pipe_cells(lines[row_index]))
                if actual != expected:
                    raise ValueError(f"line {row_index + 1}: table row has {actual} cells; expected {expected} from header")
                row_index += 1


def add_table(document, rows: list[list[str]]) -> None:
    if not rows:
        return
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("table rows do not match the header width")
    table = document.add_table(rows=len(rows), cols=width)
    table.autofit = True
    table.style = "Table Grid"
    set_cell_borders(table)
    for r, row in enumerate(rows):
        for c in range(width):
            cell = table.cell(r, c); cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cell.text = ""
            p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(3); p.paragraph_format.space_before = Pt(3)
            add_inline(p, row[c] if c < len(row) else "")
            for run in p.runs:
                run.font.size = Pt(9)
                if r == 0:
                    run.bold = True; run.font.color.rgb = RGBColor(255, 255, 255)
            if r == 0:
                shade(cell, "1F4E79")
    table.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    document.add_paragraph().paragraph_format.space_after = Pt(1)


def configure(document, title: str) -> None:
    section = document.sections[0]
    section.top_margin = Inches(.8); section.bottom_margin = Inches(.75)
    section.left_margin = Inches(.9); section.right_margin = Inches(.9)
    styles = document.styles
    normal = styles["Normal"]; normal.font.name = "Cambria"; normal.font.size = Pt(11); normal.font.color.rgb = RGBColor(35, 39, 43)
    normal.paragraph_format.line_spacing = 1.15; normal.paragraph_format.space_after = Pt(7)
    for name, size in (("Title", 24), ("Heading 1", 16), ("Heading 2", 13), ("Heading 3", 11)):
        style = styles[name]; style.font.name = "Cambria"; style.font.size = Pt(size); style.font.bold = True; style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.keep_with_next = True
    styles["Title"].paragraph_format.space_after = Pt(12)
    styles["Heading 1"].paragraph_format.space_before = Pt(17); styles["Heading 1"].paragraph_format.space_after = Pt(6)
    styles["Heading 2"].paragraph_format.space_before = Pt(12); styles["Heading 2"].paragraph_format.space_after = Pt(4)
    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = header.add_run(title); run.font.name = "Cambria"; run.font.size = Pt(8); run.font.color.rgb = RGBColor(90, 98, 105)
    footer = section.footer.paragraphs[0]; footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rr = footer.add_run("Advanced Software Engineering Case Study  ·  "); rr.font.size = Pt(8); rr.font.color.rgb = RGBColor(90, 98, 105)
    add_page_field(footer)


def add_local_image(document, path: Path, caption: str) -> None:
    """Insert the image within the page bounds and preserve its aspect ratio."""
    section = document.sections[-1]
    max_width = section.page_width - section.left_margin - section.right_margin
    # Leave room for a caption and the paragraph spacing on the same page.
    max_height = min(Inches(6.0), section.page_height - section.top_margin - section.bottom_margin - Inches(0.8))
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.keep_with_next = bool(caption)
    shape = paragraph.add_run().add_picture(str(path))
    factor = min(1.0, max_width / shape.width, max_height / shape.height)
    if factor < 1:
        shape.width = int(shape.width * factor)
        shape.height = int(shape.height * factor)
    # Text alternatives remain present even if the user removes the caption.
    shape._inline.docPr.set("descr", caption)
    if caption:
        text = document.add_paragraph(style="Caption")
        text.alignment = WD_ALIGN_PARAGRAPH.CENTER
        text.add_run(caption)


def convert(source: Path, output: Path) -> None:
    lines = source.read_text(encoding="utf-8-sig").splitlines()
    validate_markdown(lines, source.parent)
    first_title = next((m.group(1).strip() for line in lines if (m := re.match(r"^#\s+(.+)$", line))), source.stem.replace("-", " "))
    doc = Document(); configure(doc, first_title)
    i = 0; paragraph_lines: list[str] = []
    def flush() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            p = doc.add_paragraph(); add_inline(p, " ".join(part.strip() for part in paragraph_lines))
            paragraph_lines = []
    while i < len(lines):
        line = lines[i]; stripped = line.strip()
        if not stripped:
            flush(); i += 1; continue
        image = IMAGE_LINE.fullmatch(stripped)
        if image:
            flush()
            add_local_image(doc, local_image(image, source.parent, i + 1), image.group(1))
            i += 1
            continue
        if stripped.startswith("```"):
            flush(); i += 1; code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i]); i += 1
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Inches(.25); p.paragraph_format.space_after = Pt(7)
            for n, code_line in enumerate(code):
                if n: p.add_run().add_break()
                r = p.add_run(code_line); r.font.name = "Consolas"; r.font.size = Pt(8.5)
            i += 1; continue
        if stripped.startswith("|") and i + 1 < len(lines) and lines[i + 1].strip().startswith("|") and is_separator(lines[i + 1]):
            flush(); rows = [pipe_cells(stripped)]; i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(pipe_cells(lines[i])); i += 1
            add_table(doc, rows); continue
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", stripped)
        if heading:
            flush(); level = len(heading.group(1)); p = doc.add_paragraph(style="Title" if level == 1 and not any(x.style.name == "Title" for x in doc.paragraphs) else f"Heading {min(level, 3)}")
            add_inline(p, heading.group(2)); i += 1; continue
        bullet = re.match(r"^\s*[-*+]\s+(.+)$", line)
        numbered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if bullet or numbered:
            flush(); style = "List Bullet" if bullet else "List Number"; p = doc.add_paragraph(style=style); add_inline(p, (bullet or numbered).group(1)); i += 1; continue
        paragraph_lines.append(stripped); i += 1
    flush()
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a polished academic DOCX from a Markdown case-study report.")
    parser.add_argument("input", type=Path, help="Markdown report path")
    parser.add_argument("--output", "-o", type=Path, help="DOCX destination (default: input path with .docx extension)")
    parser.add_argument("--force", action="store_true", help="replace an existing output file")
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"input file does not exist: {args.input}")
    output = args.output or args.input.with_suffix(".docx")
    if output.resolve() == args.input.resolve():
        parser.error("output must not overwrite the Markdown input")
    if output.exists() and not args.force:
        parser.error(f"output already exists: {output} (pass --force to replace it)")
    try:
        convert(args.input, output)
    except ValueError as error:
        parser.error(str(error))
    print(f"Created {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
