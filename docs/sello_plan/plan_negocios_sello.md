# PLAN DE NEGOCIOS: IM MUSIC — SELLO DISCOGRÁFICO INDEPENDIENTE

**Versión:** 1.0 (sello como negocio autónomo, independiente de Intelligent Markets)
**Escenarios de mercado evaluados:** Medellín, Colombia / Dubái, Emiratos Árabes Unidos (EAU)

---

## 1. RESUMEN EJECUTIVO

IM Music es un sello discográfico independiente enfocado en música urbana y latina, con identidad de marca propia ya desarrollada y en uso real ("REBEL LUXURY": violeta #5E17EB, tipografías Sceageus/Anton, cuenta @immusicsello). A diferencia del plan anterior, este documento presenta a IM Music como **negocio autónomo**, sin fusión operativa ni financiera con ninguna agencia de marketing: todo ingreso, costo y función descrita aquí pertenece exclusivamente a la actividad de sello discográfico.

IM Music ya opera: tiene un artista firmado ("LA S — EL DIABLO DEL CHANTEO"), catálogo publicado bajo distribución con Nexus (8% de comisión sobre regalías) y, como ventaja estructural, un **Content Engine propio ya construido y funcionando** (investigación, redacción, diseño gráfico, video y voz sintética automatizados en Python — Pillow, FFmpeg, edge-tts) que reemplaza gran parte del gasto tradicional en producción de contenido y equipo creativo de un sello de este tamaño.

Este plan evalúa dos escenarios de sede/mercado para la operación y/o expansión del sello:

- **Medellín, Colombia:** mercado de origen, con catálogo y artista ya activos, ecosistema de música urbana consolidado y entidades de gestión de derechos (SAYCO, ACINPRO) operando hace décadas.
- **Dubái, EAU:** mercado emergente para música latina/urbana (presencia creciente de eventos y headliners latinos), marco fiscal corporativo favorable, pero con infraestructura de derechos musicales locales recién creada y sin cifras país-específicas verificables en reportes de industria.

Las proyecciones financieras detalladas (CAPEX, OPEX, punto de equilibrio, flujo de caja, TIR/VAN) se presentan en un documento separado: **Modelo Financiero IM Music — Sello**. Este documento cubre la tesis de negocio, el mercado, la operación, el equipo, los riesgos y los aspectos legales de cada escenario.

---

## 2. DESCRIPCIÓN DE LA EMPRESA

**Nombre:** IM Music
**Misión:** Impulsar carreras de artistas urbanos y latinos independientes mediante producción musical de calidad, desarrollo de marca personal y distribución profesional, usando tecnología propia para operar con la eficiencia de un sello mucho más grande.
**Visión:** Ser el sello independiente de referencia en música urbana latina para artistas que buscan crecer sin perder el control creativo ni la propiedad de su obra.

A diferencia del plan original, IM Music **no depende de una agencia matriz** para sus funciones de marketing, diseño o desarrollo de IA: esas capacidades ya están internalizadas en el Content Engine del propio sello (ver Sección 3).

---

## 3. ESTRUCTURA ORGANIZACIONAL Y FUNCIONES

### 3.1 Principio rector

El sello se diseña deliberadamente **lean**: solo se contratan o se paga por proyecto aquello que el Content Engine no puede hacer (producción de audio, decisiones creativas, relación humana con artistas y contrapartes legales/comerciales). Todo lo que es generación de contenido digital, diseño gráfico, copywriting y voz en off ya está automatizado y operando (ver `src/content_engine/`, `src/core/brand.py`), por lo que **no se presupuestan** roles de Filmmaker, Traficker de pauta ni Desarrollador de IA como personal fijo o freelance recurrente — son funciones que el sistema ya cubre a costo marginal casi nulo.

### 3.2 Roles reales del sello

| Rol | Naturaleza | Función |
|---|---|---|
| CEO / Director del Sello | Fijo | Dirección general, A&R, relación con artistas e inversionistas, decisión final de catálogo |
| Gerente Comercial | Fijo o por comisión | Captación de artistas y clientes de producción, negociación de contratos, licencias y sync |
| Productor Musical | Freelance por proyecto | Dirección creativa y producción de grabaciones |
| Ingeniero de Sonido | Freelance por proyecto | Grabación, mezcla y masterización |
| Social Media Manager | Fijo o part-time | Supervisión y curaduría del contenido generado por el Content Engine, interacción con comunidad; no genera contenido desde cero manualmente |
| Abogado | Asesor externo | Contratos con artistas, derechos de autor, registro de marca, cumplimiento normativo |
| Contador | Asesor externo | Estados financieros, impuestos, nómina |

No hay junta directiva compartida con terceros: las decisiones estratégicas las toma el CEO del sello, con el inversionista según los términos que se acuerden en la ronda de capital.

---

## 4. SERVICIOS

IM Music presta servicios **exclusivamente a artistas**, no a empresas ni marcas externas (se elimina por completo la línea de "servicios de marketing para empresas" del plan anterior, que correspondía a la agencia).

- **Producción musical:** composición, arreglos, grabación, mezcla y masterización, para artistas del roster propio y para artistas externos que contratan el servicio por proyecto.
- **Desarrollo de marca personal:** identidad visual y narrativa del artista, aplicando la misma metodología de marca que ya usa IM Music internamente.
- **Distribución digital:** vía el acuerdo vigente con Nexus (8% de comisión) a plataformas de streaming (Spotify, Apple Music, YouTube Music, Deezer, etc.).
- **Estrategia de contenido y presencia digital:** apalancada en el Content Engine propio — generación asistida de piezas para redes, guiones y calendarización — a una fracción del costo de contratar un equipo creativo tradicional.
- **Asesoría legal y de derechos de autor:** gestión de registro de obras y relación con las sociedades de gestión colectiva correspondientes a cada mercado.
- **Gestión de regalías:** seguimiento de regalías de master y publishing del catálogo propio y de los artistas producidos.

---

## 5. ANÁLISIS DE MERCADO

### 5.1 Medellín / Colombia

**Tamaño de mercado (TAM):**
El mercado colombiano de música grabada facturó aproximadamente **USD $105.2 millones en 2025**, creciendo **17.9%** y superando por primera vez los USD $100M (IFPI Global Music Report 2026, vía musicbusinessworldwide.com y forbes.pe). Latinoamérica fue la región de mayor crecimiento global por dieciséis años consecutivos, con **+17.1%** en 2025, tras +22.5% en 2024. El 78% de los ingresos de música grabada en Colombia proviene de streaming (Warner, vía La República).

**Mercado disponible (SAM):**
De ese TAM, el segmento relevante para IM Music es música urbana/independiente autogestionada o gestionada por sellos boutique (no majors, no catálogo internacional). No existe una cifra oficial que aísle este subsegmento; como **supuesto a validar**, se estima conservadoramente entre el 15% y 25% del TAM colombiano (rango de referencia de la proporción que representa la música urbana/latina dentro del consumo digital total en Colombia, sin fuente país-específica que lo confirme con exactitud — se recomienda validar con Procolombia o Mincultura antes de usar en un pitch formal).

**Mercado obtenible (SOM):**
Para un sello boutique en fase de crecimiento (1 artista firmado + producciones externas por proyecto), el SOM realista en los primeros 1-3 años es una fracción mínima del SAM: el objetivo no es capturar cuota de mercado agregada, sino construir un catálogo de 3 a 8 artistas y un flujo estable de 2 a 4 proyectos de producción externa por mes (ver Sección 10). Cualquier proyección de ingresos agregados sobre el TAM/SAM total sería, a este tamaño de operación, una distorsión — el valor real está en el crecimiento del catálogo propio y su desempeño en streaming, no en la cuota de mercado.

**Competencia:**
- *Sellos multinacionales* (Sony Music Colombia, Universal Music Colombia, Warner Music Colombia): amplia red de distribución y capital, pero procesos burocráticos y menor flexibilidad con talento emergente.
- *Sellos independientes establecidos* (Codiscos, Discos Fuentes): trayectoria y catálogo histórico, pero menor enfoque en estrategia digital/IA.
- *Plataformas DIY* (DistroKid, TuneCore, CD Baby): dan acceso a distribución global sin acompañamiento artístico, de marca ni de contenido — el artista hace todo el trabajo de desarrollo solo.
- **Diferenciación de IM Music:** acompañamiento real de desarrollo artístico + producción profesional + motor de contenido automatizado que reduce drásticamente el costo de mantener presencia digital constante, algo que ni los sellos independientes tradicionales ni las plataformas DIY ofrecen juntos.

### 5.2 Dubái / EAU

**Tamaño de mercado (TAM):**
No existe una cifra de ingresos de música grabada específica para EAU en los reportes de industria accesibles; el dato disponible es regional: **MENA (Medio Oriente y Norte de África) fue la región de mayor crecimiento mundial** en música grabada tanto en 2024 (+22.8%, ingresos ~USD $144M) como en 2025 (+15.2%, con ~97.5% de participación de streaming) (IFPI Global Music Report 2025/2026). **Esta es una limitación real de los datos, no un supuesto conservador**: no hay forma de aislar el tamaño del mercado de EAU dentro de esa cifra regional sin acceso directo a las tablas completas de gmr.ifpi.org.

**Señales cualitativas de demanda (no cuantitativas):**
- J Balvin fue headliner de UNTOLD Dubai 2025 (6-9 de noviembre), su debut en EAU — evidencia de que el mercado latino/urbano ya es suficientemente relevante para traer a un headliner de ese perfil.
- Dubai Latin Fest se realiza anualmente, y existen noches recurrentes de reggaetón/música latina en clubes de la ciudad.
- Estas señales indican demanda en vivo creciente, pero **no sustituyen datos de streaming o ventas** que permitan calcular un SAM/SOM confiable para EAU.

**Infraestructura de derechos musicales:**
EAU licenció su **primera sociedad de gestión de derechos musicales, EMRA (Emirates Music Rights Association)**, el 10 de abril de 2025, bajo la Ley Federal 38/2021. Sus tarifas comerciales entran en vigor en **diciembre de 2026**. Esto significa que, a la fecha de este plan, **no existe un historial de recaudación de regalías locales equivalente a SAYCO/ACINPRO** — cualquier proyección de ingresos por regalías locales en EAU debe tratarse como especulativa hasta que EMRA tenga al menos un ciclo de operación comercial completo.

**Competencia:**
No se identificó, en esta investigación, un sello boutique enfocado específicamente en música urbana/latina operando desde EAU — lo que sugiere un espacio de posicionamiento abierto, pero también la ausencia de comparables para validar supuestos de mercado.

**Oportunidad estratégica: crear la categoría, no competir en ella.**
La ausencia de datos país-específicos y de un competidor boutique latino/urbano establecido en EAU no es solo una limitación de información — es, en sí misma, la tesis de inversión de este escenario. EAU no tiene hoy un sello independiente de música urbana/latina de referencia, y su sociedad de gestión de derechos musicales (EMRA) apenas nace en 2025. Entrar ahora, en la región de mayor crecimiento mundial en música grabada (MENA, +15.2% a +22.8% interanual), con una identidad de marca y un catálogo ya construidos en Colombia, no es llegar a competir por una porción de un mercado existente: es la oportunidad de **construir desde cero la infraestructura y la referencia de la industria de música latina/urbana en el Golfo**, antes de que exista un incumbente. Ese es el atractivo real para un inversionista que busca una posición de pionero, no una cuota de mercado — y es distinto, en naturaleza, a la oportunidad de Medellín (mercado maduro, de crecimiento orgánico del catálogo propio).

Hay además una razón adicional, cualitativa y no cuantificada en este documento, para priorizar Dubái: es un mercado con una de las concentraciones más altas del mundo de patrimonio privado y gasto de lujo (hospitalidad, eventos, entretenimiento premium), lo que abre líneas de ingreso que van más allá de las regalías de streaming — eventos privados, patrocinios de marca y shows premium pagados directamente por un público con alto poder adquisitivo. Esto encaja de forma natural con el posicionamiento ya existente de la marca ("REBEL LUXURY"). **Esta es una tesis estratégica, no una cifra de mercado**: no hay en este documento un dato verificado de gasto en entretenimiento musical de la población de alto patrimonio en EAU — se señala como argumento cualitativo a favor del escenario, pendiente de cuantificar con investigación local antes de usarse como proyección de ingresos.

**Conclusión del análisis de mercado para Dubái:** la oportunidad es real a nivel de señales de demanda, entorno regulatorio/fiscal (ver Sección 11) y posicionamiento de pionero de categoría, pero **no se puede construir un TAM/SAM/SOM defendible para EAU con los datos públicos disponibles hoy**. Se recomienda, si este escenario avanza, una investigación de mercado local pagada (o contacto directo con EMRA y promotores como Dubai Latin Fest/UNTOLD) antes de comprometer capital.

---

## 6. PLAN OPERATIVO

1. **Selección de talento:** scouting directo y por convocatoria, priorizando artistas con tracción orgánica inicial (seguidores, streams) sobre potencial no probado.
2. **Producción musical:** preproducción → grabación (estudio propio o alianzas) → mezcla y masterización → entrega final.
3. **Marketing y contenido:** toda la generación de piezas, guiones y calendarización se apoya en el Content Engine existente; el Social Media Manager cura y aprueba, no produce desde cero.
4. **Distribución:** vía Nexus (8% de comisión) a todas las plataformas de streaming relevantes en cada mercado.
5. **Gestión de derechos de autor:** registro de obras ante la entidad correspondiente al mercado de operación (SAYCO/ACINPRO en Colombia; EMRA en EAU, sujeto a las limitaciones de la Sección 5.2) y protección de los derechos del artista y del sello.
6. **Organización del trabajo:** gestión de proyectos online, comunicación asincrónica entre freelancers y el equipo fijo.

---

## 7. PLAN DE RECURSOS HUMANOS

La estructura es intencionalmente mínima:

- **Roles fijos (1-2 personas):** CEO/Director y, según volumen, un Social Media Manager part-time.
- **Roles variables/freelance (por proyecto):** Productor Musical, Ingeniero de Sonido, Gerente Comercial (puede ser por comisión en lugar de salario fijo en etapa temprana).
- **Asesores externos (no nómina):** Abogado, Contador.

Esta estructura puede escalar agregando un segundo rol fijo (Gerente Comercial de tiempo completo) cuando el flujo de proyectos de producción externa supere, de forma sostenida, los 4-5 proyectos mensuales.

---

## 8. GESTIÓN DE RIESGOS

| Riesgo | Mitigación |
|---|---|
| Cambios en gustos musicales / saturación del mercado | Diversificación de géneros dentro de lo urbano/latino; foco en desarrollo de marca del artista, no solo en un sencillo |
| Dependencia de un solo artista en el catálogo inicial | Captación activa de 2-3 artistas adicionales en el primer año |
| Flujo de caja insuficiente en etapa temprana | Mezcla de ingresos por producción a terceros (más predecible) con regalías de catálogo propio (más lenta) |
| Riesgos legales de derechos de autor/contratos | Asesoría legal especializada desde el primer contrato, no reactiva |
| Entorno regulatorio de derechos musicales inmaduro (EAU) | No proyectar ingresos de EMRA hasta que tenga historial comercial (post diciembre 2026) |
| Dependencia de Nexus como distribuidor único | Evaluar, a partir del año 2, una segunda vía de distribución o negociación de mejores términos según volumen de catálogo |
| Obsolescencia tecnológica del Content Engine propio | Mantenimiento y actualización continua del stack (Pillow/FFmpeg/edge-tts) como parte de la operación, no como proyecto aparte |

---

## 9. MARCA E IMAGEN CORPORATIVA

A diferencia del plan original, la identidad de marca de IM Music **ya existe y está en uso activo**, verificada contra la cuenta real @immusicsello:

- **Concepto:** REBEL LUXURY
- **Color primario:** violeta #5E17EB (fondo de toda pieza visual), negro #000000 (closing cards), crema #F2EDE5 y blanco #FFFFFF como acentos
- **Tipografías:** Sceageus (headline principal, sin excepción) y Anton (textos secundarios/CTA)
- **Logo:** `logo_immusic.png`, ya diseñado
- **Sistema de ilustración:** grabados estilo Gustave Doré en líneas finas sobre fondo violeta, con reglas de procesamiento ya codificadas (umbral de contraste, opacidad)

No hay trabajo de diseño de identidad pendiente: el trabajo restante es de **aplicación consistente** de esta identidad a nuevos mercados (adaptación de idioma/tono si se opera en Dubái) y a materiales de inversionista, no de creación desde cero.

---

## 10. ESTRATEGIAS DE GENERACIÓN DE INGRESOS

Líneas de ingreso reales y relevantes para un sello de este tamaño (se elimina toda línea de ingreso de servicios de marketing a empresas, que pertenecía a la agencia):

1. **Producción musical para terceros:** servicio de grabación/mezcla/masterización cobrado por proyecto. *Volumen realista: 2-4 proyectos externos por mes* (no 100 — esa cifra del plan anterior correspondía al modelo de agencia de automatización masiva, no a un sello boutique). Precio por proyecto: **supuesto a validar** con cotizaciones reales de mercado (ver limitación de datos en Sección 5.1 sobre tarifas de estudio en Medellín).
2. **Desarrollo de marca personal para artistas:** servicio de posicionamiento y estrategia de contenido para artistas externos al roster. Volumen y precio: **supuesto a validar**.
3. **Regalías de catálogo propio:** ingresos de streaming vía Nexus (menos 8% de comisión) de los artistas firmados por el sello. Depende directamente del crecimiento del catálogo y del desempeño de cada lanzamiento — es la línea de ingreso con mayor potencial a largo plazo pero la más lenta de construir.
4. **Licencias y sincronización (sync):** uso de música del catálogo en medios audiovisuales de terceros. Línea de ingreso incipiente, sin pipeline activo todavía — oportunidad a desarrollar, no ingreso proyectable en el corto plazo.
5. **Eventos y shows en vivo:** ingreso futuro, condicionado al crecimiento de base de fans de los artistas del roster; no se proyecta en los primeros 12-18 meses.

Todas las cifras de precio/ticket por servicio que no tengan fuente verificada en este documento se presentan como **supuestos pendientes de validar** en el Modelo Financiero IM Music — Sello, y deben confirmarse con cotizaciones reales antes de presentarse a un inversionista como dato cerrado.

---

## 11. ASPECTOS LEGALES

### 11.1 Colombia

- **Constitución:** Sociedad por Acciones Simplificada (SAS), registro ante Cámara de Comercio y DIAN.
- **Registro de marca:** ante la Superintendencia de Industria y Comercio (SIC).
- **Gestión de derechos de autor:** afiliación a SAYCO (autores/compositores) y ACINPRO (productores fonográficos). Ambas entidades publican requisitos documentales (SAYCO: identificación, formulario biográfico; ACINPRO: constitución legal de la empresa discográfica, formulario FO-A-16, certificación bancaria), **pero ninguna publica una tarifa de afiliación vigente para 2025** — este costo debe confirmarse llamando directamente a ambas entidades antes de incluirlo como cifra cerrada en el plan financiero.
- **Impuesto de renta:** tarifa general para sociedades (incluye SAS) del **35%** para los años gravables 2025 y 2026 (Art. 240 E.T., Ley 2277/2022). Existe un proyecto de reforma que bajaría la tarifa a partir de 2027, pero no está vigente.
- **Régimen Simple de Tributación (RST):** alternativa simplificada para emprendimientos pequeños; aplicabilidad y tarifa real para este tipo de negocio deben confirmarse en el simulador oficial de la DIAN antes de asumirla en el modelo financiero.
- **Contratos con artistas:** deben cubrir producción, promoción, distribución y reparto de regalías, con asesoría legal especializada en propiedad intelectual y derecho del entretenimiento.

### 11.2 Dubái / EAU

- **Estructura:** elegir entre zona franca (free zone) o territorio continental (mainland). Zonas francas relevantes para medios/música: Dubai Media City, Dubai Studio City, twofour54 (Abu Dhabi, exenta de tarifas de licencia los primeros 2 años), IFZA.
- **Costos de constitución:** las cifras disponibles son estimaciones de consultoras, no tarifas oficiales — por ejemplo, licencia en Dubai Media City entre AED 15,000-30,000/año con capital mínimo de AED 50,000; IFZA desde AED 12,900. **Se recomienda cotizar directamente con la zona franca elegida antes de usar estas cifras en un documento financiero formal.**
- **Impuesto corporativo:** 0% sobre los primeros AED 375,000 de ingreso gravable, 9% sobre el excedente. Las empresas de zona franca pueden mantener 0% sobre "ingreso calificado" solo si cumplen el test de Qualifying Free Zone Person y su ingreso no calificado no supera el menor de 5% del ingreso total o AED 5 millones — incumplir esto implica perder el beneficio por 5 años.
- **IVA:** 5% general; los servicios de medios/entretenimiento digital (incluyendo streaming) son explícitamente gravables, y el IVA pagado en insumos de entretenimiento generalmente no es recuperable.
- **Aranceles de importación:** 5% sobre valor CIF para equipo (cámaras, audio) importado — verificar código arancelario específico contra el Arancel Aduanero Unificado del CCG.
- **Gestión de derechos de autor:** EMRA, la primera sociedad de gestión de derechos musicales de EAU, se licenció en abril de 2025 bajo la Ley Federal 38/2021; sus tarifas comerciales entran en vigor en diciembre de 2026. No hay historial operativo previo.
- **Visas:** visa de empleo (2 años) estimada en AED 3,000-7,500 todo incluido; visa de inversionista, con información escasa, estimada en AED 7,000-20,000+ — ambas cifras requieren confirmación oficial antes de usarse en el plan financiero.

---

## 12. INDICADORES CLAVE DE RENDIMIENTO (KPIs)

**Financieros:** ingresos totales por línea (producción, regalías, licencias), margen neto, costo de adquisición de artista (CAA), valor de vida del artista (LTV) para el sello.

**De catálogo y desempeño artístico:** número de artistas firmados, canciones producidas por año, streams/oyentes mensuales por artista, crecimiento de seguidores en redes.

**De operación:** número de proyectos de producción externa cerrados por mes, tiempo promedio de entrega de un proyecto, satisfacción del artista (encuestas).

**De eficiencia del Content Engine:** piezas de contenido publicadas por semana vs. costo marginal, tiempo ahorrado frente a un flujo de trabajo manual equivalente.

---

## 13. ESTRATEGIA DE SALIDA PARA EL INVERSIONISTA

Las mismas opciones de salida aplican, evaluadas con mayor realismo dado el tamaño del negocio:

- **Venta de participación a otro inversionista:** fondos especializados en música, otros sellos independientes, inversionistas estratégicos del sector.
- **Adquisición por un sello mayor:** una vez el catálogo y el roster alcancen una masa crítica demostrable (streams, ingresos recurrentes).
- **Recompra por parte de los fundadores:** opción adicional, realista en un negocio de este tamaño, no contemplada en el plan original.

La Oferta Pública Inicial (OPI), mencionada en el plan original, es una opción teórica de largo plazo que no aplica a la escala actual de este negocio y no debería presentarse a un inversionista temprano como una expectativa realista de salida.

---

## 14. PRESENTACIÓN AL INVERSIONISTA / CONCLUSIÓN

IM Music ofrece una oportunidad de inversión en un sello discográfico independiente que ya opera (catálogo real, artista firmado, distribución activa vía Nexus) y que cuenta con una ventaja estructural verificable: un Content Engine propio que reduce drásticamente el costo de mantener presencia digital constante frente a cualquier sello boutique comparable.

El mercado colombiano de música grabada crece de forma sostenida y por encima del promedio mundial (+17.9% en 2025, IFPI), lo que da viento de cola al escenario Medellín — la base operativa real, con catálogo y artista ya activos.

El escenario Dubái se presenta con una lógica distinta y deliberada: no es una réplica del negocio colombiano en otra ciudad, sino una apuesta de **creación de industria**. EAU es la región de mayor crecimiento mundial en música grabada (MENA), tiene un entorno fiscal corporativo favorable, demanda en vivo creciente y verificable por música latina (J Balvin/UNTOLD, Dubai Latin Fest) — y, a la vez, carece por completo de un sello boutique de referencia en ese género y apenas estrena infraestructura de derechos musicales (EMRA, 2025). Para un inversionista, eso significa entrar antes de que exista competencia establecida, no después. **No cuenta hoy con datos de mercado país-específicos ni con infraestructura de regalías con historial comprobado**, así que se presenta como una opción de expansión de alta convicción pero de validación pendiente, no como una alternativa equivalente y lista para ejecutar en el corto plazo sin investigación local adicional.

Las cifras de inversión requerida, estructura de costos, punto de equilibrio y retorno proyectado para cada escenario se desarrollan en el documento **Modelo Financiero IM Music — Sello**, construido exclusivamente con supuestos de volumen reales para un sello de este tamaño y con cada cifra sin fuente verificable marcada explícitamente como pendiente de validación.
