# IM Music — Flujos de Decisión y Stack de Herramientas

Documento complementario al **Manual de Funciones** (`manual_funciones_im_music.xlsx`). Mientras el manual describe QUÉ hace cada rol, este documento describe CÓMO se conectan los roles entre sí en los procesos reales del día a día, con los puntos de decisión explícitos ("SI pasa A → se hace X; SI pasa B → se hace Y"), y qué herramientas sostienen ese circuito para que opere con el mínimo de personas posible.

Roles usados: **CEO/Director** (fundador, cubre legal rutinario), **Gerente Comercial**, **Project Manager Élite 360**, **Comunicadora/Estrategia de Contenido** (define parrilla/calendario editorial, dirige al Content Engine), **Filmmaker/Editor con IA** (freelance, edita material humano real con herramientas de IA — distinto del video sintético automatizado), **Diseñadora Gráfica** (freelance, diseño a la medida más allá de las plantillas automatizadas), **Productor Musical**, **Ingeniero de Sonido**, **Contador** (externo), **Desarrollador Full-Stack** (plataforma), **Asesor Legal Externo** (solo casos de alta complejidad).

---

## PARTE 1 — FLUJOS DE DECISIÓN

### 1. Proceso de firma de un nuevo artista (scouting → primer lanzamiento)

```
INICIO: Gerente Comercial identifica un artista (scouting directo o convocatoria)
│
├─ SI el artista NO encaja en el perfil (sin tracción orgánica mínima, sin coherencia
│  de marca con REBEL LUXURY) → Gerente Comercial descarta. FIN.
│
└─ SI el artista SÍ encaja →
   Gerente Comercial presenta el caso al CEO/Director (go/no-go de A&R)
   │
   ├─ SI el CEO rechaza → se comunica al artista, se documenta el motivo. FIN.
   │
   └─ SI el CEO aprueba →
      CEO/Director redacta/envía el contrato estándar (cubre la función legal rutinaria)
      │
      ├─ SI el artista acepta el contrato estándar → continúa abajo.
      │
      ├─ SI el artista negocia términos no estándar (% de regalías, exclusividad,
      │  cláusulas de salida) →
      │  ├─ SI la negociación es de bajo riesgo (ajustes menores) → CEO decide directamente.
      │  └─ SI la negociación es de alto riesgo (ej. inversión de capital grande,
      │     cláusulas de exclusividad atípicas — ver caso real Lucki vs. Empire Distribution
      │     en la matriz de riesgos) → se escala al Asesor Legal Externo antes de firmar.
      │
      └─ SI el artista rechaza el contrato → Gerente Comercial cierra el caso. FIN.

   Contrato firmado → CEO/Director decide el modelo de arranque:
   │
   ├─ SI el sello invierte capital en el primer proyecto (financia grabación/video) →
   │  pasa al Proceso 3 (Producción de una canción) con presupuesto asignado por el CEO.
   │
   └─ SI es solo distribución (el artista financia su propia producción) →
      Gerente Comercial coordina directamente con Desarrollador/plataforma para el
      onboarding de distribución (ver Proceso 2, rama Élite 360 o Pro según el caso).

   En paralelo, siempre: Project Manager Élite 360 evalúa si hay CUPO disponible
   (máx. 12-15 artistas, ver Manual de Funciones) para ofrecer el servicio 360 completo:
   │
   ├─ SI hay cupo → el artista entra a Élite 360 (Project Manager toma el relevo
   │  operativo: management, contenido, Meta Ads, campamentos).
   │
   └─ SI NO hay cupo → el artista queda en el roster "básico" del sello (producción +
      distribución vía Nexus, sin el paquete 360 completo) hasta que se libere un cupo
      o se decida escalar el equipo (ver Manual de Funciones, criterio de escalamiento).
```

### 2. Proceso de onboarding de un cliente de la plataforma (Básico / Pro / Élite 360)

```
INICIO: lead llega vía la Máquina de Captación (WhatsApp IA, DM automático, email
marketing) o por registro directo en la plataforma.
│
├─ SI el lead se registra directo en Básico o Pro (autoservicio) →
│  flujo 100% automatizado por la plataforma:
│  │
│  ├─ SI el país del usuario está en Colombia → pasarela Wompi.
│  └─ SI el país del usuario es cualquier otro → pasarela Stripe.
│  (sin intervención humana salvo error de pago, ver Proceso 5)
│
└─ SI el lead pide específicamente Élite 360 (vía WhatsApp IA o formulario) →
   la IA de primer contacto escala la conversación al Gerente Comercial
   │
   Gerente Comercial confirma el interés real (presupuesto, perfil de artista)
   │
   ├─ SI el lead no es un fit real (no tiene la tracción o el presupuesto esperado) →
   │  se le ofrece Pro como alternativa. FIN (pasa a flujo autoservicio de Pro).
   │
   └─ SI el lead sí es un fit →
      Gerente Comercial consulta cupo con Project Manager Élite 360
      │
      ├─ SI HAY cupo disponible (≤15 clientes activos) →
      │  Gerente Comercial cierra el acuerdo → pago (Wompi si es Colombia, Stripe si
      │  no) → Project Manager inicia onboarding operativo (igual que un artista
      │  firmado directamente por el sello, ver Proceso 1 rama Élite 360).
      │
      └─ SI NO HAY cupo disponible →
         ├─ Se ofrece lista de espera con fecha estimada de apertura de cupo
         │  (ligada a la curva de crecimiento del roster del Modelo Financiero), O
         └─ Se ofrece Pro como alternativa inmediata con la opción de subir a Élite 360
            cuando se libere un cupo.
```

### 3. Proceso de producción de una canción/lanzamiento (brief → publicación)

```
INICIO: Brief creativo (definido por CEO/Director + artista)
│
Productor Musical desarrolla preproducción (composición/arreglos)
│
├─ SI el CEO/Director NO aprueba la dirección creativa → se ajusta el brief,
│  vuelve a preproducción. (loop hasta aprobación)
│
└─ SI el CEO/Director aprueba →
   Grabación (estudio propio o alianza externa)
   │
   Ingeniero de Sonido ejecuta mezcla y masterización
   │
   ├─ SI la calidad técnica no cumple el estándar REBEL LUXURY (ver Sección 9 del
   │  Plan de Negocios — "cada pieza debe ejecutarse con el mismo nivel de impacto") →
   │  vuelve a mezcla/masterización. (loop hasta aprobación)
   │
   └─ SI cumple el estándar →
      CEO/Director da aprobación final de lanzamiento
      │
      Comunicadora/Estrategia de Contenido define qué piezas se necesitan y arma la
      parrilla de lanzamiento, decidiendo pieza por pieza el canal de producción:
      │
      ├─ SI la pieza es contenido estándar de calendario (carrusel, caption, story) →
      │  se genera vía Content Engine (automatizado, costo marginal casi nulo).
      │
      └─ SI la pieza requiere material humano real editado a la medida (video del
         artista grabado en vivo, sesión de estudio, detrás de cámaras) →
         ├─ SI es edición de video → Filmmaker/Editor con IA edita el material real
         │  con herramientas de IA (no es el video sintético del Content Engine).
         └─ SI es diseño gráfico a la medida (portada de single, merch, pieza de
            campaña específica fuera de plantilla) → Diseñadora Gráfica lo produce.

      Comunicadora aprueba el set completo de piezas antes de que entren al
      calendario de publicación (coordinado con Social Media Manager, que cura/
      publica, no produce).
      │
      Desarrollador/plataforma gestiona la entrega a Nexus (distribución, 8% comisión)
      │
      ├─ SI Nexus aprueba y publica a tiempo → se activa el calendario de contenido
      │  del Content Engine para el día de lanzamiento (coordinado con Social Media
      │  Manager, que solo cura/aprueba, no produce desde cero).
      │
      └─ SI hay un rechazo o retraso de Nexus (metadata incorrecta, derechos no
         registrados ante SAYCO/ACINPRO/EMRA) → Desarrollador corrige y reenvía;
         si el problema es de derechos de autor, se escala al CEO/Director (función
         legal) antes de reenviar.
```

### 4. Proceso de manejo de una crisis de marca/artista o streamer aliado

Basado en los casos reales ya documentados en `matriz_riesgos_im_music.xlsx` (d4vd soltado y banneado de Twitch en 24h; Dr Disrespect perdiendo 4 patrocinios en días; FN Meka soltado en <2 semanas por contenido dañino).

```
INICIO: se detecta una situación de riesgo reputacional (noticia, denuncia, contenido
controversial) sobre un artista del roster O sobre el streamer aliado.
│
CEO/Director es notificado de inmediato (siempre el primer punto de contacto —
es quien comunica hacia afuera, ver Manual de Funciones)
│
├─ SI la gravedad es BAJA (opinión controversial menor, sin acusación legal/ética
│  grave) →
│  CEO/Director decide: monitorear 24-48h antes de actuar, sin suspender la relación.
│
└─ SI la gravedad es ALTA (acusación legal, ética grave, o ya hay reacción pública/
   de plataformas — ej. ban de la plataforma de streaming del streamer, como en los
   casos reales de d4vd/Dr Disrespect) →
   │
   ├─ SI los hechos están confirmados o la plataforma (Twitch/Kick/YouTube) ya actuó
   │  → CEO/Director suspende la relación/exposición de marca de inmediato (no se
   │  espera investigación propia cuando la plataforma externa ya actuó — el patrón
   │  real es que las marcas que esperan pierden más, ver G FUEL: perdió 75+
   │  streamers patrocinados por reaccionar tarde en un caso similar).
   │
   └─ SI los hechos NO están confirmados (denuncia sin resolver, sin acción de
      plataforma externa) →
      CEO/Director + Asesor Legal Externo evalúan el caso antes de actuar
      │
      ├─ SI el riesgo de esperar es mayor que el de actuar → se suspende
      │  preventivamente la exposición de marca hasta aclarar.
      └─ SI se decide esperar → se define una fecha límite de revisión (no queda
         abierto indefinidamente).

En cualquier rama que termine en suspensión: Comunicadora/Estrategia de Contenido
coordina la respuesta de contenido (retiro de menciones, pausa de piezas programadas,
mensaje público si el CEO lo decide), apoyada por Filmmaker/Editor o Diseñadora si
se requiere material nuevo urgente; Gerente Comercial coordina el retiro de la
exposición comercial, y Contador evalúa el impacto financiero de la pérdida del
acuerdo.
```

### 5. Proceso de resolución de un problema de pago/regalías en la plataforma

```
INICIO: se reporta un problema de pago o de regalías no reflejadas correctamente
│
Desarrollador Full-Stack diagnostica el origen
│
├─ SI el fallo es de Stripe o Wompi (caída del proveedor, rechazo de transacción,
│  error de su API) →
│  Desarrollador escala directamente al soporte del proveedor de pagos
│  │
│  ├─ SI el proveedor resuelve en el SLA esperado → se notifica al usuario afectado
│  │  (vía IA de soporte) y se cierra el caso.
│  └─ SI el proveedor NO resuelve a tiempo → CEO/Director es notificado si el
│     usuario afectado es un cliente Élite 360 (relación de alto valor) para
│     gestión directa.
│
└─ SI el fallo es un bug de la plataforma (error de cálculo de regalías, de splits,
   o de sincronización con Nexus) →
   │
   ├─ SI el bug afecta fondos de terceros YA DESEMBOLSADOS incorrectamente (dinero
   │  de regalías mal distribuido) →
   │  esto es responsabilidad fiduciaria (ver matriz de riesgos, R-LEG-001) →
   │  se notifica de inmediato al CEO/Director y al Asesor Legal Externo ANTES de
   │  comunicar al usuario, para definir el plan de corrección/reembolso.
   │
   └─ SI el bug NO ha desembolsado fondos todavía (error detectado antes del pago) →
      Desarrollador corrige el bug, Contador verifica que los montos corregidos
      sean correctos antes de que se libere el pago. No requiere escalar a legal.
```

---

## PARTE 2 — STACK DE HERRAMIENTAS

Criterio: cada herramienta debe justificar su costo/complejidad contra el tamaño real del equipo (6-8 personas, varias freelance/part-time). Nada de tooling empresarial que resuelve un problema que este equipo no tiene todavía.

| Función | Herramienta elegida | Por qué esta y no otra |
|---|---|---|
| **Gestión de proyectos/tareas** | **Notion** (no ClickUp, no Trello) | Un solo espacio que sirve a la vez como base de datos de tareas, documentación (manuales de funciones, contratos, briefs creativos) y wiki del equipo. ClickUp y Trello son mejores para equipos más grandes con flujos de trabajo complejos entre departamentos; para 6-8 personas, tener documentación y tareas en la misma herramienta evita que el CEO (que ya concentra demasiados roles) tenga que mantener dos sistemas separados. |
| **Comunicación interna** | **WhatsApp Business** (no Slack) | El equipo ya usa WhatsApp como canal operativo con artistas y leads (es la base de la Máquina de Captación); usar la misma plataforma internamente evita fragmentar la comunicación en una herramienta más. Slack se justifica cuando hay >10-15 personas o integraciones complejas de desarrollo — no es el caso aún. Revaluar si el equipo crece más allá de ~10 personas fijas. |
| **Automatización entre herramientas** | **Make** (no Zapier) | Según el ejemplo de referencia del usuario, el perfil de "Desarrollador" ya trabaja con Zapier/Make/HighLevel. Make se prefiere sobre Zapier para este caso porque su lógica de escenarios con routers/filtros maneja mejor flujos condicionados como el de captación→venta descrito abajo, con un costo por operación más bajo a este volumen. Flujo clave a automatizar primero: lead capturado por WhatsApp IA → si califica → tarea automática creada en Notion para el Gerente Comercial → si el Gerente Comercial marca "cerrado" → tarea automática creada para el Project Manager Élite 360 (onboarding) o notificación al Desarrollador (alta en la plataforma Básico/Pro). |
| **Control de tiempo/cumplimiento de plazos** | **Vistas de Notion con fecha límite + fórmulas de atraso, revisadas en una reunión semanal fija del CEO** | No se justifica una herramienta de time-tracking dedicada (ej. Toggl) para freelancers que cobran por proyecto, no por hora. Lo que sí se necesita es visibilidad de qué está atrasado: una vista de Notion filtrada por "fecha límite < hoy y no completado" cumple esa función sin agregar otra suscripción. SLA sugeridos por tipo de tarea: producción musical (preproducción→demo: 5 días hábiles; mezcla/masterización: 3 días hábiles), onboarding Élite 360 (primer contacto a kickoff: 48h), soporte de pagos (primera respuesta de la IA: inmediata; escalado a Desarrollador: 4h hábiles). |
| **Documentación compartida** | **Google Drive** (ya en uso) | El proyecto ya usa Google Drive como base documental (carpeta "IM Music - Content Engine" y "PLAN SELLO IM MUSIC"); se mantiene como el repositorio de archivos pesados (contratos firmados, piezas de diseño, financieros en Excel), con Notion como la capa de organización/tareas que enlaza a esos archivos en Drive en vez de duplicarlos. |
| **Edición de video con IA (Filmmaker)** | **CapCut Pro** | Ya es parte del stack de edición ligera del proyecto (mencionado en el organigrama funcional); maneja edición asistida por IA de material humano real (recorte, subtítulos automáticos, color) a un costo mucho menor que Adobe Premiere para el volumen de este equipo. Adobe se reevalúa solo si el Filmmaker necesita un control de color/VFX que CapCut no ofrece. |
| **Diseño gráfico a la medida (Diseñadora)** | **Canva Pro + plantillas de marca REBEL LUXURY** (no Adobe Illustrator/Photoshop como herramienta principal) | Para piezas que salen del alcance del Content Engine automatizado, Canva Pro con las plantillas de marca ya definidas (violeta #5E17EB, Sceageus/Anton) permite producir rápido sin la curva de aprendizaje ni el costo de la suite completa de Adobe. Se reevalúa si se necesita una pieza que exige manipulación avanzada (retoque fotográfico complejo, ilustración desde cero) — ahí sí se factura por proyecto a un freelance con Photoshop/Illustrator en vez de agregar la licencia al stack fijo. |

**Nota de honestidad:** ninguna de estas herramientas está implementada todavía — esto es una recomendación de diseño del sistema operativo, no un hecho ya en marcha. El Desarrollador Full-Stack es quien debería configurar la automatización en Make una vez el equipo esté contratado, no antes.
