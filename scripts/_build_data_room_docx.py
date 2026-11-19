"""Convierte los documentos markdown de docs/sello_plan/data_room/ a .docx con
identidad de marca IM Music (Bahnschrift violeta / Georgia), con una advertencia
legal destacada en rojo al inicio de cada documento."""
import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "docs" / "sello_plan" / "data_room"

VIOLETA = RGBColor(0x5E, 0x17, 0xEB)
ROJO = RGBColor(0xB0, 0x20, 0x20)
NEGRO = RGBColor(0x00, 0x00, 0x00)
GRIS_TEXTO = RGBColor(0x22, 0x22, 0x22)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)

HEADING_FONT = "Bahnschrift"
BODY_FONT = "Georgia"

DOCS = [
    ("01_estatutos_im_music.md", "Estatutos_IM_Music_SAS.docx"),
    ("02_contrato_artista.md", "Contrato_de_Artista_IM_Music.docx"),
    ("03_split_composicion.md", "Split_de_Composicion_IM_Music.docx"),
    ("04_autorizacion_imagen_voz.md", "Autorizacion_Uso_Imagen_y_Voz_IM_Music.docx"),
    ("05_contrato_prestacion_servicios.md", "Contrato_Prestacion_de_Servicios_IM_Music.docx"),
    ("06_contrato_alianza_estrategica.md", "Contrato_Alianza_Estrategica_IM_Music.docx"),
]


def set_cell_background(cell, hex_color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    cell._tc.get_or_add_tcPr().append(shd)


def style_heading(p, text, size, color, font=HEADING_FONT, space_before=18, space_after=8, align_center=False):
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.color.rgb = color
    r.font.name = font
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if align_center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return p


def add_inline_runs(paragraph, text, base_size=11, base_color=GRIS_TEXTO, italic=False):
    parts = re.split(r"(\*\*.*?\*\*)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            r = paragraph.add_run(part[2:-2])
            r.bold = True
            r.font.color.rgb = VIOLETA
        else:
            r = paragraph.add_run(part)
            r.font.color.rgb = base_color
        r.font.name = BODY_FONT
        r.font.size = Pt(base_size)
        r.italic = italic


def add_table_from_lines(doc, lines):
    rows = [l.strip() for l in lines if l.strip().startswith("|")]
    rows = [r for r in rows if not re.match(r"^\|[\s\-:|]+\|$", r)]
    data = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
    if not data:
        return
    n_cols = len(data[0])
    table = doc.add_table(rows=0, cols=n_cols)
    table.style = "Light Grid Accent 1"
    for i, row in enumerate(data):
        cells = table.add_row().cells
        for j, val in enumerate(row):
            if j >= n_cols:
                continue
            cells[j].text = ""
            p = cells[j].paragraphs[0]
            r = p.add_run(re.sub(r"\*\*", "", val))
            r.font.size = Pt(9.5)
            r.font.name = BODY_FONT
            if i == 0:
                r.bold = True
                r.font.color.rgb = BLANCO
                set_cell_background(cells[j], "5E17EB")
            else:
                r.font.color.rgb = GRIS_TEXTO
    doc.add_paragraph()


def add_disclaimer_box(doc, lines):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(14)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), "FDEAEA")
    p._p.get_or_add_pPr().append(shd)
    pbdr = OxmlElement("w:pBdr")
    for edge in ("top", "left", "bottom", "right"):
        b = OxmlElement(f"w:{edge}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "12")
        b.set(qn("w:color"), "B02020")
        pbdr.append(b)
    p._p.get_or_add_pPr().append(pbdr)
    for i, line in enumerate(lines):
        r = p.add_run(("" if i == 0 else "\n") + line)
        r.bold = True
        r.font.color.rgb = ROJO
        r.font.name = BODY_FONT
        r.font.size = Pt(10.5)


def build_body(doc, md_text):
    lines = md_text.split("\n")
    i = 0
    first_h1_done = False
    while i < len(lines):
        line = lines[i]

        if line.strip() == "---":
            i += 1
            continue

        if line.startswith("**ADVERTENCIA LEGAL:**"):
            text = line.replace("**ADVERTENCIA LEGAL:**", "").strip()
            add_disclaimer_box(doc, [
                "⚠ ADVERTENCIA LEGAL — BORRADOR SIN REVISION DE ABOGADO",
                text,
            ])
            i += 1
            continue

        if line.startswith("# "):
            p = doc.add_paragraph()
            style_heading(p, line[2:].strip(), 20, VIOLETA, space_before=0, space_after=14, align_center=True)
            first_h1_done = True
            i += 1
            continue

        if line.startswith("### "):
            p = doc.add_paragraph()
            style_heading(p, line[4:].strip(), 12.5, NEGRO, space_before=14, space_after=6)
            i += 1
            continue

        if line.startswith("## "):
            p = doc.add_paragraph()
            style_heading(p, line[3:].strip(), 14.5, VIOLETA, space_before=16, space_after=8)
            i += 1
            continue

        if line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            add_table_from_lines(doc, table_lines)
            continue

        if re.match(r"^\s*-\s", line):
            p = doc.add_paragraph(style="List Bullet")
            add_inline_runs(p, line.strip()[2:])
            i += 1
            continue

        if line.strip() == "":
            i += 1
            continue

        if line.strip().startswith("*") and line.strip().endswith("*") and not line.strip().startswith("**"):
            p = doc.add_paragraph()
            add_inline_runs(p, line.strip().strip("*"), base_size=9.5, base_color=RGBColor(0x66, 0x66, 0x66), italic=True)
            i += 1
            continue

        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        add_inline_runs(p, line.strip())
        i += 1


def build_one(md_name, out_name):
    md_path = SRC_DIR / md_name
    out_path = SRC_DIR / out_name
    md_text = md_path.read_text(encoding="utf-8")

    doc = Document()
    section = doc.sections[0]
    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(11)
    normal.paragraph_format.line_spacing = 1.2
    normal.paragraph_format.space_after = Pt(6)

    build_body(doc, md_text)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    print(f"OK: {out_path} ({out_path.stat().st_size // 1024}KB)")


def main():
    for md_name, out_name in DOCS:
        build_one(md_name, out_name)


if __name__ == "__main__":
    main()
