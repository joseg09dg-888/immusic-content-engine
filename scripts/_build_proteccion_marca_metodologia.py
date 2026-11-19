# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

VIOLETA = RGBColor(0x5E, 0x17, 0xEB)
NEGRO = RGBColor(0x00, 0x00, 0x00)
GRIS_TEXTO = RGBColor(0x22, 0x22, 0x22)
ROJO = RGBColor(0xB0, 0x20, 0x20)
GRIS_FOOTER = RGBColor(0x66, 0x66, 0x66)


def add(doc, text, font="Georgia", size=11, color=GRIS_TEXTO, bold=False, align=None, space_after=10):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    r = p.add_run(text)
    r.font.name = font
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.bold = bold
    p.paragraph_format.space_after = Pt(space_after)
    return p


def build():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Georgia"
    style.font.size = Pt(11)

    add(doc, "IM MUSIC", "Bahnschrift", 16, VIOLETA, True, WD_ALIGN_PARAGRAPH.CENTER, 2)
    add(doc, "PROTECCIÓN DE MARCA Y METODOLOGÍA", "Bahnschrift", 22, NEGRO, True, WD_ALIGN_PARAGRAPH.CENTER, 6)
    add(doc, "Cómo registrar el nombre IM Music y proteger legalmente la metodología propia (construcción de marca de artista, composición con neurociencia, lanzamiento de canciones) frente a filtración o uso no autorizado", "Georgia", 11, GRIS_TEXTO, False, WD_ALIGN_PARAGRAPH.CENTER, 16)

    add(doc, "⚠ GUÍA INFORMATIVA — VERIFICAR CIFRAS Y PROCEDIMIENTO ANTES DE ACTUAR", "Georgia", 10, ROJO, True, None, 2)
    add(doc,
        "Este documento explica los mecanismos legales reales disponibles en Colombia y da rangos de costo y tiempo de fuentes públicas consultadas en 2026. "
        "No es una radicación, no es una cotización firme, y no sustituye la revisión de un abogado antes de presentar cualquier solicitud. "
        "La tarifa exacta de la SIC y el procedimiento exacto de la DNDA deben confirmarse directamente en sic.gov.co y en el portal oficial de la DNDA antes de pagar o firmar nada.",
        "Georgia", 10, ROJO, True, None, 16)

    add(doc, "0. POR QUÉ ESTO IMPORTA AHORA", "Bahnschrift", 15, VIOLETA, True, None, 6)
    add(doc,
        "El sello ya tiene tres documentos de metodología propia formalizados por escrito en este Data Room: la construcción de marca de artista "
        "(Metodologia_Construccion_Marca_Artista_IM_Music.docx), la composición con neurociencia (Metodologia_Composicion_Neurociencia_IM_Music.docx) "
        "y el lanzamiento de canciones (Metodologia_Lanzamiento_Canciones_IM_Music.docx). Antes de que esto existiera por escrito, la metodología vivía "
        "solo en la cabeza del fundador y era, de hecho, difícil de copiar. Ahora que está documentada —que es precisamente lo que la hace transferible "
        "al equipo y escalable— también es mucho más fácil de copiar si cae en las manos equivocadas. Formalizar la metodología y protegerla legalmente "
        "tienen que ir de la mano, no una sin la otra.",
        space_after=16)

    add(doc, "1. MARCA REGISTRADA — SUPERINTENDENCIA DE INDUSTRIA Y COMERCIO (SIC)", "Bahnschrift", 15, VIOLETA, True, None, 6)
    add(doc,
        "Qué protege: el nombre \"IM Music\" como marca, frente a que un tercero registre un nombre igual o similar antes, o use el nombre del sello sin "
        "autorización. No protege la metodología — eso es el punto 2.",
        space_after=8)
    add(doc,
        "Dónde: ante la Superintendencia de Industria y Comercio, por el portal sic.gov.co. Hay una búsqueda previa de antecedentes (una versión gratuita "
        "y una de pago) recomendada antes de radicar, para evitar que la solicitud choque con una marca ya registrada.",
        space_after=8)
    add(doc,
        "Clases de Niza a evaluar con un abogado de marcas antes de radicar (no radicar sin esta revisión): Clase 41 (entretenimiento, producción musical, "
        "educación — el núcleo del sello), Clase 9 (si se comercializan grabaciones o descargas), Clase 35 (servicios de negocio/publicidad, relevante si "
        "la plataforma SaaS se posiciona como servicio B2B) y Clase 42 (software/plataforma). Desde el 1 de enero de 2026 aplica la versión Niza 13-2026 "
        "para solicitudes nuevas.",
        space_after=8)
    add(doc,
        "Tiempo: entre 9 y 12 meses desde la radicación hasta la decisión, más si un tercero presenta oposición durante la ventana de publicación. "
        "Vigencia: 10 años desde la concesión, renovable indefinidamente por periodos iguales.",
        space_after=8)
    add(doc,
        "Costo: las fuentes públicas 2026 reportan un rango de aproximadamente $900.000 a $1.371.000 COP por clase de Niza en tarifa oficial, con un "
        "descuento para microempresa reportado entre $560.500 y $1.179.000 según la fuente — este documento NO fija una cifra exacta porque las fuentes "
        "consultadas no coinciden entre sí; confirmar la tarifa vigente directamente en sic.gov.co antes de radicar.",
        space_after=8)
    add(doc,
        "A futuro — expansión internacional (Dubái/EAU y otros mercados): el Protocolo de Madrid permite extender un registro de marca colombiano a otros "
        "países miembros, incluido EAU, de forma más eficiente en costo que registrar por separado en cada país. No es un paso urgente hoy — tiene sentido "
        "una vez haya tracción internacional real que justifique la inversión.",
        space_after=16)

    add(doc, "2. SECRETO EMPRESARIAL — DECISIÓN 486 DE 2000 (COMUNIDAD ANDINA)", "Bahnschrift", 15, VIOLETA, True, None, 6)
    add(doc,
        "Esta es la protección real para la metodología (marca de artista, composición, lanzamiento de canciones) — no la marca registrada del punto 1. "
        "No requiere ningún registro, pero solo aplica si se cumplen tres condiciones, según el artículo 260 de la Decisión 486: la información es secreta "
        "(no es de conocimiento general ni fácilmente accesible), tiene valor comercial precisamente porque es secreta, y el titular ha tomado medidas "
        "razonables para mantenerla en reserva.",
        space_after=8)
    add(doc,
        "El artículo 265 impone un deber de no divulgar ni usar esa información a quien accedió a ella por razón de su cargo, profesión o relación comercial. "
        "Esta es la base legal exacta de por qué poner al Filmmaker, la Comunicadora y la Diseñadora Gráfica en planta fija, con cláusula de confidencialidad "
        "firmada, protege más que dejarlos freelance sin ese contrato específico: la ley exige \"medidas razonables\", y un contrato con cláusula de "
        "confidencialidad es evidencia directa de haberlas tomado. Un freelancer sin ese documento firmado deja la protección legal mucho más débil, "
        "aunque la información siga siendo técnicamente secreta.",
        space_after=8)
    add(doc, "Medidas razonables concretas a implementar ya:", "Georgia", 11, VIOLETA, True, None, 4)
    add(doc, "a. Marcar explícitamente los documentos de metodología como confidenciales (ya se hace en los disclaimers de este Data Room).", space_after=4)
    add(doc, "b. Firmar el Acuerdo de Confidencialidad (ver Acuerdo_de_Confidencialidad_IM_Music.docx, en esta misma carpeta) con todo el equipo con acceso real a la metodología — planta fija Y freelance ocasional (Productor Musical, Ingeniero de Sonido) si llegan a ver fragmentos.", space_after=4)
    add(doc, "c. Limitar el acceso por necesidad de conocer: no entregar el documento completo a quien solo necesita una sección puntual.", space_after=4)
    add(doc, "d. Control de acceso real en Notion/Drive mediante permisos — no dejar todo abierto a todo el equipo por defecto.", space_after=16)

    add(doc, "3. DERECHOS DE AUTOR COMO OBRA INÉDITA — DIRECCIÓN NACIONAL DE DERECHO DE AUTOR (DNDA)", "Bahnschrift", 15, VIOLETA, True, None, 6)
    add(doc,
        "Los tres documentos de metodología YA están protegidos por derecho de autor desde el momento mismo de su creación — Colombia sigue el Convenio de "
        "Berna, y el derecho de autor no requiere registro para existir. Pero registrarlos ante la DNDA, única entidad autorizada en Colombia para esto, "
        "como \"obra inédita\" (bajo el Decreto 460 de 1995), crea una constancia oficial con fecha cierta: una prueba documental de quién creó el texto y "
        "cuándo, útil en caso de disputa futura sobre autoría u origen.",
        space_after=8)
    add(doc,
        "No es necesario publicar la obra ni revelar la autoría para registrarla: la Ley 44 de 1993 permite que una obra presentada como inédita solo pueda "
        "ser consultada por su propio autor, manteniendo la metodología fuera de un registro público abierto.",
        space_after=8)
    add(doc,
        "Costo y tiempo reportados por una guía comercial 2026 (no la fuente oficial — verificar en el portal de la DNDA antes de confiar en esta cifra): "
        "registro gratuito tanto en línea como presencial, con un trámite en línea de 1 a 5 días hábiles.",
        space_after=16)

    add(doc, "4. CHECKLIST DE ACCIÓN CONCRETA", "Bahnschrift", 15, VIOLETA, True, None, 6)
    add(doc, "☐ Evaluar con un abogado de marcas las clases de Niza correctas para \"IM Music\" (y \"Élite 360\" si se usa como nombre comercial distintivo) y radicar ante la SIC.", space_after=4)
    add(doc, "☐ Registrar los tres documentos de metodología ante la DNDA como obra inédita.", space_after=4)
    add(doc, "☐ Firmar el Acuerdo de Confidencialidad con todo el equipo con acceso — fijo y freelance.", space_after=4)
    add(doc, "☐ Configurar control de acceso real en Notion/Drive por rol, no acceso abierto por defecto.", space_after=4)
    add(doc, "☐ A futuro, cuando haya tracción internacional real: evaluar extensión de marca vía Protocolo de Madrid para Dubái/EAU y otros mercados.", space_after=16)

    add(doc,
        "Elaborado con asistencia de IA a partir de fuentes públicas consultadas en 2026 (Superintendencia de Industria y Comercio, Decisión 486 de 2000, "
        "Decreto 460 de 1995, Ley 44 de 1993, y guías comerciales sobre trámites ante la DNDA). No reemplaza asesoría legal específica.",
        "Georgia", 9.5, GRIS_FOOTER, False, None, 0)

    doc.save("docs/sello_plan/data_room/Proteccion_Marca_y_Metodologia_IM_Music.docx")
    print("OK: Proteccion_Marca_y_Metodologia_IM_Music.docx")


if __name__ == "__main__":
    build()
