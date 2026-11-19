# PLAN DE NEGOCIOS: IM MUSIC — ELITE ARTIST PLATFORM

## 1. Resumen Ejecutivo

IM Music — Elite Artist Platform es una plataforma SaaS de distribución musical digital, nacida dentro del ecosistema de IM Music (el sello discográfico) como una herramienta propia que ahora se constituye en un negocio independiente y escalable. A diferencia de los distribuidores DIY genéricos (DistroKid, TuneCore, CD Baby, UnitedMasters), IM Music Platform integra en un solo producto: distribución a las plataformas de streaming principales, administración de regalías y splits, un módulo de evaluación de elegibilidad para financiamiento de artistas, un marketplace de beats, tracking de certificaciones RIAA y un agente legal con IA — todo pensado desde y para el mercado de artistas independientes latinoamericanos, con una pasarela de pago local (Wompi, Colombia) además de Stripe.

**Estado real del producto:** existe hoy un backend funcional (Node.js/Express/TypeScript, PostgreSQL vía Neon) y un frontend (React/Vite) con la mayoría de estos módulos ya codificados — no es solo una idea en papel. Sin embargo, el producto **no está en producción, no ha pasado por QA formal, no tiene revisión legal de sus términos de servicio, y su tabla de precios actual en el código es un borrador con errores** (ver sección 5). Este plan presenta la oportunidad de negocio y la hoja de ruta para llevarlo de prototipo funcional a producto lanzable.

El sello IM Music actúa como primer cliente ancla y caso de uso real: sus propios artistas (incluyendo el ya firmado "LA S — El Diablo del Chanteo") pueden ser los primeros usuarios reales de la plataforma antes de abrirla al mercado.

### Etapa de Financiamiento Recomendada: PRE-SEED

Con base en la auditoría real del producto (prototipo funcional backend+frontend, **cero usuarios reales, cero ingresos**, sin QA formal, sin revisión legal de términos de servicio, sin producción desplegada, y un equipo de desarrollo esencialmente unipersonal), esta plataforma se encuentra inequívocamente en **etapa Pre-Seed**, no Seed y mucho menos Series A. Esto importa porque determina a qué tipo de inversionista y de ronda aplicar:

- **Por qué no es Seed:** una ronda Seed estándar en la industria de VC espera evidencia de tracción — usuarios activos reales, algo de ingreso recurrente (aunque sea mínimo), o al menos un producto en producción siendo usado por terceros. Nada de esto existe hoy.
- **Por qué no es Series A:** Series A exige métricas de crecimiento comprobadas (MRR creciente, retención, unit economics validados) sobre una base de usuarios ya existente. Esta plataforma no tiene ni la base de usuarios ni las métricas.
- **Por qué sí es Pre-Seed:** Pre-Seed es la ronda diseñada exactamente para este caso — un prototipo funcional construido (reduce el riesgo de ejecución técnica frente a una idea en papel), un founder/equipo con dominio del dominio (el sello real, los artistas reales, el conocimiento de la industria musical latina), y una tesis de mercado clara, pero sin tracción comercial todavía. El capital Pre-Seed en este caso debe destinarse a: cerrar las brechas de producción (QA, seguridad, legal), ejecutar la Fase 1 del Go-to-Market (roster propio) para generar la primera evidencia de tracción real, y recién ahí calificar para una ronda Seed.

## 2. Descripción del Producto

**Qué es:** una plataforma SaaS de autoservicio para que artistas y sellos independientes distribuyan su música a las plataformas de streaming, administren sus regalías y colaboraciones, y accedan a herramientas adicionales de crecimiento y financiamiento — todo desde un solo panel.

**Para quién:** artistas independientes (principalmente urbano/latino en una primera fase), productores que quieren vender beats, y sellos pequeños que gestionan varios artistas bajo una sola cuenta.

**Estado real de desarrollo:**
- Backend funcional con integración real a la API de Spotify, Stripe y Wompi.
- Frontend construido en React/Vite (prototipo, generado parcialmente con herramientas de AI Studio — revisar calidad/seguridad del código antes de producción).
- Falta: pruebas de carga, auditoría de seguridad (maneja dinero y datos de terceros), términos de servicio y política de privacidad revisados por un abogado, pruebas de los flujos de pago en ambiente real (no solo sandbox), definición de SLA de soporte.

### Módulo Blockchain — honestidad sobre su estado real

En el código existe un endpoint `verifyBlockchain` (en `publishingController.ts`) y una tabla `blockchain_verifications` que guardan un `tx_hash` y un `certificate_url` para certificar regalías/contratos. El frontend (`Wallet.tsx`) incluso tiene un método de pago tipo "crypto" como opción, bajo un branding interno tipo "Neural Wallet"/"Neural Distributions". **Esto NO es una implementación real on-chain:** el propio código marca la transacción como "// Simulate blockchain transaction", y no existe ninguna librería de blockchain real en el proyecto (no hay ethers.js, web3.js, Solidity ni SDK de wallet alguno en `package.json`).

Lo correcto y honesto es presentar esto como **arquitectura blockchain-ready**: un módulo de verificación de certificados de regalías/contratos ya diseñado y simulado en código, con la implementación on-chain real (verificación de contratos de regalías inmutable, y a futuro financiamiento de artistas tokenizado) como ítem de roadmap, no como funcionalidad ya operativa. Es un diferenciador de producto legítimo frente a la competencia — ninguno de los distribuidores comparados en la sección 4 ofrece esto — pero presentarlo ante un inversionista como "ya funciona on-chain" sería engañoso y debe evitarse explícitamente en cualquier pitch o deck.

## 3. Análisis de Mercado

**TAM — Mercado global de distribución musical digital DIY:** el segmento de artistas independientes que se autodistribuyen es la parte de más rápido crecimiento de la industria musical grabada global, impulsado por el crecimiento sostenido del streaming (IFPI Global Music Report 2026 reporta ingresos globales de música grabada de USD $31.7 mil millones en 2025, +6.4% — dato ya verificado en este proyecto en el plan del sello). No se encontró en esta investigación una cifra pública y confiable del tamaño específico del submercado "distribución DIY" a nivel global — **se marca como supuesto a validar** con una fuente de la industria tipo MIDiA Research o Water & Music antes de usarla frente a un inversionista.

**SAM — Artistas independientes LatAm/Colombia:** Colombia facturó ~USD $105.2M en música grabada en 2025 (+17.9%, IFPI 2026, ya verificado en el plan del sello), con 78% proveniente de streaming. El universo de artistas emergentes colombianos (16-31 años) se estimó en el plan de negocio viejo en ~35.000 a nivel nacional y ~5.250 en Medellín (estimación propia del plan anterior basada en cruces de DANE/SAYCO — **no es una cifra oficial, es un supuesto heredado, válido como orden de magnitud pero a validar**).

**SOM — Lanzamiento inicial:** fase 1 cerrada al roster propio de IM Music (caso de uso real, bajo riesgo). Fase 2: artistas independientes de Medellín, apalancando la red del propio sello y su comunidad (ej. grupo de Facebook "Red de Músicos en Medellín", 10k seguidores, ya usado como canal de promoción del libro del sello). No hay una cifra de penetración de mercado proyectada todavía — se recomienda definirla en el Modelo Financiero con supuestos conservadores (decenas de artistas en año 1, no miles).

## 4. Análisis Competitivo

| Plataforma | Precio (2025/2026, verificado vía fuentes de terceros — confirmar en sitio oficial) | Modelo | Diferencial vs. IM Music |
|---|---|---|---|
| **DistroKid** | Musician $24.99/año (1 artista); Musician Plus ~$44.99/año (2 artistas); Ultimate desde $89.99/año (5-100 artistas) | Suscripción anual, distribución ilimitada, artista conserva 100% regalías | Sin financiamiento integrado, sin agente legal IA, sin pasarela de pago local LatAm |
| **TuneCore** | Rising Artist ~$24.99/año; Breakout Artist ~$44.99/año; Professional ~$54.99/año (cifras varían entre fuentes); comisión de publishing subida de 15% a 20% desde enero 2026 | Suscripción anual ilimitada + opción legacy pago-por-release | Comisión de publishing relativamente alta; sin marketplace de beats |
| **CD Baby** | $9.99/sencillo, $14.99/álbum (pago único, sin renovación) + 9% de comisión permanente sobre ingresos de distribución; CDB Boost add-on $39.99/release | Pago por release, sin suscripción | Más económico a bajo volumen (1-5 lanzamientos/año), pero la comisión permanente del 9% pesa a largo plazo |
| **UnitedMasters** | DEBUT+ ~$19.99/año; SELECT ~$59.99/año ($5/mes) | Suscripción + oportunidades de marca/sync (no garantizadas) en el tier superior | Fuerte en partnerships de marca; sin foco específico en LatAm ni en financiamiento |
| **IM Music Platform** | A definir (ver sección 5) | Suscripción + marketplace de beats + financiamiento + agente legal IA | Pasarela Wompi (LatAm), nace de un sello real con artistas reales, no es una herramienta genérica — integra desarrollo de artista, no solo distribución |

**Nota:** los precios de la competencia provienen de agregadores/trackers de terceros (PricingSaaS, Subger, Toolradar, RouteNote, OnesToWatch), no de las páginas oficiales directamente — varias cifras entre fuentes no coinciden exactamente (ej. TuneCore Professional reportado entre $49.99 y $54.99). **Confirmar en las páginas oficiales de cada competidor antes de publicar esta tabla a un inversionista.**

**Diferenciación real de IM Music:** (1) financiamiento de artistas integrado (módulo de elegibilidad ya construido, inspirado en el partnership declarado con Sound Royalties), (2) agente legal con IA para consultas de contratos/derechos — ningún competidor listado lo ofrece, (3) pasarela de pago Wompi nativa para Colombia (ningún competidor global la tiene), (4) marketplace de beats integrado (acerca el producto a BeatStars, pero dentro del mismo panel de distribución), (5) viene de un sello real con artistas reales, no es una herramienta aislada de un tercero sin trayectoria en la industria.

## 5. Modelo de Precios (Rediseñado)

La tabla de precios actual en el código (`wompiController.ts`) es un borrador con un error evidente: el plan "Músico Plus" ($3.75) cuesta menos que el plan "Básico" ($15), a pesar de ofrecer más artistas. **No se debe usar esa tabla en ningún documento para inversionistas.** Propuesta de estructura corregida, benchmarked contra la competencia verificada en la sección 4 (precios de referencia anuales, a validar con el equipo antes de fijarlos):

| Plan | Precio propuesto (año) | Artistas | Posicionamiento |
|---|---|---|---|
| Básico | ~$19-25 USD/año | 1 | Entrada, competitivo con DistroKid Musician / TuneCore Rising |
| Plus | ~$39-45 USD/año | 2-3 | Agrega splits avanzados, fecha de lanzamiento programable |
| Premium | ~$69-80 USD/año | 5 | Incluye acceso al marketplace de beats y al módulo de financiamiento |
| Sello (Enterprise) | ~$120-150 USD/año | 10+ | Reportes consolidados, API, agente legal IA incluido |

Estos números son un punto de partida estratégico, no una tarifa cerrada — deben validarse con margen real (costo de Stripe/Wompi por transacción, costo de servidor/DB, soporte) en el Modelo Financiero IM Music — Plataforma SaaS.

## 6. Modelo de Negocio / Fuentes de Ingreso

1. **Suscripciones** (por artista/plan, ver sección 5) — ingreso recurrente principal.
2. **Comisión del marketplace de beats** — % sobre cada venta de beat entre productores y artistas (el modelo ya tiene un campo `precio` en beats; falta definir el % de comisión de la plataforma).
3. **Fee de originación en financiamiento** (si aplica) — si el financiamiento se ejecuta vía un partner como Sound Royalties, posible comisión por originar la solicitud; **esto depende de un acuerdo comercial real con el partner, no confirmado en este plan — supuesto a validar.**
4. **Servicios de certificación RIAA** — posible fee de gestión/tracking, bajo volumen esperado.
5. **Upsell cruzado con el sello** — artistas de la plataforma que usan servicios de producción/desarrollo de marca del sello IM Music (ver Plan de Negocios del Sello, documento separado).

## 7. Estrategia Go-to-Market

**Fase 1 — Roster propio del sello:** usar a los artistas ya firmados por IM Music como primeros usuarios reales, antes de abrir la plataforma al público. Permite validar flujos de pago, distribución y soporte con bajo riesgo reputacional.

**Fase 2 — Músicos independientes en Medellín/Colombia:** apalancar la red del sello (comunidad "Red de Músicos en Medellín", estudios locales, relaciones ya construidas en el plan de afiliados del libro del sello) para onboarding orgánico antes de pagar adquisición.

**Fase 3 — Expansión a Dubái/MENA — tesis de creación de categoría:** EAU no tiene hoy, hasta donde se pudo verificar en esta investigación, un competidor establecido enfocado en distribución musical latina/urbana. MENA fue la región de mayor crecimiento mundial en música grabada tanto en 2024 (+22.8%) como en 2025 (+15.2%, IFPI — ya verificado en el Plan del Sello), y hay evidencia cualitativa real de demanda de música latina en la región (J Balvin como headliner de UNTOLD Dubai 2025, Dubai Latin Fest anual). Esto plantea una tesis estratégica de **creación de categoría**, no de competir por cuota de un mercado ya disputado: ser el primer distribuidor-plataforma enfocado en el nicho latino/urbano en una región que crece más rápido que ninguna otra en el mundo.

Dubái/EAU además concentra una de las densidades más altas del mundo de patrimonio privado y gasto de lujo, lo que — **de forma cualitativa, sin una cifra dura de gasto en entretenimiento de lujo en EAU que se haya podido verificar en esta investigación** — abre la puerta a líneas de ingreso premium más allá de la suscripción pura: eventos exclusivos, patrocinios de marcas de lujo, y servicios VIP para artistas (managers/sellos que buscan presencia en la región). Esto debe tratarse como tesis a validar con datos reales de la industria del entretenimiento de lujo en EAU antes de dimensionarla financieramente, no como una proyección de ingresos.

La brecha operativa real sigue sin resolver: **Wompi solo opera en Colombia.** Para operar en EAU se necesitaría otro riel de pago (Stripe ya soporta la región, pero habría que validar retenciones fiscales, VAT 5% sobre servicios digitales, y si los artistas de la región tienen fricción para pagar con tarjeta internacional). No se propone una solución aquí — se señala como tarea pendiente de resolver antes de intentar el lanzamiento en ese mercado.

## 8. Estructura de Equipo

El desarrollo actual del producto tiene las características de un esfuerzo individual (naming genérico de paquetes como "react-example", tabla de precios con un bug evidente no corregido, ausencia de pruebas automatizadas visibles). Llevarlo a producción real y escalarlo requiere como mínimo:
- 1 desarrollador backend/full-stack para estabilizar, corregir bugs (como el de precios) y mantener
- QA — pruebas de los flujos de pago y distribución antes de manejar dinero real de terceros
- Soporte al cliente — alguien que responda a artistas con problemas de regalías o pagos (riesgo reputacional alto si se maneja mal)
- Asesoría legal especializada en fintech/derechos de autor para los términos de servicio

Esto es una necesidad de inversión en sí misma, a dimensionar en el Modelo Financiero.

## 9. Aspectos Legales

- **Términos de servicio y política de privacidad** — no existen o no han sido revisados por un abogado; son indispensables antes de manejar regalías y datos de artistas.
- **Responsabilidad fiduciaria** — la plataforma retiene y distribuye dinero de terceros (regalías, pagos de splits); esto implica obligaciones de transparencia y trazabilidad superiores a una app común.
- **Cumplimiento de pagos** — PCI-DSS delegado a Stripe/Wompi (correcto: la plataforma no debe tocar directamente datos de tarjetas), pero debe auditarse que la integración no filtre datos sensibles en logs o en la base de datos.
- **Protección de datos** — aplica la Ley 1581 de 2012 (Colombia) sobre datos personales de los artistas registrados.
- **Derechos de autor de las obras distribuidas** — la plataforma necesita un proceso claro para verificar que quien sube una canción tiene derecho a distribuirla (riesgo de distribución no autorizada de contenido con copyright de terceros).

## 10. Gestión de Riesgos

| Riesgo | Mitigación propuesta |
|---|---|
| Competencia global establecida (DistroKid, TuneCore) con escala y marca reconocida | Enfoque en diferenciación real (financiamiento, agente legal IA, Wompi) y nicho LatAm/urbano en vez de competir en precio puro |
| Dependencia de APIs de terceros (Spotify, YouTube) que pueden cambiar términos o acceso | Monitoreo activo de cambios de API, no construir funciones críticas sobre endpoints no oficiales/inestables |
| Manejo de dinero de terceros (regalías) | Auditoría financiera y de seguridad antes de producción; trazabilidad completa de cada transacción |
| Fraude/seguridad de pagos | Delegar el procesamiento de tarjetas 100% a Stripe/Wompi (ya es el diseño actual); nunca almacenar datos de tarjetas propios |
| Producto no probado en producción | Fase 1 cerrada (roster propio) antes de abrir al público, como ya se definió en el Go-to-Market |

## 11. KPIs

- MRR (ingreso recurrente mensual) y su crecimiento mes a mes
- Churn de suscripciones
- CAC (costo de adquisición de artista) y LTV
- # de artistas onboarded (acumulado y nuevos por mes)
- # de streams distribuidos a través de la plataforma
- GMV (volumen bruto transaccionado) del marketplace de beats
- Tiempo promedio de resolución de soporte

## 12. Estrategia de Salida para el Inversionista

Mismas opciones estructurales que el plan del sello (documento separado): venta de la participación a otro inversionista, adquisición por un distribuidor/sello mayor interesado en tecnología propia, o eventual ronda de crecimiento (Series A) si el producto demuestra tracción real en Fase 1-2 antes de buscar escala internacional.

## 13. Conclusión

IM Music — Elite Artist Platform parte de una ventaja poco común: no es una idea sin construir, ya existe un prototipo funcional con integraciones reales a Spotify, Stripe y Wompi, y nace con un cliente ancla real (el propio sello y sus artistas). El camino a producto lanzable requiere corregir deficiencias concretas (precios, QA, legal, seguridad) más que inventar el producto desde cero — lo que reduce el riesgo de ejecución frente a un inversionista comparado con una idea en etapa de concepto. Las proyecciones financieras detalladas, estructura de costos de desarrollo/mantenimiento, y retorno esperado se presentan en el **Modelo Financiero IM Music — Plataforma SaaS (documento separado)**.
