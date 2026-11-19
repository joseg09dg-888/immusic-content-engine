# Modelo Financiero IM Music — Sello (notas en lenguaje simple)

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

## Medellín, Colombia (COP)

- **Inversión requerida (NTI):** $210,275,000 COP (~USD $50,100) — sin cambio (el camp no agrega CAPEX).
- **Roster:** crece de 2 artistas (Año 1) a 15 (Año 5). Ocupación Marca 360: 30% → 70%, **supuesto propio, no dato de mercado**.
- **Año 1:** Ingresos **$421.5M** (bajó de $445.5M — el camp genera menos ingreso bruto que la producción suelta que reemplaza), EBITDA **$92.3M** (subió de $24.5M, +277%), Utilidad Neta **$47.3M** (subió de $3.3M).
- **Año 5:** Ingresos $2,287.4M, EBITDA $1,737.3M, Utilidad Neta $1,116.6M.
- **VAN (30% descuento): $770.0M COP positivo (subió de $612.1M). TIR: 107.1%** (subió de 90.2%).
- **Lectura honesta — ojo con esto:** el camp mejora la rentabilidad porque tiene mucho mejor margen (68.5% vs 10% de la producción suelta), **a pesar de generar menos ingreso bruto total** (2-4 eventos/año vs 36-72 proyectos/año de la producción mensual que reemplaza). No hay que confundir "margen alto por evento" con "impacto financiero enorme": cada camp aporta ~$41M de margen, y con solo 2-4 al año eso son $82-164M/año — real y valioso, pero sigue siendo secundario frente a Marca 360, que para el Año 5 mueve más de $1.700M. El camp es un complemento rentable, no el motor principal del negocio.

## Dubái, EAU (AED)

- **Inversión requerida (NTI):** AED 358,506 (~USD $97,600) — sin cambio (el camp no se incluye aquí).
- **Roster:** crece de 1 artista (Año 1) a 7 (Año 5). Ocupación Marca 360: 15% → 55%.
- **Año 1:** EBITDA -AED 410,238, Utilidad Neta -AED 434,803.
- **Año 5:** EBITDA +AED 86,000, Utilidad Neta +AED 61,435 — sigue siendo el único año positivo.
- **VAN (25% descuento): -AED 1,106,000. TIR: sigue sin ser calculable.** Sin cambio frente al corte anterior — el camp no se incluyó como ingreso en Dubái porque no es viable al precio actual.
- **Lectura honesta:** Dubái pierde, de nuevo, una fuente de rentabilidad que sí funciona en Medellín (el camp), ampliando la brecha entre ambos mercados. Confirma el patrón de todo este modelo: lo que funciona en Medellín no se traslada 1:1 a Dubái sin ajustar precio, y para Dubái siempre hace falta validación adicional antes de presentarlo con la misma confianza.

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
