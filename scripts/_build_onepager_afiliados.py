"""Genera el PDF de una pagina para adjuntar al correo de outreach a
managers de artistas — resumen del programa de afiliados Hotmart."""
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = ROOT / "assets" / "logo" / "logo_immusic.png"
OUT_PATH = ROOT / "docs" / "libro" / "OnePager_Programa_Afiliados_IM_Music.docx"

VIOLETA = RGBColor(0x5E, 0x17, 0xEB)
NEGRO = RGBColor(0x00, 0x00, 0x00)
GRIS = RGBColor(0x33, 0x33, 0x33)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)
CREMA = "F2EDE5"

HEADING_FONT = "Bahnschrift"
BODY_FONT = "Georgia"


def set_cell_bg(cell, hex_color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    cell._tc.get_or_add_tcPr().append(shd)


def para(doc, text=None, size=10.5, color=GRIS, bold=False, italic=False,
         align=None, space_before=0, space_after=6, font=BODY_FONT):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.font.bold = bold
        r.font.italic = italic
        r.font.name = font
    return p


def main():
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.6)
    section.right_margin = Inches(0.6)

    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(10.5)
    normal.paragraph_format.line_spacing = 1.05
    normal.paragraph_format.space_after = Pt(4)

    # Logo + título
    if LOGO_PATH.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(LOGO_PATH), height=Inches(0.55))
        p.paragraph_format.space_after = Pt(2)

    para(doc, "MUSIC BUSINESS PARA TODOS LOS HUMANOS", size=16, color=VIOLETA,
         bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font=HEADING_FONT, space_after=0)
    para(doc, "Una forma de ayudar a artistas emergentes — y que a ustedes también les quede algo",
         size=10, color=GRIS, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    para(doc, "Miles de artistas están perdiendo dinero que ya es suyo, solo porque nadie se "
              "los explicó. Este libro se los explica. Ustedes solo tienen que decir \"léanlo\".",
         size=11, color=NEGRO, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

    # Qué es / para quién / por qué
    para(doc, "¿Qué es?", size=11, color=NEGRO, bold=True, font=HEADING_FONT, space_after=2)
    para(doc, "Guía de negocio musical — derechos, contratos, regalías y marca — escrita por "
              "IM Music, sello independiente en operación. 92 páginas, $16,90 USD.")

    para(doc, "¿Por qué le sirve a su audiencia?", size=11, color=NEGRO, bold=True, font=HEADING_FONT, space_after=2)
    para(doc, "Su audiencia ya se está haciendo estas preguntas. Recomendarlo no se siente "
              "como publicidad — se siente como ayudar.")

    para(doc, "¿Cómo funciona?", size=11, color=NEGRO, bold=True, font=HEADING_FONT, space_after=2)
    para(doc, "1. Les damos una copia gratis para leerla, sin compromiso.")
    para(doc, "2. Si les gusta, la comparten con su link de afiliado.")
    para(doc, "3. Cada venta les paga automático — sin gestionar nada.", space_after=10)

    # Tabla de comisión
    para(doc, "Comisión del 70% (sobre el neto, después de la comisión de Hotmart)",
         size=11, color=NEGRO, bold=True, font=HEADING_FONT, space_after=4)

    table = doc.add_table(rows=2, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["100 ventas", "500 ventas", "1.000 ventas"]
    values = ["≈ $1.031 USD", "≈ $5.155 USD", "≈ $10.310 USD"]
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = BLANCO
        r.font.name = BODY_FONT
        set_cell_bg(cell, "5E17EB")
    for j, v in enumerate(values):
        cell = table.rows[1].cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(v)
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = VIOLETA
        r.font.name = HEADING_FONT
        set_cell_bg(cell, CREMA)
        cell.paragraphs[0].paragraph_format.space_before = Pt(4)
        cell.paragraphs[0].paragraph_format.space_after = Pt(4)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Pauta opcional
    para(doc, "¿Quieren más alcance?", size=11, color=NEGRO, bold=True, font=HEADING_FONT, space_after=2, space_before=8)
    para(doc, "Nosotros armamos y manejamos la pauta en Meta Ads sin cobrar fee — ustedes "
              "solo ponen el presupuesto que va directo a la plataforma.", space_after=12)

    # Contacto
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    r = p.add_run("IM Music")
    r.font.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = VIOLETA
    r.font.name = HEADING_FONT

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("[correo de contacto]  ·  Instagram @immusicsello  ·  [teléfono opcional]")
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = GRIS
    r2.font.name = BODY_FONT

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT_PATH))
    print(f"OK: {OUT_PATH} ({OUT_PATH.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
