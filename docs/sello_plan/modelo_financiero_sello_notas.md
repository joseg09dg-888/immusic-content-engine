# Modelo Financiero IM Music — Sello (notas en lenguaje simple)

## Corrección de arriendo: el espacio tiene que caber 4 funciones, no solo oficina

Gap real detectado por el usuario: el arriendo modelado ($2M COP/mes) era explícitamente "espacio reducido", pero el sello necesita un espacio que quepa oficina administrativa + estudio de grabación + área de foto/contenido + área de streaming/transmisión en vivo (para el streamer aliado y conciertos virtuales). $2M no alcanza.

- **Medellín:** subió a **$5.000.000 COP/mes** (punto medio del rango real de mercado que dio el usuario: $4M-$9M COP/mes según ubicación/tamaño), flagueado como supuesto a validar con ese rango explícito en Supuestos_COL.
- **Dubái:** subió a **AED 17.500/mes**, con referencia real encontrada: Al Quoz, el distrito de bodegas/estudios creativos de Dubái (galerías, estudios fotográficos, showrooms — calza con lo que necesita el sello), unidades de 2.100-2.700 pies² por AED 15.800-19.200/mes, antes de IVA 5% y comisión de agencia (fuentes: Dubizzle y PropertyFinder, listados 2026). Se agregó también la **comisión de agencia inmobiliaria** (~10% de la renta anual, práctica común en Dubái) como CAPEX único de AED 21.000.
- **No se modeló compra de sede propia** (~$3.000M COP) — es 12+ veces toda la Necesidad Total de Inversión actual (~$240M), decisión de Año 4-5+ con EBITDA acumulado real, no algo para el Año 1.

### Impacto honesto

**Medellín:** NTI $240.45M→**$258.45M COP**. Año1 EBITDA $172.99M→**$136.99M** (-21%), Utilidad Neta $97.6M→**$74.2M**. VAN $995.6M→**$913.3M**, TIR 119.6%→**107.3%**.

**Medellín reducido (Escenario B):** NTI $222.58M (subió de $204.58M). VAN $1,014.9M, TIR 126.2% (bajó de 141.9%).

**Dubái:** NTI AED 438,583→**AED 546,283**. Año5 EBITDA AED 236,458→**AED 25,498** (-89%), y lo más importante: **Utilidad Neta Año5 pasa de +AED 208,831 a -AED 6,959** — **Dubái ya no tiene NINGÚN año con utilidad neta positiva en todo el horizonte de 5 años** bajo el modelo completo (equipo fijo desde el día 1). VAN -AED 1,110,909→**-AED 1,712,425** (empeoró 54%).

**Lectura honesta:** este es, otra vez, el mismo patrón de todo este modelo — cada corrección de costo real hace que Dubái se vea peor, nunca mejor, porque los costos reales ahí (ahora también el arriendo) son sistemáticamente más altos que lo que el modelo anterior asumía. El escenario de Dubái completo (equipo fijo local desde el día 1) queda cada vez más lejos de ser defendible frente a un inversionista sin: (a) validar demanda real, o (b) usar el modelo Dubái Lean/por fases en su lugar (que sí es positivo, ver `modelo_financiero_sello_dubai_lean_notas.md`).

## Reorganización del workbook (formato/estructura, sin cambiar ningún número)

El usuario reportó que `modelo_financiero_sello.xlsx` era ilegible comparado con el Excel de referencia (`financiero_viejo.xlsx`). Se corrigieron 4 problemas reales:

1. **Bug de referencia rota:** el resumen prometía pestañas `Supuestos_COL`/`Supuestos_DXB` que en realidad se llamaban solo `COL`/`DXB`. Ya están creadas con el nombre correcto.
2. **Formato numérico roto:** casi todas las celdas de dinero mostraban floats crudos sin separador de miles (ej. `384267164.672`). Se aplicó formato `#,##0` a toda celda de dinero en las 12 pestañas.
3. **Columna de notas ilegible:** la columna "Nota" de 75 de ancho con texto largo pegado a cada fila de dato se acortó a una referencia corta ("Ver Supuestos_COL") — el texto completo vive solo en Supuestos_COL/DXB.
4. **OPEX reestructurado en bloques con subtotal**, como en el Excel viejo: EQUIPO/NÓMINA (con columnas Puesto | Salario Base | Factor Prestaciones | Costo Empresa, igual que la Tabla 2 del ejemplo), ADECUACIONES Y ARRIENDO, HERRAMIENTAS Y TECNOLOGÍA (cada herramienta por separado: Notion, WhatsApp Business, Make, CapCut Pro, Canva Pro, Google Drive), PAUTA Y PUBLICIDAD/MARKETING (pauta separada de marketing genérico), OTROS/ADMINISTRATIVOS. Cada bloque con subtotal, y el total mensual es la suma de subtotales.

**Verificado: todos los totales de Medellín y Dubái quedaron idénticos a la versión anterior** (NTI, EBITDA, Utilidad Neta, VAN y TIR de ambos mercados no cambiaron ni un peso/dirham) — esto fue reorganización de formato, no un recálculo.

## Nueva pestaña: COMPARATIVO_ESCENARIOS (Escenario A vs Escenario B)

El usuario aclaró que la pregunta real no es "Medellín o Dubái" en abstracto, sino **dónde se radica el fundador**. Se agregó una pestaña con 4 bloques y 2 escenarios combinados, sin recomendar cuál elegir:

- **Bloque 1 — Medellín completo** (el modelo de siempre, equipo fijo local).
- **Bloque 2 — Dubái completo** (el modelo de siempre, equipo fijo local).
- **Bloque 3 — Dubái Lean/por fases** (archivo separado ya existente, `modelo_financiero_sello_dubai_lean.xlsx`, fundador radicado allá con escalamiento gradual — NTI AED 168.787, VAN +AED 35.292, TIR 29,1%, único bloque de Dubái con TIR positiva, pero solo tiene datos de Año 1/3/5).
- **Bloque 4 — Medellín reducido (NUEVO):** si el fundador se muda a Dubái, Comunicadora/Filmmaker/Diseñadora se comparten remoto desde allá y dejan de ser costo fijo de Medellín; se agrega un **Project Manager — Élite 360** (rol nuevo, no presupuestado antes, costo estimado sin cotización) para cubrir el roster existente. El ingreso se asume igual al Bloque 1 (el catálogo no desaparece porque el fundador se mude). Resultado: **NTI $204.575.000 COP** (bajó de $240.450.000), **VAN $1.097.190.960 COP, TIR 141,9%** (subió de 119,6% — el equipo reducido es, lógicamente, más rentable que el completo).
- **Escenario A = Bloque 1 + Bloque 3.** **Escenario B = Bloque 2 + Bloque 4.**

**Nota metodológica importante:** no se combina VAN/TIR entre bloques en monedas y tasas de descuento distintas en una sola cifra — sería una mezcla matemáticamente cuestionable. Se muestran EBITDA/Utilidad Neta nominal por año (sumas válidas) y VAN/TIR por bloque, separados.


Acompaña a `modelo_financiero_sello.xlsx`. Versión 3: estructura de ingresos del roster corregida — tope duro de 12-15 artistas, servicio "Marca 360" al precio REAL de la plataforma (USD $2,999.99/mes/artista), regalías de catálogo como línea única (inversión propia en proyectos especiales, caso por caso), más YouTube propio y el libro. Legal reducido casi a cero (el fundador cubre el día a día).

## Nueva línea: alianza con streamer (CAPEX único, sin ingreso garantizado)

Se agregó un CAPEX único de setup de transmisión (cámara + capturadora + micrófono + kit de luces) para firmar/apoyar a un creador de contenido en vivo a cambio de exposición de marca/roster: **$3,000,000 COP (Medellín) / AED 2,623 (Dubái)**, ambos marcados como **supuesto conservador — no hay streamer identificado ni cotización real**. No se modela ningún ingreso garantizado de esta línea: el retorno esperado es marketing/exposición, cualitativo. Se deja una fila de **memo** (NO sumada a Ingresos Totales ni a TIR/VAN) con un upside opcional muy conservador, solo por si se llegara a negociar un % de los ingresos del streamer — explícitamente marcado como no garantizado.

## Nuevo OPEX: 3 roles humanos (Comunicadora, Filmmaker/Editor IA, Diseñadora)

Se agregaron al equipo (el principio lean de marketing/video 100% automatizado se mantiene, pero estos 3 roles cubren dirección de estrategia y trabajo bespoke que el Content Engine no hace):
- **Comunicadora / Estrategia de Contenido** (fijo/part-time): ajustada por analogía al Social Media Manager ya existente — $2,000,000 COP/mes / AED 6,000/mes, **sin cotización propia independiente**.
- **Filmmaker / Editor con IA** (freelance, ~1.5 proyectos/mes): $1,200,000 COP/mes / AED 1,049/mes, **estimación conservadora sin cotización real**.
- **Diseñadora Gráfica** (freelance, ~1.5 proyectos/mes): $750,000 COP/mes / AED 656/mes, **estimación conservadora sin cotización real**.

Este OPEX nuevo pesa doble en el modelo: sube el gasto mensual recurrente **y** sube el capital de trabajo (6 meses de OPEX), por lo que el NTI sube más de lo que parece a primera vista.

## Corrección de margen: Producción Musical para terceros (según experiencia real del usuario)

Esta línea estaba modelada con 50% de margen (heredado, erróneo, del plan anterior). Según experiencia real del usuario en la industria, la producción musical para terceros normalmente **no deja margen real** una vez se contabilizan costos de estudio, tiempo de productor/ingeniero y equipo: es casi punto de equilibrio, y su función real es ser puerta de entrada de relación/A&R con artistas externos, no motor de rentabilidad. Se bajó el margen a **10% real** (C.V.U. del 90% del precio) en ambos mercados. No se tocó ninguna otra línea de ingreso.

## Nueva línea: Campamento de Creación / turismo artístico (reemplaza la producción suelta)

Validado con investigación real (`docs/sello_plan/investigacion_campamentos_musicales.md`): empacar la producción en un camp de **12 artistas × 3 noches** es la forma real de monetizarla — no venderla como proyecto suelto mes a mes (eso ya se corrigió a margen casi nulo). La línea "Producción musical para terceros" queda en cero (superada, no borrada del código) y se reemplaza por esto:

- **Medellín:** ingreso $60.000.000 COP/camp (12 × $5.000.000, dato del fundador). Costos: finca 3 noches $3.500.000 (cotización real) + alimentación ~20 personas × 3 días $5.400.000 (**supuesto, sin fuente Medellín verificada**) + 3-6 productores/ingenieros freelance × 3 días, punto medio $5.400.000 (**supuesto, sin fuente verificada**) + Filmmaker+Diseñadora+Comunicadora 3 días $3.600.000 (se asume **adicional** al retainer mensual, no cubierto por él, para no subestimar costo) + transporte $1.000.000 = **$18.9M costo, margen ~$41.1M (68.5%)**. Volumen: **2 a 4 camps/año** (ramp [2,3,3,4,4]) — es un evento, **no un servicio mensual recurrente**.
- **Dubái: NO viable al precio actual.** Convirtiendo el mismo precio (~AED 48.280 de ingreso), solo villa+catering para ~20 personas×3 días ya consumen AED 49.000-52.000 (91-96% del ingreso) — sin margen para producción, staff ni vuelos del equipo desde Medellín. Se deja en **0 camps/año** explícitamente — no se inventa un precio mayor sin validar.

## Nueva línea: Representación / Entrada a Mercado (precio real ya cotizado)

Coincide exactamente con `plan_negocios_sello.md` Secciones 4 y 10: servicio de booking/representación para artistas **externos al roster** (sin inversión de catálogo ni producción de video, a diferencia de Élite 360). Dos modalidades con **precio real ya cotizado**: Servicio completo USD $2.000/mes, Solo dirección USD $1.000/mes — se modela con un blend 50/50 (USD $1.500/mes promedio, supuesto de mezcla, no de precio). Volumen: 1-2 clientes simultáneos al inicio, creciendo a 5 para el Año 5 (supuesto a validar, limitado por capacidad del agente de booking). Costo: el tiempo principal ya es del Gerente Comercial, **ya pagado como OPEX fijo** — no se duplica aquí, solo se resta un 5% de costo incidental, así que el margen de esta línea es alto (95%). Se incluye **igual en ambos mercados, al mismo precio en USD** (no se convierte a una cifra distinta) — en Dubái, "entrada a mercado" es literalmente parte de la tesis estratégica del escenario (Sección 5.2).

## Cambio de estructura: Filmmaker y Diseñadora Gráfica pasan de freelance a planta fija

Confirmado por el usuario: ambos tienen acceso a la metodología de marca ya formalizada por escrito, y no se quiere personal rotativo con esa exposición (ver `plan_negocios_sello.md` Secciones 3.2, 6.1 y 7, ya actualizadas con "Fijo"). Esto cambia dos cosas:
- **OPEX:** el costo pasa de variable/por-proyecto (~1.5 proyectos/mes cada uno) a salario fijo mensual, nómina recurrente incluso en meses sin proyectos de diseño/video. Referencia salarial propia nivel junior-mid, **supuesto a validar**: Filmmaker $2,200,000 COP/mes (AED 6,500), Diseñadora $2,000,000 COP/mes (AED 6,000).
- **CAPEX:** el sello ahora es dueño de la estación de edición y de diseño (equipo de cómputo + periféricos) de ambos roles, ya que no traen su propio equipo: +$14,500,000 COP (Medellín) / +AED 12,677 + arancel de importación AED 634 (Dubái). Las licencias de software (CapCut Pro, Canva Pro) siguen en OPEX, sin duplicarse.

## Medellín, Colombia (COP)

- **Inversión requerida (NTI):** $240,450,000 COP (~USD $57,300) — subió $30.2M por el CAPEX nuevo y el OPEX fijo más alto (afecta también el capital de trabajo).
- **Roster:** crece de 2 artistas (Año 1) a 15 (Año 5). Ocupación Marca 360: 30% → 70%, **supuesto propio, no dato de mercado**.
- **Año 1:** EBITDA **$172.99M** (bajó de $199.99M, -13.5%), Utilidad Neta **$97.6M** (bajó de $117.4M, -16.9%).
- **Año 5:** EBITDA $2,059.7M, Utilidad Neta $1,324.0M.
- **VAN (30% descuento): $995.6M COP positivo (bajó de $1,071.1M). TIR: 119.6%** (bajó de 136.6%).
- **Lectura honesta:** el impacto es real pero no catastrófico — el negocio sigue siendo muy rentable bajo estos supuestos. Tiene sentido que el impacto sea moderado: la nómina fija recurrente de 2 roles junior-mid es chica frente a la escala de ingresos que ya mueve Marca 360 para esta altura del modelo.

## Dubái, EAU (AED)

- **Inversión requerida (NTI):** AED 438,583 (~USD $119,400) — subió AED 80,077 (+22.3%).
- **Año 4:** EBITDA vuelve a ser **NEGATIVO (-AED 37,788)**, perdiendo el segundo año positivo que había ganado con la línea de Representación/Entrada a Mercado en el corte anterior (ahí era +AED 116,496).
- **Año 5:** EBITDA +AED 236,458 (bajó de +AED 399,999), Utilidad Neta +AED 208,831 (bajó de +AED 375,395) — sigue siendo el único año positivo.
- **VAN (25% descuento): -AED 1,110,909** (empeoró 71% frente a -AED 648,026). **TIR: sigue sin ser calculable.**
- **Lectura honesta — hay que decirlo claro:** este cambio de estructura le pega fuerte a Dubái, mucho más que a Medellín en términos relativos, y **borra casi toda la mejora que había logrado la línea de Representación/Entrada a Mercado** en el paso anterior. La causa es la misma de siempre: salarios y equipo en EAU cuestan más, y dos nóminas fijas adicionales pesan mucho más sobre una base de ingresos todavía pequeña ahí. Si el plan es contratar Filmmaker y Diseñadora en planta fija también para la operación de Dubái, valdría la pena evaluar si realmente se necesitan ahí desde el día 1, o si ese contenido se puede seguir produciendo desde el equipo de Medellín mientras el roster de Dubái crece — antes de presentarlo así a un inversionista.

## Qué es un dato real confirmado vs. qué sigue siendo supuesto

**Confirmado (no es un supuesto):**
- Precio de Marca 360: USD $2,999.99/mes/artista — viene directo del código de la plataforma IM Music (plan "ÉLITE 360 / ARTIST DEVELOPMENT 360").
- El libro "Music Business Para Todos Los Humanos" es un producto real ya en venta en Hotmart (ES/EN/PT) — lo que no está confirmado es el VOLUMEN de ventas proyectado.
- Impuesto de renta SAS Colombia 35% (2025-2026); impuesto corporativo EAU 0% hasta AED 375,000 y 9% después; IVA EAU 5%.
- Comisión Nexus 8% sobre regalías distribuidas.

**Supuesto a validar (no inventar como dato cerrado ante un inversionista):**
- **La ocupación/retención del plan Marca 360** — es el supuesto más importante de todo el modelo. No hay ningún dato sobre qué fracción de un roster de artistas emergentes puede o quiere pagar $36,000 USD/año por este servicio.
- Costo de afiliación SAYCO/ACINPRO (Colombia) — no hay tarifa pública, hay que llamar directamente.
- Cotización real de tratamiento acústico y equipo de estudio en Medellín (el rango $25M-$50M COP es heredado del plan anterior, sin cotización 2025/2026).
- Salarios reales de CEO/Director del sello y Gerente Comercial en Medellín (solo el rol de Social Media Manager tiene rango verificado).
- Todo el CAPEX de Dubái y el precio de Marca 360 convertido a AED: son conversiones vía tipo de cambio, **no cotizaciones ni validaciones locales de EAU**.
- Precio y volumen de "producción musical" y "desarrollo de marca personal" para clientes externos (no roster) — ambos anclados en el plan anterior, nunca verificados con cotizaciones de mercado actuales.
- Volumen y % de regalías de catálogo por inversión en proyectos especiales — depende de cuántos proyectos así se financien cada año, hoy en cero.
- Vistas/RPM del canal de YouTube propio.

## Nueva línea: eventos de industria, pauta puntual de lanzamiento, y rifa de Élite 360 (Medellín)

El fundador preguntó si las estrategias de promoción y financiamiento ya descritas en `plan_negocios_sello.md` Secciones 10.1 y 10.2 (eventos como Circulart/BOmm/BIME/Latin Alternative Music Conference/XP Music Futures, pauta puntual en cuentas de farándula tipo Última Hora Colombia, y la rifa de un año de Élite 360) estaban reflejadas en el modelo financiero real. No lo estaban — se agregaron ahora.

**1. Eventos de industria (OPEX_COL, nuevo bloque anual, fila 52+):** Circulart $300.000 COP (punto medio 200-400k, supuesto 2027), BOmm $0 (convocatoria, sin costo público), BIME Bogotá $680.000 COP (estimado por analogía con BIME Bilbao, NO tarifa real de Bogotá), Latin Alternative Music Conference $415.800 COP ($99 USD × 4.200 COP/USD, precio real confirmado), XP Music Futures $0 (costo no anunciado). Subtotal: **$1.395.800 COP/año**.

**2. Pauta de lanzamiento puntual:** $9.000.000 COP/año (2 lanzamientos/año × $4,5M COP, punto medio del rango 4-5M que estima el fundador sin tarifa pública confirmada de Última Hora Colombia) — modelada aparte del presupuesto mensual de pauta digital ($1.200.000 COP/mes), tal como exige la Sección 10.1 (un solo post de 4-5M consumiría 2.7-3.3 meses de ese presupuesto si se tratara como gasto mensual).

**3. Rifa de un año de Élite 360:** el fundador decidió ejecutarla pese al riesgo legal ya documentado (Sección 10.2 — Coljuegos, Ley 643/2001, 35+ procesos activos). Se modela el **efecto neto**, no el ingreso bruto: escenario central $50.000 COP × 910 boletas = $45.500.000 COP recaudados, menos ~$35M COP de costo incremental real (producción de 3-4 canciones+video, pauta dedicada, imprevistos — ya detallado en la Sección 10.2) = **+$10.500.000 COP neto, solo en Año 1** (nueva fila "Otros ingresos — financiamiento neto por rifa Elite 360" en `EstadoResultados_COL`, antes de Ingresos Totales).

**Impacto honesto en cascada (Medellín, `EstadoResultados_COL` / `FlujoCaja_TIR_VAN_COL` / `RESUMEN_COMPARATIVO` / `COMPARATIVO_ESCENARIOS` Bloque 1):**

| Indicador | Antes | Después |
|---|---|---|
| OPEX anual Año 1 | $291.200.000 | $301.595.800 |
| Ingresos Totales Año 1 | $534.899.698 | $545.399.698 |
| EBITDA Año 1 | $136.989.698 | $137.093.898 |
| Utilidad Neta Año 1 | $74.242.803 | $74.310.534 |
| EBITDA Año 5 | $2.010.689.941 | $2.000.294.141 |
| Utilidad Neta Año 5 | $1.292.147.961 | $1.285.390.692 |
| VAN (30%) | $913.329.955 | $902.122.153 |
| TIR | 107,3% | 106,5% |

**Lectura honesta:** el Año 1 mejora muy levemente (+$67.731 en utilidad neta) porque el ingreso neto de la rifa ($10,5M) casi compensa el nuevo costo anual de eventos+pauta puntual ($10,4M) — es casi un empate, no una mejora real de fondo. Los Años 2-5 **empeoran** de forma consistente (-$6,76M COP en utilidad neta cada año) porque el nuevo costo anual de eventos/pauta se mantiene, pero la rifa es un ingreso de una sola vez en el Año 1. El VAN baja ~1,2% y la TIR baja 0,8 puntos — es un impacto pequeño pero real, y debe reportarse así, no esconderse.

**Propagación a Dubái — auditada en una ronda posterior, con resultado real y específico por concepto (no un "sí" o "no" uniforme):**
- **Eventos de industria**: no se agregó ningún costo a Dubái completo — Circulart/BOmm/BIME Bogotá/Latin Alternative Music Conference son eventos colombianos/internacionales sin relación directa con la operación en EAU. El único evento real de la región (XP Music Futures, Riad) no tiene costo anunciado públicamente — no se inventa cifra.
- **Pauta puntual tipo "Última Hora Colombia"**: no se investigó un equivalente para Dubái — queda pendiente, no inventado.
- **La rifa NO se propaga a Dubái, por una razón legal verificada, no por descuido**: en EAU el juego de azar (incluidas rifas/loterías) es delito penal bajo el Artículo 355, con solo 3 loterías autorizadas en todo el país (régimen de licencia nacional del Ministerio de Economía/GCGRA) y sin una vía de autorización municipal de bajo trámite comparable a Coljuegos — fuentes: Al Tamimi & Co., Gulf News, Khaleej Times. Es una diferencia real entre mercados: lo que en Colombia es una decisión de riesgo ya tomada conscientemente (Sección 10.2 del plan), en EAU sería un delito sin vía de autorización accesible disponible.
- Hallazgo aparte, fuera del alcance de este archivo: "Dubai Latin Fest", citado como señal de demanda en la Sección 5.2 del plan de negocios, no se pudo confirmar como evento real indexable en esta ronda de investigación — señalado para que el plan de negocios lo revise, no corregido aquí.

**Sí se propagó, con mejora real y sustancial, a `modelo_financiero_sello_dubai_lean.xlsx`** (Dubái Lean): se completó la línea "Representación/Entrada a Mercado" que estaba ausente ahí (ver notas de ese archivo para el detalle completo) — VAN de ese escenario pasó de +AED 35.292 a +AED 493.278, TIR de 29,1% a 78,2%.

**No se propagó a:** el Bloque 4 "Medellín Reducido" / Escenario B de `COMPARATIVO_ESCENARIOS` (tiene su propia estructura de OPEX con Project Manager y equipo remoto que no es recalculable desde este workbook sin inventar cifras) — pendiente si se quiere consistencia total entre todos los escenarios.

**Pendiente de validar, no inventado:** número real de lanzamientos/año que recibirían pauta puntual (se asumió 2, conservador); si los eventos se repiten cada año al mismo costo (se asumió flat, sin crecimiento, en los 5 años); costo real de la rifa si se cotiza formalmente (el costo incremental de $30-40M sigue siendo estimado, no cotizado, per Sección 10.2).

## Qué conclusión estratégica sugiere esto

Medellín muestra un retorno fuerte, pero ese retorno está casi enteramente apalancado en un solo supuesto no validado: que el roster puede sostener el ticket de Marca 360. Antes de llevar esta TIR a un inversionista, hay que validar con al menos 2-3 artistas reales si pagarían ese servicio (o si se financiaría vía advance/financiamiento, como ya contempla la plataforma) — de lo contrario, el número es, en el mejor de los casos, una meta comercial, no una proyección. Dubái, incluso con el precio real del producto, no cierra el caso de negocio en 5 años — tratarlo como expansión financiada con las utilidades de Colombia, no como alternativa de lanzamiento día 1 con capital de inversionista.
