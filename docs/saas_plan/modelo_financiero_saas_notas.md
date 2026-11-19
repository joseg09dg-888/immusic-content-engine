# Modelo Financiero — IM MUSIC Elite Artist Platform (SaaS)
## Notas en lenguaje simple (versión final — SOLO Básico + Pro, equipo lean, sin Élite 360)

Prototipo pre-producción: backend/frontend funcionando (Node/TypeScript + Express + PostgreSQL, integración real con Spotify, Stripe y Wompi), **$0 usuarios de pago reales**.

**Este modelo quedó, por decisión final y obligatoria, SOLO con los 2 planes de autoservicio puro — Básico y Pro.** Élite 360 existe y se vende a través de esta misma plataforma, pero su ingreso ($2.999,99/mes) y el costo del equipo que lo entrega (Project Manager, management, desarrollo artístico) se contabilizan **únicamente en `docs/sello_plan/modelo_financiero_sello.xlsx`** — porque es exactamente el mismo roster, el mismo equipo y el mismo ingreso que ya está presupuestado ahí. Sumarlo aquí también habría sido contarlo dos veces.

## Los 2 planes que sí se modelan aquí

| Plan | Precio/mes | Precio/año |
|---|---|---|
| Básico — Distribución | $19,99 | $239,88 |
| Pro — Crecimiento | $149,99 | $1.799,88 |

## Equipo lean (filosofía explícita del fundador)

- **1 solo programador full-stack** en nómina, todos los años — nunca un segundo dev, nunca un rol de QA separado. Testing básico lo hace el mismo programador.
- **Soporte al cliente y ventas de primer nivel con herramientas de IA** (Claude/Gemini API), no con personas — aparece como línea de costo de herramientas, no como salario.
- Legal/administrativo recurrente, casi a cero.

**Riesgo que hay que decir de frente:** con un solo programador y cero QA dedicado, cualquier ausencia, renuncia o cuello de botella técnico detiene el desarrollo y el soporte de la plataforma por completo. Es una decisión deliberada de bajo costo, no una ausencia de riesgo.

## El resultado honesto — Año 1 da pérdida

| Año | Ingresos | EBITDA | Utilidad Neta |
|---|---|---|---|
| 1 | $24.474 | -$25.105 | **-$45.105 (pérdida)** |
| 2 | $142.164 | $69.477 | $45.160 |
| 3 | $568.656 | $436.510 | $283.731 |
| 4 | $1.658.580 | $1.404.037 | $912.624 |
| 5 | $3.791.040 | $3.321.798 | $2.159.169 |

**Tal como se pidió: si Básico+Pro solos no son rentables en el año 1, se dice así, sin forzar un número bonito.** El Año 1 da pérdida neta de -$45.105 (el costo único de la revisión legal/seguridad de $20.000 cae justo en ese año, encima de un EBITDA ya negativo de -$25.105). A partir del Año 2 el negocio se vuelve rentable y crece con fuerza.

- **NTI (ronda PRE-SEED): ~USD $74.300** — puente de arranque de 6-12 meses (programador + herramientas IA + revisión legal/seguridad + colchón de adquisición de usuarios).
- **VAN a 5 años (38% de descuento): +$707.739.** **TIR a 5 años: 132,7%.**
- Esta TIR sigue siendo alta porque el NTI de arranque es pequeño frente al crecimiento modelado de Básico/Pro a 5 años — pero ya NO depende de ningún ingreso de respaldo tipo Élite 360. Ahora depende 100% de que el autoservicio (Básico+Pro) realmente llegue a los 8.000 suscriptores modelados en el Año 5.

## La hoja de Sensibilidad — y por qué hay que leerla con cuidado

| Escenario Año 5 | Ingresos | EBITDA |
|---|---|---|
| Base (100% de adopción modelada) | $3.791.040 | $3.321.798 |
| Conservador (50% de adopción) | $1.895.520 | $1.502.099 |
| Pesimista (25% de adopción) | $947.760 | $592.250 |

Incluso al 25% de la adopción modelada, el EBITDA del Año 5 sigue siendo positivo en esta hoja — pero eso es en parte porque el modelo **mantiene el mismo equipo lean (1 programador) en los tres escenarios**, sin reducirlo si la adopción es baja. Es una simplificación razonable (el costo de 1 programador + herramientas de IA no cambia mucho entre tener 2.000 o 8.000 suscriptores), pero no es garantía — si la adopción real es baja, probablemente también haya que ajustar el ritmo de inversión en tecnología/marketing, no solo mirar el resultado de esta tabla de forma aislada.

## El riesgo central, sin Élite 360 de respaldo

**Básico ($19,99/mes) y Pro ($149,99/mes) cobran POR MES lo que DistroKid (~$19,99-89,99/año) y TuneCore (~$9,99-49,99/año) cobran POR AÑO** — 5-10 veces más caro (comparación de conocimiento general, no verificada con tarifas vigentes en esta sesión). Antes, si la adopción de autoservicio fallaba, Élite 360 sostenía el negocio. **Ahora que Élite 360 se contabiliza aparte, este modelo vive o muere exclusivamente de que el mercado acepte ese precio de autoservicio.** Esa es la conversación honesta que hay que tener antes de llevar este número a un inversionista.

## La corrección sobre "blockchain"

`verifyBlockchain` (en `publishingController.ts`) es un **placeholder/simulación** — genera un `tx_hash` falso, sin ethers.js/web3.js/Solidity en el proyecto. No se modeló ningún costo de gas/transacción real. Quedó anotado en `CAPEX_Unico` como línea de **roadmap futuro no comprometido**.

## Supuestos que TIENES que validar antes de mostrarle esto a un inversionista real

- **Que el mercado acepte el pricing de Básico/Pro** tal como está — ahora es el único supuesto que sostiene todo el modelo, sin ingreso de respaldo.
- **Comisión real de Wompi** (rango público ~2,65%-3,99%+IVA, no confirmado).
- **Precio actual de hosting** (Neon Postgres, Cloudinary, Gemini API) y **costo real de las herramientas de IA de soporte/ventas** — estimaciones de conocimiento general, no verificadas en esta sesión.
- **Salario real de un programador full-stack remoto en Colombia** (~$3.000-3.800 USD/mes usado) — no verificado con fuente actual.
- **Conversión y churn real** — no existen datos porque la plataforma no tiene usuarios de pago aún.
- **Costo real de la revisión legal/seguridad** (~$20.000 estimado) — pedir cotización real.
- **Riesgo de key-person**: un solo programador sin respaldo técnico es un punto único de falla operativo.
