# Modelo Financiero IM Music — Sello (notas en lenguaje simple)

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

## Qué conclusión estratégica sugiere esto

Medellín muestra un retorno fuerte, pero ese retorno está casi enteramente apalancado en un solo supuesto no validado: que el roster puede sostener el ticket de Marca 360. Antes de llevar esta TIR a un inversionista, hay que validar con al menos 2-3 artistas reales si pagarían ese servicio (o si se financiaría vía advance/financiamiento, como ya contempla la plataforma) — de lo contrario, el número es, en el mejor de los casos, una meta comercial, no una proyección. Dubái, incluso con el precio real del producto, no cierra el caso de negocio en 5 años — tratarlo como expansión financiada con las utilidades de Colombia, no como alternativa de lanzamiento día 1 con capital de inversionista.
