"""Formaliza la metodologia de construccion de marca de artista de IM Music,
adaptada del framework real "7 Maletas" + funnel de 6 fases que ya usa
IM System (la plataforma B2B de prospeccion de Intelligent Markets), pero
reenfocada de "cliente empresa" a "artista y su fanbase"."""
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "docs" / "sello_plan" / "data_room" / "Metodologia_Construccion_Marca_Artista_IM_Music.docx"

VIOLETA = RGBColor(0x5E, 0x17, 0xEB)
NEGRO = RGBColor(0x00, 0x00, 0x00)
ROJO = RGBColor(0xB0, 0x20, 0x20)
GRIS_TEXTO = RGBColor(0x22, 0x22, 0x22)

HEADING_FONT = "Bahnschrift"
BODY_FONT = "Georgia"


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


def add_body(doc, text, size=11, bold_lead=None, italic=False, color=GRIS_TEXTO, space_after=10):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    if bold_lead:
        r = p.add_run(bold_lead)
        r.bold = True
        r.font.name = BODY_FONT
        r.font.size = Pt(size)
        r.font.color.rgb = VIOLETA
    r2 = p.add_run(text)
    r2.font.name = BODY_FONT
    r2.font.size = Pt(size)
    r2.font.color.rgb = color
    r2.italic = italic
    return p


def add_bullet(doc, text, bold_lead=None, size=11):
    p = doc.add_paragraph(style="List Bullet")
    if bold_lead:
        r = p.add_run(bold_lead)
        r.bold = True
        r.font.name = BODY_FONT
        r.font.size = Pt(size)
        r.font.color.rgb = VIOLETA
    r2 = p.add_run(text)
    r2.font.name = BODY_FONT
    r2.font.size = Pt(size)
    r2.font.color.rgb = GRIS_TEXTO
    return p


def main():
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(11)
    normal.paragraph_format.line_spacing = 1.2
    normal.paragraph_format.space_after = Pt(8)

    # Cover
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    style_heading(p, "IM MUSIC", 20, VIOLETA, space_before=0, space_after=4, align_center=True)
    p2 = doc.add_paragraph()
    style_heading(p2, "METODOLOGIA DE CONSTRUCCION DE MARCA DE ARTISTA", 16, VIOLETA, space_before=0, space_after=6, align_center=True)
    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = p3.add_run("Investigacion de audiencia, analisis psicologico y funnel de contenido, adaptados del framework \u201c7 Maletas\u201d de Felipe Vergara que ya opera IM System para prospeccion B2B")
    r3.italic = True
    r3.font.size = Pt(11)
    r3.font.name = BODY_FONT
    r3.font.color.rgb = GRIS_TEXTO
    p3.paragraph_format.space_after = Pt(20)

    # Disclaimer
    pd = doc.add_paragraph()
    pd.paragraph_format.space_after = Pt(16)
    rd = pd.add_run(
        "ACTIVO DE MARCA / PROPIEDAD INTELECTUAL INTERNA \u2014 NO DISTRIBUIR EXTERNAMENTE SIN REVISION DEL FUNDADOR. "
        "Este documento adapta, para artistas de musica, un framework de investigacion y persuasion (\u201c7 Maletas\u201d de Felipe "
        "Vergara) que IM System ya ejecuta en produccion para investigar y posicionar clientes B2B (PyMEs/empresas). La "
        "adaptacion aqui generaliza ese framework de \u201ccliente que compra un servicio\u201d a \u201coyente que se vuelve fan\u201d \u2014 "
        "es una extrapolacion razonada, no una copia literal, y no ha sido validada todavia con un caso real aplicado a un "
        "artista (a diferencia del documento hermano de composicion, que si tiene un caso real ejecutado: ver "
        "Metodologia_Composicion_Neurociencia_IM_Music.docx). No es una obra con derechos de autor registrados a la fecha; "
        "su proteccion hoy es de secreto comercial/know-how interno."
    )
    rd.font.name = BODY_FONT
    rd.font.size = Pt(9.5)
    rd.font.color.rgb = ROJO
    rd.bold = True

    # 0. Que es
    style_heading(doc.add_paragraph(), "0. QUE ES ESTE DOCUMENTO", 14, VIOLETA)
    add_body(doc,
        "El plan de negocios del sello hace referencia constante a \u201cla metodologia propia de desarrollo de marca y de "
        "artista del fundador\u201d como el activo diferencial del negocio, y a la Comunicadora como quien \u201cdefine el plan "
        "editorial y la parrilla de contenido\u201d sin producir desde cero (Secciones 3.1 y 6 del plan de negocios). Este "
        "documento es lo que convierte esa afirmacion en un proceso concreto, repetible y revisable por un inversionista: "
        "como se investiga a la audiencia de un artista, como se traduce esa investigacion en un analisis psicologico "
        "estructurado, y como ese analisis se convierte en la parrilla de contenido que ejecutan el Content Engine, el "
        "Filmmaker y la Disenadora Grafica."
    )
    add_body(doc,
        "La fuente real de este metodo es el modulo de investigacion \u201c7 Maletas\u201d que ya opera, en produccion, en IM "
        "System (la plataforma hermana de prospeccion B2B de Intelligent Markets, carpeta C:\\Users\\JOSE\\Projects\\IMSYSTEM, "
        "archivo CLAUDE.md y agent/deep_researcher.py). Ahi el framework investiga PyMEs y empresas para conseguirlas como "
        "clientes de pauta publicitaria. Lo que sigue es la misma arquitectura de investigacion y persuasion, reenfocada de "
        "\u201cnegocio que vende un servicio\u201d a \u201cartista que construye una audiencia\u201d \u2014 cada adaptacion esta marcada como tal, "
        "no se presenta como si ya hubiera sido probada en un caso real de artista."
    )

    # 1. Investigacion
    style_heading(doc.add_paragraph(), "1. INVESTIGACION DE AUDIENCIA \u2014 NIVEL MACRO Y NIVEL MICRO", 14, VIOLETA)
    add_body(doc, "El original investiga en dos niveles antes de construir cualquier estrategia. Adaptado a un artista:", space_after=8)
    add_bullet(doc, "del genero/escena a la que pertenece el artista, no del artista todavia: estudios academicos sobre psicologia del fandom musical (Google Scholar), tendencias de consumo cultural del genero (datos tipo DANE/Mincultura si existen para ese genero en Colombia, ver limitaciones ya documentadas en el plan de negocios sobre disponibilidad de estos datos), noticias y reportes de industria del genero, gremios o comunidades del genero.", bold_lead="Nivel macro: ")
    add_bullet(doc, "del artista especifico y su audiencia ya existente: comentarios y reacciones reales en sus redes sociales, perfiles de artistas comparables en el mismo genero (el equivalente a \u201ctop 5 competidores\u201d del original), menciones externas (foros, grupos, comunidades), y cualquier dato de streaming o redes que el artista ya tenga. El original usa Google Maps con minimo 50 reviews con texto completo como estandar de evidencia; para un artista el equivalente es un minimo de comentarios/reacciones reales recolectados en sus publicaciones, no una muestra arbitraria mas pequena.", bold_lead="Nivel micro: ")
    add_body(doc,
        "Esta investigacion es trabajo real de la Comunicadora antes de definir la parrilla de un artista nuevo en el "
        "roster, no un paso ceremonial \u2014 es la misma logica detras de por que el plan de negocios insiste en que el "
        "Content Engine ejecuta pero no decide la estrategia (Seccion 3.1 del plan de negocios)."
    )

    # 2. Sesgos
    style_heading(doc.add_paragraph(), "2. ANALISIS PSICOLOGICO: SESGOS COGNITIVOS DEL OYENTE", 14, VIOLETA)
    add_body(doc,
        "El original identifica, con evidencia real (nunca generica), que sesgos cognitivos estan activos en la decision "
        "de compra. Adaptados a la decision de un oyente de volverse fan:", space_after=8
    )
    add_bullet(doc, "que se pierde el oyente si no sigue al artista ahora (lanzamiento, momento cultural, comunidad que se esta formando).", bold_lead="Aversion a la perdida: ")
    add_bullet(doc, "quien o que valida al artista ante el oyente (otro artista reconocido, un medio, un numero de streams/seguidores visible).", bold_lead="Sesgo de autoridad: ")
    add_bullet(doc, "cuantos comentarios, reacciones o menciones de otros necesita ver un oyente casual antes de tomarse en serio a un artista nuevo.", bold_lead="Prueba social: ")
    add_bullet(doc, "con que referencia compara el oyente a este artista (otro artista parecido ya establecido) para decidir si \u201cvale la pena\u201d.", bold_lead="Sesgo de anclaje: ")
    add_bullet(doc, "que primeros 3 segundos de una cancion o un video convencen a un oyente de quedarse (ver Principio 1 de la metodologia de composicion, el documento hermano de este).", bold_lead="Efecto halo: ")
    add_bullet(doc, "por que un oyente se queda con los artistas que ya escucha y no prueba uno nuevo.", bold_lead="Sesgo de statu quo: ")
    add_body(doc,
        "A diferencia del documento hermano de composicion, que ya tiene un caso real aplicado, esta lista de sesgos es "
        "una adaptacion directa de la lista que usa IM System para negocios \u2014 no se ha confirmado todavia con evidencia "
        "real de audiencia de un artista del roster, porque el roster hoy no tiene artistas firmados (ver plan de "
        "negocios, Seccion 1). Se presenta como punto de partida de la investigacion, no como hallazgo ya probado."
    )

    # 3. 7 maletas
    style_heading(doc.add_paragraph(), "3. ANALISIS 7 MALETAS APLICADO AL ARTISTA Y SU FANBASE", 14, VIOLETA)
    add_body(doc,
        "El framework original organiza la investigacion de un cliente potencial en 7 \u201cmaletas\u201d. Adaptadas de "
        "\u201cnegocio que evalua comprar un servicio\u201d a \u201coyente que evalua volverse fan\u201d:", space_after=8
    )
    add_bullet(doc, "identidad visual, catalogo existente, estetica, historia personal del artista \u2014 lo que ya tiene para construir sobre eso, con evidencia real (web, redes, lanzamientos previos).", bold_lead="Maleta 1 \u2014 Que tiene: ")
    add_bullet(doc, "frente a otros artistas del mismo genero: que le falta en presencia digital, en consistencia de marca, en frecuencia de lanzamiento, comparado con los \u201ccompetidores\u201d reales de su escena.", bold_lead="Maleta 2 \u2014 Que le falta: ")
    add_bullet(doc, "que necesidad emocional resuelve la musica del artista para su audiencia (identificacion, catarsis, pertenencia a una comunidad) \u2014 con citas textuales reales de comentarios de oyentes cuando existan, minimo 5, igual que exige el original para reviews de clientes.", bold_lead="Maleta 3 \u2014 Que duele: ")
    add_bullet(doc, "que quiere la audiencia del artista sentir o vivir, declarado (lo que comentan) versus profundo (lo que realmente los mueve a compartir o asistir a un show).", bold_lead="Maleta 4 \u2014 Que desea: ")
    add_bullet(doc, "que detiene a un oyente casual de convertirse en fan activo: saturacion de contenido similar, falta de autenticidad percibida, falta de prueba social suficiente.", bold_lead="Maleta 5 \u2014 Que lo frena: ")
    add_bullet(doc, "que dispara que un oyente actue de verdad: seguir, compartir, comprar merch, ir a un show \u2014 el equivalente al \u201cdisparador de compra\u201d del original, aqui aplicado a accion de fan, no a transaccion comercial.", bold_lead="Maleta 6 \u2014 Que lo mueve: ")
    add_bullet(doc, "el angulo de posicionamiento que ningun otro artista de ese genero/escena esta ocupando todavia \u2014 el mismo principio de \u201cgap del sector que nadie cubre\u201d del original, aplicado a posicionamiento artistico.", bold_lead="Maleta 7 \u2014 Oportunidad: ")

    # 4. Perfil psicografico
    style_heading(doc.add_paragraph(), "4. PERFIL PSICOGRAFICO DEL FAN IDEAL Y EL CAMINO DE OYENTE A FAN", 14, VIOLETA)
    add_body(doc,
        "El original construye un perfil psicografico del cliente ideal (edad, nivel socioeconomico, motivacion, miedo, "
        "como busca) y mapea su \u201ccustomer journey\u201d completo: cuanto tiempo demora en decidir, que busca antes de actuar, "
        "que lo hace finalmente actuar en vez de seguir buscando. Adaptado a un artista, esto se convierte en dos piezas "
        "de trabajo real de la Comunicadora antes de armar una parrilla:"
    )
    add_bullet(doc, "edad, intereses culturales, otros artistas que ya escucha, en que plataformas consume musica y contenido, que lo hace compartir musica con otros.", bold_lead="Perfil del fan ideal: ")
    add_bullet(doc, "como un oyente casual pasa de descubrir al artista (por que canal), a escucharlo de forma repetida, a seguirlo activamente, a convertirse en promotor (comparte, comenta, asiste a shows). Cada etapa de este camino necesita un tipo de contenido distinto \u2014 esto es exactamente lo que organiza la Seccion 5 de este documento.", bold_lead="El camino de oyente a fan: ")
    add_body(doc,
        "Tambien influye quien mas afecta la decision del oyente \u2014 el equivalente a los \u201cinfluenciadores de decision\u201d "
        "del original (pareja, hijos, padres, amigos): para un artista, esto es el circulo social del oyente (que amigos "
        "escuchan musica parecida, que comunidades o espacios fisicos/digitales frecuenta), relevante para decidir en que "
        "canales y con que tono se construye la presencia del artista."
    )

    # 5. Funnel
    style_heading(doc.add_paragraph(), "5. EL FUNNEL DE CONTENIDO DE 6 FASES", 14, VIOLETA)
    add_body(doc,
        "Esta es la ejecucion practica de todo lo anterior, y ya esta definida en el modulo de contenido de IM System "
        "(18 guiones: 6 fases por 3 piezas cada una). Cada pieza necesita Hook, Escena, Desarrollo, CTA y el principio "
        "psicologico que activa \u2014 la misma estructura que ya usa el Content Engine del sello para generar contenido "
        "(ver plan de negocios, Seccion 3.1). Aplicado a un artista:", space_after=8
    )
    add_bullet(doc, "objetivo: aversion a la perdida. Primer contacto con un oyente nuevo \u2014 por que debe quedarse ahora, no \u201cver despues\u201d.", bold_lead="Fase 1 \u2014 Atraccion: ")
    add_bullet(doc, "objetivo: autoridad. Mostrar el proceso creativo, el oficio, la seriedad detras del artista \u2014 no solo el producto final.", bold_lead="Fase 2 \u2014 Educativo / detras de camaras: ")
    add_bullet(doc, "objetivo: prueba social. Documentar el proceso de creacion, giras, estudio \u2014 evidencia de que esto es real y esta pasando.", bold_lead="Fase 3 \u2014 Documentacion: ")
    add_bullet(doc, "objetivo: evidencia concreta. Resultados medibles \u2014 numeros de streams, reacciones reales de oyentes, reconocimiento externo.", bold_lead="Fase 4 \u2014 Validacion: ")
    add_bullet(doc, "objetivo: conexion. Historia personal del artista, lo que hay detras de la musica \u2014 contenido que no vende nada directamente.", bold_lead="Fase 5 \u2014 Organico / storytelling: ")
    add_bullet(doc, "objetivo: identidad tribal. Contenido para quien ya es fan \u2014 lo que convierte a un fan en parte de una comunidad, no solo en oyente.", bold_lead="Fase 6 \u2014 Fidelizacion: ")
    add_body(doc,
        "Esta estructura de 6 fases es, en la practica, la parrilla de contenido que la Comunicadora disena y que "
        "dispara en paralelo al Content Engine, al Filmmaker y a la Disenadora Grafica, exactamente como ya describe el "
        "plan de negocios (Seccion 6): cada ciclo retroalimenta el siguiente con metricas reales de que fase funciono "
        "mejor para ese artista en particular."
    )

    # 6. Cierre
    style_heading(doc.add_paragraph(), "6. SEGUNDO PILAR DE LA METODOLOGIA PROPIA", 14, VIOLETA)
    add_body(doc,
        "Junto con la metodologia de composicion con neurociencia (el documento hermano de este, con un caso real ya "
        "aplicado), este documento formaliza el segundo pilar de lo que el plan de negocios llama \u201cla metodologia propia "
        "del fundador\u201d: uno decide como se escribe y produce una cancion para que se quede en la cabeza del oyente, el "
        "otro decide como se investiga y construye la marca del artista alrededor de esa cancion. Juntos son el activo "
        "de propiedad intelectual/know-how real detras de cada mencion de \u201cmetodologia propia\u201d en el plan de negocios "
        "del sello \u2014 y, igual que el resto de este Data Room, estan sujetos a revision del fundador antes de cualquier "
        "uso o presentacion externa como documento cerrado."
    )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT_PATH))
    print(f"OK: {OUT_PATH} ({OUT_PATH.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
