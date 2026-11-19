"""Formaliza la metodologia de lanzamiento de canciones de IM Music.
Nuevo documento (2026-11-19), separado de Metodologia_Construccion_Marca_Artista_IM_Music.docx
por correccion del fundador: lanzar un sencillo es una herramienta tactica de 90
dias, distinta de construir la marca de un artista. Contenido generalizado del
caso real de "Adicto" (La S) - se elimino el nombre del artista, el concepto de
marca especifico y la letra de la cancion; se conserva la arquitectura, los
tiempos y los principios psicologicos con sus citas academicas reales."""
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "docs" / "sello_plan" / "data_room" / "Metodologia_Lanzamiento_Canciones_IM_Music.docx"

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


def add_callout(doc, title, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run(title + " — ")
    r.bold = True
    r.italic = True
    r.font.name = BODY_FONT
    r.font.size = Pt(10)
    r.font.color.rgb = VIOLETA
    r2 = p.add_run(text)
    r2.italic = True
    r2.font.name = BODY_FONT
    r2.font.size = Pt(10)
    r2.font.color.rgb = GRIS_TEXTO
    return p


def add_table(doc, header, rows):
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
    style_heading(p2, "METODOLOGIA DE LANZAMIENTO DE CANCIONES", 16, VIOLETA, space_before=0, space_after=6, align_center=True)
    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = p3.add_run(
        "Arquitectura de 5 fases, 90 dias, 100% organica — generalizada de un caso real ejecutado por el fundador. "
        "Herramienta tactica de campana, distinta de la construccion de marca del artista."
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
        "ACTIVO DE MARCA / PROPIEDAD INTELECTUAL INTERNA — NO DISTRIBUIR EXTERNAMENTE SIN REVISION DEL FUNDADOR. Este "
        "documento se separa de Metodologia_Construccion_Marca_Artista_IM_Music.docx por correccion explicita del "
        "fundador: lanzar una cancion no es una etapa de construccion de marca, es una campana tactica de 90 dias que "
        "se activa cada vez que un artista — del roster propio o de Representacion/Entrada a Mercado — publica un "
        "sencillo nuevo. Generalizado del caso real de “Adicto” (La S): se elimino el nombre del artista, el "
        "concepto de marca especifico y la letra de la cancion; se conserva la arquitectura, los tiempos y los "
        "principios psicologicos, reutilizables para cualquier sencillo futuro de cualquier genero. No es una obra "
        "con derechos de autor registrados a la fecha; su proteccion hoy es de secreto comercial/know-how interno."
    )
    rd.font.name = BODY_FONT
    rd.font.size = Pt(9.5)
    rd.font.color.rgb = ROJO
    rd.bold = True

    # 0. Que es
    style_heading(doc.add_paragraph(), "0. QUE ES ESTE DOCUMENTO Y DONDE ENCAJA", 14, VIOLETA)
    add_body(doc,
        "Este framework es una herramienta tactica, no un sustituto de la construccion de marca del artista (ver el "
        "documento hermano Metodologia_Construccion_Marca_Artista_IM_Music.docx). Se activa en un momento especifico: "
        "cuando un artista con marca ya en desarrollo lanza una cancion nueva. En terminos del metodo de 7 etapas del "
        "documento hermano, esta campana se ejecuta DENTRO de la Etapa 5 (Contenido) y de la Etapa 7 (Pauta) — es, en "
        "la practica, la cadencia y la psicologia especifica que toma el contenido y, opcionalmente, la pauta paga, "
        "durante los 90 dias alrededor de un lanzamiento. No reemplaza el Diagnostico, la Investigacion, el Lenguaje y "
        "Comunicacion ni la Identidad de Artista — los asume ya resueltos por el metodo de marca.",
        space_after=8
    )
    add_body(doc,
        "Honestidad sobre el estado de esta pieza: el framework se diseno para “Adicto”, la cancion de La S — el "
        "unico artista con el que el sello exploro una relacion hasta la fecha. Como ya establece el plan de negocios "
        "(Seccion 1), esa relacion “no se concreto en una colaboracion activa”: el framework esta disenado y lo "
        "suficientemente detallado como para ejecutarse, pero no hay todavia una cancion lanzada con el de principio a "
        "fin ni metricas reales de resultado. Es metodo real y usable, no ejecucion ya demostrada con resultados."
    )

    # 1. Resumen
    style_heading(doc.add_paragraph(), "1. RESUMEN DE LA ARQUITECTURA", 14, VIOLETA)
    add_body(doc, "Principio rector de toda la arquitectura:", space_after=4)
    add_body(doc,
        "la anticipacion libera mas dopamina que la recompensa misma (Wolfram Schultz, Cambridge): el sistema de "
        "recompensa dopaminergico se activa mas intensamente durante la espera que durante el evento. Las 5 fases "
        "estan disenadas para maximizar la anticipacion antes de dar la recompensa, y luego sostener el enganche "
        "durante 60+ dias despues del lanzamiento.", italic=True
    )
    add_table(doc, ["Fase", "Duracion", "Objetivo"], [
        ["Fase 1 — Tension y expectativa", "Dias 1-7", "Crear necesidad antes de que exista el lanzamiento — ver detalle en 2.1"],
        ["Fase 2 — El Dia D", "Dia 14", "Lanzamiento como evento, secuencia cronometrica en todas las plataformas el mismo dia (Peak-End Rule de Kahneman: el pico emocional y el cierre son lo que la audiencia recuerda)"],
        ["Fase 3 — Trafico 1", "Dias 15-21", "Llevar a quienes ya conocen al artista de vuelta a las plataformas de streaming (Mere Exposure Effect de Zajonc: mas exposicion = mas gusto)"],
        ["Fase 4 — Trafico 2", "Dias 22-35", "Abrir 4 puertas de entrada distintas para 4 audiencias distintas, cada una activando un algoritmo diferente sin pauta paga (Context Effect / Reframing)"],
        ["Fase 5 — Sostenimiento", "Dias 36-90+", "60+ dias de refuerzo impredecible — version acustica, remix, testimonios reales, mini documental — para que la cancion se vuelva un himno permanente, no un pico de un dia (Variable Reward Schedule de Skinner)"],
    ])

    # 2. Fase 1 detalle
    style_heading(doc.add_paragraph(), "2.1 Fase 1, dia a dia (Dias 1-7): Tension y Expectativa", 12, NEGRO, space_before=10)
    add_body(doc,
        "Regla general: nunca revelar mas del 30% de la informacion por pieza de contenido. El objetivo psicologico es "
        "el Efecto Zeigarnik (el cerebro recuerda mejor lo inacabado, Zeigarnik 1927) combinado con el Curiosity Gap de "
        "George Loewenstein (Carnegie Mellon): la tension entre lo que sabemos y lo que queremos saber. Cada dia tiene "
        "una funcion psicologica distinta, no es solo “publicar contenido”:", space_after=8
    )
    add_bullet(doc, "una pieza corta (12-15 segundos), sin contexto, sin revelar que es un lanzamiento proximo — solo una fraccion de la cancion o del proceso, sin explicacion. Corte abrupto. El objetivo es generar la primera pregunta en la mente del oyente, sin responderla.", bold_lead="Dia 1 — El teaser sin contexto: ")
    add_bullet(doc, "una pregunta abierta dirigida a la audiencia (via sticker de pregunta en redes), y el artista responde publicamente a las primeras respuestas reales. El objetivo es activar participacion antes de pedir nada, y generar la sensacion de comunidad (“este es de los nuestros”).", bold_lead="Dias 2-3 — La pregunta que involucra: ")
    add_bullet(doc, "mostrar el proceso creativo sin mostrar el resultado — el artista trabajando, sin que la camara revele el contenido completo. El objetivo es prueba de autenticidad/esfuerzo sin dar aun informacion consumible.", bold_lead="Dia 4 — El proceso sin resultado: ")
    add_bullet(doc, "presencia fisica real en la comunidad/barrio/escena del artista, estilo documental, con gente real de fondo. El objetivo es anclar el lanzamiento a un lugar y una comunidad reales, no a una produccion aislada.", bold_lead="Dia 5 — Presencia fisica y comunidad: ")
    add_bullet(doc, "primera vez que se revela informacion concreta (un fragmento breve a volumen alto, luego silencio, luego el nombre de la pieza y la fecha). El objetivo es convertir siete dias de tension acumulada en una fecha concreta que la audiencia ya quiere.", bold_lead="Dias 6-7 — El preview y la fecha: ")
    add_body(doc,
        "Lo que NUNCA se hace en la Fase 1 (reglas negativas, igual de importantes que las positivas): anunciar "
        "“nueva cancion proxima” de forma generica, usar hashtags en la primera semana, dar la fecha antes del dia "
        "6-7, responder comentarios con palabras en vez de manejar la expectativa, o mostrar contenido completo antes "
        "del lanzamiento."
    )
    add_callout(doc, "NEUROCIENCIA APLICADA · FASE 1",
        "Efecto Zeigarnik + Curiosity Gap + dopamina anticipatoria. Cada video termina sin resolver. Dar siempre el "
        "30% de informacion, nunca el 100%. La anticipacion dopaminergica hace el resto."
    )

    # 2.2 Fase 2
    style_heading(doc.add_paragraph(), "2.2 Fase 2 (Dia 14): El Dia D", 12, NEGRO, space_before=10)
    add_body(doc,
        "Un evento, no una cancion. Secuencia cronometrica en todas las plataformas el mismo dia:", space_after=8
    )
    add_table(doc, ["Hora", "Accion", "Detalle"], [
        ["6:00 AM", "Spotify + DSPs live", "Confirmar que la cancion esta live. Story inmediata con screenshot. CTA: “GUARDENLA”, no solo “dale play”."],
        ["9:00 AM", "TikTok — reaccion real", "El artista escuchando la cancion en vivo. El sound disponible para duetos. Stitch abierto. Link en bio."],
        ["12:00 PM", "YouTube — video oficial", "Video completo en la estetica visual del artista. Pinned comment con link de Spotify."],
        ["3:00 PM", "IG Feed — manifiesto", "Carrusel de 3 slides: foto cinematografica + arte del single + coro/hook como arte visual."],
        ["6:00 PM ★", "IG Live — PICO EMOCIONAL", "30 min, estructura en la Tabla 2.2.1 abajo."],
        ["9:00 PM", "Street marketing — CIERRE", "Presencia fisica real en la comunidad del artista. Parlante con la cancion. Reacciones reales. El circulo narrativo se cierra."],
    ])
    style_heading(doc.add_paragraph(), "2.2.1 Guion del Live de las 6PM — estructura de 30 minutos", 11, NEGRO, space_before=6)
    add_table(doc, ["Minuto", "Momento", "Que pasa"], [
        ["0-3", "La espera", "El artista aparece sin decir nada. Musica de fondo muy baja. El silencio crea tension."],
        ["3-5", "El reconocimiento", "Leer nombres de quienes estan en el chat. Personalizacion = fidelidad."],
        ["5-10", "La historia detras", "El origen emocional de la cancion. No el proceso tecnico — la historia de vida. Maximo 5 minutos."],
        ["10-13", "La escucha colectiva", "Pone la cancion en el parlante. La audiencia la escucha en tiempo real con el artista. ESTE ES EL PICO EMOCIONAL."],
        ["13-25", "Los comentarios reales", "Leer y responder comentarios. Los mas potentes en voz alta. Prueba social en tiempo real."],
        ["25-28", "El save colectivo", "“Ahora mismo, abran Spotify y guardenla. 1, 2, 3 — guardenla.” Accion colectiva = senal algoritmica masiva."],
        ["28-30", "El cierre memorable", "La frase final. Corte abrupto. El final que el cerebro recordara junto al pico emocional."],
    ])
    add_callout(doc, "NEUROCIENCIA APLICADA · FASE 2",
        "Peak-End Rule (Kahneman, Nobel 2002): la memoria de una experiencia esta determinada por como se sintio en su "
        "momento mas intenso y en su ultimo momento. El pico es el Live. El cierre es el street marketing de las 9PM. "
        "Todo lo demas es preparacion para esos dos momentos."
    )

    # 2.3 Estrategia Spotify
    style_heading(doc.add_paragraph(), "2.3 Capa tecnica: estrategia de Spotify (aplica a toda la campana)", 12, NEGRO, space_before=10)
    add_body(doc,
        "Spotify no mide popularidad — mide senales de calidad. Un artista con pocos streams pero alto porcentaje de "
        "guardados (saves) supera algoritmicamente a uno con muchos streams y bajo porcentaje de guardados. Las 5 "
        "senales, de mayor a menor peso:", space_after=8
    )
    add_table(doc, ["Senal", "Peso", "Que pedir a la audiencia"], [
        ["Guardar a biblioteca (save)", "Maximo", "CTA siempre “guardenla”, nunca solo “dale play” — es la senal #1 del algoritmo"],
        ["Completion rate", "Alto", "Enganchar en los primeros 5 segundos para que escuchen la pieza completa"],
        ["Compartir desde dentro de la app", "Alto", "Pedir que compartan desde Spotify a WhatsApp/Stories, no el link externo"],
        ["Velocidad en las primeras 24h", "Medio", "Concentrar a la comunidad para escuchar el mismo dia del lanzamiento"],
        ["Repeticion de escucha", "Medio", "El contenido de Trafico 1 existe para generar razones reales de volver a escuchar"],
    ])
    add_body(doc,
        "Checklist tecnico pre-lanzamiento: subir al distribuidor minimo 7 dias antes (nunca el mismo dia — es el "
        "error mas comun de artistas emergentes, porque para entonces Spotify ya no lo considera nuevo y los editores "
        "ya cerraron las playlists de esa semana), hacer el pitch editorial completo en Spotify for Artists, optimizar "
        "el perfil (foto, bio, Canvas activado), crear un Smart Link a todas las plataformas, y activar Spotify "
        "Canvas (un video loop corto en la estetica del artista — genera 145% mas shares que un perfil sin el)."
    )
    add_body(doc,
        "Playlists objetivo: editoriales, via pitch manual (la principal del genero en el mercado local, playlists de "
        "artistas emergentes del pais, playlists de lanzamientos nuevos semanales, playlists de expansion regional del "
        "genero) y algoritmicas, automaticas con senales (Release Radar al lanzamiento, Discover Weekly activado con "
        "saves altos en las primeras 48h, Daily Mix de quienes guardaron la cancion, y la “radio” del artista, que se "
        "construye con streams repetidos)."
    )

    # 2.4 Fase 3 y 4
    style_heading(doc.add_paragraph(), "2.4 Fase 3 (Dias 15-21): Trafico 1", 12, NEGRO, space_before=10)
    add_body(doc,
        "El contenido de esta fase no busca nuevos seguidores — genera razones para que quienes ya conocen la "
        "cancion vuelvan a escucharla: prueba social en tiempo real (el artista leyendo comentarios reales en voz "
        "alta), desglose de la letra en formato “fake podcast”, y un challenge de participacion con un sound propio "
        "en TikTok, donde cada video del challenge es distribucion organica a nuevas audiencias."
    )
    add_callout(doc, "NEUROCIENCIA · FASE 3",
        "Mere Exposure Effect (Zajonc, 1968): cuanto mas se expone alguien a algo, mas lo valora. Una cancion que "
        "alguien escucha 5 veces le gusta mas que la primera vez. Cada vuelta a Spotify es un stream, un save, una "
        "senal positiva."
    )
    style_heading(doc.add_paragraph(), "2.5 Fase 4 (Dias 22-35): Trafico 2 — los 4 angulos de entrada", 12, NEGRO, space_before=10)
    add_body(doc,
        "4 puertas de entrada distintas para 4 audiencias distintas, cada una activando un algoritmo diferente sin "
        "gastar un peso en pauta:", space_after=8
    )
    add_table(doc, ["Audiencia", "Hook", "Algoritmo que activa"], [
        ["Fitness / Motivacion", "Encuadre de disciplina y esfuerzo que conecta con el mensaje de la cancion", "Gym, boxeo, emprendimiento, disciplina"],
        ["Fans del genero musical", "Posicionamiento de “algo diferente esta pasando” en la escena local del artista", "Fans del genero y la escena local, nuevos artistas"],
        ["Fans de un artista colaborador", "Dueto o reaccion de otro artista — acceso directo a su audiencia", "Seguidores del artista colaborador"],
        ["Gente de la comunidad del artista", "Reacciones reales de personas que escuchan la cancion por primera vez sin guion", "Contenido autentico, organico, local"],
    ])
    add_callout(doc, "NEUROCIENCIA · FASE 4",
        "Context Effect / Reframing: el cerebro evalua la novedad en relacion al contexto, no al contenido absoluto. "
        "La cancion es completamente nueva para millones de personas que aun no la conocen — cada puerta la presenta "
        "en un contexto distinto."
    )

    # 2.6 Fase 5
    style_heading(doc.add_paragraph(), "2.6 Fase 5 (Dias 36-90+): Sostenimiento — el himno permanente", 12, NEGRO, space_before=10)
    add_body(doc,
        "El objetivo del sostenimiento no es conseguir mas streams. Es que la cancion se convierta en el himno que la "
        "audiencia escucha en un momento especifico de su vida. Una vez que eso pasa, la cancion vive para siempre "
        "independientemente del algoritmo. El sostenimiento debe ser impredecible — 4 formatos distintos en semanas "
        "distintas:", space_after=8
    )
    add_table(doc, ["Semana", "Formato", "Que hace"], [
        ["6-7 (Dias 36-49)", "Version acustica", "El artista canta la cancion sin produccion, en un espacio intimo. Nuevo ciclo de algoritmo en YouTube."],
        ["8-9 (Dias 50-63)", "Remix / feat estrategico", "Siembra → reveal del feat → preview breve → lanzamiento. Reactiva la psicologia de la Fase 1. Nuevo ciclo en Spotify."],
        ["10-11 (Dias 64-77)", "Testimonios reales", "Pregunta en stories sobre que significo la cancion para la audiencia — mini videos de 30 seg con personas reales contando su historia."],
        ["12+ (Dias 78-90+)", "Mini documental", "10-15 minutos en YouTube: origen, proceso, impacto, lo que viene. Contenido evergreen que trae trafico indefinidamente."],
    ])
    add_body(doc,
        "Estructura del mini documental: apertura con el contraste entre el antes y el ahora del artista; Acto 1 "
        "(0-3 min) el origen, que momento de vida inspiro la cancion; Acto 2 (3-8 min) el proceso, el estudio y los "
        "meses de trabajo; Acto 3 (8-13 min) el impacto, testimonios y numeros reales; Acto 4 (13-15 min) lo que "
        "viene, sembrando el proximo lanzamiento."
    )
    add_callout(doc, "NEUROCIENCIA APLICADA · FASE 5",
        "Variable Reward Schedule (B.F. Skinner): las recompensas variables generan el mayor nivel de enganche "
        "sostenido. El sostenimiento impredecible mantiene al cerebro en estado de alerta permanente, y el priming "
        "musical hace que cada escucha del hook se asocie emocionalmente con la identidad de marca del artista."
    )

    # 3. Reglas de oro
    style_heading(doc.add_paragraph(), "3. LAS REGLAS DE ORO DE LA ESTRATEGIA COMPLETA", 14, VIOLETA)
    add_bullet(doc, "pedir SIEMPRE “guardenla”, nunca solo “dale play”.", bold_lead="El save supera al stream: ")
    add_bullet(doc, "nunca el mismo dia del lanzamiento.", bold_lead="El pitch editorial de Spotify va 7 dias antes: ")
    add_bullet(doc, "el algoritmo premia la conversacion activa.", bold_lead="Responder TODOS los comentarios en las primeras 2 horas de cada post: ")
    add_bullet(doc, "en la Fase 1.", bold_lead="Nunca revelar mas del 30% de informacion por pieza de contenido: ")
    add_bullet(doc, "no puede fallar — es el pico emocional de toda la campana.", bold_lead="El Live del Dia D: ")
    add_bullet(doc, "activarlo antes del lanzamiento — genera 145% mas shares.", bold_lead="El Canvas de Spotify: ")
    add_bullet(doc, "que este disponible como sound desde el Dia D — es el activo viral de TikTok.", bold_lead="El hook/coro de 15 seg: ")
    add_bullet(doc, "no es opcional — es donde se construye el himno permanente.", bold_lead="El sostenimiento de 60 dias: ")
    add_bullet(doc, "sigue trayendo trafico meses despues — es contenido evergreen.", bold_lead="El mini documental de la semana 12: ")
    add_bullet(doc, "usar los 4 angulos de la Fase 4 para maxima cobertura organica.", bold_lead="Cada puerta de entrada activa un algoritmo diferente: ")
    add_body(doc, "Metricas a monitorear durante toda la campana: saves en Spotify (senal #1 del algoritmo), completion rate, shares desde dentro de Spotify, retention rate en YouTube, usos del sound propio en TikTok, y comentarios organicos sin CTA explicito.")

    # 4. Cierre
    style_heading(doc.add_paragraph(), "4. TERCER PILAR DE LA METODOLOGIA PROPIA", 14, VIOLETA)
    add_body(doc,
        "Junto con la metodologia de composicion con neurociencia (caso real: Mosco Cana Brava) y la metodologia de "
        "construccion de marca de artista (las 7 etapas que ya ejecuta Elite 360), este documento formaliza el tercer "
        "pilar de “la metodologia propia del fundador”: como se lanza tacticamente una cancion especifica, una vez "
        "que la marca del artista ya existe y la cancion ya esta compuesta. Se activa para cualquier artista del "
        "roster o de Representacion/Entrada a Mercado que tenga un lanzamiento de sencillo, dentro de las Etapas 5 "
        "(Contenido) y 7 (Pauta) del metodo de marca. Igual que el resto de este Data Room, esta sujeto a revision del "
        "fundador antes de cualquier uso o presentacion externa como documento cerrado."
    )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT_PATH))
    print(f"OK: {OUT_PATH} ({OUT_PATH.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
