"""Genera el brochure (una pagina) de IM Music -- Elite Artist Platform,
la plataforma SaaS de distribucion musical, para mostrar a artistas/sellos
prospecto e inversionistas."""
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = ROOT / "assets" / "logo" / "logo_immusic.png"
OUT_PATH = ROOT / "docs" / "saas_plan" / "Brochure_Plataforma_SaaS_IM_Music.docx"

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


def bullet(doc, text, size=10, color=NEGRO):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.font.name = BODY_FONT
    return p


def main():
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.45)
    section.bottom_margin = Inches(0.45)
    section.left_margin = Inches(0.6)
    section.right_margin = Inches(0.6)

    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(10.5)
    normal.paragraph_format.line_spacing = 1.05
    normal.paragraph_format.space_after = Pt(4)

    # Logo + titulo
    if LOGO_PATH.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(LOGO_PATH), height=Inches(0.55))
        p.paragraph_format.space_after = Pt(2)

    para(doc, "IM MUSIC — ELITE ARTIST PLATFORM", size=18, color=VIOLETA,
         bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, font=HEADING_FONT, space_after=0)
    para(doc, "La plataforma de distribución musical hecha para artistas que quieren crecer en serio",
         size=10.5, color=GRIS, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

    # Problema / oportunidad
    para(doc, "El problema", size=11.5, color=NEGRO, bold=True, font=HEADING_FONT, space_after=2)
    para(doc, "Miles de lanzamientos compiten cada día por la misma atención. Las plataformas "
              "de distribución DIY (DistroKid, TuneCore, CD Baby) te suben la música, pero ahí "
              "se acaba su trabajo — el artista queda solo frente al algoritmo, sin acompañamiento "
              "real de marca, de contenido ni de desarrollo de carrera.",
         size=10.5, color=NEGRO, space_after=12)

    # Tabla de planes
    para(doc, "Tres niveles, un solo panel", size=11.5, color=NEGRO, bold=True, font=HEADING_FONT, space_after=4)

    plans = [
        ("BÁSICO", "$19,99/mes",
         "Distribución a 9 plataformas (Spotify, Apple Music, YouTube Music, Deezer, Tidal, "
         "Amazon Music, TikTok, Pandora, Claro Música), gestión de catálogo, splits de regalías, "
         "reportes básicos."),
        ("PRO", "$149,99/mes",
         "Todo lo de Básico + investigación de mercado con IA, branding básico, ads automáticos, "
         "creativos generados con IA, reporting avanzado."),
        ("ÉLITE 360", "$2.999,99/mes",
         "Todo lo de Pro + Project Manager dedicado, manager musical y desarrollo artístico, "
         "producción de videos musicales, branding artístico completo, Meta Ads gestionado por "
         "expertos, campamentos musicales, acceso a red de industria. Cupo limitado."),
    ]

    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, (name, price, _) in enumerate(plans):
        cell = table.rows[0].cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"{name}\n{price}")
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = BLANCO
        r.font.name = HEADING_FONT
        set_cell_bg(cell, "5E17EB")

    row2 = table.add_row()
    for j, (_, _, features) in enumerate(plans):
        cell = row2.cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        r = p.add_run(features)
        r.font.size = Pt(8.5)
        r.font.color.rgb = NEGRO
        r.font.name = BODY_FONT
        set_cell_bg(cell, CREMA)
        cell.paragraphs[0].paragraph_format.space_before = Pt(5)
        cell.paragraphs[0].paragraph_format.space_after = Pt(5)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Diferenciadores
    para(doc, "Por qué IM Music y no otro distribuidor", size=11.5, color=NEGRO, bold=True,
         font=HEADING_FONT, space_after=3, space_before=4)
    bullet(doc, "El único con un tier de desarrollo artístico 360 real — no es una herramienta "
                "genérica, es el mismo equipo que ya desarrolla artistas firmados.")
    bullet(doc, "Pasarela de pago local para Colombia (Wompi) además de Stripe — pensado para "
                "LatAm, no adaptado después.")
    bullet(doc, "Nace de un sello discográfico real, con artistas reales, no de una idea en papel.")
    bullet(doc, "Arquitectura blockchain-ready para verificación de contratos de regalías, con "
                "roadmap hacia financiamiento colectivo de artistas por parte de su propia audiencia.")

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Contacto
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    r = p.add_run("IM Music — Elite Artist Platform")
    r.font.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = VIOLETA
    r.font.name = HEADING_FONT

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("[correo de contacto]  ·  Instagram @immusicsello  ·  [WhatsApp/teléfono]")
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = GRIS
    r2.font.name = BODY_FONT

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT_PATH))
    print(f"OK: {OUT_PATH} ({OUT_PATH.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
