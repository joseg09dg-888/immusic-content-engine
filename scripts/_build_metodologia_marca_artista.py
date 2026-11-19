"""Formaliza la metodologia de construccion de marca de artista de IM Music.
V3: correccion estructural del fundador (2026-11-19) - Elite 360 ES la metodologia
de construccion de marca, no un framework paralelo a ella. El documento se
reorganiza en las 7 etapas reales que el fundador nombro: Diagnostico,
Investigacion, Lenguaje y Comunicacion, Identidad de Artista, Contenido,
Marketing Tradicional y Digital, Pauta. El lanzamiento de sencillos (Adicto/La S)
se mueve a su propio documento (Metodologia_Lanzamiento_Canciones_IM_Music.docx)
porque es una herramienta tactica distinta, no una sub-etapa de construccion de
marca."""
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


def add_bullet(doc, text, bold_lead=None, size=11, level=0):
    style = "List Bullet" if level == 0 else "List Bullet 2"
    p = doc.add_paragraph(style=style)
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


def add_table(doc, header, rows, col_widths=None):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Light Grid Accent 1"
    hdr = t.rows[0].cells
    for i, h in enumerate(header):
        hdr[i].text = ""
        pr = hdr[i].paragraphs[0]
        rr = pr.add_run(h)
        rr.bold = True
        rr.font.name = BODY_FONT
        rr.font.size = Pt(10)
        rr.font.color.rgb = VIOLETA
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            pr = cells[i].paragraphs[0]
            rr = pr.add_run(str(val))
            rr.font.name = BODY_FONT
            rr.font.size = Pt(10)
            rr.font.color.rgb = GRIS_TEXTO
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return t


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
    r3 = p3.add_run(
        "Version 3 \u2014 las 7 etapas reales del metodo (Diagnostico, Investigacion, Lenguaje y Comunicacion, Identidad "
        "de Artista, Contenido, Marketing Tradicional y Digital, Pauta), el mismo proceso que ejecuta el tier Elite 360 "
        "de la plataforma, validado a escala reducida con un caso real de entrada a mercado"
    )
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
        "Esta version 3 corrige un error de estructura de la version anterior: el lanzamiento de sencillos NO es una "
        "sub-etapa de construccion de marca, es una herramienta tactica distinta que se activa cada vez que un artista "
        "lanza una cancion (ver el documento hermano Metodologia_Lanzamiento_Canciones_IM_Music.docx). Este documento "
        "formaliza unicamente la construccion de marca: las 7 etapas reales por las que pasa un artista, de principio a "
        "fin. No es una obra con derechos de autor registrados a la fecha; su proteccion hoy es de secreto "
        "comercial/know-how interno."
    )
    rd.font.name = BODY_FONT
    rd.font.size = Pt(9.5)
    rd.font.color.rgb = ROJO
    rd.bold = True

    # 0. Que es / que cambio
    style_heading(doc.add_paragraph(), "0. QUE ES ESTE DOCUMENTO Y QUE CORRIGE ESTA VERSION", 14, VIOLETA)
    add_body(doc,
        "El plan de negocios del sello hace referencia constante a \u201cla metodologia propia de desarrollo de marca y de "
        "artista del fundador\u201d como el activo diferencial del negocio. Las versiones 1 y 2 de este documento "
        "formalizaban esa frase mezclando dos cosas de naturaleza distinta en un solo documento: la construccion de "
        "marca y el lanzamiento tactico de un sencillo especifico, tratados como dos \u201cframeworks\u201d paralelos. El "
        "fundador corrigio ese error directamente: construir la marca de un artista y lanzar una cancion de ese artista "
        "son procesos distintos, con objetivos distintos y horizontes de tiempo distintos. Uno es continuo y estructural "
        "\u2014 asi es como Elite 360 ya lo define, de principio a fin. El otro es una campana puntual de 90 dias que se "
        "activa cada vez que hay un lanzamiento. Esta version 3 separa ambos: este documento queda unicamente sobre "
        "construccion de marca, en 7 etapas; el lanzamiento de sencillos vive en su propio documento.",
        space_after=8
    )
    add_body(doc,
        "Honestidad sobre el estado de cada pieza: las 7 etapas que formaliza este documento son, etapa por etapa, el "
        "mismo proceso que ya define el tier Elite 360 de la plataforma (producto en diseno, sin cliente todavia "
        "ejecutando el ciclo completo). La unica etapa de este metodo con un caso real de ejecucion hasta la fecha es el "
        "Diagnostico y, de forma parcial, Investigacion, Contenido y Marketing \u2014 a traves de la propuesta comercial "
        "real (con precio ya cotizado) hecha a una artista de jazz panamena establecida para su entrada al mercado "
        "colombiano. Ese caso no cubrio las etapas de Lenguaje y Comunicacion ni Identidad de Artista completas, porque "
        "la artista ya tenia una identidad consolidada en otro mercado \u2014 exactamente la razon por la que Elite 360 y "
        "el servicio de Representacion/Entrada a Mercado son alcances distintos del mismo metodo (ver Secciones 4 y "
        "10)."
    )

    # 1. El metodo es uno solo
    style_heading(doc.add_paragraph(), "1. UN SOLO METODO, DOS PROFUNDIDADES SEGUN LA SITUACION DEL ARTISTA", 14, VIOLETA)
    add_body(doc,
        "IM Music no tiene dos metodologias de marca distintas seg\u00fan el tipo de artista. Tiene un solo metodo de 7 "
        "etapas, que se ejecuta a distinta profundidad segun si el artista entra al roster propio o solo necesita "
        "representacion en un mercado nuevo:", space_after=8
    )
    add_bullet(doc,
        "las 7 etapas completas, a maxima profundidad, con inversion de catalogo, produccion de video, asesoria legal "
        "y financiamiento. Para el artista que se vuelve parte del roster y se construye de cero, incluyendo identidad "
        "donde todavia no existe una consolidada.",
        bold_lead="Elite 360 ($2.999,99 USD/mes): "
    )
    add_bullet(doc,
        "una version mas angosta de las mismas 7 etapas, sin las etapas 3 y 4 (Lenguaje y Comunicacion, Identidad de "
        "Artista) porque el artista ya llega con una identidad consolidada en otro mercado, y sin inversion de catalogo "
        "ni produccion de video. Para un artista externo, ya establecido, que solo necesita entrar a un mercado nuevo "
        "donde el sello opera (ver Seccion 10 para el detalle etapa por etapa).",
        bold_lead="Representacion / Entrada a Mercado ($1.000-$2.000 USD/mes): "
    )
    add_body(doc,
        "Esto no es una inconsistencia de precio entre dos servicios distintos \u2014 es el mismo metodo aplicado con "
        "distinto alcance, y la Seccion 10 de este documento explica exactamente que etapas entran y cuales no en cada "
        "caso."
    )

    # 2. Las 7 etapas
    style_heading(doc.add_paragraph(), "2. LAS 7 ETAPAS DEL METODO", 14, VIOLETA)
    add_table(doc, ["Etapa", "Que resuelve"], [
        ["1. Diagnostico", "Donde esta el artista hoy, de verdad, comparando lo que ya tiene contra lo que todavia no convierte"],
        ["2. Investigacion", "Quien es su audiencia real y potencial, a nivel macro (genero/escena) y micro (el artista y sus oyentes actuales)"],
        ["3. Lenguaje y Comunicacion", "Como habla la marca del artista, con que tono y que palabras \u2014 autenticidad cultural, no generico"],
        ["4. Identidad de Artista", "La identidad visual y narrativa consistente del artista, a partir de lo que ya tiene o desde cero"],
        ["5. Contenido", "La produccion y calendarizacion de piezas que ejecutan todo lo anterior, via el Content Engine y el equipo humano"],
        ["6. Marketing Tradicional y Digital", "Los canales, online y fisicos, por donde esa identidad y ese contenido llegan a audiencias reales"],
        ["7. Pauta", "La gestion profesional de inversion publicitaria paga en esos canales (distinta del gasto de pauta en si, que se cobra aparte)"],
    ])
    add_body(doc,
        "Las 7 etapas son secuenciales en su primera pasada por un artista nuevo, pero ciclicas en operacion continua: "
        "una vez que el artista esta en marcha, Contenido, Marketing y Pauta corren en paralelo de forma permanente, "
        "retroalimentados por lo que la Investigacion sigue descubriendo sobre la audiencia real."
    )

    # 2.1 Diagnostico
    style_heading(doc.add_paragraph(), "2.1 Etapa 1 \u2014 Diagnostico", 12, NEGRO, space_before=10)
    add_body(doc,
        "El diagnostico no es generico \u2014 compara dos tipos de numero que casi nunca se ven juntos, y esa comparacion "
        "ES el diagnostico central. El caso real que valida este metodo (una artista de jazz panamena, 15+ anios de "
        "carrera, tarima compartida con figuras internacionales de su genero) tenia 9.878 seguidores reales en "
        "Instagram \u2014 comunidad genuina ya construida \u2014 y solo 91 oyentes mensuales en Spotify. La conclusion del "
        "diagnostico no fue \u201cfalta audiencia\u201d, fue \u201cel problema no es la audiencia, es que se le esta ofreciendo a "
        "esa audiencia\u201d: el feed era documentacion reactiva de eventos pasados, no una maquina que convirtiera "
        "prestigio real en streaming real.", space_after=8
    )
    add_body(doc,
        "Este es el patron del diagnostico, generalizado para cualquier artista: medir por un lado la trayectoria y la "
        "comunidad ya construida (anios de carrera, seguidores reales, reconocimiento en su escena), y por otro lado la "
        "senal de conversion real (oyentes mensuales, streams, ventas de boletos) \u2014 el gap entre ambos numeros define "
        "que etapas del metodo necesitan mas inversion de esfuerzo para ese artista en particular."
    )

    # 2.2 Investigacion
    style_heading(doc.add_paragraph(), "2.2 Etapa 2 \u2014 Investigacion", 12, NEGRO, space_before=10)
    add_body(doc,
        "Adaptada del modulo de investigacion \u201c7 Maletas\u201d que ya opera, en produccion, en IM System (la plataforma "
        "hermana de prospeccion B2B de Intelligent Markets, carpeta C:\\Users\\JOSE\\Projects\\IMSYSTEM, archivo CLAUDE.md "
        "y agent/deep_researcher.py), reenfocada de \u201cnegocio que vende un servicio\u201d a \u201cartista que construye una "
        "audiencia\u201d. Dos niveles:", space_after=8
    )
    add_bullet(doc, "del genero/escena a la que pertenece el artista, no del artista todavia: estudios academicos sobre psicologia del fandom musical (Google Scholar), tendencias de consumo cultural del genero, noticias y reportes de industria del genero, gremios o comunidades del genero.", bold_lead="Nivel macro: ")
    add_bullet(doc, "del artista especifico y su audiencia ya existente: comentarios y reacciones reales en sus redes sociales, perfiles de artistas comparables en el mismo genero, menciones externas, y cualquier dato de streaming o redes que el artista ya tenga \u2014 exactamente el tipo de comparacion (seguidores reales vs. oyentes mensuales reales) que define el Diagnostico de la Etapa 1.", bold_lead="Nivel micro: ")
    add_body(doc,
        "El caso real tambien incluyo investigacion de mercado como parte concreta de esta etapa: una tabla de "
        "festivales y eventos del genero del artista en el mercado objetivo (Voces del Jazz y del Caribe en Cartagena, "
        "Jazz al Parque y Festival Internacional de Jazz en Bogota, MedeJazz en Medellin), cada uno con una columna "
        "explicita de \u201cpor que calza\u201d con el perfil del artista \u2014 el equivalente, para entrada a mercado, de la "
        "investigacion macro de genero en cualquier otro caso."
    )
    add_body(doc, "Analisis que corre dentro de esta etapa, adaptado de negocio-que-compra a oyente-que-se-vuelve-fan:", space_after=8)
    add_bullet(doc, "identidad visual, catalogo existente, estetica, historia personal del artista \u2014 lo que ya tiene para construir sobre eso, con evidencia real.", bold_lead="Que tiene: ")
    add_bullet(doc, "frente a otros artistas del mismo genero: que le falta en presencia digital, en consistencia de marca, en frecuencia de lanzamiento.", bold_lead="Que le falta: ")
    add_bullet(doc, "que necesidad emocional resuelve la musica del artista para su audiencia \u2014 con citas textuales reales de comentarios de oyentes cuando existan, minimo 5.", bold_lead="Que duele: ")
    add_bullet(doc, "que quiere la audiencia del artista sentir o vivir, declarado versus profundo.", bold_lead="Que desea: ")
    add_bullet(doc, "que detiene a un oyente casual de convertirse en fan activo: saturacion de contenido similar, falta de autenticidad percibida, falta de prueba social suficiente.", bold_lead="Que lo frena: ")
    add_bullet(doc, "que dispara que un oyente actue de verdad: seguir, compartir, comprar merch, ir a un show.", bold_lead="Que lo mueve: ")
    add_bullet(doc, "el angulo de posicionamiento que ningun otro artista de ese genero/escena esta ocupando todavia.", bold_lead="Oportunidad: ")
    add_body(doc,
        "A partir de esta investigacion se construye el perfil psicografico del fan ideal (edad, intereses culturales, "
        "otros artistas que ya escucha, en que plataformas consume musica, que lo hace compartir) y el camino de oyente "
        "a fan: como pasa de descubrir al artista, a escucharlo de forma repetida, a seguirlo activamente, a "
        "convertirse en promotor \u2014 informacion que alimenta directamente las Etapas 5 y 6."
    )

    # 2.3 Lenguaje y Comunicacion
    style_heading(doc.add_paragraph(), "2.3 Etapa 3 \u2014 Lenguaje y Comunicacion", 12, NEGRO, space_before=10)
    add_body(doc,
        "Define con que palabras, que tono y que nivel de autenticidad cultural habla la marca del artista \u2014 distinto "
        "de la identidad visual (Etapa 4). El modelo de referencia es la voz de marca que ya usa IM Music mismo: REBEL "
        "LUXURY, verificada en uso real contra la cuenta @immusicsello. \u201cJaqueamos mentes\u201d no es solo un eslogan, es "
        "una postura \u2014 cuestionar como se ha hecho la industria tradicionalmente y demostrar con resultados reales que "
        "se puede hacer distinto. Esa misma logica, de que postura real respalda el tono del artista (no un tono "
        "generico de redes), es lo que esta etapa define para cada artista nuevo.", space_after=8
    )
    add_body(doc,
        "Precedente real de este principio aplicado a letra y narrativa: la metodologia de composicion con neurociencia "
        "de IM Music (documento hermano, caso real Mosco \u2014 Cana Brava) usa expresiones autenticas de la jerga paisa "
        "real de Medellin (qu\u00e9 vuelta, parcero, cucha, visajes, coronar) en lugar de lenguaje generico, apoyada en el "
        "Efecto Espejo: el oyente que escucha su propio lenguaje callejero sin filtro desactiva su filtro critico y "
        "genera empatia inmediata. El mismo principio \u2014 lenguaje real de la cultura del artista, no generico \u2014 es lo "
        "que esta etapa aplica a toda la comunicacion de marca del artista, no solo a la letra de una cancion "
        "especifica."
    )

    # 2.4 Identidad de Artista
    style_heading(doc.add_paragraph(), "2.4 Etapa 4 \u2014 Identidad de Artista", 12, NEGRO, space_before=10)
    add_body(doc,
        "Identidad visual y narrativa consistente del artista. El caso real que valida esta etapa a escala reducida "
        "demuestra un principio clave, explicito en el metodo: no siempre se rehace la identidad desde cero. Cuando el "
        "artista ya tiene un sistema visual propio pero desordenado o inconsistente, la etapa consiste en ordenar ese "
        "sistema existente \u2014 \u201corden visual al feed existente, sin rehacer la identidad\u201d \u2014 no en reemplazarlo. Cuando "
        "el artista entra al roster sin una identidad consolidada (el caso tipico de Elite 360), la etapa si construye "
        "esa identidad desde cero, con el mismo nivel de exigencia de marca que define a REBEL LUXURY (Seccion 9 del "
        "plan de negocios): nada generico, nada diluido."
    )

    # 2.5 Contenido
    style_heading(doc.add_paragraph(), "2.5 Etapa 5 \u2014 Contenido", 12, NEGRO, space_before=10)
    add_body(doc,
        "Esta etapa no redefine el proceso de contenido del sello \u2014 lo ejecuta. La Comunicadora define el plan "
        "editorial y la parrilla, y dispara en paralelo al Content Engine (piezas masivas y automatizadas), al "
        "Filmmaker/Editor con IA (edicion de material humano real del artista) y a la Disenadora Grafica (piezas a la "
        "medida que exceden el sistema de plantillas). El Content Engine ejecuta, no decide la estrategia \u2014 la decide "
        "esta etapa, con base en lo que arrojaron las Etapas 1 a 4.", space_after=8
    )
    add_body(doc,
        "Cuando un artista tiene un lanzamiento de sencillo en curso, la produccion tactica de ese lanzamiento (ver el "
        "documento hermano Metodologia_Lanzamiento_Canciones_IM_Music.docx) se ejecuta DENTRO de esta etapa \u2014 el "
        "lanzamiento es, en la practica, contenido con una cadencia y una psicologia especificas, no un proceso aparte "
        "del Content Engine."
    )

    # 2.6 Marketing
    style_heading(doc.add_paragraph(), "2.6 Etapa 6 \u2014 Marketing Tradicional y Digital", 12, NEGRO, space_before=10)
    add_body(doc,
        "Los canales por donde la identidad y el contenido del artista llegan a audiencias reales, tanto digitales "
        "como fisicos. El caso real que valida esta etapa aporta ejemplos concretos de ambos tipos de canal, sin que "
        "este documento reimporte el framework completo de lanzamiento del que provienen:", space_after=8
    )
    add_bullet(doc, "pauta segmentada en el mercado objetivo (fans y programadores culturales), contenido que empuja streaming real en vez de solo documentar eventos pasados, y un agente de booking contactando activamente festivales, venues y programadores \u2014 con seguimiento a fechas de postulacion.", bold_lead="Canal digital + relaciones de industria (caso de entrada a mercado): ")
    add_bullet(doc, "presencia fisica real en la comunidad/barrio del artista, estilo documental, con gente real de fondo \u2014 anclar la marca a un lugar y una comunidad reales, no solo a produccion digital aislada (tactica de \u201cpresencia fisica\u201d documentada en el framework de lanzamiento de sencillos).", bold_lead="Canal fisico/callejero (ejemplo del framework de lanzamiento): ")
    add_body(doc,
        "El principio comun a ambos: el marketing de esta etapa combina siempre un canal digital escalable con un canal "
        "fisico/relacional que el algoritmo no puede replicar \u2014 ninguno sustituye al otro."
    )

    # 2.7 Pauta
    style_heading(doc.add_paragraph(), "2.7 Etapa 7 \u2014 Pauta", 12, NEGRO, space_before=10)
    add_body(doc,
        "Gestion profesional de la inversion publicitaria paga (Meta Ads gestionado), parte del alcance ya definido de "
        "Elite 360. Esta etapa es explicitamente distinta del GASTO de pauta en si: la gestion (la estrategia, "
        "segmentacion y optimizacion de la campana) esta incluida en el fee mensual del servicio que corresponda; el "
        "gasto publicitario real que se paga a Meta/Google (desde USD $300-500/mes en el caso real de referencia) se "
        "cobra aparte, en ambos servicios \u2014 Elite 360 y Representacion/Entrada a Mercado \u2014 tal como ya establece el "
        "plan de negocios (Seccion 4)."
    )

    # 10. Reconciliacion de precio
    style_heading(doc.add_paragraph(), "3. COMO SE APLICAN LAS 7 ETAPAS SEGUN EL SERVICIO \u2014 RECONCILIACION DE PRECIO YA RESUELTA", 14, VIOLETA)
    add_body(doc,
        "Elite 360 y Representacion/Entrada a Mercado no son dos metodologias distintas con precios que compiten entre "
        "si \u2014 son el mismo metodo de 7 etapas aplicado a dos situaciones de artista distintas, ya reconciliado en el "
        "plan de negocios (Seccion 4) y en el modelo financiero del sello:", space_after=8
    )
    add_table(doc, ["Etapa", "Elite 360 ($2.999,99 USD/mes)", "Representacion / Entrada a Mercado ($1.000-$2.000 USD/mes)"], [
        ["1. Diagnostico", "Si, completo", "Si, completo \u2014 es el punto de partida del caso real"],
        ["2. Investigacion", "Si, completo (macro y micro)", "Si, completo \u2014 incluye la tabla de festivales/mercado objetivo"],
        ["3. Lenguaje y Comunicacion", "Si", "No \u2014 el artista ya llega con tono y comunicacion establecidos en su mercado de origen"],
        ["4. Identidad de Artista", "Si, desde cero si no existe", "No se rehace \u2014 solo se ordena el sistema visual ya existente"],
        ["5. Contenido", "Si, completo (Content Engine + Filmmaker + Disenadora)", "Si, mas angosto \u2014 piezas que empujan streaming, sin produccion de video musical"],
        ["6. Marketing Tradicional y Digital", "Si, completo", "Si, mas agente de booking activo (no incluido en Elite 360)"],
        ["7. Pauta", "Si, Meta Ads gestionado incluido", "Si, gestion incluida \u2014 gasto publicitario real cobrado aparte en ambos"],
        ["Inversion de catalogo / produccion de video / legal / financiamiento", "Si, exclusivo de Elite 360", "No incluido \u2014 el artista no entra al catalogo del sello"],
    ])
    add_body(doc,
        "La diferencia de precio no es una inconsistencia: Elite 360 construye un artista de cero dentro del roster "
        "propio, con inversion de catalogo y produccion de video incluidas; Representacion/Entrada a Mercado abre un "
        "mercado nuevo para un artista externo que ya tiene carrera, catalogo y equipo propio en otro lugar \u2014 son dos "
        "profundidades del mismo metodo, no dos productos que compiten por el mismo cliente."
    )

    # 4. Cierre
    style_heading(doc.add_paragraph(), "4. SEGUNDO PILAR DE LA METODOLOGIA PROPIA", 14, VIOLETA)
    add_body(doc,
        "Junto con la metodologia de composicion con neurociencia (el documento hermano de este, con un caso real ya "
        "aplicado: Mosco Cana Brava) y la metodologia de lanzamiento de canciones (Metodologia_Lanzamiento_Canciones_"
        "IM_Music.docx, tambien hermano de este), este documento formaliza el segundo pilar de \u201cla metodologia propia "
        "del fundador\u201d: como se construye, de principio a fin, la marca de un artista \u2014 distinto de como se escribe "
        "una cancion y distinto de como se lanza una cancion especifica una vez que la marca ya existe. Igual que el "
        "resto de este Data Room, esta sujeto a revision del fundador antes de cualquier uso o presentacion externa "
        "como documento cerrado."
    )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT_PATH))
    print(f"OK: {OUT_PATH} ({OUT_PATH.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
