"""Genera el Manual de Funciones y Procesos de IM Music: un sheet por rol,
con el mismo formato que el ejemplo de referencia del usuario (Columnas A-G:
Tarea/Proceso, Subpasos/Detalles, Responsable, Herramientas, Metricas de
Exito, Posibles Automatizaciones, Frecuencia) mas una fila de interconexion
con otros roles al final de cada hoja."""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "docs" / "sello_plan" / "manual_funciones_im_music.xlsx"

VIOLETA = "5E17EB"
CREMA = "F2EDE5"
GRIS = "4A3D5E"

HEADERS = [
    "Tarea/Proceso", "Subpasos/Detalles", "Responsable", "Herramientas",
    "Metricas de Exito", "Posibles Automatizaciones", "Frecuencia",
]

ROLES = {}

ROLES["1. CEO - Director del Sello"] = {
    "resumen": "El fundador: direccion estrategica, A&R, firma de artistas, relacion con inversionistas, y cubre la funcion legal rutinaria.",
    "rows": [
        ("I. Scouting y Captacion de Talento", "1. Monitorear redes sociales, plataformas de streaming y referidos para identificar artistas potenciales (cualquier genero/idioma/pais).", "CEO", "Spotify for Artists, Instagram/TikTok, Google Trends, hoja de pipeline", "N artistas evaluados/mes", "Alerta automatica de menciones/crecimiento de artistas candidatos", "Semanal"),
        ("I. Scouting y Captacion de Talento", "2. Evaluar encaje del artista con la metodologia de desarrollo de marca de IM Music.", "CEO", "Criterios de evaluacion propios (checklist)", "Criterios aplicados consistentemente", "Checklist digital con scoring", "Por candidato"),
        ("I. Scouting y Captacion de Talento", "3. Primer acercamiento y reunion de diagnostico con el artista.", "CEO", "WhatsApp Business, Calendly", "Reunion agendada en <5 dias habiles", "Agendamiento automatico vinculado a WhatsApp", "Por candidato"),
        ("II. Negociacion y Firma", "1. Definir terminos del contrato (Elite 360 a USD 2.999,99/mes, inversion en catalogo si aplica).", "CEO", "Plantilla de contrato propia, hoja de pricing", "Terminos claros y acordados por escrito", "Generador de propuesta desde plantilla", "Por artista"),
        ("II. Negociacion y Firma", "2. Redactar/adaptar el contrato estandar del sello.", "CEO", "Plantilla de contrato, DocuSign", "Contrato firmado sin retrabajos legales", "Autocompletado de plantilla con datos del artista", "Por artista"),
        ("II. Negociacion y Firma", "3. Firmar contrato y dar de alta al artista en el roster (max. 12-15).", "CEO", "DocuSign, base de datos del roster", "Alta registrada el mismo dia de firma", "Alta automatica en sistema al firmar", "Por artista"),
        ("II. Negociacion y Firma", "4. Escalar al Asesor Legal Externo SOLO en casos de alta complejidad (litigios, estructuracion en Dubai, clausulas atipicas).", "CEO + Asesor Legal Externo", "Correo/WhatsApp directo con el asesor", "Escalado solo cuando aplica, sin sobrecostos innecesarios", "Ninguna - decision humana deliberada", "Segun necesidad"),
        ("III. Direccion Estrategica y A&R", "1. Aprobar el catalogo y calendario de lanzamientos del roster.", "CEO", "Calendario compartido (Notion/Google Calendar)", "Calendario de lanzamientos cumplido en 90%+", "Recordatorios automaticos de hitos", "Mensual"),
        ("III. Direccion Estrategica y A&R", "2. Decidir inversion de capital propio en proyectos especiales (canciones/EPs/albumes) y negociar % de regalia caso por caso.", "CEO", "Modelo financiero del sello (Excel)", "ROI estimado documentado antes de invertir", "Plantilla de evaluacion de inversion por proyecto", "Por proyecto"),
        ("III. Direccion Estrategica y A&R", "3. Supervisar que la ejecucion de marca cumpla el estandar REBEL LUXURY en todas las piezas.", "CEO", "Brand guidelines (brand.py), revision visual", "0 piezas publicadas fuera de estandar de marca", "Checklist de marca antes de publicar", "Continuo"),
        ("IV. Relacion con Inversionistas", "1. Reportar KPIs financieros y de catalogo trimestralmente.", "CEO + Contador", "Dashboard financiero, modelo financiero del sello", "Reporte entregado a tiempo cada trimestre", "Generacion automatica de reporte desde el modelo financiero", "Trimestral"),
        ("IV. Relacion con Inversionistas", "2. Gestionar la ronda de inversion activa (pre-seed) y preparar material para la siguiente ronda.", "CEO", "Pitch deck, modelo financiero", "Avance medible hacia hito de la siguiente ronda", "Ninguna - decision estrategica humana", "Segun ronda"),
        ("V. Funcion Legal Rutinaria", "1. Gestionar registro de marca ante la SIC (Colombia) y equivalente en Dubai si aplica.", "CEO", "Portal SIC, asesoria puntual si se requiere", "Marca registrada sin objeciones", "Recordatorio automatico de renovaciones", "Anual/Segun tramite"),
        ("V. Funcion Legal Rutinaria", "2. Revisar y aprobar contratos estandar con artistas y proveedores (no litigiosos).", "CEO", "Plantillas de contrato propias", "0 contratos firmados sin revision", "Checklist de clausulas minimas obligatorias", "Por contrato"),
        ("VI. Gestion Administrativa General", "1. Supervisar al Contador en el cierre mensual.", "CEO + Contador", "Dashboard financiero", "Cierre mensual validado en <5 dias habiles del mes siguiente", "Alertas automaticas de cierre pendiente", "Mensual"),
        ("VI. Gestion Administrativa General", "2. Aprobar presupuesto de CAPEX/OPEX (incluye setup de streamer si aplica).", "CEO", "Modelo financiero del sello", "Gasto real dentro del +-10% del presupuesto", "Alertas de desviacion presupuestal", "Mensual"),
    ],
    "interconexion": "La firma del contrato (Fase II.3) da de alta al artista y DISPARA dos procesos en paralelo: el del Gerente Comercial (activacion de facturacion mensual) y el del Project Manager Elite 360 (Fase I de onboarding). La aprobacion de inversion en catalogo (Fase III.2) dispara el proceso del Productor Musical.",
}

ROLES["2. Gerente Comercial"] = {
    "resumen": "Capta artistas y clientes de produccion, cierra leads que entrega la Maquina de Captacion con IA, y gestiona la relacion comercial continua.",
    "rows": [
        ("I. Gestion del Pipeline de Leads", "1. Recibir leads calificados de la Maquina de Captacion (bot de WhatsApp IA, DM automatico en redes, email marketing).", "Gerente Comercial", "WhatsApp Business API, CRM (Notion/HubSpot free)", "100% de leads inbound registrados en el CRM", "Ya automatizado: calificacion inicial por IA antes de llegar aqui", "Diario"),
        ("I. Gestion del Pipeline de Leads", "2. Clasificar leads por tipo: artista para roster Elite 360, cliente de produccion externa, o cliente de plataforma Basico/Pro.", "Gerente Comercial", "CRM, hoja de pipeline", "Clasificacion correcta en <24h de recibido", "Etiquetado automatico por palabras clave del lead", "Diario"),
        ("I. Gestion del Pipeline de Leads", "3. Priorizar seguimiento segun score de calificacion del lead.", "Gerente Comercial", "CRM con scoring", "Leads de alto score contactados en <24h", "Scoring automatico basado en interaccion previa", "Diario"),
        ("II. Negociacion Comercial", "1. Presentar propuesta de valor y pricing segun el segmento (Elite 360, produccion por proyecto, Basico/Pro).", "Gerente Comercial", "Brochure de la plataforma, plantillas de propuesta", "Propuesta enviada en <48h de la reunion", "Generador de propuesta desde plantilla segun segmento", "Por lead"),
        ("II. Negociacion Comercial", "2. Negociar terminos (produccion musical por proyecto, desarrollo de marca, licencias/sync).", "Gerente Comercial", "Tabla de pricing de referencia", "Cierre dentro del rango de precio aprobado por CEO", "Ninguna - negociacion humana deliberada", "Por lead"),
        ("II. Negociacion Comercial", "3. Enviar contrato para firma (via CEO si es artista del roster Elite 360).", "Gerente Comercial + CEO", "DocuSign", "Contrato enviado el mismo dia del acuerdo verbal", "Generacion automatica del contrato desde CRM", "Por cierre"),
        ("III. Cierre y Entrega", "1. Confirmar pago/activacion de suscripcion o anticipo de proyecto.", "Gerente Comercial", "Stripe/Wompi dashboard", "Pago confirmado antes de iniciar ejecucion", "Webhook automatico de confirmacion de pago", "Por cierre"),
        ("III. Cierre y Entrega", "2. Transferir el cliente/artista cerrado al responsable de ejecucion (Project Manager Elite 360 o Productor Musical).", "Gerente Comercial", "CRM, Notion compartido", "Handoff completado en <24h del cierre", "Notificacion automatica al responsable al marcar 'cerrado-ganado'", "Por cierre"),
        ("IV. Gestion de Clientes Existentes", "1. Dar seguimiento a renovaciones y upsell (Basico a Pro, servicio puntual a roster Elite 360).", "Gerente Comercial", "CRM con fechas de renovacion", "Tasa de renovacion >80%", "Recordatorio automatico 30 dias antes del vencimiento", "Mensual"),
        ("IV. Gestion de Clientes Existentes", "2. Resolver objeciones o quejas comerciales de primer nivel.", "Gerente Comercial", "WhatsApp Business, CRM", "Primera respuesta en <4h habiles", "Triage inicial por IA de soporte antes de escalar aqui", "Continuo"),
        ("V. Reporting Comercial", "1. Reportar pipeline, tasa de cierre y facturacion al CEO semanalmente.", "Gerente Comercial", "CRM, dashboard financiero", "Reporte entregado cada lunes", "Reporte automatico generado desde el CRM", "Semanal"),
    ],
    "interconexion": "Un lead cerrado como artista del roster (Fase III.2) dispara el inicio del proceso del Project Manager Elite 360 (Fase I de onboarding). Un lead cerrado como produccion externa dispara el proceso del Productor Musical (Fase I). Un lead cerrado como suscripcion Basico/Pro dispara el alta en la plataforma a cargo del Desarrollador.",
}

ROLES["3. Project Manager - Elite 360"] = {
    "resumen": "Convierte el contrato cerrado por el Gerente Comercial en ejecucion real para cada uno de los 12-15 artistas del roster: management, contenido, branding, ads y campamentos.",
    "rows": [
        ("I. Onboarding del Artista", "1. Reunion de diagnostico y definicion de objetivos de marca con el artista recien firmado.", "Project Manager", "Notion/Trello, cuestionario de diagnostico", "Onboarding completado en <7 dias de la firma", "Cuestionario de diagnostico autogestionado por el artista", "Por artista nuevo"),
        ("I. Onboarding del Artista", "2. Definir calendario de lanzamientos y campanas para los primeros 90 dias.", "Project Manager", "Calendario compartido", "Calendario aprobado por el artista y el CEO en <14 dias", "Plantilla de calendario de 90 dias", "Por artista nuevo"),
        ("II. Coordinacion de Management Musical", "1. Coordinar con Productor Musical/Ingeniero de Sonido el calendario de grabacion.", "Project Manager", "Calendario compartido, estudio propio", "0 sesiones reprogramadas por falta de coordinacion", "Reserva automatica de estudio vinculada al calendario", "Continuo"),
        ("II. Coordinacion de Management Musical", "2. Dar seguimiento al estado de cada cancion/EP en produccion.", "Project Manager", "Tablero Kanban (Trello/Notion)", "Estado actualizado semanalmente para cada track", "Tablero con estados automaticos por etapa", "Semanal"),
        ("III. Produccion de Contenido y Video", "1. Briefing y coordinacion de produccion de videos musicales (freelance/equipo externo).", "Project Manager", "Brief creativo, Google Drive compartido", "Brief entregado antes del rodaje en 100% de los casos", "Plantilla de brief creativo reutilizable", "Por lanzamiento"),
        ("III. Produccion de Contenido y Video", "2. Supervisar y curar (no crear desde cero) las piezas generadas por el Content Engine para el artista.", "Project Manager", "Content Engine (src/content_engine/)", "Piezas aprobadas en <48h de generadas", "Generacion ya automatizada; solo queda la curaduria humana", "Semanal"),
        ("IV. Gestion de Branding", "1. Aplicar la metodologia de desarrollo de marca del fundador al artista especifico.", "Project Manager", "Guia de metodologia del CEO", "Identidad de marca del artista definida en <30 dias del onboarding", "Ninguna - trabajo creativo deliberadamente humano", "Por artista nuevo"),
        ("IV. Gestion de Branding", "2. Aprobar identidad visual/narrativa del artista, alineada a REBEL LUXURY.", "Project Manager + CEO", "Brand guidelines", "0 piezas publicadas sin aprobacion", "Checklist de alineacion de marca", "Por pieza"),
        ("V. Meta Ads y Campanas", "1. Definir presupuesto y segmentacion de campanas pagadas para el artista.", "Project Manager", "Meta Ads Manager", "Presupuesto aprobado antes de lanzar campana", "Plantillas de segmentacion por genero/mercado", "Por campana"),
        ("V. Meta Ads y Campanas", "2. Monitorear desempeno y optimizar campanas activas.", "Project Manager", "Meta Ads Manager, dashboard de la plataforma", "ROAS objetivo alcanzado o campana ajustada en <7 dias", "Alertas automaticas de bajo desempeno", "Semanal"),
        ("VI. Campamentos Musicales y Red de Industria", "1. Organizar campamentos musicales (logistica, invitados, agenda creativa).", "Project Manager", "Hoja de logistica, proveedores de alojamiento/transporte", "Campamento ejecutado segun presupuesto aprobado", "Checklist de logistica reutilizable", "Segun calendario"),
        ("VI. Campamentos Musicales y Red de Industria", "2. Facilitar conexiones del artista con la red de industria del sello.", "Project Manager", "Red de contactos del sello", "Al menos 1 conexion relevante facilitada por trimestre/artista", "Ninguna - relacionamiento humano deliberado", "Trimestral"),
        ("VII. Reporting", "1. Reporte mensual de resultados (streams, seguidores, campanas) al artista.", "Project Manager", "Dashboard de la plataforma IM Music", "Reporte entregado el primer dia habil del mes", "Generacion automatica de reporte desde la plataforma", "Mensual"),
        ("VII. Reporting", "2. Reporte de estado del roster completo al CEO.", "Project Manager", "Dashboard consolidado", "Reporte entregado antes del reporte del CEO a inversionistas", "Consolidacion automatica desde reportes individuales", "Mensual"),
    ],
    "interconexion": "La aprobacion de una cancion lista (Fase II.2) dispara el proceso de publicacion del Desarrollador (upload a Nexus/la plataforma) y el proceso de regalias del Contador. Un bajo desempeno de campana (Fase V.2) puede escalar al CEO si requiere reasignar presupuesto del roster.",
}

ROLES["4. Productor Musical (freelance)"] = {
    "resumen": "Direccion creativa y produccion de grabaciones para el roster propio y para producciones externas (2-4 proyectos/mes).",
    "rows": [
        ("I. Preproduccion", "1. Reunion creativa con el artista/Project Manager para definir vision sonora.", "Productor Musical", "Notion/Google Meet", "Vision sonora documentada antes de grabar", "Plantilla de brief sonoro", "Por proyecto"),
        ("I. Preproduccion", "2. Seleccion o composicion de temas, arreglos iniciales.", "Productor Musical", "DAW (Logic Pro/Ableton Live), MIDI controllers", "Demo inicial aprobado por el artista", "Ninguna - trabajo creativo deliberadamente humano", "Por proyecto"),
        ("II. Grabacion", "1. Coordinar sesion de grabacion (estudio propio o alianza externa).", "Productor Musical + Project Manager", "Calendario de estudio", "Sesion confirmada con 72h de anticipacion", "Reserva automatica vinculada al calendario del PM", "Por sesion"),
        ("II. Grabacion", "2. Dirigir la sesion, asegurar calidad de performance.", "Productor Musical", "Microfonos, interfaz de audio, DAW", "Toma final aprobada sin necesidad de re-grabacion", "Ninguna - direccion artistica humana", "Por sesion"),
        ("III. Produccion Creativa", "1. Definir estructura final, instrumentacion y produccion del track.", "Productor Musical", "DAW, librerias de sonido", "Produccion entregada segun el brief acordado", "Ninguna - decision creativa humana", "Por proyecto"),
        ("III. Produccion Creativa", "2. Entregar stems/multipistas al Ingeniero de Sonido.", "Productor Musical", "Google Drive/almacenamiento en la nube", "Entrega sin archivos corruptos o faltantes", "Checklist automatico de archivos requeridos antes de subir", "Por proyecto"),
        ("IV. Validacion y Entrega", "1. Revisar la mezcla/master entregado por el Ingeniero de Sonido, aprobar o solicitar ajustes.", "Productor Musical", "DAW, monitores de estudio", "Maximo 2 rondas de ajuste por track", "Ninguna - validacion de oido humano insustituible", "Por proyecto"),
        ("IV. Validacion y Entrega", "2. Entregar producto final aprobado al Project Manager/CEO.", "Productor Musical", "Google Drive compartido", "Entrega dentro del plazo acordado en el calendario de 90 dias", "Notificacion automatica al PM al subir el archivo final", "Por proyecto"),
        ("V. Produccion para Clientes Externos", "1. Coordinar y ejecutar producciones por proyecto para clientes externos al roster (2-4/mes).", "Productor Musical", "DAW, calendario de estudio", "Entrega a tiempo en el 90%+ de los proyectos externos", "Plantilla de brief y cotizacion estandar por tipo de proyecto", "Mensual"),
    ],
    "interconexion": "La entrega aprobada en la Fase IV dispara el proceso del Ingeniero de Sonido (si la mezcla/master aun no esta lista) y, una vez masterizado, el proceso de publicacion del Desarrollador y el proceso de regalias del Contador.",
}

ROLES["5. Ingeniero de Sonido (freelance)"] = {
    "resumen": "Grabacion, mezcla y masterizacion segun los estandares de loudness de cada plataforma de streaming.",
    "rows": [
        ("I. Recepcion de Material", "1. Recibir stems/multipistas del Productor Musical.", "Ingeniero de Sonido", "Google Drive compartido", "Material recibido completo, sin reenvios", "Checklist automatico de archivos requeridos", "Por proyecto"),
        ("II. Mezcla", "1. Balance de niveles, ecualizacion, efectos, automatizacion.", "Ingeniero de Sonido", "DAW, plugins de mezcla", "Mezcla preliminar entregada en el plazo acordado", "Ninguna - criterio de oido humano insustituible", "Por proyecto"),
        ("II. Mezcla", "2. Entregar mezcla preliminar para aprobacion del Productor Musical.", "Ingeniero de Sonido", "Google Drive, WeTransfer", "Entrega con notas tecnicas incluidas", "Notificacion automatica al Productor al subir el archivo", "Por proyecto"),
        ("III. Masterizacion", "1. Masterizar segun estandar de cada plataforma (Spotify -14 LUFS, YouTube -13 LUFS, Apple Music -16 LUFS).", "Ingeniero de Sonido", "DAW, plugins de masterizacion, pyloudnorm", "100% de los masters dentro del rango de LUFS objetivo", "Verificacion automatizada de loudness con script (ya en el stack del proyecto)", "Por proyecto"),
        ("III. Masterizacion", "2. Generar exports finales (WAV 24bit/44.1kHz, MP3 320kbps, FLAC segun necesidad).", "Ingeniero de Sonido", "DAW, scripts de exportacion por lotes", "Exports entregados en todos los formatos requeridos", "Script de exportacion automatica en los formatos estandar", "Por proyecto"),
        ("IV. Control de Calidad", "1. Verificar ausencia de errores tecnicos (clipping, ruido, problemas de fase).", "Ingeniero de Sonido", "Analizador de espectro, checklist de QA", "0 errores tecnicos detectados post-publicacion", "Checklist de QA automatizado antes de marcar como listo", "Por proyecto"),
        ("IV. Control de Calidad", "2. Entrega final aprobada al Productor Musical/Project Manager.", "Ingeniero de Sonido", "Google Drive compartido", "Entrega dentro del plazo del calendario de 90 dias", "Notificacion automatica de entrega final", "Por proyecto"),
    ],
    "interconexion": "La masterizacion aprobada (Fase IV.2) dispara el proceso de publicacion del Desarrollador (upload a la plataforma/Nexus) y el inicio del tracking de regalias del Contador.",
}

ROLES["6. Contador (externo)"] = {
    "resumen": "Estados financieros, impuestos, nomina y pago a terceros para el sello y la plataforma.",
    "rows": [
        ("I. Registro y Conciliacion", "1. Registrar ingresos (Elite 360, produccion, regalias, plataforma, libro, streamer) y egresos mensuales.", "Contador", "Software contable (Siigo/Alegra), Excel", "Registro completo antes del dia 5 del mes siguiente", "Importacion automatica de transacciones desde Stripe/Wompi", "Mensual"),
        ("I. Registro y Conciliacion", "2. Conciliar cuentas bancarias y pasarelas de pago (Stripe, Wompi).", "Contador", "Dashboard de Stripe/Wompi, banco", "0 diferencias sin explicar al cierre", "Conciliacion automatica via API cuando sea posible", "Mensual"),
        ("II. Estados Financieros", "1. Elaborar estado de resultados y flujo de caja mensual.", "Contador", "Software contable, modelo financiero del sello", "Entregado al CEO antes del dia 10 del mes", "Plantilla automatizada desde el software contable", "Mensual"),
        ("II. Estados Financieros", "2. Reportar al CEO desviaciones vs. presupuesto.", "Contador", "Modelo financiero del sello (Excel)", "Desviaciones >10% reportadas de inmediato", "Alerta automatica de desviacion presupuestal", "Mensual"),
        ("III. Impuestos", "1. Calcular y presentar obligaciones tributarias (renta, IVA/VAT segun sede).", "Contador", "Portal DIAN (Colombia) / portal tributario EAU", "0 presentaciones tardias", "Recordatorio automatico de vencimientos tributarios", "Segun calendario tributario"),
        ("III. Impuestos", "2. Gestionar el regimen tributario aplicable (RST en Colombia, 0%/9% en Dubai segun corresponda).", "Contador", "Simulador DIAN, asesoria puntual si aplica", "Regimen optimo confirmado anualmente", "Ninguna - decision que requiere criterio profesional", "Anual"),
        ("IV. Nomina y Pagos a Terceros", "1. Procesar pagos a freelancers (Productor, Ingeniero de Sonido) y al Project Manager.", "Contador", "Plataforma de pagos, software contable", "Pagos realizados en la fecha acordada en 100% de los casos", "Pagos recurrentes programados automaticamente", "Mensual/Por proyecto"),
        ("IV. Nomina y Pagos a Terceros", "2. Procesar distribucion de regalias a artistas del roster (via Nexus, 8% comision).", "Contador", "Reporte de regalias de Nexus/la plataforma", "Distribucion correcta y a tiempo cada ciclo de pago", "Calculo automatico de distribucion desde el reporte de regalias", "Segun ciclo de Nexus"),
        ("V. Auditoria y Control", "1. Revision periodica de controles internos.", "Contador", "Checklist de controles", "Revision realizada cada trimestre sin hallazgos criticos", "Ninguna - revision de criterio humano", "Trimestral"),
        ("V. Auditoria y Control", "2. Preparar informacion financiera para revision de inversionistas.", "Contador", "Modelo financiero del sello", "Informacion lista antes del reporte trimestral del CEO", "Extraccion automatica de datos desde el software contable", "Trimestral"),
    ],
    "interconexion": "El cierre mensual de ingresos y egresos (Fase I-II) alimenta directamente el reporte que el CEO presenta a inversionistas. El reporte de regalias de Nexus (Fase IV.2) depende de la publicacion previa hecha por el Desarrollador.",
}

ROLES["7. Desarrollador Full-Stack - Plataforma SaaS"] = {
    "resumen": "Unica persona de desarrollo: mantiene y evoluciona la plataforma IM Music Elite Artist Platform (Node/TS/Express, PostgreSQL via Neon, React/Vite, Spotify/Stripe/Wompi).",
    "rows": [
        ("I. Desarrollo y Mantenimiento", "1. Desarrollar nuevas funcionalidades del roadmap, priorizadas con el CEO.", "Desarrollador", "VS Code, Node.js/TypeScript, React/Vite", "Funcionalidad entregada segun el sprint acordado", "Ninguna - desarrollo deliberadamente humano", "Continuo"),
        ("I. Desarrollo y Mantenimiento", "2. Corregir bugs reportados (ej. el bug de pricing ya identificado en wompiController.ts).", "Desarrollador", "GitHub Issues, debugger", "Bugs criticos corregidos en <48h", "Alertas automaticas de errores vinculadas a tickets", "Continuo"),
        ("II. Control de Versiones y Despliegue", "1. Gestionar repositorio (Git/GitHub), ramas y pull requests.", "Desarrollador", "Git, GitHub", "100% de los cambios con historial de commits trazable", "Ninguna - practica estandar ya es el flujo base", "Continuo"),
        ("II. Control de Versiones y Despliegue", "2. Desplegar a entornos de staging antes de produccion.", "Desarrollador", "GitHub Actions (CI/CD), entorno de staging", "0 despliegues directos a produccion sin pasar por staging", "Pipeline de CI/CD automatizado", "Por release"),
        ("II. Control de Versiones y Despliegue", "3. Desplegar a produccion con plan de rollback.", "Desarrollador", "GitHub Actions, Neon (PostgreSQL)", "Rollback disponible y probado para cada release", "Rollback automatizado en el pipeline de CI/CD", "Por release"),
        ("III. Calidad y Seguridad", "1. Ejecutar pruebas (unitarias/integracion) antes de cada release.", "Desarrollador", "Jest/Playwright, GitHub Actions", "Cobertura de pruebas creciente, 0 releases sin pruebas minimas", "Pruebas automatizadas en el pipeline de CI/CD", "Por release"),
        ("III. Calidad y Seguridad", "2. Monitorear errores en produccion.", "Desarrollador", "Sentry (o equivalente)", "Tiempo de deteccion de error critico <15 minutos", "Alertas automaticas Sentry -> WhatsApp/email", "Continuo"),
        ("III. Calidad y Seguridad", "3. Revisar seguridad de integraciones de pago (Stripe/Wompi) y de datos de terceros (regalias).", "Desarrollador + Asesor Legal Externo (si aplica)", "Checklist de seguridad, auditoria externa puntual", "0 incidentes de seguridad con datos de pago/regalias", "Escaneo automatizado de dependencias vulnerables", "Trimestral"),
        ("IV. Infraestructura y Base de Datos", "1. Administrar base de datos (PostgreSQL via Neon), backups y migraciones.", "Desarrollador", "Neon, scripts de migracion", "Backups verificados sin fallos", "Backups automaticos programados", "Diario (backup) / Por cambio (migracion)"),
        ("IV. Infraestructura y Base de Datos", "2. Monitorear uptime y performance de APIs externas (Spotify, Stripe, Wompi).", "Desarrollador", "Dashboard de monitoreo, Postman", "Uptime >99.5%", "Alertas automaticas de caida de API externa", "Continuo"),
        ("V. Soporte Tecnico de Segundo Nivel", "1. Resolver incidencias tecnicas escaladas por la IA de soporte al cliente.", "Desarrollador", "Sistema de tickets, Sentry", "Incidencias escaladas resueltas en <24h", "Triage inicial ya cubierto por la IA de soporte antes de llegar aqui", "Segun incidencia"),
        ("VI. Documentacion Tecnica", "1. Mantener documentacion del codigo y de la arquitectura actualizada.", "Desarrollador", "README, Notion/Confluence", "Documentacion actualizada en cada release mayor", "Generacion asistida de documentacion desde comentarios de codigo", "Por release mayor"),
    ],
    "interconexion": "La publicacion de un track (disparada por la masterizacion aprobada del Ingeniero de Sonido) depende de que la integracion de distribucion este operativa. Una caida de uptime (Fase IV.2) puede bloquear el cobro de suscripciones que recibe el Contador, y debe notificarse de inmediato al CEO si afecta Elite 360.",
}

ROLES["8. Asesor Legal Externo"] = {
    "resumen": "Solo casos puntuales de alta complejidad (litigios, estructuracion multi-pais, clausulas atipicas) — el CEO cubre lo rutinario.",
    "rows": [
        ("I. Activacion del Servicio", "1. Recibir caso escalado por el CEO (solo alta complejidad).", "Asesor Legal Externo", "Correo/WhatsApp directo con el CEO", "Caso recibido con contexto completo en el primer contacto", "Ninguna - escalamiento es una decision humana deliberada", "Segun necesidad"),
        ("II. Analisis y Diagnostico", "1. Revisar documentacion y antecedentes del caso.", "Asesor Legal Externo", "Documentos del caso, normatividad aplicable", "Diagnostico entregado en el plazo acordado con el CEO", "Ninguna", "Por caso"),
        ("II. Analisis y Diagnostico", "2. Evaluar riesgo legal y opciones disponibles.", "Asesor Legal Externo", "Analisis juridico propio", "Opciones presentadas con riesgo/costo de cada una", "Ninguna", "Por caso"),
        ("III. Asesoria y Resolucion", "1. Redactar o ajustar contratos complejos o clausulas especificas (ej. estructuracion en Dubai).", "Asesor Legal Externo", "Plantillas legales especializadas", "Contrato entregado sin vacios legales detectados despues", "Ninguna - trabajo juridico especializado", "Por caso"),
        ("III. Asesoria y Resolucion", "2. Representar o asesorar en negociacion/litigio si aplica.", "Asesor Legal Externo", "Representacion legal directa", "Resultado documentado al cierre del caso", "Ninguna", "Por caso"),
        ("IV. Seguimiento", "1. Reportar avance y cierre del caso al CEO.", "Asesor Legal Externo", "Correo/informe escrito", "Reporte de cierre entregado en <5 dias de resuelto el caso", "Ninguna", "Por caso"),
    ],
    "interconexion": "La resolucion de un caso (ej. estructuracion legal para operar en Dubai) habilita al CEO a proceder con la firma de contratos o la constitucion legal en ese mercado (Fase II del CEO).",
}


ROLES["9. Comunicadora - Estrategia de Contenido"] = {
    "resumen": "Define el plan editorial y dirige al Content Engine, al Filmmaker y a la Disenadora -- no reemplaza a ninguno, decide que y cuando produce cada uno.",
    "rows": [
        ("I. Investigacion de Tendencias y Audiencia", "1. Monitorear tendencias de redes sociales, consumo musical y comportamiento de audiencia por artista/mercado.", "Comunicadora", "Google Trends, dashboards de redes sociales, Spotify for Artists", "Reporte de tendencias actualizado cada semana", "Alertas automaticas de tendencias relevantes por palabra clave", "Semanal"),
        ("I. Investigacion de Tendencias y Audiencia", "2. Analizar desempeno del contenido anterior para informar la estrategia.", "Comunicadora", "Meta Business Suite, YouTube Analytics, dashboard de la plataforma", "Analisis de desempeno entregado antes de planear el siguiente periodo", "Reporte automatizado de metricas desde las APIs de redes sociales", "Mensual"),
        ("II. Planeacion Editorial", "1. Definir el calendario editorial mensual (que se publica, en que canal, para que artista o para la marca).", "Comunicadora", "Notion/Airtable (calendario editorial)", "Calendario aprobado antes del dia 25 del mes anterior", "Plantilla de calendario editorial reutilizable", "Mensual"),
        ("II. Planeacion Editorial", "2. Priorizar que piezas requieren produccion humana (Filmmaker/Disenadora) vs. que cubre el Content Engine automatizado.", "Comunicadora", "Calendario editorial, criterios de priorizacion", "0 piezas bespoke asignadas por error al flujo automatizado (o viceversa)", "Clasificacion asistida por checklist de criterios", "Mensual"),
        ("III. Briefing a Produccion", "1. Briefing al Content Engine (parametros de generacion masiva: temas, tono, cadencia).", "Comunicadora", "Content Engine (src/content_engine/)", "Parametros definidos antes del primer dia del periodo", "La generacion en si ya esta automatizada; solo se brief ea la configuracion", "Mensual"),
        ("III. Briefing a Produccion", "2. Briefing al Filmmaker para piezas de edicion de material humano real.", "Comunicadora", "Brief creativo, Google Drive compartido", "Brief entregado antes del rodaje/edicion en 100% de los casos", "Plantilla de brief reutilizable", "Por pieza bespoke"),
        ("III. Briefing a Produccion", "3. Briefing a la Disenadora Grafica para piezas bespoke (campanas, portadas de lanzamiento).", "Comunicadora", "Brief creativo, brand guidelines (brand.py)", "Brief entregado con referencias de marca incluidas", "Plantilla de brief reutilizable", "Por pieza bespoke"),
        ("IV. Revision y Aprobacion", "1. Revisar piezas entregadas antes de publicacion (curaduria de calidad y alineacion de marca).", "Comunicadora", "Brand guidelines, checklist de marca", "Piezas aprobadas o devueltas en <24h de entregadas", "Checklist de alineacion de marca", "Continuo"),
        ("IV. Revision y Aprobacion", "2. Aprobar o devolver con ajustes especificos.", "Comunicadora", "Notion/Google Drive", "Maximo 2 rondas de ajuste por pieza", "Ninguna - criterio editorial humano", "Continuo"),
        ("V. Medicion y Ajuste de Estrategia", "1. Medir desempeno del contenido publicado (alcance, engagement, conversion).", "Comunicadora", "Meta Business Suite, YouTube Analytics, dashboard de la plataforma", "Reporte de desempeno entregado antes de planear el siguiente periodo", "Reporte automatizado desde APIs de redes sociales", "Mensual"),
        ("V. Medicion y Ajuste de Estrategia", "2. Ajustar la parrilla del siguiente periodo segun resultados.", "Comunicadora", "Calendario editorial", "Ajustes documentados y aplicados en el siguiente calendario", "Ninguna - decision estrategica humana", "Mensual"),
    ],
    "interconexion": "La Comunicadora dispara el briefing hacia el Filmmaker, la Disenadora Grafica Y el Content Engine automatizado, segun el tipo de pieza requerida (Fase III), y recibe de vuelta las metricas de desempeno (Fase V) para ajustar la proxima parrilla editorial. Tambien coordina con el Project Manager Elite 360 cuando el contenido es especifico de un artista del roster.",
}

ROLES["10. Filmmaker - Editor con IA (freelance)"] = {
    "resumen": "Edita material humano real (grabaciones de artistas firmados) con herramientas de IA -- es la contraparte del video 100% sintetico que genera el Content Engine.",
    "rows": [
        ("I. Recepcion de Material", "1. Recibir material crudo (grabaciones reales de artistas, contenido humano) de la Comunicadora/Project Manager.", "Filmmaker", "Google Drive/almacenamiento en la nube", "Material recibido completo y organizado por proyecto", "Checklist automatico de archivos requeridos al subir", "Por proyecto"),
        ("II. Seleccion y Curacion", "1. Seleccionar los mejores tomas/momentos con asistencia de herramientas de IA.", "Filmmaker", "Herramientas de deteccion automatica de highlights (IA)", "Seleccion completada en <50% del tiempo vs. revision manual", "Deteccion automatica de highlights/momentos clave con IA", "Por proyecto"),
        ("III. Edicion", "1. Editar y hacer corte de video.", "Filmmaker", "Adobe Premiere Pro / CapCut Pro + plugins de IA", "Primer corte entregado en el plazo acordado con la Comunicadora", "Subtitulado automatico generado con IA", "Por proyecto"),
        ("III. Edicion", "2. Correccion de color y audio basico.", "Filmmaker", "Premiere/CapCut, plugins de color y audio", "Entrega sin errores tecnicos de color/audio detectados despues", "Preset de color/audio de marca reutilizable", "Por proyecto"),
        ("IV. Entrega y Aprobacion", "1. Entregar para aprobacion de la Comunicadora/CEO.", "Filmmaker", "Google Drive compartido", "Entrega dentro del plazo del calendario editorial", "Notificacion automatica de entrega", "Por proyecto"),
        ("IV. Entrega y Aprobacion", "2. Ajustar segun feedback recibido.", "Filmmaker", "Premiere/CapCut", "Maximo 2 rondas de ajuste por pieza", "Ninguna - ajuste creativo humano", "Por proyecto"),
    ],
    "interconexion": "Recibe el briefing y el material de la Comunicadora (Fase III de la Comunicadora) y entrega la pieza final para su aprobacion antes de publicarse en los canales definidos por la parrilla editorial.",
}

ROLES["11. Disenadora Grafica (freelance)"] = {
    "resumen": "Diseno a la medida para campanas, portadas de lanzamiento y piezas que exceden el sistema de plantillas automatizado (Pillow/brand.py).",
    "rows": [
        ("I. Briefing", "1. Recibir briefing de la Comunicadora para piezas bespoke (campanas, portadas de lanzamiento, piezas fuera del sistema de plantillas automatizado).", "Disenadora Grafica", "Brief creativo, brand guidelines (brand.py)", "Briefing recibido con referencias de marca completas", "Plantilla de brief reutilizable (ya la provee la Comunicadora)", "Por pieza bespoke"),
        ("II. Bocetos y Propuestas", "1. Generar bocetos/propuestas iniciales alineadas a REBEL LUXURY.", "Disenadora Grafica", "Adobe Illustrator/Photoshop, Figma", "Al menos 2 propuestas entregadas en el plazo acordado", "Ninguna - trabajo creativo deliberadamente humano", "Por pieza bespoke"),
        ("III. Diseno Final", "1. Desarrollar el diseno final aprobado por la Comunicadora/CEO.", "Disenadora Grafica", "Illustrator/Photoshop, Figma", "Diseno final aprobado en maximo 2 rondas de ajuste", "Ninguna", "Por pieza bespoke"),
        ("IV. Entrega", "1. Entregar en los formatos de marca ya establecidos (paleta #5E17EB/crema/negro, tipografias Sceageus/Anton).", "Disenadora Grafica", "Brand guidelines (brand.py), exportacion en formatos requeridos", "Entrega en todos los formatos/tamanos requeridos sin reprocesos", "Plantilla de exportacion multi-formato", "Por pieza bespoke"),
    ],
    "interconexion": "Recibe el briefing de la Comunicadora (Fase III de la Comunicadora) junto con el Filmmaker y el Content Engine, y entrega la pieza final que la Comunicadora cura y aprueba antes de publicar.",
}


def set_header_fill(cell):
    cell.fill = PatternFill(start_color=VIOLETA, end_color=VIOLETA, fill_type="solid")
    cell.font = Font(color="FFFFFF", bold=True, size=11)
    cell.alignment = Alignment(wrap_text=True, vertical="center")


def build():
    wb = Workbook()
    wb.remove(wb.active)

    # Hoja indice
    idx = wb.create_sheet("00_Indice")
    idx["A1"] = "MANUAL DE FUNCIONES Y PROCESOS - IM MUSIC"
    idx["A1"].font = Font(bold=True, size=16, color=VIOLETA)
    idx["A3"] = "Rol"
    idx["B3"] = "Resumen de la funcion"
    set_header_fill(idx["A3"])
    set_header_fill(idx["B3"])
    r = 4
    for role, data in ROLES.items():
        idx.cell(row=r, column=1, value=role)
        idx.cell(row=r, column=2, value=data["resumen"])
        idx.cell(row=r, column=2).alignment = Alignment(wrap_text=True)
        r += 1
    idx.column_dimensions["A"].width = 32
    idx.column_dimensions["B"].width = 90

    for role, data in ROLES.items():
        sheet_name = role[:31]
        ws = wb.create_sheet(sheet_name)
        ws["A1"] = f"Proceso y Responsabilidades: {role}"
        ws["A1"].font = Font(bold=True, size=13, color=VIOLETA)
        ws.merge_cells("A1:G1")

        for col, header in enumerate(HEADERS, start=1):
            c = ws.cell(row=2, column=col, value=header)
            set_header_fill(c)

        row_idx = 3
        for fase, subpaso, resp, herram, metr, autom, freq in data["rows"]:
            ws.cell(row=row_idx, column=1, value=fase)
            ws.cell(row=row_idx, column=2, value=subpaso)
            ws.cell(row=row_idx, column=3, value=resp)
            ws.cell(row=row_idx, column=4, value=herram)
            ws.cell(row=row_idx, column=5, value=metr)
            ws.cell(row=row_idx, column=6, value=autom)
            ws.cell(row=row_idx, column=7, value=freq)
            for col in range(1, 8):
                ws.cell(row=row_idx, column=col).alignment = Alignment(wrap_text=True, vertical="top")
            row_idx += 1

        row_idx += 1
        ws.cell(row=row_idx, column=1, value="INTERCONEXION CON OTROS ROLES")
        ws.cell(row=row_idx, column=1).font = Font(bold=True, color="FFFFFF")
        ws.cell(row=row_idx, column=1).fill = PatternFill(start_color=GRIS, end_color=GRIS, fill_type="solid")
        ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=7)
        row_idx += 1
        ws.cell(row=row_idx, column=1, value=data["interconexion"])
        ws.cell(row=row_idx, column=1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=7)
        ws.row_dimensions[row_idx].height = 60

        widths = [28, 48, 22, 30, 28, 32, 16]
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.freeze_panes = "A3"

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(OUT_PATH))
    print(f"OK: {OUT_PATH} ({OUT_PATH.stat().st_size // 1024}KB) - {len(ROLES)} roles")


if __name__ == "__main__":
    build()
