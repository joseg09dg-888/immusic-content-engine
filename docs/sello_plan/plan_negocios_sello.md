# PLAN DE NEGOCIOS: IM MUSIC — SELLO DISCOGRÁFICO INDEPENDIENTE

**Versión:** 1.0 (sello como negocio autónomo, independiente de Intelligent Markets)
**Escenarios de mercado evaluados:** Medellín, Colombia / Dubái, Emiratos Árabes Unidos (EAU)

---

## 1. RESUMEN EJECUTIVO

IM Music es un sello discográfico independiente de vocación global y multigénero. No está limitado a un género ni a un idioma. Tiene una identidad de marca propia ya desarrollada y en uso real ("REBEL LUXURY": violeta #5E17EB, tipografías Sceageus/Anton, cuenta @immusicsello). A diferencia del plan anterior, este documento presenta a IM Music como negocio autónomo, sin fusión operativa ni financiera con ninguna agencia de marketing: todo ingreso, costo y función descrita aquí pertenece exclusivamente a la actividad de sello discográfico.

IM Music todavía no tiene artistas firmados. No hay catálogo propio activo ni artista bajo contrato a la fecha de este plan; el roster está por construirse desde cero. La única relación con un artista explorada hasta ahora ("LA S — EL DIABLO DEL CHANTEO") no se concretó en una colaboración activa. Lo que sí existe y es verificable hoy: la identidad de marca REBEL LUXURY en uso real, el acuerdo de distribución vigente con Nexus (8% de comisión) listo para cuando haya catálogo que distribuir, y un Content Engine propio ya construido y funcionando (investigación, redacción, diseño gráfico, video y voz sintética automatizados en Python con Pillow, FFmpeg y edge-tts) que reemplaza gran parte del gasto tradicional en producción de contenido y equipo creativo de un sello de este tamaño. Esto último es la ventaja estructural real del proyecto.

Este plan evalúa dos escenarios de sede/mercado para la operación y expansión del sello:

- **Medellín, Colombia:** mercado de origen y base operativa, con ecosistema de música urbana/latina consolidado y entidades de gestión de derechos (SAYCO, ACINPRO) operando hace décadas. Es el punto de partida geográfico, no un límite del género o idioma del roster.
- **Dubái, EAU:** mercado emergente con señales de demanda de música latina/urbana (presencia creciente de eventos y headliners latinos) y marco fiscal corporativo favorable, pero con infraestructura de derechos musicales locales recién creada y sin cifras país-específicas verificables en reportes de industria.

Este documento cubre la tesis de negocio, el mercado, la operación, el equipo, los riesgos y los aspectos legales de cada escenario. Se apoya en siete documentos complementarios que no se repiten aquí por extensión pero son parte integral del paquete completo:

- **Modelo Financiero IM Music — Sello** (Medellín + Dubái completo) y **Modelo Financiero IM Music — Sello — Dubái (Lean)**: CAPEX, OPEX, punto de equilibrio, flujo de caja y TIR/VAN de cada escenario.
- **Manual de Funciones y Procesos IM Music**: las fases, herramientas, métricas y automatizaciones de cada uno de los ocho roles del equipo.
- **Flujos de Decisión y Herramientas IM Music**: los flujos paso a paso ("si pasa A, se hace X; si pasa B, se hace Y") de los cinco procesos críticos del negocio, y el stack tecnológico completo.
- **Matriz de Riesgos IM Music**: 61 riesgos específicos con probabilidad por impacto, responsable y, en 18 casos, un precedente real documentado de otro sello o distribuidor.
- **Plan de Negocios IM Music — Elite Artist Platform** y su **Modelo Financiero**: documentos separados, negocio distinto pero conectado. La plataforma SaaS es donde vive el motor de ingreso masivo del ecosistema (Básico/Pro) y donde se vende el tier Élite 360; el sello es quien lo entrega. Los números de la plataforma no se repiten aquí para evitar doble conteo de ingresos y costos (ver Sección 10).

---

## 2. DESCRIPCIÓN DE LA EMPRESA

**Nombre:** IM Music

**Misión (global):** democratizar el desarrollo real de artistas, el mismo nivel de estrategia de marca, tecnología y acompañamiento que antes solo tenían los artistas de un sello grande con presupuesto grande, para dos públicos distintos y por razones distintas:

Para los artistas emergentes, porque la barrera que los detiene no es el talento. Es la falta de conocimiento, acceso y capital, el mismo problema de fondo que ya identificó el libro "Music Business Para Todos Los Humanos" del propio sello. "Jaqueamos mentes" significa, en la práctica, pelear contra esa asimetría de información que ha dejado a generaciones de artistas firmando contratos que no entendían, o sin saber cómo construir una carrera real.

Para los artistas ya posicionados, el problema ya no es el acceso, es la eficiencia y el techo de crecimiento. Un artista con tracción real suele quedar atrapado entre hacerlo todo solo (sin apalancamiento tecnológico) o entrar a la maquinaria lenta y poco flexible de un sello grande. IM Music ofrece el nivel de ejecución tecnológica de un sello grande (el Content Engine) con la atención boutique de un equipo pequeño (Élite 360), sin pedirle al artista que ceda el control de su obra.

**Visión (global):** ser el sello independiente de referencia a nivel global, sin limitarse a un género, idioma, etapa de carrera ni mercado, reconocido por aplicar con rigor una metodología de desarrollo de marca que funciona igual para un artista emergente que para uno posicionado, y por construir, junto a su propia plataforma SaaS, la infraestructura que permite escalar ese desarrollo a miles de artistas sin perder el criterio humano que lo hace funcionar.

La marca REBEL LUXURY no es solo estética. "Jaqueamos mentes" es una postura: cuestionar cómo se ha hecho la industria musical tradicionalmente, de forma opaca, lenta y extractiva con el artista, y demostrar con resultados reales que se puede hacer distinto. Eso conecta al sello, donde se prueba el modelo con artistas reales, con la plataforma, donde se escala, y con el libro, donde se explica la causa de fondo, como un solo proyecto y no como tres negocios sueltos.

### Misión y visión por mercado, y por qué no son la misma

**Medellín, Colombia.** La misión es construir y probar el modelo con artistas reales, en el mercado de origen, donde ya existe infraestructura de derechos consolidada (SAYCO, ACINPRO) y un ecosistema urbano/latino maduro que permite operar con bajo riesgo y costo conocido. La visión es ser el sello de referencia en Colombia por el rigor de su desarrollo de artista, demostrando con resultados medibles que la metodología escala. Esa es la base de evidencia que hace creíble todo lo demás, incluida la plataforma y la expansión a Dubái.

**Dubái, EAU.** Aquí la misión no es replicar Medellín, es crear la categoría de sello boutique multigénero en una región que todavía no tiene uno, aprovechando que es la de mayor crecimiento mundial en música grabada (MENA) y una de las concentraciones más altas del mundo de patrimonio privado, lo que abre líneas de ingreso premium (eventos, patrocinios de lujo) que en Medellín no existen de la misma forma. La visión es ser la primera infraestructura de referencia de música urbana/global en el Golfo, antes de que exista un competidor establecido: posicionamiento de pionero, no cuota de mercado.

Medellín trata de construir y validar, con mercado maduro, costo bajo, riesgo conocido y urgencia inmediata. Dubái trata de crear categoría, con mercado nuevo, costo alto, riesgo regulatorio y de demanda sin validar, y un upside premium si funciona. Forzar el mismo libreto en los dos contextos sería un error, porque cada uno exige decisiones de inversión, ritmo y métricas de éxito distintas. Por eso este plan las separa en todas las secciones (mercado, legal, financiero) en vez de promediarlas.

**Alcance de género, idioma y nacionalidad.** IM Music no es un sello de nicho urbano/latino. El roster se construye alrededor de géneros urbanos y latinos como punto de partida natural, dado el origen del sello en Medellín (R&B, jazz, rap, trap, reggaetón, salsa), pero se extiende deliberadamente a corridos y música regional mexicana, y a cualquier otro género que resulte una oportunidad real de desarrollo de artista. El idioma tampoco es una limitación: el sello trabaja en español, inglés y, según la oportunidad, otros idiomas relevantes para el mercado objetivo del artista. La sede de operación, Medellín o Dubái, es dónde está el equipo, no un filtro de qué artistas se pueden firmar. Un artista estadounidense, europeo o de cualquier otra nacionalidad que represente una buena oportunidad se firma igual, sin importar desde qué sede opere el sello en ese momento. La metodología de desarrollo de marca del fundador es agnóstica al género, idioma y origen del artista.

A diferencia del plan original, IM Music no depende de una agencia matriz para sus funciones de marketing, diseño o desarrollo de IA. Esas capacidades ya están internalizadas en el Content Engine del propio sello (ver Sección 3).

---

## 3. ESTRUCTURA ORGANIZACIONAL Y FUNCIONES

### 3.1 Principio rector

El sello se diseña deliberadamente lean: solo se contratan o se paga por proyecto aquello que el Content Engine no puede hacer, es decir, producción de audio, decisiones creativas, y relación humana con artistas y contrapartes legales o comerciales. Todo lo que es generación de contenido digital masivo o repetitivo, diseño gráfico de plantilla y voz en off ya está automatizado y operando (ver `src/content_engine/`, `src/core/brand.py`). Por eso no se presupuesta un Traficker de pauta ni un Desarrollador de IA como personal fijo o freelance recurrente: son funciones que el sistema ya cubre a costo marginal casi nulo.

Sí se presupuestan tres roles humanos adicionales que el Content Engine no puede reemplazar, porque son de dirección y criterio y no de ejecución repetitiva: la Comunicadora, el Filmmaker/Editor con IA y la Diseñadora Gráfica. La Comunicadora, a cargo de la estrategia de contenido, define qué se publica y cuándo: el plan editorial y la parrilla de contenido. El Content Engine ejecuta la generación, pero no decide la estrategia; alguien tiene que dirigirlo. El Filmmaker, que edita con IA, trabaja con el material humano real (grabaciones de los artistas, contenido tipo "CONTENIDO HUMANO" ya existente en el proyecto), distinto del video cien por ciento sintético que ya genera el Content Engine. Y la Diseñadora Gráfica se encarga del diseño a la medida para campañas, portadas y piezas que exceden el sistema de plantillas automatizado, que cubre el contenido recurrente pero no el trabajo creativo bespoke.

Los tres son **planta fija, no freelance**, por una razón principalmente operativa: el sello no solo construye marca de artista, necesita construir su propia marca como sello con la misma disciplina, y eso exige que quien ejecuta la metodología día a día esté disponible de forma constante y sincronizada con el resto del equipo — no por proyecto suelto, con la rotación y pérdida de consistencia de marca que eso implica. La metodología de desarrollo de marca y de composición ya está formalizada por escrito (ver Data Room), y cualquier colaborador que la use firma cláusula de confidencialidad — fijo o freelance por igual, ya que la protección legal bajo la Decisión 486 de 2000 depende del acuerdo firmado, no del tipo de vínculo laboral (ver `Proteccion_Marca_y_Metodologia_IM_Music.docx` y `Acuerdo_de_Confidencialidad_IM_Music.docx` en el Data Room). La planta fija es, por tanto, una decisión de control de calidad y disponibilidad operativa, no el mecanismo de protección de la metodología en sí.

El equipo que sí existe, fijo y freelance, no está ahí para hacer tareas sueltas. Está para ejecutar la metodología propia de desarrollo de marca de artista completo del fundador, el know-how diferencial del sello. Por eso el equipo debe ser propio y no tercerizado a una agencia externa: la metodología es el activo, y solo un equipo interno, entrenado directamente en ella, puede aplicarla de forma consistente en cada artista firmado.

### 3.2 Roles reales del sello

| Rol | Naturaleza | Función |
|---|---|---|
| CEO / Director del Sello | Fijo | Dirección general, A&R, relación con artistas e inversionistas, decisión final de catálogo |
| Gerente Comercial | Fijo o por comisión | Captación de artistas y clientes de producción, negociación de contratos, licencias y sync |
| Project Manager — Élite 360 | Fijo (cuando haya ocupación en el roster) | Coordina la entrega real del servicio 360 a cada artista del roster: management musical, producción de video, branding, Meta Ads gestionado, campamentos musicales. Convierte el contrato cerrado por el Gerente Comercial en ejecución concreta. |
| Productor Musical | Freelance por proyecto | Dirección creativa y producción de grabaciones |
| Ingeniero de Sonido | Freelance por proyecto | Grabación, mezcla y masterización |
| Social Media Manager | Fijo o part-time | Supervisión y curaduría del contenido generado por el Content Engine, interacción con comunidad; no genera contenido desde cero manualmente |
| Comunicadora / Estrategia de Contenido | Fijo | Plan editorial y parrilla de contenido; dirige al Content Engine, no lo reemplaza |
| Filmmaker / Editor con IA | Fijo | Edición de material humano real (grabaciones de artistas) con herramientas de IA, distinto del video sintético automatizado |
| Diseñadora Gráfica | Fijo | Diseño a la medida para campañas y piezas que exceden el sistema de plantillas automatizado |
| Función legal | Cubierta directamente por el CEO/Director | Contratos con artistas, derechos de autor, registro de marca, cumplimiento normativo. El fundador ya tiene esta capacidad, así que no se presupuesta como cargo ni retainer fijo; solo se contempla asesoría externa puntual para casos de alta complejidad, como litigios o estructuración en un segundo país |
| Contador | Asesor externo | Estados financieros, impuestos, nómina |

No hay junta directiva compartida con terceros. Las decisiones estratégicas las toma el CEO del sello, con el inversionista según los términos que se acuerden en la ronda de capital.

---

## 4. SERVICIOS

IM Music presta servicios exclusivamente a artistas, no a empresas ni marcas externas. Se elimina por completo la línea de "servicios de marketing para empresas" del plan anterior, que correspondía a la agencia.

- **Producción musical:** composición, arreglos, grabación, mezcla y masterización, para artistas del roster propio y para artistas externos que contratan el servicio por proyecto.
- **Desarrollo de marca personal:** identidad visual y narrativa del artista, aplicando la misma metodología de marca que ya usa IM Music internamente.
- **Distribución digital:** vía el acuerdo vigente con Nexus (8% de comisión) a plataformas de streaming como Spotify, Apple Music, YouTube Music y Deezer.
- **Estrategia de contenido y presencia digital:** apalancada en el Content Engine propio, con generación asistida de piezas para redes, guiones y calendarización, a una fracción del costo de contratar un equipo creativo tradicional.
- **Asesoría legal y de derechos de autor:** gestión de registro de obras y relación con las sociedades de gestión colectiva correspondientes a cada mercado.
- **Gestión de regalías:** seguimiento de regalías de master y publishing del catálogo propio y de los artistas producidos.
- **Alianza o firma de un streamer:** acuerdo con un creador de contenido en vivo en Twitch, Kick o YouTube Live. El sello financia o cofinancia su setup de transmisión (cámara, capturadora, micrófono, iluminación, PC si aplica) a cambio de exposición constante de la marca IM Music y de los artistas del roster dentro de su contenido en vivo. Es, ante todo, una inversión de marketing y exposición masiva, no una línea de servicio tradicional. El streamer no reemplaza al Content Engine, lo complementa con presencia en vivo y comunidad activa que el contenido automatizado no puede replicar.
- **Representación / Entrada a Mercado:** servicio distinto de Élite 360, para artistas externos al roster, ya establecidos en otro país o ciudad, que quieren entrar a un mercado nuevo (Colombia, y a futuro Dubái) sin unirse al catálogo del sello. Alcance más angosto que Élite 360: diagnóstico del estado digital actual del artista, ordenamiento del sistema visual existente (sin rehacer su identidad), estrategia de contenido orientada a streaming, y un agente de booking que contacta activamente festivales y venues en el mercado de destino. No incluye producción de videos musicales, inversión en catálogo, asesoría legal ni financiamiento — eso es exclusivo de Élite 360. Dos modalidades, con precio real ya cotizado y validado con un caso concreto (ver Modelo Financiero, Sección 10 y el documento de metodología en el Data Room): **Servicio completo, $2.000 USD/mes** (IM Music arma y dirige el equipo, agente de booking activo, control total de calidad) y **Solo dirección, $1.000 USD/mes** (el artista o su equipo externo ejecuta, IM Music dirige estrategia y contenido — migrable a servicio completo). Pauta publicitaria, marketing físico y comisión de promotor en shows se cobran aparte en ambas modalidades, no están incluidos en el fee mensual.

**Por qué dos precios distintos para "desarrollo de artista" no es una inconsistencia:** Élite 360 ($2.999,99 USD/mes) es para un artista que se vuelve parte del roster — el sello invierte en su catálogo, produce sus videos, lo representa legalmente y lo desarrolla de cero. Representación/Entrada a Mercado ($1.000-$2.000 USD/mes) es para un artista que ya tiene carrera, catálogo y equipo propio en otro lugar, y que solo necesita que IM Music le abra puerta en un mercado nuevo — es logística y relaciones de industria, no desarrollo integral. Son dos productos con alcance distinto, no el mismo servicio con dos precios.

---

## 5. ANÁLISIS DE MERCADO

### 5.1 Medellín / Colombia

**Tamaño de mercado (TAM).** El mercado colombiano de música grabada facturó aproximadamente USD 105,2 millones en 2025, creciendo 17,9% y superando por primera vez los USD 100M (IFPI Global Music Report 2026, vía musicbusinessworldwide.com y forbes.pe). Latinoamérica fue la región de mayor crecimiento global por dieciséis años consecutivos, con +17,1% en 2025 tras +22,5% en 2024. El 78% de los ingresos de música grabada en Colombia proviene de streaming (Warner, vía La República).

**Mercado disponible (SAM).** De ese TAM, el segmento relevante para IM Music es música urbana/independiente autogestionada o gestionada por sellos boutique, no majors ni catálogo internacional. No existe una cifra oficial que aísle este subsegmento. Como supuesto a validar, se estima conservadoramente entre el 15% y el 25% del TAM colombiano, un rango de referencia de lo que representa la música urbana/latina dentro del consumo digital total en el país, sin fuente país-específica que lo confirme con exactitud. Se recomienda validar con Procolombia o Mincultura antes de usarlo en un pitch formal.

**Mercado obtenible (SOM).** Para un sello boutique que parte sin artistas firmados todavía, con producciones externas por proyecto como primera fuente de ingreso mientras se construye el roster, el SOM realista en los primeros uno a tres años es una fracción mínima del SAM. El objetivo no es capturar cuota de mercado agregada, sino construir un catálogo de tres a ocho artistas, de cualquier género, y un flujo estable de dos a cuatro proyectos de producción externa por mes (ver Sección 10). Cualquier proyección de ingresos agregados sobre el TAM/SAM total sería, a este tamaño de operación, una distorsión. El valor real está en el crecimiento del catálogo propio y su desempeño en streaming, no en la cuota de mercado.

**Competencia.** Los sellos multinacionales, Sony, Universal y Warner Colombia, tienen amplia red de distribución y capital, pero procesos burocráticos y menor flexibilidad con talento emergente. Los sellos independientes establecidos, como Codiscos y Discos Fuentes, tienen trayectoria y catálogo histórico, aunque menor enfoque en estrategia digital o IA. Las plataformas DIY, DistroKid, TuneCore y CD Baby, dan acceso a distribución global sin acompañamiento artístico, de marca ni de contenido: el artista hace todo el trabajo de desarrollo solo. IM Music se diferencia al juntar acompañamiento real de desarrollo artístico, producción profesional y un motor de contenido automatizado que reduce drásticamente el costo de mantener presencia digital constante, algo que ni los sellos independientes tradicionales ni las plataformas DIY ofrecen juntos.

### 5.2 Dubái / EAU

**Tamaño de mercado (TAM).** No existe una cifra de ingresos de música grabada específica para EAU en los reportes de industria accesibles. El dato disponible es regional: MENA fue la región de mayor crecimiento mundial en música grabada tanto en 2024 (+22,8%, ingresos ~USD 144M) como en 2025 (+15,2%, con ~97,5% de participación de streaming), según el IFPI Global Music Report 2025/2026. Esta es una limitación real de los datos, no un supuesto conservador: no hay forma de aislar el tamaño del mercado de EAU dentro de esa cifra regional sin acceso directo a las tablas completas de gmr.ifpi.org.

**Señales cualitativas de demanda, no cuantitativas.** J Balvin fue headliner de UNTOLD Dubai 2025, del 6 al 9 de noviembre, en su debut en EAU: evidencia de que el mercado latino/urbano ya es suficientemente relevante para traer a un headliner de ese perfil. Dubai Latin Fest se realiza anualmente, y existen noches recurrentes de reggaetón y música latina en clubes de la ciudad. Estas señales indican demanda en vivo creciente, pero no sustituyen datos de streaming o ventas que permitan calcular un SAM/SOM confiable para EAU.

**Infraestructura de derechos musicales.** EAU licenció su primera sociedad de gestión de derechos musicales, EMRA (Emirates Music Rights Association), el 10 de abril de 2025, bajo la Ley Federal 38/2021. Sus tarifas comerciales entran en vigor en diciembre de 2026. Esto significa que, a la fecha de este plan, no existe un historial de recaudación de regalías locales equivalente a SAYCO/ACINPRO. Cualquier proyección de ingresos por regalías locales en EAU debe tratarse como especulativa hasta que EMRA tenga al menos un ciclo de operación comercial completo.

**Competencia.** No se identificó, en esta investigación, un sello boutique multigénero con desarrollo de artista real operando desde EAU. Eso sugiere un espacio de posicionamiento abierto, pero también la ausencia de comparables para validar supuestos de mercado. La evidencia de demanda recogida, J Balvin y Dubai Latin Fest, es específica de música latina/urbana: es una señal de un género con tracción comprobada en la región, no una limitación del roster del sello a ese género.

**Oportunidad estratégica: crear la categoría, no competir en ella.** La ausencia de datos país-específicos y de un competidor boutique latino/urbano establecido en EAU no es solo una limitación de información. Es, en sí misma, la tesis de inversión de este escenario. EAU no tiene hoy un sello independiente de música urbana/latina de referencia, y su sociedad de gestión de derechos musicales apenas nace en 2025. Entrar ahora, en la región de mayor crecimiento mundial en música grabada, con una identidad de marca y un catálogo ya construidos en Colombia, no es llegar a competir por una porción de un mercado existente. Es la oportunidad de construir desde cero la infraestructura y la referencia de la industria de música latina/urbana en el Golfo, antes de que exista un incumbente. Ese es el atractivo real para un inversionista que busca una posición de pionero, no una cuota de mercado, y es distinto en naturaleza a la oportunidad de Medellín, que es un mercado maduro de crecimiento orgánico del catálogo propio.

Hay además una razón cualitativa, no cuantificada en este documento, para priorizar Dubái: es un mercado con una de las concentraciones más altas del mundo de patrimonio privado y gasto de lujo, hospitalidad, eventos, entretenimiento premium. Eso abre líneas de ingreso que van más allá de las regalías de streaming: eventos privados, patrocinios de marca y shows premium pagados directamente por un público con alto poder adquisitivo. Encaja de forma natural con el posicionamiento ya existente de la marca REBEL LUXURY. Pero es una tesis estratégica, no una cifra de mercado: no hay en este documento un dato verificado de gasto en entretenimiento musical de la población de alto patrimonio en EAU. Se señala como argumento cualitativo a favor del escenario, pendiente de cuantificar con investigación local antes de usarse como proyección de ingresos.

**Conclusión del análisis de mercado para Dubái.** La oportunidad es real a nivel de señales de demanda, entorno regulatorio y fiscal (ver Sección 11), y posicionamiento de pionero de categoría. Pero no se puede construir un TAM/SAM/SOM defendible para EAU con los datos públicos disponibles hoy. Se recomienda, si este escenario avanza, una investigación de mercado local pagada, o contacto directo con EMRA y promotores como Dubai Latin Fest y UNTOLD, antes de comprometer capital.

### 5.3 Casos de referencia: qué le pasó realmente a otros sellos independientes

Esta sección no es una lista decorativa. Cada caso real tiene al menos una decisión aplicable, positiva o negativa, a IM Music hoy, en la misma línea de lo que ya hace la Matriz de Riesgos con precedentes reales (Sección 8).

- **Rimas Entertainment (Puerto Rico, fundado 2014 por Noah Assad).** Empezó firmando a Jowell y Randy, descubrió a Bad Bunny en 2016 y hoy es el sello independiente más grande de música latina, con Bad Bunny produciendo el álbum en español más vendido de la historia en 2023. Lección aplicable: un solo artista bien desarrollado, no el tamaño del roster, puede sostener un sello independiente entero en sus primeros años — valida el enfoque de IM Music de calidad sobre volumen en el roster inicial. Riesgo real documentado: en enero de 2026, Bad Bunny y Rimas enfrentan una demanda de USD 16 millones por uso no autorizado de la voz de una persona en dos canciones (fuente: Billboard, vía cobertura de enero 2026) — aplica directamente al riesgo ya identificado en la Matriz de Riesgos sobre uso de voz/imagen sin autorización clara, y refuerza por qué el contrato `04_autorizacion_imagen_voz.md` del Data Room no es un trámite menor. Rimas también creció mediante adquisición de participación en otros sellos (Dale Play Records, 2025) en vez de solo desarrollo orgánico — un camino de crecimiento a considerar una vez el catálogo propio sea sólido, no antes.

- **White Lion Records (Puerto Rico, años 90).** Descubrió y lanzó a Daddy Yankee, Tego Calderón y Calle 13 antes de que el reggaetón fuera un género reconocido internacionalmente — el mismo tipo de apuesta temprana en talento sin categoría establecida que IM Music busca en su roster multigénero. Lección aplicable: un sello pequeño puede definir un género completo si firma primero y con convicción, no si espera validación externa del mercado.

- **Dirty Hit (Reino Unido, fundado 2009-2010 por Jamie Oborne).** Firmó a The 1975 y a Benjamin Francis Leftwich cuando, según su propio fundador, "nadie los quería firmar". Se mantuvo independiente usando distribución de terceros (Ingroves) y un acuerdo de licencia con Universal/Interscope solo para ciertos mercados, sin ceder el sello completo. Lección aplicable: depender de un distribuidor externo (como IM Music depende de Nexus) es compatible con mantener independencia real, siempre que el acuerdo de licencia sea específico y no total. Riesgo real: el propio fundador reconoce que gestiona tanto el sello como al artista principal (The 1975) y a otro artista (Jack Antonoff) a la vez — concentración de rol similar al riesgo ya identificado en la Matriz de Riesgos de "dependencia total del fundador".

- **Mad Decent (EE.UU., fundado 2006 por Diplo).** Pasó de tres personas en Filadelfia a veinte empleados mezclando sello, gira (Mad Decent Block Party) y un sub-sello incubadora (Jeffree's) que publicaba música gratis para detectar qué artista merecía un contrato formal, antes de comprometerse. Lección aplicable directa: Mad Decent validó el talento antes de invertir el contrato completo, el mismo principio que ya sigue IM Music al usar producción externa por proyecto (Sección 10.1) como forma de evaluar artistas antes de ofrecerles roster. Riesgo real documentado: en 2013 Mad Decent tuvo un problema de muestras (samples) no autorizadas en una canción, que el propio Diplo reconoció haber tenido que resolver después — aplica al mismo riesgo de autorización de uso de obra de terceros que ya cubre el Data Room.

- **300 Entertainment (EE.UU., fundado 2012 por Lyor Cohen y Kevin Liles).** Se convirtió en uno de los sellos independientes más exitosos del negocio con Megan Thee Stallion y Young Thug, y en 2021 fue adquirido por Warner Music Group por aproximadamente USD 400 millones, manteniendo su identidad y oficinas independientes dentro del grupo. Lección aplicable: una adquisición por un sello mayor manteniendo identidad operativa propia (no fusión total) es una salida de inversionista real y ya ejecutada en la industria, consistente con lo que ya plantea la Sección 13 de este plan.

- **La Industria Inc. (Puerto Rico/Panamá, Rauw Alejandro, Sech).** A diferencia de los anteriores, no es un sello totalmente independiente: sus lanzamientos se editan bajo "Sony Music Latin - La Industria", una alianza de distribución/gestión con una major, no una operación 100% propia. Lección aplicable como advertencia, no como modelo a replicar: cuando un sello boutique crece atado a una sola major para distribución y gestión, pierde parte del control que supuestamente lo diferencia de un sello grande — un argumento más a favor de que IM Music mantenga su acuerdo de distribución con Nexus como relación comercial específica (8% de comisión), no como fusión operativa, igual que hace Dirty Hit.

**Patrón que se repite en los seis casos:** ningún sello independiente de esta lista empezó con un roster grande. Todos crecieron apostando primero por uno o dos artistas con convicción (Rimas con Bad Bunny, Dirty Hit con The 1975, White Lion con Daddy Yankee), no diversificando el riesgo entre muchos artistas desde el día uno. Esto valida directamente la decisión ya tomada en este plan de construir un roster de tres a ocho artistas en los primeros años (Sección 5.1), en vez de intentar escalar el número de artistas antes de tener un caso de éxito propio y verificable.

### 5.4 Análisis competitivo detallado (DOFA individual por competidor)

Esta sección complementa el párrafo general de "Competencia" de las Secciones 5.1 y 5.2 con un análisis más profundo de competidores específicos en cuatro frentes: Medellín, Colombia nacional, mundial, y Dubái/EAU. Cada DOFA es del competidor como negocio propio (sus propias fortalezas, oportunidades, debilidades y amenazas), no un DOFA de IM Music frente a él. Donde la evidencia lo permite, se anota brevemente la implicación para IM Music. Cuando la información pública verificable no alcanza para construir un DOFA completo y honesto, este documento lo dice explícitamente en vez de rellenarlo con contenido genérico.

**Nota metodológica:** la investigación se hizo por búsqueda web en noviembre de 2026, en dos rondas — la segunda con técnicas más profundas (registro mercantil, LinkedIn, Spotify/sitios oficiales) después de que el fundador confirmara que los 3 competidores de Medellín son sellos reales aunque no aparecieran así en la primera búsqueda superficial. Para negocios pequeños o locales sin presencia digital fuerte, la ausencia de resultados no prueba que el negocio no exista — prueba que no se pudo verificar en esta ronda de investigación. Cada entrada cierra con una conclusión **"Cómo superar a [competidor]"**: una acción concreta y específica para IM Music basada en una brecha real detectada, no una generalidad.

**Estructura de 6 dimensiones por competidor:** cada entrada se analiza en Administrativo, Financiero, Legal, Comercial, Marketing y Tecnología, seguido del DOFA y la conclusión "Cómo superarlo". Donde falta evidencia pública verificable en una dimensión específica, se dice explícitamente en esa dimensión en vez de omitirla o rellenarla con contenido genérico.

#### Medellín — los 3 competidores puntuales señalados por el fundador

**Vion Music** (razón social probable: Vion Music Network S.A.S.)

| Dimensión | Hallazgos |
|---|---|
| **Administrativo** | Fundada por "Christian Hernández" (nombre solo aparece en la versión en español del sitio oficial, no en la versión en inglés). Sin tamaño de equipo, organigrama o estructura de gestión encontrados — LinkedIn de la empresa devolvió error de acceso (403), no se pudo confirmar headcount por esa vía. |
| **Financiero** | Clasificada como microempresa (Datacrédito Empresas, agregador privado). Sin capital social, ingresos o inversión levantada encontrados en ninguna fuente pública. |
| **Legal** | Constituida el 16-07-2015 en Medellín (dirección Calle 24 39 07) — dato de agregador privado, pendiente de verificar en RUES oficial (rues.org.co). Sin evidencia de contratos tipo artista; no se encontró ningún artista propio bajo contrato. |
| **Comercial** | Distribución global a 250+ plataformas vía plataforma propia (app.vionmusic.co); gestión y optimización de canales de YouTube (MCN); "producción y cinematografía profesional" para contenido; consultoría personalizada; "VION CLUB" (cursos y mentoría); programa VIP de "song pitching a majors" para sellos/estudios B2B. Sin precios públicos en ningún servicio. |
| **Marketing** | Sitio bilingüe ES/EN con inconsistencias de traducción entre versiones (el nombre del fundador solo aparece en una). Reclama "más de 15 años de experiencia", cifra que no cuadra con la constitución legal de 2015 (11 años) — posible exageración de marketing o experiencia previa del fundador antes de constituir la empresa. Cero artistas, lanzamientos, cifras de streams o testimonios nombrados en todo el sitio. |
| **Tecnología** | Plataforma de distribución propia (app.vionmusic.co). Ninguna mención de IA en ninguna parte del sitio oficial. |

| | Vion Music — DOFA |
|---|---|
| **Fortalezas** | Operación B2B ya resuelta (distribución propia a 250+ plataformas, MCN de YouTube) con alcance binacional Medellín-Tampa — más infraestructura de distribución construida que IM Music hoy. |
| **Debilidades** | Cero evidencia pública de un artista, catálogo o resultado propio en 11 años de operación — ni un nombre, ni una cifra de streams, ni un caso de éxito en todo su sitio oficial. Sin mención de IA ni de ningún proceso propietario; "producción profesional" es un término genérico sin diferenciación técnica visible. |
| **Oportunidades** | El programa VIP B2B ("song pitching a majors") sugiere que buscan posicionarse como puente hacia sellos grandes — un nicho de servicios que no compite directamente con el desarrollo de artista propio de IM Music. |
| **Amenazas** | Su escala de distribución (250+ plataformas, MCN activo) ya resuelve de entrada un problema que a IM Music le toma construir — si decidieran ofrecer desarrollo de marca integral (no solo distribución), competirían directo por el mismo cliente. |

*Cómo superar a Vion Music:* su mayor debilidad verificable es la ausencia total de prueba social — ningún artista, cifra o caso nombrado en 11 años. IM Music debe hacer exactamente lo contrario desde el día uno: publicar métricas y casos reales (como ya hace con Idania Dowman y el libro) de forma visible, porque un cliente que compare ambos sitios encontrará evidencia en uno y un vacío de resultados en el otro.

**Kaital Music → Kapital Music & Entertainment S.A.S.** (confirmado; la ortografía original llevaba a un resultado equivocado)

| Dimensión | Hallazgos |
|---|---|
| **Administrativo** | ~5 empleados reportados (EMIS, 2025). Su CEO y fundador, Fredy Marín, murió en accidente de tránsito en 2021 (El Peñol) — un evento de continuidad de liderazgo real, no hipotético, sin que se haya encontrado quién asumió la dirección desde entonces. |
| **Financiero** | Ventas netas creciendo 58,11% en 2024 (EMIS); utilidad neta reportada por debajo de $1.000 millones COP (Informa Colombia, cifra exacta tras paywall). Sin capital social reportado en las fuentes consultadas. |
| **Legal** | Kapital Music & Entertainment S.A.S., constituida el 17-04-2013 en Medellín (dirección Carrera 78 32F-21). Sin evidencia pública de contratos formales con artistas, aunque el catálogo histórico sugiere relaciones comerciales estables de largo plazo. |
| **Comercial** | Sello discográfico y estudio de producción de trap/reggaetón. Catálogo histórico verificado: Jowell y Randy, Arcángel, Kevin Roldán; vínculos actuales: Blessd, Kris R, ROA, Hades666, Luar La L. |
| **Marketing** | Presencia activa en Facebook, X/Threads y YouTube ("KapitalMusicTv"), se autodescribe como el sello "que define el estándar del trap en Colombia". Sin métricas de alcance de redes encontradas en esta ronda. |
| **Tecnología** | Ninguna evidencia pública encontrada de uso de IA, plataforma propia, o herramienta tecnológica diferenciadora. |

| | Kapital Music & Entertainment S.A.S. — DOFA |
|---|---|
| **Fortalezas** | Catálogo histórico verificable con artistas de impacto real (Arcángel, Kevin Roldán, Blessd) — una credibilidad de marca en la escena urbana de Medellín que IM Music, sin artistas firmados aún, no tiene. Crecimiento de ventas de +58% en 2024 indica negocio activo y en expansión, no estancado. |
| **Debilidades** | Equipo reportado de solo ~5 personas pese al catálogo — sugiere operación artesanal, no un motor de contenido/marketing escalable; sin evidencia pública de IA, metodología documentada, ni estrategia de contenido sistemática. La pérdida de su CEO fundador en 2021 es un riesgo de continuidad de liderazgo real que ya ocurrió, no hipotético. |
| **Oportunidades** | Ninguna identificada con evidencia directa en esta ronda — no hay información pública reciente (2025-2026) sobre su estrategia de crecimiento actual. |
| **Amenazas** | Más de 600 productoras musicales nuevas en Medellín entre 2011 y 2021 (La República) compitiendo por el mismo talento emergente y la misma atención del público urbano. |

*Cómo superar a Kapital Music:* no se puede competir en catálogo histórico (ellos ya tienen a Arcángel y Kevin Roldán, IM Music no tiene artistas firmados). La vía real es la escala de ejecución: un equipo de ~5 personas sin automatización no puede sostener el ritmo de publicación que exige el algoritmo actual (94% de entradas al Billboard Global 200 2025 viralizaron primero en TikTok, dato ya citado en la Sección 4). El Content Engine de IM Music permite publicar ese volumen con un equipo del mismo tamaño o menor — ofrecer explícitamente "la misma calidad de desarrollo, el doble de frecuencia de contenido" como propuesta de valor frente a un competidor con catálogo pero sin ese motor.

**Palma Production(s)**

| Dimensión | Hallazgos |
|---|---|
| **Administrativo** | Sin fundador, tamaño de equipo o estructura de gestión confirmados en ninguna fuente consultada. |
| **Financiero** | Sin datos de capital, ingresos o inversión encontrados en esta ronda. |
| **Legal** | Sin registro mercantil localizado en Cámara de Comercio de Medellín en esta ronda (la búsqueda por nombre requiere NIT o matrícula exacta, que no se tiene). Sin evidencia de contratos formales con artistas — sus lanzamientos recientes aparecen bajo licencia a terceros, no contratos directos visibles. |
| **Comercial** | Estudio + sello de género urbano/trap/pop latino/reggaetón. **Hallazgo relevante:** sus lanzamientos recientes aparecen distribuidos "exclusive license to Disetti Music" o vía Jersey Records — no distribuye directamente, depende de acuerdos con otros sellos/distribuidores para llegar a plataformas. |
| **Marketing** | Reclama 17-18 años de trayectoria, pero sus propias fuentes se contradicen entre sí (X dice "más de 17 años" con la cuenta creada en 2012; YouTube dice "18 años"). Presencia en YouTube/X/Facebook/Apple Music/Deezer, pero sin actividad indexada reciente (2024-2026) encontrada en esta búsqueda. |
| **Tecnología** | Ninguna evidencia de IA o plataforma propia encontrada. |

| | Palma Production(s) — DOFA parcial (evidencia limitada) |
|---|---|
| **Fortalezas** | Ser pionero: el primer estudio dedicado exclusivamente al género urbano naciente en Medellín le da legitimidad histórica y relación temprana con la escena local. |
| **Debilidades** | Depende de licencias de distribución con terceros (Disetti Music, Jersey Records) en vez de tener su propio acuerdo de distribución — cede margen y control de catálogo que un sello con distribución propia no cede. Sin presencia digital indexada reciente (2024-2026) encontrada en esta búsqueda. |
| **Oportunidades** | Ninguna identificada con evidencia directa — no hay información suficiente sobre su estrategia actual para inferir hacia dónde podría crecer. |
| **Amenazas** | Más de 600 productoras musicales nuevas en Medellín entre 2011 y 2021 (La República) — un estudio pionero sin renovación de marca/contenido corre el riesgo real de quedar invisible frente a competidores nuevos con mejor estrategia digital. |

*Cómo superar a Palma Production(s):* su dependencia de licencias con terceros (Disetti Music, Jersey Records) para distribuir es la brecha explotable — IM Music ya tiene su propio acuerdo de distribución directo con Nexus (8% de comisión, Sección 1) desde el día uno, sin ceder catálogo ni márgenes a un intermediario adicional. Ofrecer eso como argumento directo a cualquier artista que hoy esté bajo un esquema de licencia similar al de Palma.

#### Colombia nacional

**Rich Music**

| Dimensión | Hallazgos |
|---|---|
| **Administrativo** | 48 empleados totales (Built In; dato puede no estar actualizado a 2026). Fundado por Richard y Joshua Mendez (padre e hijo) junto con Jim Aquino; nombramientos corporativos ejecutivos reportados en 2021 (David Alvarado, SVP de Operaciones) — estructura con roles ejecutivos formales, no una operación informal. |
| **Financiero** | Sin cifra de capital levantado o ingresos encontrada en esta ronda (empresa privada, sin perfil financiero público detallado en los resultados). |
| **Legal** | HQ Miami, fundado 2007. Relación de distribución formal y de largo plazo con Warner Music Latina desde 2017 (nominado Latin Label of the Year ese año) — evidencia de contratos corporativos estables a gran escala. |
| **Comercial** | Sello discográfico con roster de artistas firmados: Sech, Dalex, Justin Quiles, Dimelo Flow, y el productor paisa Animal. Distribución vía Warner Music Latina. **Tamaño confirmado: 48 empleados totales**, fue reportado expandiéndose a Colombia con planes de abrir oficina en Medellín — **esta segunda ronda de investigación NO encontró evidencia adicional (LinkedIn, prensa 2026) de que esa oficina esté operativa hoy**: sigue siendo un anuncio de intención, no una presencia confirmada en el terreno. |
| **Marketing** | Casi 20 años de trayectoria, premiado/nominado (Latin Label of the Year 2017, Billboard Latin Music Awards), comunicados de prensa recurrentes (PR Newswire) — estrategia de relaciones públicas activa y profesionalizada. |
| **Tecnología** | Ninguna evidencia específica de IA o tecnología propietaria encontrada en esta ronda. |

| | Rich Music — DOFA |
|---|---|
| **Fortalezas** | Trayectoria de casi 20 años, roster de éxito comprobado en reggaetón/R&B urbano, distribución ya resuelta vía Warner Music Latina, equipo de 48 personas — una escala de operación que IM Music no alcanzará en años. |
| **Debilidades** | Es un sello de Miami entrando a Medellín, no un sello nativo de la ciudad; la oficina anunciada en Medellín no tiene confirmación operativa en esta ronda de búsqueda — puede seguir siendo solo un anuncio. |
| **Oportunidades** | El anuncio explícito de abrir oficina en Medellín confirma que ellos mismos ven la ciudad como mercado prioritario de crecimiento — validación externa real de la tesis de mercado de este plan (Sección 5.1). |
| **Amenazas** | Depende de una sola relación de distribución mayor (Warner) para su escala — el mismo riesgo de concentración que La Industria Inc. (Sección 5.3), aunque mitigado por mantener identidad de marca propia. |

*Cómo superar a Rich Music:* su aterrizaje en Medellín sigue siendo, a la fecha de esta investigación (noviembre 2026), un anuncio sin confirmación operativa — la ventana para que IM Music se consolide primero como el operador *nativo* de la ciudad (estudio propio, equipo fijo, presencia constante desde el día uno, no una sucursal remota gestionada desde Miami) sigue abierta. La velocidad de instalación real, no la escala, es la variable que IM Music puede ganarle hoy.

#### Mundial — competidores con enfoque de IA en desarrollo de artista

**Greater Music Group**

| Dimensión | Hallazgos |
|---|---|
| **Administrativo** | Sin datos de tamaño de equipo o estructura organizacional encontrados en ninguna fuente de esta ronda. |
| **Financiero** | Sin perfil de Crunchbase verificable con este nombre exacto (existe una entidad distinta y no relacionada, "GMG Music Group", que no debe confundirse con esta); sin capital levantado o ingresos confirmados en ninguna fuente — su transparencia financiera pública es, en sí misma, baja. |
| **Legal** | Forma societaria no determinada en esta ronda. Sin evidencia pública de un método propietario documentado y protegido legalmente. |
| **Comercial** | Usa IA de forma transversal en A&R, desarrollo de artista, inteligencia de fans y optimización de catálogo (Music Ally, mayo 2026). No está claro si ofrece estos servicios a terceros o solo los aplica a su propio roster — esta ronda no encontró evidencia de un modelo B2B. |
| **Marketing** | Posicionamiento como innovador en "IA aplicada a la industria musical", con cobertura de prensa especializada (Music Ally). Sin más detalle de estrategia de marca o canales propios encontrado. |
| **Tecnología** | Diferenciador central: IA aplicada transversalmente a A&R, desarrollo de artista, inteligencia de fans y optimización de catálogo — sin detalle técnico público de qué herramientas o modelos usan específicamente. |

| | Greater Music Group — DOFA |
|---|---|
| **Fortalezas** | Enfoque de IA aplicado a toda la operación (A&R, desarrollo, inteligencia de fans, catálogo), no a un solo paso del proceso — sugiere una ventaja de eficiencia operativa de alcance mayor al Content Engine actual de IM Music, que se concentra en contenido/marketing. |
| **Debilidades** | No se encontró evidencia pública de un método propietario documentado y protegido legalmente (como el de IM Music, formalizado como secreto empresarial bajo Decisión 486), ni de capital levantado o tamaño de equipo en ningún registro público verificable — su ventaja de IA parece ser más una práctica operativa opaca que un activo de propiedad intelectual defendible y comunicable. |
| **Oportunidades** | Al operar a escala internacional con IA en todo el pipeline, puede capturar eficiencias de costo que un sello boutique de un solo mercado no alcanza todavía. |
| **Amenazas** | Mayor escrutinio público y regulatorio sobre el uso de IA en la industria musical (ver el caso de IngaRose y el debate sobre contenido sintético en los charts, 2026) puede exponerlo a riesgo reputacional que un sello con artistas 100% humanos, como IM Music, no enfrenta de la misma forma. |

*Cómo superar a Greater Music Group:* su ventaja de IA no está documentada públicamente como propiedad intelectual defendible — IM Music sí tiene esto (metodología formalizada y protegida bajo Decisión 486, Data Room completo). Frente a un inversionista o un artista, IM Music puede mostrar y explicar su método con rigor legal; Greater Music Group, por ahora, solo puede describir una práctica operativa interna sin ese respaldo — usar esa diferencia de forma explícita en cualquier pitch que compita por la misma narrativa de "IA aplicada a desarrollo de artista".

*Mención aparte, no DOFA completo:* **Stage Zero** (de Timbaland) y **Higgsfield Records** representan el extremo opuesto del espectro: firman "artistas" de IA (TaTa, Kion) en vez de usar IA como herramienta para artistas humanos. Es un modelo de negocio fundamentalmente distinto al de IM Music, no un competidor directo por el mismo talento o audiencia, pero sí compite por el mismo capital de inversión e interés mediático en "IA + música" — relevante para contextualizar cualquier pitch a inversionistas que ya conozcan ese espacio.

#### Dubái / EAU

**GXR Records** (+ matriz Galaxy Racer)

| Dimensión | Hallazgos |
|---|---|
| **Administrativo** | Liderado por Elia Mssawir (manager de artistas, head of label). Empleados de la matriz Galaxy Racer: entre <100 (Dealroom) y 60 (PitchBook) — no desglosado para GXR Records específicamente. |
| **Financiero** | Capital de la matriz Galaxy Racer: las fuentes no coinciden — entre USD 10-50M (Dealroom) y USD 20M en una ronda de mayo 2025 (LeadIQ, comunicado de prensa). **Hallazgo de gobierno corporativo real:** reportes contradictorios sobre una posible adquisición de Galaxy Racer por Riva Technology and Entertainment (RTE) para formar una nueva entidad ("Celestial") — Dealroom la da como anunciada en mayo 2023 y luego cancelada, PitchBook reporta una fecha de adquisición distinta (agosto 2025) — señal de inestabilidad o reestructuración corporativa en curso, no un dato menor. |
| **Legal** | Lanzado en 2022 como joint venture formal entre Galaxy Racer (medios/esports, Dubái) y Empire (distribuidora independiente, EEUU) — estructura de alianza corporativa, no un sello aislado. |
| **Comercial** | Desarrollo de talento en territorios WANA (Asia Occidental/Norte de África), distribución vía Empire. **Esta segunda ronda buscó específicamente evidencia de expansión a talento latino/reggaetón en 2026 y no encontró ninguna** — el roster confirmado sigue siendo 100% WANA (Freek, Noel Kharman, Dyler, Hanody Awesome, Noor Stars). |
| **Marketing** | Cobertura de prensa real y consistente (Gulf Business, ScenNoise) desde su lanzamiento en 2022, posicionado como "primer sello indie boutique" de la región. |
| **Tecnología** | Ninguna evidencia específica de IA o tecnología propietaria encontrada — su diferenciador reportado es la alianza de distribución (Empire) y el respaldo de capital (Galaxy Racer), no tecnología. |

| | GXR Records — DOFA |
|---|---|
| **Fortalezas** | Respaldo de Empire (distribuidora global real, con track record en mercados urbanos/hip-hop) y de Galaxy Racer (empresa de medios/esports con alcance regional, USD 10-50M levantados) le da capital y distribución desde el lanzamiento, algo que IM Music no tiene en Dubái. |
| **Debilidades** | Enfoque geográfico y cultural 100% en talento WANA, sin ninguna señal confirmada de movimiento hacia música latina/urbana a la fecha de esta investigación (noviembre 2026); reportes contradictorios sobre una posible adquisición/reestructuración de su matriz sugieren posible inestabilidad corporativa. |
| **Oportunidades** | Posición ya establecida como sello de referencia regional en Dubái podría facilitarle expandirse a otros géneros, incluido el latino, si detecta la misma señal de demanda que ya identificó este plan. |
| **Amenazas** | Si decide entrar al nicho latino/urbano antes que IM Music, tiene más capital y relación de distribución ya resuelta para hacerlo rápido. |

*Cómo superar a GXR Records / aprovechar la ventana:* confirmado en dos rondas de investigación (mayo y noviembre 2026) que GXR sigue 100% enfocado en talento WANA, sin ninguna señal pública de interés en el nicho latino — la ventana de "ser pionero" de la Sección 5.2 sigue completamente abierta. Sumado a la posible reestructuración corporativa de su matriz (adquisición por RTE en disputa entre fuentes), el momento real de menor resistencia para que IM Music entre al nicho latino en Dubái es ahora, no después — cada trimestre que GXR no diversifica es una validación adicional, no una señal de que vayan a tardar para siempre.

*Nota adicional — otros sellos de Medellín fuera de los 3 señalados:* la investigación también ubicó a **Codiscos** (fundado 1950) y **Discos Fuentes** (fundado 1934) como sellos históricos de Medellín, pero ambos operan a escala de major/legado (décadas de catálogo diversificado, no modelo boutique de desarrollo de artista urbano) — no son competidores directos por el mismo segmento de cliente que IM Music, Vion Music, Kapital Music o Palma Production(s) sí disputan.

---

## 6. PLAN OPERATIVO

1. **Selección de talento:** scouting directo y por convocatoria, priorizando artistas con tracción orgánica inicial (seguidores, streams) sobre potencial no probado.
2. **Producción musical:** preproducción, grabación en estudio propio o mediante alianzas, mezcla y masterización, entrega final.
3. **Marketing y contenido:** la Comunicadora define la parrilla editorial y dispara en paralelo el briefing al Content Engine para las piezas masivas y automatizadas, al Filmmaker para la edición de material humano real, y a la Diseñadora Gráfica para las piezas bespoke. El Social Media Manager cura y publica, no produce desde cero. El resultado de cada ciclo retroalimenta la siguiente parrilla.
4. **Distribución:** vía Nexus, con 8% de comisión, a todas las plataformas de streaming relevantes en cada mercado.
5. **Gestión de derechos de autor:** registro de obras ante la entidad correspondiente al mercado de operación, SAYCO/ACINPRO en Colombia o EMRA en EAU (sujeto a las limitaciones de la Sección 5.2), y protección de los derechos del artista y del sello.
6. **Organización del trabajo:** gestión de proyectos online y comunicación asincrónica entre freelancers y el equipo fijo.

### 6.1 Equipamiento físico

El sello es dueño del equipo de filmación en vivo, lo que el Content Engine no puede generar sintéticamente: cámara híbrida con un lente, kit de dos a tres luces, trípode y micrófono lapel o shotgun, más el estudio de audio propio con tratamiento acústico, micrófonos, interfaz, monitores y licencia de DAW. Al ser el Filmmaker y la Diseñadora Gráfica planta fija y no freelance, el sello también es dueño de su estación de edición y diseño (equipo de cómputo, licencias de software, periféricos): es un CAPEX más alto que el escenario freelance, pero evita que el trabajo creativo y el acceso a la metodología dependan de equipo externo. Las cifras exactas y las notas de cada rubro, todas marcadas como supuesto a validar salvo donde se indique lo contrario, están en el Modelo Financiero IM Music — Sello, hoja CAPEX.

### 6.2 Herramientas y stack tecnológico

Para que el equipo opere como un sistema interconectado y no como procesos sueltos, se usa Notion para gestión de proyectos, tareas y documentación compartida: una sola herramienta ligera para un equipo de este tamaño, no un stack enterprise. WhatsApp Business cubre la comunicación interna y con artistas o clientes. Make automatiza la conexión entre herramientas, de la "Máquina de Captación" (bots de WhatsApp con IA, DM automático en redes, email marketing) hacia tareas automáticas para el Gerente Comercial y, si se cierra el trato, para el Project Manager de Élite 360. El Filmmaker trabaja con CapCut Pro y la Diseñadora Gráfica con Canva Pro, ambas herramientas de edición y diseño asistidas por IA. Google Drive funciona como repositorio de archivos pesados de audio, video y diseño. El control de plazos se maneja con SLA por tipo de tarea dentro de Notion en vez de una herramienta de time-tracking dedicada, innecesaria a esta escala.

El detalle completo de cada rol, sus fases, subpasos, responsable, herramienta específica, métrica de éxito y qué se puede automatizar, está en el documento Manual de Funciones y Procesos IM Music. Los flujos de decisión paso a paso para firma de artista, onboarding de la plataforma, producción de un lanzamiento, manejo de una crisis de marca o streamer, y resolución de problemas de pago o regalías, están en Flujos de Decisión y Herramientas IM Music, ambos documentos separados.

---

## 7. PLAN DE RECURSOS HUMANOS

La estructura es intencionalmente lean, pero completa: ocho roles reales, no dos. Los roles fijos son el CEO/Director, el Gerente Comercial, el Project Manager de Élite 360 (activo cuando haya ocupación en el roster), el Social Media Manager, la Comunicadora de estrategia de contenido, el Filmmaker/Editor con IA y la Diseñadora Gráfica — estos tres últimos en planta fija y no freelance, precisamente porque son quienes ejecutan la metodología de marca y de composición ya formalizada por escrito, y mantenerlos dentro de la empresa, con contrato y cláusulas de confidencialidad, protege ese activo de propiedad intelectual de una forma que el freelanceo rotativo no permite. Los roles variables o freelance, pagados por proyecto, quedan limitados al Productor Musical y al Ingeniero de Sonido, cuyo trabajo es por naturaleza específico a cada grabación y no requiere acceso a la metodología completa del sello. Los asesores externos, sin nómina, son el Contador y un Asesor Legal Externo para casos puntuales de alta complejidad; el CEO/Director cubre lo rutinario.

Esta estructura puede escalar agregando un segundo rol fijo, un Gerente Comercial de tiempo completo, cuando el flujo de proyectos de producción externa supere, de forma sostenida, los cuatro o cinco proyectos mensuales.

Cada uno de estos roles tiene su proceso completo documentado por fases: qué hace, con qué herramienta, con qué métrica de éxito, qué se puede automatizar, y cómo su trabajo dispara el de otro rol. Un ejemplo: la Comunicadora dispara en paralelo al Content Engine, al Filmmaker y a la Diseñadora, y recibe de vuelta las métricas para ajustar la siguiente parrilla. Todo esto vive en el documento separado Manual de Funciones y Procesos IM Music. No se repite aquí por extensión, pero es parte integral de este plan.

---

## 8. GESTIÓN DE RIESGOS

Este plan se apoya en una matriz de riesgos exhaustiva y aparte, el documento Matriz de Riesgos IM Music, con 61 riesgos específicos en ocho categorías: industria, mercado, político/regulatorio, financiero, marca, marketing, administrativo/comercial y legal. Cada uno tiene probabilidad por impacto y un responsable de mitigación, y está deliberadamente respaldado, cuando es posible, en casos reales documentados de otros sellos y distribuidores, no en supuestos genéricos, porque lo que le puede pasar a IM Music ya le pasó, en alguna forma, a un comparable real. Dieciocho de esos riesgos citan una fuente verificable.

Los cinco riesgos más críticos de la matriz, con un score máximo de 25, son estos:

| Riesgo | Precedente real citado | Responsable |
|---|---|---|
| Dependencia total del fundador (CEO, legal, ventas, relación con artistas a la vez) | — | CEO/Director |
| Ocupación del roster Élite 360 no alcanza el supuesto de $2.999,99 USD/mes/artista | Lucki vs. Empire Distribution — demanda por ruptura de exclusividad tras +$600K invertidos | Gerente Comercial |
| Artistas emergentes no pueden sostener el ticket de Élite 360 | — | CEO/Director |
| Desarrollador único de la plataforma — punto único de falla | — | CEO/Director |
| La plataforma maneja dinero de terceros (regalías) sin revisión legal/seguridad | UMG/Believe vs. TuneCore (acuerdo de $500M); DistroKid retuvo $14K de un artista por disputa de terceros | Asesor Legal Externo |

La matriz completa documenta otros precedentes directamente relevantes para decisiones ya tomadas en este plan. El caso d4vd, soltado por su sello y bloqueado de Twitch en 24 horas en 2026, y el caso Dr Disrespect, que perdió cuatro patrocinios de marca en días, son ambos riesgo reputacional por asociación con un artista o un streamer, y aplican directamente a la alianza con streamer de la Sección 4 y a la firma de artistas de la Sección 6. El caso de Michael Smith, imputado criminalmente por fraude de streams con IA y bots, y la demanda colectiva RBX vs. Spotify por streams fraudulentos, son relevantes para la línea de regalías de catálogo propio de la Sección 10.3.

Hay además riesgos que este plan ya resolvió en su propio diseño, por lo que no requieren mitigación activa:

| Riesgo | Cómo ya se mitigó en el diseño del plan |
|---|---|
| Cambios en gustos musicales / saturación del mercado | Roster deliberadamente multigénero (no solo urbano/latino) y multi-idioma |
| Entorno regulatorio de derechos musicales inmaduro (EAU) | No se proyectan ingresos de EMRA hasta que tenga historial comercial (post diciembre 2026) |
| Dependencia de Nexus como distribuidor único | Evaluar, a partir del año 2, una segunda vía de distribución según volumen de catálogo |
| Obsolescencia tecnológica del Content Engine propio | Mantenimiento y actualización continua del stack (Pillow/FFmpeg/edge-tts) como parte de la operación |

---

## 9. MARCA E IMAGEN CORPORATIVA

A diferencia del plan original, la identidad de marca de IM Music ya existe y está en uso activo, verificada contra la cuenta real @immusicsello. El concepto es REBEL LUXURY. El color primario es violeta #5E17EB como fondo de toda pieza visual, con negro #000000 en closing cards y crema #F2EDE5 y blanco #FFFFFF como acentos. Las tipografías son Sceageus para headline principal, sin excepción, y Anton para textos secundarios y CTA. El logo, `logo_immusic.png`, ya está diseñado. El sistema de ilustración usa grabados estilo Gustave Doré en líneas finas sobre fondo violeta, con reglas de procesamiento ya codificadas para umbral de contraste y opacidad.

No hay trabajo de diseño de identidad pendiente. Lo que queda es aplicar esa identidad de forma consistente a nuevos mercados, con adaptación de idioma y tono si se opera en Dubái, y a materiales de inversionista, no crearla desde cero.

Para el fundador, la marca es el intangible más importante del negocio, más que cualquier línea de ingreso individual. El estándar no es solo mantener los colores, la tipografía y el logo ya definidos. Cada pieza de comunicación que se produzca, sea contenido del Content Engine, materiales del servicio Élite 360, piezas de la plataforma o el libro, debe ejecutarse con el mismo nivel de impacto que ya define a REBEL LUXURY: nada genérico, nada diluido. No es una meta de diseño aislada. Es lo que hace que la inversión en catálogo, en servicios y en contenido se acumule como valor de marca a largo plazo, en vez de diluirse en piezas sueltas sin identidad consistente.

---

## 10. ESTRATEGIAS DE GENERACIÓN DE INGRESOS

Estas son las líneas de ingreso reales y relevantes para un sello de este tamaño. Se elimina toda línea de ingreso de servicios de marketing a empresas, que pertenecía a la agencia.

1. **Producción musical para terceros.** Servicio de grabación, mezcla y masterización cobrado por proyecto. Hay que corregir una expectativa aquí, con base en experiencia real de la industria: vendida suelta, como servicio técnico aislado, esta línea normalmente no deja un margen significativo. Los costos de estudio, el tiempo de ingeniero y productor, y el equipo absorben la mayor parte del ingreso, así que no se debe presentar a un inversionista como motor de rentabilidad en ese formato. Ahí su función real es doble: cubre costos fijos del estudio, casi en punto de equilibrio, y es la herramienta de relación que permite firmar y retener un productor, además de descubrir y evaluar artistas externos antes de ofrecerles un contrato de roster.

   La forma real de sacarle margen es empaquetarla, no venderla suelta: un **campamento de creación / turismo artístico** de varios días, con estadía y tours incluidos, donde el equipo completo —Productor, Ingeniero de Sonido, Diseñadora, Filmmaker, Comunicadora con su plan de contenido— conceptualiza y produce un EP o un álbum entero como proyecto integral, no solo "la marca personal" del artista. Se investigó esto directamente contra la práctica real de la industria (camps de composición en Nashville y similares), y el hallazgo más importante es que **un productor no puede atender bien a 12 artistas**: el patrón real de la industria es de 2 a 4 artistas por productor trabajando en paralelo, lo que para un camp de 12 significa contratar entre 3 y 6 productores/ingenieros, no solo el Productor+Ingeniero que hoy tiene presupuestado el plan. Esto no rompe el principio de equipo mínimo del plan (Sección 3.1): esos 3-6 productores son freelance, contratados únicamente por los días que dura cada camp, no una ampliación del equipo fijo — el camp escala de personal solo cuando hay un evento real que lo justifique. Con esa corrección, el cálculo original del fundador (12 artistas a $5.000.000 COP cada uno, ingreso de $60.000.000 COP por camp) sí parece dejar un margen real en Medellín —entre $39 y $43 millones COP, 65-71% bruto, cubriendo finca (~$3.5M, cotización real en Copacabana), alimentación y el equipo ampliado de producción/contenido— aunque dos de esos rubros (tarifa de catering y de productor en Medellín) siguen sin una cotización local verificada. **En Dubái, el mismo precio no alcanza**: convertido a AED, el ingreso de los 12 artistas (~AED 54.000) apenas cubre villa y comida (AED 49.000-52.000, 91-96% del ingreso), sin dejar nada para producción, staff ni vuelos del equipo si viaja desde Medellín — ahí hay que subir el precio por artista (apalancando el argumento de poder adquisitivo de la Sección 5.2) o no ofrecer este paquete todavía. El detalle completo, con cada fuente, está en el documento de investigación de campamentos musicales.

   El volumen realista de este paquete es de dos a cuatro camps/proyectos externos por mes, no los cien del plan anterior, que correspondían a una escala de agencia. El precio por paquete y el margen real en Medellín son una hipótesis con evidencia a favor, no un dato cerrado: falta cotizar directamente la alimentación y la tarifa de los productores/ingenieros antes de presentarlo a un inversionista como cifra firme.
2. **Desarrollo de marca personal para artistas:** servicio de posicionamiento y estrategia de contenido para artistas externos al roster. El volumen y el precio son supuesto a validar.
3. **Regalías de catálogo propio:** ingresos de streaming vía Nexus, menos 8% de comisión, de los artistas firmados por el sello. Esta línea depende directamente de la inversión activa del sello en el desarrollo de sus propios artistas, es decir, financiar grabación, video musical y lanzamiento de canciones, no solo prestar el servicio a terceros. Es la línea con mayor potencial a largo plazo pero la más lenta de construir, y requiere capital de trabajo propio destinado a esa inversión (ver Modelo Financiero). Tiene además un retorno secundario no financiero: un lanzamiento exitoso financiado por el sello funciona como vitrina de la metodología de desarrollo de artista, lo que atrae tanto a nuevos artistas al roster Élite 360 como a nuevos usuarios de los planes de la plataforma. Parte del retorno de esta inversión es marketing y adquisición, no solo la regalía directa. No se proyecta un valor monetario para ese efecto porque sería especulativo, pero se señala como justificación estratégica adicional de la inversión en catálogo.
4. **Ingresos del canal de YouTube propio:** monetización publicitaria vía AdSense y Content ID del canal de YouTube del sello, independiente de las regalías de streaming vía Nexus. El volumen de vistas y el CPM son supuesto a validar, y dependen del ritmo de publicación de contenido, apalancado en el Content Engine, y del crecimiento orgánico del canal.
5. **Licencias y sincronización (sync):** uso de música del catálogo en medios audiovisuales de terceros. Es una línea incipiente, sin pipeline activo todavía, una oportunidad a desarrollar y no un ingreso proyectable en el corto plazo.
6. **Eventos y shows en vivo:** ingreso futuro, condicionado al crecimiento de la base de fans de los artistas del roster. No se proyecta en los primeros 12 a 18 meses.
7. **Alianza con un streamer:** el sello invierte en el setup de transmisión de un creador de contenido en vivo, cámara, capturadora, micrófono y luces, a cambio de un acuerdo de exposición de marca y de los artistas del roster, y opcionalmente un porcentaje de los ingresos del streamer si así se negocia. El retorno principal esperado no es la regalía directa, es el marketing y la exposición masiva y constante que un streamer activo genera, el mismo principio que la inversión en catálogo de la Sección 10.3, pero con un canal de exposición distinto, en vivo y con comunidad, no solo streaming de música. El volumen, el costo del setup y los términos del acuerdo son supuesto a validar; no hay un streamer identificado todavía a la fecha de este plan.
8. **Libro "Music Business Para Todos Los Humanos":** producto existente y ya en venta en Hotmart, incluyendo programa de afiliados, con ediciones en español, inglés y portugués. Es una línea de ingreso real y activa, aunque menor en escala frente a las anteriores. Se incluye en el Modelo Financiero IM Music — Sello como ingreso adicional, no como línea de crecimiento principal.
9. **Representación / Entrada a Mercado:** servicio de booking y representación para artistas externos al roster (ver Sección 4), con dos modalidades de precio ya cotizado y validado en un caso real: $2.000 USD/mes servicio completo, $1.000 USD/mes solo dirección. A diferencia de Élite 360, no requiere inversión de catálogo ni producción de video, por lo que su margen por cliente es más alto en proporción al costo de entrega. Volumen realista: 1-2 artistas externos simultáneos al inicio, limitado por la capacidad del agente de booking, no por demanda.

**Sobre la jerarquía de ingresos del ecosistema IM Music.** Dentro del conjunto completo del proyecto, sello, plataforma SaaS, libro y YouTube, el dinero real viene de las líneas de escala masiva: la plataforma SaaS con sus planes Básico y Pro de suscripción sin límite de usuarios, el libro ya en venta, y el canal de YouTube propio. Estas tres son, por diseño, el motor de ingresos del negocio. El servicio Élite 360, con su roster de 12 a 15 artistas, la inversión en catálogo propio y la alianza con un streamer no son el motor de caja principal. Son lo que robustece el negocio: construyen la credibilidad, la metodología probada, la exposición de marca y el moat que hacen creíble y defendible la oferta de la plataforma frente a la competencia, y van creciendo de forma acumulativa en el tiempo. Esta jerarquía se desarrolla con más detalle en el plan de negocios de la plataforma SaaS, documento separado.

Todas las cifras de precio o ticket por servicio que no tengan fuente verificada en este documento se presentan como supuestos pendientes de validar en el Modelo Financiero IM Music — Sello, y deben confirmarse con cotizaciones reales antes de presentarse a un inversionista como dato cerrado.

---

## 11. ASPECTOS LEGALES

### 11.1 Colombia

- **Constitución:** Sociedad por Acciones Simplificada (SAS), registro ante Cámara de Comercio y DIAN.
- **Registro de marca:** ante la Superintendencia de Industria y Comercio (SIC).
- **Protección de la metodología propia:** más allá del registro de marca, la metodología de construcción de marca de artista, de composición con neurociencia y de lanzamiento de canciones se protege como secreto empresarial bajo la Decisión 486 de 2000 (Comunidad Andina), que exige medidas razonables de confidencialidad — un acuerdo de confidencialidad firmado por cada colaborador que accede a ella, sea planta fija o freelance (el tipo de vínculo laboral no modifica el alcance de esa protección). El Filmmaker, la Comunicadora y la Diseñadora Gráfica son planta fija por disponibilidad operativa constante y control de consistencia de marca (ver Sección 3.1), no porque el freelanceo deje la metodología desprotegida. El mecanismo completo (marca, secreto empresarial, registro de obra inédita ante la DNDA) y la plantilla del acuerdo de confidencialidad están en el Data Room (`Proteccion_Marca_y_Metodologia_IM_Music.docx` y `Acuerdo_de_Confidencialidad_IM_Music.docx`).
- **Gestión de derechos de autor:** afiliación a SAYCO, para autores y compositores, y ACINPRO, para productores fonográficos. Ambas entidades publican requisitos documentales (SAYCO pide identificación y formulario biográfico; ACINPRO pide constitución legal de la empresa discográfica, formulario FO-A-16 y certificación bancaria), pero ninguna publica una tarifa de afiliación vigente para 2025. Este costo debe confirmarse llamando directamente a ambas entidades antes de incluirlo como cifra cerrada en el plan financiero.
- **Impuesto de renta:** tarifa general para sociedades, incluyendo SAS, del 35% para los años gravables 2025 y 2026 (Art. 240 E.T., Ley 2277/2022). Hay un proyecto de reforma que bajaría la tarifa a partir de 2027, pero todavía no está vigente.
- **Régimen Simple de Tributación (RST):** alternativa simplificada para emprendimientos pequeños. Su aplicabilidad y tarifa real para este tipo de negocio deben confirmarse en el simulador oficial de la DIAN antes de asumirla en el modelo financiero.
- **Contratos con artistas:** deben cubrir producción, promoción, distribución y reparto de regalías, con asesoría legal especializada en propiedad intelectual y derecho del entretenimiento.

### 11.2 Dubái / EAU

- **Estructura:** elegir entre zona franca (free zone) o territorio continental (mainland). Las zonas francas relevantes para medios y música son Dubai Media City, Dubai Studio City, twofour54 en Abu Dhabi (exenta de tarifas de licencia los primeros dos años) e IFZA.
- **Costos de constitución:** las cifras disponibles son estimaciones de consultoras, no tarifas oficiales. Por ejemplo, la licencia en Dubai Media City va de AED 15.000 a 30.000 al año con capital mínimo de AED 50.000, e IFZA desde AED 12.900. Se recomienda cotizar directamente con la zona franca elegida antes de usar estas cifras en un documento financiero formal.
- **Impuesto corporativo:** 0% sobre los primeros AED 375.000 de ingreso gravable, 9% sobre el excedente. Las empresas de zona franca pueden mantener 0% sobre "ingreso calificado" solo si cumplen el test de Qualifying Free Zone Person y su ingreso no calificado no supera el menor de 5% del ingreso total o AED 5 millones. Incumplir esto implica perder el beneficio por cinco años.
- **IVA:** 5% general. Los servicios de medios y entretenimiento digital, incluyendo streaming, son explícitamente gravables, y el IVA pagado en insumos de entretenimiento generalmente no es recuperable.
- **Aranceles de importación:** 5% sobre valor CIF para equipo importado, cámaras y audio. Hay que verificar el código arancelario específico contra el Arancel Aduanero Unificado del CCG.
- **Gestión de derechos de autor:** EMRA, la primera sociedad de gestión de derechos musicales de EAU, se licenció en abril de 2025 bajo la Ley Federal 38/2021, y sus tarifas comerciales entran en vigor en diciembre de 2026. No hay historial operativo previo.
- **Visas:** la visa de empleo, de dos años, se estima entre AED 3.000 y 7.500 todo incluido. La visa de inversionista, con información escasa, se estima entre AED 7.000 y 20.000 o más. Ambas cifras requieren confirmación oficial antes de usarse en el plan financiero.

---

## 12. INDICADORES CLAVE DE RENDIMIENTO (KPIs)

En lo financiero: ingresos totales por línea (producción, regalías, licencias), margen neto, costo de adquisición de artista y valor de vida del artista para el sello.

En catálogo y desempeño artístico: número de artistas firmados, canciones producidas por año, streams u oyentes mensuales por artista, crecimiento de seguidores en redes.

En operación: número de proyectos de producción externa cerrados por mes, tiempo promedio de entrega de un proyecto, satisfacción del artista medida por encuestas.

En eficiencia del Content Engine: piezas de contenido publicadas por semana frente a costo marginal, y tiempo ahorrado frente a un flujo de trabajo manual equivalente.

---

## 13. ESTRATEGIA DE SALIDA PARA EL INVERSIONISTA

Las mismas opciones de salida aplican, evaluadas con mayor realismo dado el tamaño del negocio: venta de participación a otro inversionista, fondos especializados en música u otros sellos independientes; adquisición por un sello mayor, una vez el catálogo y el roster alcancen una masa crítica demostrable en streams e ingresos recurrentes; o recompra por parte de los fundadores, una opción realista en un negocio de este tamaño que no estaba contemplada en el plan original.

La Oferta Pública Inicial, mencionada en el plan original, es una opción teórica de largo plazo que no aplica a la escala actual de este negocio y no debería presentarse a un inversionista temprano como una expectativa realista de salida.

---

## 14. PRESENTACIÓN AL INVERSIONISTA / CONCLUSIÓN

IM Music ofrece una oportunidad de inversión en un sello discográfico independiente de vocación global y multigénero que parte sin artistas firmados, con el catálogo por construirse desde cero, pero que ya cuenta con una ventaja estructural verificable: identidad de marca REBEL LUXURY en uso real, acuerdo de distribución vigente con Nexus, y un Content Engine propio que reduce drásticamente el costo de mantener presencia digital constante frente a cualquier sello boutique comparable.

El mercado colombiano de música grabada crece de forma sostenida y por encima del promedio mundial, +17,9% en 2025 según IFPI, lo que da viento de cola al escenario Medellín: la base operativa real desde la que se construirá el roster, sin que eso limite el género, idioma o nacionalidad de los artistas que se firmen.

El escenario Dubái se presenta con una lógica distinta y deliberada. No es una réplica del negocio colombiano en otra ciudad, es una apuesta de creación de industria. EAU es la región de mayor crecimiento mundial en música grabada, tiene un entorno fiscal corporativo favorable y demanda en vivo creciente y verificable por música latina, y al mismo tiempo carece por completo de un sello boutique de referencia en ese género y apenas estrena infraestructura de derechos musicales. Para un inversionista, eso significa entrar antes de que exista competencia establecida, no después. No cuenta hoy con datos de mercado país-específicos ni con infraestructura de regalías con historial comprobado, así que se presenta como una opción de expansión de alta convicción pero de validación pendiente, no como una alternativa equivalente y lista para ejecutar en el corto plazo sin investigación local adicional.

Las cifras de inversión requerida, estructura de costos, punto de equilibrio y retorno proyectado para cada escenario se desarrollan en el documento Modelo Financiero IM Music — Sello, construido con supuestos de volumen reales para un sello de este tamaño y con cada cifra sin fuente verificable marcada explícitamente como pendiente de validación.

---

## 15. ANÁLISIS DOFA

**Fortalezas.** Identidad de marca REBEL LUXURY ya desarrollada y en uso real, no por construir. Content Engine propio ya construido y funcionando, con ventaja de costo estructural frente a cualquier sello boutique comparable. Metodología de desarrollo de artista propia del fundador, aplicable a cualquier género e idioma, sin depender de un nicho. Conexión directa con la plataforma SaaS: el sello es el caso de uso real que valida y vende el tier Élite 360.

**Debilidades.** Cero artistas firmados a la fecha, con todo el catálogo, la reputación de roster y la tracción por construirse desde cero. Dependencia total del fundador en CEO, legal, ventas y relación con artistas, el riesgo de punto único de falla ya identificado como el más crítico de la matriz. Varias líneas de ingreso, como producción musical y licencias/sync, tienen margen bajo o no comprobado, así que la rentabilidad real depende casi enteramente de la ocupación del roster Élite 360, un supuesto no validado. Capital y track record limitados frente a sellos multinacionales o fondos especializados en música.

**Oportunidades.** Ningún sello boutique multigénero con tecnología propia opera hoy desde Medellín con el nivel de automatización del Content Engine, ni existe un competidor así en Dubái: es un vacío concreto, no una suposición de que "hay espacio en el mercado". La alianza con un streamer y la inversión en catálogo generan exposición medible, seguidores, vistas, menciones, a una fracción del costo de una campaña de pauta paga tradicional; el retorno no es solo cualitativo, es rastreable con las métricas que ya usa el Content Engine. Los conciertos virtuales en vivo monetizados vía YouTube o streaming (ver Sección 16) son una forma de probar demanda internacional, en Dubái y otros mercados, sin el costo de una gira física. Y el módulo de financiamiento de artistas ya construido en la plataforma (ver Sección 16) convierte al sello en el primer cliente real de esa función cuando se active.

**Amenazas.** Los precedentes reales de otros sellos y distribuidores que recoge la Matriz de Riesgos, como Lucki vs. Empire, UMG/TuneCore, d4vd y Dr Disrespect, muestran que disputas contractuales, fraude y crisis reputacionales son recurrentes en esta industria, no hipotéticas. El entorno regulatorio en Dubái sigue inmaduro, con EMRA sin historial comercial hasta diciembre de 2026. Y la saturación de lanzamientos diarios en plataformas de streaming hace cada vez más difícil competir por atención, incluso con buen producto.

### 15.1 Oportunidades y amenazas confirmadas con datos de industria 2025-2026

Lo siguiente complementa el DOFA de arriba con hallazgos reales de investigación de mercado, no supuestos:

**Oportunidad confirmada — sync crece más rápido que streaming.** Según RIAA, los ingresos de sincronización (cine, TV, publicidad, videojuegos) crecieron 18,2% a USD 231,8 millones en el primer semestre de 2026, frente a un crecimiento general de ingresos de música grabada en EE.UU. de 6,9% en el mismo periodo. El mercado global de licenciamiento musical se proyecta en USD 14,84 mil millones para 2031 (CAGR 8,81%, Research and Markets). La ventaja real para un sello pequeño como IM Music: los supervisores de sync evitan catálogos con estructura de propiedad confusa o splits poco claros — exactamente lo que este plan ya resuelve formalizando por escrito cada split de composición en el Data Room (ver `03_split_composicion.md`). Esto refuerza que la línea de sync (Sección 10.5, hoy "incipiente, sin pipeline activo") merece desarrollarse antes de lo previsto, apalancando precisamente la documentación legal ya ordenada como ventaja competitiva frente a catálogos informales.

**Amenaza/oportunidad doble — desaceleración del streaming.** El crecimiento de streams globales bajó de 15% a 10% interanual en la primera mitad de 2025, y en EE.UU. de 8% a 5% (Luminate Midyear Music Report 2025). El consumo sigue creciendo en volumen absoluto (2,5 billones de streams globales), pero más lento. Para un sello que recién empieza su catálogo, esto es una amenaza de contexto (el piso de crecimiento pasivo por streaming ya no es tan generoso como hace dos años) que refuerza por qué este plan ya correctamente no proyecta ingresos agregados de streaming como motor principal (Sección 10), sino que los trata como "la línea más lenta de construir" junto a líneas más activas (producción, representación, alianza con streamer).

**Oportunidad y riesgo simultáneo — adopción de IA en producción musical.** Una encuesta de Ditto Music (septiembre 2026, +5.000 artistas independientes) encontró que 47% ya usa IA para hacer música y 11% ha hecho música completamente generada por IA. Esto valida la apuesta estructural de IM Music en su Content Engine propio como ventaja de costo (Sección 2, 3.1), que ya es una ventaja real y no solo una ventaja de duplicar lo que el sector adoptará de todas formas. El riesgo: reportes de industria (Music Week, IFPI) señalan que la IA sin regular ya es una preocupación de artistas y titulares de derechos, y que ingresos de música funcional (publicidad, eventos corporativos, contenido de formato corto) están cayendo para músicos independientes por la competencia de IA genérica — esto refuerza, no contradice, la razón por la que este plan mantiene la producción musical suelta como línea de bajo margen (Sección 10.1) y empuja hacia el desarrollo real de artista y marca como el valor defendible, algo que la IA genérica no reemplaza.

**Validación de ubicación — Dubái.** Al Quoz, el distrito ya elegido para el escenario Dubái de este plan, tiene una tarifa de oficina promedio de AED 85/sqft (Engel & Völkers, año a la fecha mayo 2026), frente a AED 160-240/sqft en Dubai Media City, el distrito de medios más conocido de la ciudad. La elección de Al Quoz en este plan no es solo la más barata encontrada: es significativamente más barata (hasta 65% menos) que la alternativa de "distrito de medios" más obvia, lo que confirma que la decisión ya tomada es la correcta por costo, no solo por disponibilidad.

**Alternativa a evaluar — Medellín.** Esta investigación encontró un dato no considerado hasta ahora en este plan: el Distrito Creativo El Perpetuo Socorro en Medellín ofrece beneficios tributarios específicos para empresas creativas y tecnológicas (alianza Alcaldía de Medellín/Comfama/Spotify, sede del estudio público "Sonido Perpetuo"). No se encontró una tarifa de arriendo comparable verificada para esa zona frente al arriendo ya presupuestado de $5.000.000 COP/mes, así que esto no reemplaza la cifra actual del Modelo Financiero. Pero el beneficio tributario para empresas creativas, si aplica a una SAS como IM Music, podría representar un ahorro adicional no capturado hoy en el modelo. Queda como línea de investigación a profundizar directamente con la Alcaldía de Medellín antes de tomarse como supuesto validado.

---

## 16. OPORTUNIDADES FUTURAS NO DESARROLLADAS

El plan anterior, integrado con la agencia, identificaba varias ideas de proyectos asociados que nunca se desarrollaron ni se investigaron a fondo. Se listan aquí explícitamente para que no se pierdan, pero ninguna se incluye en las proyecciones financieras de este plan: son oportunidades a evaluar en el futuro, no compromisos ni líneas de ingreso actuales.

El financiamiento de artistas es la primera. El módulo de elegibilidad de financiamiento ya existe en el código de la plataforma SaaS, inspirado en un partnership declarado con Sound Royalties en material de marketing anterior que no está confirmado ni activo. Si se desarrolla, conectaría directamente el sello, que conoce y desarrolla al artista, con la plataforma, que ejecutaría el financiamiento, pendiente de validar legal y comercialmente antes de proyectar ingreso.

La segunda es una escuela de música en alianza con el municipio de Medellín, idea del plan anterior sobre una escuela pública o semi-pública de música, sin ningún desarrollo, contacto ni validación a la fecha.

La tercera son eventos ligados al desempeño en plataformas de streaming: seguimiento y eventos personalizados para artistas según cómo les va en streaming, un concepto mencionado en el plan anterior pero sin desarrollar.

La cuarta son conceptos tipo "Sound de a Tierra" y "Sound of the World", formatos de evento o branded content inspirados en conceptos similares al "W Sound" de WestCol, uno enfocado en artistas colombianos y otro en artistas extranjeros. Se mencionaban en el plan anterior como ideas, sin ningún desarrollo, derecho de uso del formato, ni validación legal de que algo así se pueda replicar sin infringir derechos de terceros.

La quinta son conciertos virtuales en vivo monetizados vía YouTube o streaming: transmisiones en vivo del roster, no grabadas ni el video sintético del Content Engine, distribuidas por YouTube Live con monetización publicitaria, membresías de canal y Super Chat, o eventualmente plataformas de concierto virtual con boletería, al estilo Moment House o Mandolin. Hay precedente real de que esto funciona a gran escala, como BTS, Billie Eilish o Travis Scott con Fortnite, aunque a una escala mucho menor para un sello que apenas construye su roster. Para IM Music es específicamente útil para probar demanda en Dubái y otros mercados internacionales antes de gastar en una gira física o en montar oficina allá: si un artista del roster llena una transmisión en vivo con audiencia real de EAU, esa es una señal de demanda mucho más barata y rápida de obtener que la investigación de mercado local que este plan ya señaló como pendiente en la Sección 5.2. Sin streaming identificado, sin plataforma de boletería elegida y sin cifra de audiencia esperada, es una oportunidad a validar, no un ingreso proyectado.

Estas cinco ideas se heredan del plan anterior únicamente como registro de oportunidades a explorar, no como parte del modelo de negocio actual.
