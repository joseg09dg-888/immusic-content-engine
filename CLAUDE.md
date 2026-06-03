# IM Music Content Engine — Claude Code Instructions

## Proyecto
Sistema automatizado REBEL LUXURY para IM Music sello discográfico.
Spec maestro: `docs/superpowers/specs/2026-05-28-immusic-system-design.md`

## Stack
- Python 3.12 | anthropic | pillow | edge-tts | gtts | ffmpeg
- Claude API: claude-sonnet-4-6

## IDENTIDAD DE MARCA (INMUTABLE — VERIFICADA CON @immusicsello)

### Fuentes (assets/fonts/)
- **Sceageus** (`sceageus.otf`) — HEADLINE PRINCIPAL. La fuente display de la marca. Gothic/redondeada.
- **Anton** (`Anton-Regular.ttf` o `Anton.ttf`) — textos secundarios, contexto, subtítulos, CTA
- NUNCA usar Impact sola. NUNCA usar Boogaloo como primaria. Siempre Sceageus primero.

### Colores
- Violeta: `#5E17EB` — fondo de TODOS los slides (verificado en brand.py)
- Negro: `#000000` — fondo closing card / videos dark
- Crema: `#F2EDE5` — texto "MUSIC" en closing card
- Blanco: `#FFFFFF` — texto principal sobre violeta

### Logo
- `assets/logo/logo_immusic.png` — 1080x1350px RGB, fondo negro, marca M en violeta
- Closing card: logo centrado sobre negro + "MUSIC" en crema

### Ilustraciones (assets/engravings/)
USAR SOLO grabados con líneas finas y nítidas (estilo Gustave Doré):
- ✅ eng_00_Jacob_Wrestling_with_the_Angel — Doré, ángel B&W
- ✅ eng_00_GustaveDoreParadiseLostSatanProfile — Doré, Satán B&W
- ✅ eng_01_Gustave_Dore_Bible_Deluge — Doré, diluvio B&W
- ✅ eng_05_Vintage_heraldic_royal_crown — corona vectorial, líneas claras
- ✅ eng_07_Indian_snakes — serpiente B&W, líneas muy nítidas
- ✅ eng_12_Vintage_heraldic_royal_crown_2 — segunda corona
- ✅ eng_17_Orchid_Album — orquídea botánica B&W

BLACKLIST (NO usar, crean manchas negras):
- ❌ Imágenes tonales/fotográficas/coloreadas
- ❌ Imágenes con texto anotado (mapas, libros)
- ❌ SVGs planos sin detalle de líneas
- El blacklist completo está en designer.py → _ENGRAVING_BLACKLIST

### Procesamiento de imagen
- threshold = 190 (solo líneas MUY oscuras = opacos)
- contrast = 1.1 (suave, NO destruir líneas finas)
- El violeta SIEMPRE debe ser visible a través de la ilustración

## Reglas absolutas de diseño
1. Sceageus para headline SIEMPRE — no hay excepción
2. El fondo es SIEMPRE violeta sólido #5E17EB (nunca negro, nunca gradiente)
3. Ilustración ocupa 60-80% del slide, líneas negras finas sobre violeta
4. Texto: contexto (pequeño Anton) → HEADLINE MASIVO (Sceageus) → subtítulo (Anton) → CTA fijo abajo
5. Closing card: negro puro + logo_immusic.png centrado en violeta

## Estructura de archivos
```
src/core/           → brand.py, config.py, drive_sync.py
src/content_engine/ → research.py, writer.py, designer.py, automated_video.py, publisher.py
scripts/            → crear_contenido_semana.py, upload_human_content.py, sync_to_drive.py
assets/fonts/       → sceageus.otf, Anton-Regular.ttf (FUENTES DE MARCA)
assets/logo/        → logo_immusic.png (LOGO REAL)
assets/engravings/  → grabados B&W Doré y similares
```

## Distribución
- Nexus (8% regalías)
- Plataformas: YouTube + Instagram + TikTok

## Publicación
- Lunes, Miércoles, Viernes
- YouTube: 18:00 COT | Instagram: 19:00 COT | TikTok: 20:00 COT
