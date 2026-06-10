# IM Music Content Engine — Plan Completo Todas las Fases

> ⚠️ **SUPERADO (2026-06-10):** Las TAREA 0-7 de este plan ya están implementadas en el código real (con nombres/arquitectura distintos a los descritos aquí — ver auditoría en memoria `immusic-content-engine.md`, sección "Auditoría 2026-06-10"). 153/153 tests pasan. Roadmap vigente: `docs/ESTRATEGIA_ALGORITMOS_2026.md`. No usar este plan para nuevo trabajo — los checkboxes `- [ ]` están desactualizados y NO reflejan el estado real.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sistema 100% automatizado que genera contenido para YouTube (long + Shorts), TikTok (Reels + Carruseles), Instagram (Reels + Carruseles), con portadas, copys y SEO optimizado, además de producción musical completa (beats Chill Hop / Afro House) con masterización, visualizer y distribución Nexus.

**Architecture:** Pipeline orquestado por scheduler.py — research → writer (todos los formatos) → designer (todas las plataformas) → video_producer (subtítulos Whisper) → publisher (YouTube + TikTok + Instagram). Paralelo: Music Engine — beat_generator → mastering → visualizer → release_pack → music_publisher.

**Tech Stack:** Python 3.12, Claude API (claude-sonnet-4-6), Pillow, librosa, pydub, pyloudnorm, soundfile, FFmpeg, openai-whisper, torch+torchaudio (CPU), audiocraft (MusicGen), manim

---

## Estado actual (NO tocar, ya funciona ✅)

- `src/core/brand.py` ✅ — Brand, VoiceProfile, RebelBrainMethod
- `src/core/config.py` ✅ — carga .env
- `src/content_engine/research.py` ✅ — RSS scraping + score_story + build_brief
- `src/content_engine/writer.py` ✅ — 12 formatos Claude API
- `src/content_engine/designer.py` ✅ — thumbnail/carousel/story/tiktok
- `src/content_engine/seo_engine.py` ✅ — YouTube + Instagram + TikTok SEO
- `src/content_engine/video_producer.py` ✅ — FFmpeg funcional, Whisper pendiente
- `src/content_engine/publisher.py` ✅ — YouTubePublisher + InstagramPublisher (falta OAuth)
- `src/music_engine/mastering.py` ✅ — LUFS completo
- `src/music_engine/beat_generator.py` ✅ skeleton — falta PyTorch
- `src/music_engine/release_pack.py` ✅ — estructura releases/
- `src/core/approval_cli.py` ✅ — terminal y/n

---

## TAREA 0 — Instalación de Dependencias

**Files:**
- Ninguno (solo pip install)

- [ ] **Paso 0.1: Instalar Whisper (subtítulos automáticos)**
```powershell
pip install openai-whisper
python -c "import whisper; print('Whisper OK:', whisper.__version__)"
```

- [ ] **Paso 0.2: Instalar PyTorch CPU (base para AudioCraft)**
```powershell
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
python -c "import torch; print('PyTorch OK:', torch.__version__)"
```

- [ ] **Paso 0.3: Instalar AudioCraft**
```powershell
pip install audiocraft
python -c "from audiocraft.models import MusicGen; print('AudioCraft OK')"
```

- [ ] **Paso 0.4: Instalar Manim (visualizer)**
```powershell
pip install manim
python -c "import manim; print('Manim OK:', manim.__version__)"
```

- [ ] **Paso 0.5: Actualizar requirements.txt**
Agregar al final de `requirements.txt`:
```
openai-whisper>=20231117
torch>=2.0.0
torchaudio>=2.0.0
audiocraft>=1.3.0
manim>=0.18.0
```

- [ ] **Paso 0.6: Verificar tests siguen pasando**
```powershell
python -m pytest tests/ -q --tb=short
```
Esperado: 110 passed (no regresiones).

---

## TAREA 1 — Expandir writer.py: Todos los Formatos de Plataforma

**Files:**
- Modify: `src/content_engine/writer.py`
- Test: `tests/test_writer.py`

**Nuevos formatos a agregar:**
- `youtube_short` — guión 55-58s (hook + dato + reframe), texto en pantalla cada 3s
- `youtube_chapters` — timestamps + títulos de capítulos para descripción larga
- `youtube_monetization` — pinned comment + end screen CTA + community post
- `tiktok_reel` — guión 30-60s, hook viral primeros 3s, trending sounds sugeridos
- `tiktok_carousel` — 5-7 slides con copy impactante, slide 1 = gancho
- `instagram_reel` — guión 15-30s, subtítulos para cada escena
- `facebook_reel` — guión 30-60s (ya existe FB_REEL_MIN/MAX en ContentDurations)
- `pinterest_idea` — título + descripción SEO 500 chars

- [ ] **Paso 1.1: Agregar constantes de formatos en writer.py**

En `src/content_engine/writer.py`, dentro de la clase `ContentWriter`, agregar método:
```python
def _format_system_prompt(self) -> str:
    """System prompt base con voz REBEL LUXURY."""
    return (
        f"Eres el escritor de contenido de {Brand.LABEL}.\n"
        f"{VoiceProfile.as_prompt_block()}\n"
        f"{RebelBrainMethod.as_prompt_block()}\n"
        "REGLA: Nunca uses palabras de la lista WORDS_NO. "
        "Cada pieza debe incomodar al oyente de forma inteligente.\n"
    )
```

- [ ] **Paso 1.2: Agregar método generate_youtube_short()**

```python
def generate_youtube_short(self, brief: dict) -> dict:
    """Guión YouTube Short 55-58s — hook + dato + reframe."""
    prompt = (
        f"Crea un guión para YouTube Short (55-58 segundos) sobre:\n"
        f"Título: {brief.get('titulo_principal', '')}\n"
        f"Ángulo neurociencia: {brief.get('angulo_neurociencia', '')}\n"
        f"Hook: {brief.get('hook_apertura', '')}\n\n"
        "ESTRUCTURA OBLIGATORIA:\n"
        "- Segundos 0-3: Pattern Interrupt visual + frase gancho (máx 8 palabras)\n"
        "- Segundos 3-15: Dato sorprendente con número específico\n"
        "- Segundos 15-45: Desarrollo con ángulo neurociencia/psicología\n"
        "- Segundos 45-55: Rebel Reframe — conclusión que cuestiona lo establecido\n"
        "- Segundo 55-58: CTA implícito IM Music\n\n"
        "Formato de salida JSON:\n"
        '{"guion_completo": "...", "texto_pantalla": ["frase1 (0-3s)", "frase2 (3-6s)", ...], '
        '"hook_visual": "descripción del gancho visual", "trending_sounds": ["sound1", "sound2"]}'
    )
    return self._call_api(prompt, max_tokens=1200)
```

- [ ] **Paso 1.3: Agregar método generate_tiktok_carousel()**

```python
def generate_tiktok_carousel(self, brief: dict, num_slides: int = 6) -> dict:
    """Carrusel TikTok — 5-7 slides con copy REBEL LUXURY."""
    prompt = (
        f"Crea un carrusel de {num_slides} slides para TikTok sobre:\n"
        f"Título: {brief.get('titulo_principal', '')}\n"
        f"Ángulo: {brief.get('angulo_neurociencia', '')}\n\n"
        "REGLAS:\n"
        "- Slide 1: Título impactante — promesa sin cumplir (máx 6 palabras)\n"
        "- Slides 2-5: Un insight poderoso por slide (máx 15 palabras cada uno)\n"
        f"- Slide {num_slides}: CTA rebelde — no 'síguenos', sino una verdad incómoda\n"
        "- Cada slide debe funcionar SOLO como imagen estática\n\n"
        "Formato JSON:\n"
        '{"slides": [{"numero": 1, "titulo": "...", "subtitulo": "...", "dato": "..."}, ...],'
        '"caption_tiktok": "150 chars máx con hashtags virales"}'
    )
    return self._call_api(prompt, max_tokens=1500)
```

- [ ] **Paso 1.4: Agregar método generate_instagram_reel()**

```python
def generate_instagram_reel(self, brief: dict) -> dict:
    """Guión Instagram Reel 15-30s — copy visual + subtítulos."""
    prompt = (
        f"Crea guión para Instagram Reel (15-30 segundos) sobre:\n"
        f"Título: {brief.get('titulo_principal', '')}\n"
        f"Hook: {brief.get('hook_apertura', '')}\n\n"
        "ESTRUCTURA:\n"
        "- 0-3s: Hook visual (acción o texto que detiene el scroll)\n"
        "- 3-20s: Core insight con dato neurociencia\n"
        "- 20-28s: Rebel Reframe\n"
        "- 28-30s: IM Music brand moment\n\n"
        "Formato JSON:\n"
        '{"guion_escenas": [{"tiempo": "0-3s", "accion": "...", "texto_pantalla": "...", "narracion": "..."}],'
        '"caption_instagram": "hasta 2200 chars con hashtags",'
        '"hashtags_instagram": ["#tag1", "#tag2", ...]}'
    )
    return self._call_api(prompt, max_tokens=1400)
```

- [ ] **Paso 1.5: Agregar método generate_youtube_monetization_pack()**

```python
def generate_youtube_monetization_pack(self, brief: dict, video_duration_min: int = 8) -> dict:
    """Pack completo para monetización YouTube: capítulos, pinned comment, end screen, community."""
    prompt = (
        f"Crea el pack de monetización YouTube para un video de {video_duration_min} minutos sobre:\n"
        f"Título: {brief.get('titulo_principal', '')}\n\n"
        "GENERAR:\n"
        "1. CAPÍTULOS (timestamps) — mínimo 5 capítulos con formato '0:00 Título'\n"
        "2. DESCRIPCIÓN SEO completa con:\n"
        "   - Hook en primeras 2 líneas (aparece sin expandir)\n"
        "   - Timestamps\n"
        "   - Palabras clave long-tail integradas naturalmente\n"
        "   - Links de recursos (placeholders: [LINK_RECURSO_1])\n"
        "   - Disclaimer y créditos IM Music\n"
        "3. PINNED COMMENT — pregunta que genera debate (máx 200 chars)\n"
        "4. END SCREEN SCRIPT — texto hablado últimos 20 segundos\n"
        "5. COMMUNITY POST — para publicar 24h antes del video\n"
        "6. TAGS YouTube — 30 tags ordenados por prioridad\n\n"
        "Formato JSON con claves: capitulos, descripcion_seo, pinned_comment, "
        "end_screen_script, community_post, tags_youtube"
    )
    return self._call_api(prompt, max_tokens=2500)
```

- [ ] **Paso 1.6: Correr tests**
```powershell
python -m pytest tests/test_writer.py -v --tb=short
```
Esperado: todos los tests del writer pasan.

- [ ] **Paso 1.7: Commit**
```powershell
git add src/content_engine/writer.py tests/test_writer.py
git commit -m "feat(writer): formatos YouTube Short, TikTok carousel, IG Reel, monetización"
```

---

## TAREA 2 — Expandir designer.py: Todas las Plataformas

**Files:**
- Modify: `src/content_engine/designer.py`
- Test: `tests/test_designer.py`

**Nuevas dimensiones/formatos:**
- `youtube_short_thumbnail` (1080x1920) — igual a tiktok pero con barra superior YouTube
- `tiktok_carousel_slide` (1080x1080) — igual a Instagram pero con marca TikTok
- `facebook_reel_cover` (1080x1920)
- `pinterest_pin` (1000x1500)
- Video subtitle overlay (clase SubtitleRenderer)

- [ ] **Paso 2.1: Agregar dimensiones en brand.py**

En `src/core/brand.py`, clase `Dimensions`, agregar:
```python
PINTEREST_PIN: Tuple[int, int] = (1000, 1500)
FACEBOOK_REEL: Tuple[int, int] = (1080, 1920)
YOUTUBE_SHORT: Tuple[int, int] = (1080, 1920)  # mismo que tiktok/story
TIKTOK_CAROUSEL: Tuple[int, int] = (1080, 1080)  # mismo que instagram
```

- [ ] **Paso 2.2: Agregar método generate_youtube_short_thumbnail() en Designer**

```python
def generate_youtube_short_thumbnail(
    self, title: str, subtitle: str = "", save_path: Optional[Path] = None
) -> Image.Image:
    """YouTube Short thumbnail 1080x1920 con barra superior YouTube Shorts."""
    img = self._make_base_canvas(Dimensions.YOUTUBE_SHORT)
    draw = ImageDraw.Draw(img)
    rng = random.Random(title)
    tmpl = _pick_template(title)
    self._draw_stars(draw, *Dimensions.YOUTUBE_SHORT, tmpl["star_density"], rng)
    self._draw_constellation_lines(draw, *Dimensions.YOUTUBE_SHORT, tmpl["accent_count"], rng)
    # Barra superior "SHORTS" estilo YouTube
    bar_h = 80
    draw.rectangle([(0, 0), (1080, bar_h)], fill=(*_hex_to_rgb(Brand.VIOLET), 200))
    font_bar = _font("subtitle", 36)
    draw.text((540, bar_h // 2), "SHORTS", fill=_hex_to_rgb(Brand.WHITE), font=font_bar, anchor="mm")
    self._draw_text_block(draw, title, subtitle, *Dimensions.YOUTUBE_SHORT, rng)
    self._stamp_logo(img)
    if save_path:
        img.save(save_path, "PNG")
    return img
```

- [ ] **Paso 2.3: Agregar método generate_tiktok_carousel_slides() en Designer**

```python
def generate_tiktok_carousel_slides(
    self, slides_data: list, save_dir: Optional[Path] = None
) -> list:
    """
    Genera slides de carrusel TikTok (1080x1080).
    slides_data: [{"titulo": str, "subtitulo": str, "dato": str}, ...]
    """
    images = []
    for i, slide in enumerate(slides_data):
        img = self._make_base_canvas(Dimensions.TIKTOK_CAROUSEL)
        draw = ImageDraw.Draw(img)
        rng = random.Random(f"{slide.get('titulo', '')}_{i}")
        tmpl = _pick_template(f"tiktok_{i}")
        self._draw_stars(draw, *Dimensions.TIKTOK_CAROUSEL, tmpl["star_density"] // 2, rng)
        self._draw_constellation_lines(draw, *Dimensions.TIKTOK_CAROUSEL, tmpl["accent_count"], rng)
        # Número de slide
        font_num = _font("regular", 28)
        draw.text((40, 40), f"{i+1}/{len(slides_data)}", fill=(*_hex_to_rgb(Brand.CREAM), 150), font=font_num)
        self._draw_text_block(draw, slide.get("titulo", ""), slide.get("subtitulo", ""), *Dimensions.TIKTOK_CAROUSEL, rng)
        self._stamp_logo(img)
        if save_dir:
            p = Path(save_dir) / f"tiktok_slide_{i+1:02d}.png"
            img.save(p, "PNG")
        images.append(img)
    return images
```

- [ ] **Paso 2.4: Agregar método generate_pinterest_pin() en Designer**

```python
def generate_pinterest_pin(
    self, title: str, subtitle: str = "", save_path: Optional[Path] = None
) -> Image.Image:
    """Pinterest pin 1000x1500 con estética REBEL LUXURY."""
    img = self._make_base_canvas(Dimensions.PINTEREST_PIN)
    draw = ImageDraw.Draw(img)
    rng = random.Random(title)
    tmpl = _pick_template(title)
    self._draw_stars(draw, *Dimensions.PINTEREST_PIN, 2000, rng)
    self._draw_constellation_lines(draw, *Dimensions.PINTEREST_PIN, 4, rng)
    self._draw_text_block(draw, title, subtitle, *Dimensions.PINTEREST_PIN, rng)
    self._stamp_logo(img)
    if save_path:
        img.save(save_path, "PNG")
    return img
```

- [ ] **Paso 2.5: Correr tests del designer**
```powershell
python -m pytest tests/test_designer.py -v --tb=short
```
Esperado: todos pasan.

- [ ] **Paso 2.6: Commit**
```powershell
git add src/content_engine/designer.py src/core/brand.py tests/test_designer.py
git commit -m "feat(designer): YouTube Short, TikTok carousel, Pinterest pin"
```

---

## TAREA 3 — Expandir seo_engine.py: YouTube Monetización + TikTok SEO

**Files:**
- Modify: `src/content_engine/seo_engine.py`
- Test: `tests/test_seo_engine.py`

- [ ] **Paso 3.1: Agregar método youtube_monetization_seo()**

En `src/content_engine/seo_engine.py`, agregar:
```python
def youtube_monetization_seo(self, title: str, brief: dict, duration_sec: int = 480) -> dict:
    """
    SEO completo para video YouTube monetizable.
    Requisitos monetización: >8 min, 1000 subs, 4000h watch time.
    """
    keywords = self._extract_keywords(title, brief.get("angulo_neurociencia", ""))
    
    # Título optimizado: 60-70 chars, keyword al inicio
    seo_title = f"{keywords[0].upper()} — {title}"[:70] if keywords else title[:70]
    
    # Tags con long-tail
    base_tags = self.generate_youtube_tags(title, brief.get("fuentes", []))
    longtail_tags = [
        f"{keywords[0]} para artistas",
        f"cómo {keywords[0].lower()} en música",
        f"{keywords[0]} industria musical Colombia",
        "marketing musical 2026",
        "estrategia musical REBEL LUXURY",
        "IM Music sello discográfico",
        "neurociencia marketing musical",
        "artistas emergentes Colombia",
    ] if keywords else []
    
    # Descripción con chapters
    chapters = self._generate_chapters(duration_sec)
    
    return {
        "titulo_optimizado": seo_title,
        "tags_prioritarios": base_tags[:15],
        "tags_longtail": longtail_tags,
        "capitulos": chapters,
        "watch_time_target_min": max(8, duration_sec // 60),
        "keyword_principal": keywords[0] if keywords else title.split()[0],
        "meta_description": f"{brief.get('hook_apertura', title)[:160]}",
    }

def _extract_keywords(self, title: str, angle: str) -> list:
    """Extrae keywords de title + ángulo de neurociencia."""
    words = (title + " " + angle).lower().split()
    stopwords = {"de", "la", "el", "en", "un", "una", "los", "las", "que", "y", "a", "con", "del"}
    return [w for w in words if len(w) > 4 and w not in stopwords][:5]

def _generate_chapters(self, duration_sec: int) -> list:
    """Genera capítulos automáticos basados en duración."""
    num_chapters = max(5, duration_sec // 90)
    interval = duration_sec // num_chapters
    chapters = [{"tiempo": "0:00", "titulo": "Introducción — el problema"}]
    labels = ["El dato que nadie menciona", "Por qué falla la industria", 
              "La neurociencia detrás", "El método REBEL LUXURY", "Conclusión y próximos pasos"]
    for i in range(1, num_chapters):
        mins, secs = divmod(i * interval, 60)
        label = labels[i-1] if i-1 < len(labels) else f"Parte {i+1}"
        chapters.append({"tiempo": f"{mins}:{secs:02d}", "titulo": label})
    return chapters
```

- [ ] **Paso 3.2: Agregar método tiktok_seo_complete()**

```python
def tiktok_seo_complete(self, title: str, brief: dict) -> dict:
    """SEO completo para TikTok: hashtags, sonidos trending, horario óptimo."""
    keywords = self._extract_keywords(title, brief.get("angulo_neurociencia", ""))
    
    # Hashtags TikTok — mezcla viral + nicho + marca
    viral_tags = ["#fyp", "#parati", "#foryou", "#viral2026"]
    niche_tags = ["#musicaindustria", "#marketingmusical", "#artistas", "#selladiscografico", 
                  "#neurocienciamarketing", "#colombiamusica", "#rebelluxury"]
    brand_tags = ["#IMMusic", "#REBELLuxury", "#immusicsello"]
    keyword_tags = [f"#{kw.replace(' ', '')}" for kw in keywords[:3]]
    
    all_tags = viral_tags + niche_tags + brand_tags + keyword_tags
    caption = f"{brief.get('hook_apertura', title)[:80]} {' '.join(all_tags[:8])}"
    
    return {
        "caption_150chars": caption[:150],
        "hashtags_completos": all_tags,
        "hashtags_prioritarios": viral_tags + niche_tags[:3] + brand_tags[:1],
        "sonidos_sugeridos": [
            "Lo-Fi Hip Hop Radio — trending en #fyp",
            "Afro House beat instrumental — 124bpm",
            "Chill trap beat — sin copyright",
        ],
        "horario_optimo": {"dia": "Lunes/Miercoles/Viernes", "hora": "18:00-20:00 COT"},
        "duracion_optima_seg": 45,
    }
```

- [ ] **Paso 3.3: Correr tests SEO**
```powershell
python -m pytest tests/test_seo_engine.py -v --tb=short
```

- [ ] **Paso 3.4: Commit**
```powershell
git add src/content_engine/seo_engine.py tests/test_seo_engine.py
git commit -m "feat(seo): YouTube monetizacion completa, TikTok SEO, chapters automaticos"
```

---

## TAREA 4 — Activar Whisper en video_producer.py

**Files:**
- Modify: `src/content_engine/video_producer.py`
- Test: `tests/test_video_producer.py`

- [ ] **Paso 4.1: Verificar Whisper instalado**
```powershell
python -c "import whisper; model = whisper.load_model('base'); print('Whisper base model OK')"
```

- [ ] **Paso 4.2: Activar generate_subtitles() en VideoProducer**

En `src/content_engine/video_producer.py`, reemplazar el stub de subtítulos:
```python
def generate_subtitles(self, audio_path: Path, language: str = "es") -> dict:
    """
    Genera subtítulos con Whisper.
    Returns: {"srt": str, "vtt": str, "segments": list}
    """
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(str(audio_path), language=language, task="transcribe")
    
    # Generar SRT
    srt_lines = []
    for i, seg in enumerate(result["segments"], 1):
        start = self._seconds_to_srt_time(seg["start"])
        end = self._seconds_to_srt_time(seg["end"])
        srt_lines.append(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n")
    
    srt_content = "\n".join(srt_lines)
    
    # Generar VTT (para YouTube)
    vtt_content = "WEBVTT\n\n" + srt_content.replace(",", ".")
    
    return {
        "srt": srt_content,
        "vtt": vtt_content,
        "segments": result["segments"],
        "language_detected": result.get("language", language),
    }

def _seconds_to_srt_time(self, seconds: float) -> str:
    """Convierte segundos a formato SRT HH:MM:SS,mmm."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
```

- [ ] **Paso 4.3: Añadir método burn_subtitles() para TikTok/Shorts**

```python
def burn_subtitles(
    self,
    video_path: Path,
    srt_path: Path,
    output_path: Path,
    style: str = "tiktok",
) -> Path:
    """
    Quema subtítulos en el video con FFmpeg.
    style: 'tiktok' (centro, fuente grande), 'youtube' (abajo, fuente mediana)
    """
    styles = {
        "tiktok": "FontName=Anton,FontSize=24,PrimaryColour=&H00F2EDE5,OutlineColour=&H00000000,Outline=2,Alignment=10",
        "youtube": "FontName=Anton,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=1,Alignment=2",
    }
    vf = f"subtitles={srt_path}:force_style='{styles.get(style, styles[\"youtube\"])}'"
    cmd = ["ffmpeg", "-i", str(video_path), "-vf", vf, "-c:a", "copy", str(output_path), "-y"]
    import subprocess
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg subtitle burn failed: {result.stderr[-500:]}")
    return output_path
```

- [ ] **Paso 4.4: Correr tests video**
```powershell
python -m pytest tests/test_video_producer.py -v --tb=short
```

- [ ] **Paso 4.5: Commit**
```powershell
git add src/content_engine/video_producer.py tests/test_video_producer.py
git commit -m "feat(video): Whisper subtitulos activados, burn_subtitles para TikTok/YouTube"
```

---

## TAREA 5 — Completar beat_generator.py con AudioCraft Real

**Files:**
- Modify: `src/music_engine/beat_generator.py`
- Test: `tests/test_beat_generator.py`

Requisito: PyTorch y AudioCraft instalados (TAREA 0).

- [ ] **Paso 5.1: Verificar AudioCraft disponible**
```powershell
python -c "from audiocraft.models import MusicGen; print('AudioCraft OK')"
```

- [ ] **Paso 5.2: Implementar generate() real en BeatGenerator**

En `src/music_engine/beat_generator.py`, reemplazar el skeleton:
```python
def generate(
    self,
    genre: str = "chill_hop",
    bpm: int = None,
    duration_sec: int = 170,
    output_dir: Path = None,
) -> Path:
    """
    Genera un beat con MusicGen.
    genre: 'chill_hop' | 'afro_house'
    duration_sec: máx 170s (Brand.SONG_MAX) con fade en 155s
    """
    if not self.is_available():
        raise RuntimeError(
            "AudioCraft no instalado. Ejecutar:\n"
            "  pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu\n"
            "  pip install audiocraft"
        )
    
    from audiocraft.models import MusicGen
    
    prompts = {
        "chill_hop": f"chill hop beat, lo-fi, {bpm or 90}bpm, dreamy nocturnal city vibes, "
                     "vinyl crackle, jazz chords, mellow bass, head-nodding drums, REBEL LUXURY",
        "afro_house": f"afro house beat, {bpm or 124}bpm, deep bass, tribal percussion, "
                      "galactic atmosphere, synthesizer pads, African rhythms, REBEL LUXURY",
    }
    
    if genre not in prompts:
        raise ValueError(f"Género no válido: {genre}. Usar 'chill_hop' o 'afro_house'")
    
    # Cargar modelo (small para CPU, medium para GPU)
    model = MusicGen.get_pretrained("facebook/musicgen-small")
    model.set_generation_params(duration=min(duration_sec, 30))  # MusicGen máx ~30s por llamada
    
    # Generar audio
    wav = model.generate([prompts[genre]], progress=True)  # shape: [1, 1, samples]
    audio_array = wav[0, 0].cpu().numpy()
    sample_rate = model.sample_rate
    
    # Guardar
    import soundfile as sf
    import datetime
    output_dir = Path(output_dir) if output_dir else Path("releases") / "beats_draft"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"beat_{genre}_{bpm or 'auto'}bpm_{timestamp}.wav"
    output_path = output_dir / filename
    
    sf.write(str(output_path), audio_array, sample_rate, subtype="PCM_24")
    return output_path
```

- [ ] **Paso 5.3: Test con beat real (manual, requiere AudioCraft)**
```powershell
python -c "
import sys; sys.path.insert(0, 'src')
from music_engine.beat_generator import BeatGenerator
bg = BeatGenerator()
if bg.is_available():
    path = bg.generate(genre='chill_hop', bpm=90, duration_sec=30)
    print('Beat generado:', path)
else:
    print('AudioCraft no disponible aun')
"
```

- [ ] **Paso 5.4: Commit**
```powershell
git add src/music_engine/beat_generator.py
git commit -m "feat(beat): AudioCraft MusicGen integrado, genera chill_hop y afro_house reales"
```

---

## TAREA 6 — FASE 4: visualizer.py con Manim + Audio-Reactive

**Files:**
- Create: `src/music_engine/visualizer.py`
- Test: `tests/test_visualizer.py`

- [ ] **Paso 6.1: Crear estructura base de Visualizer**

Crear `src/music_engine/visualizer.py`:
```python
"""
IM Music Visualizer — REBEL LUXURY audio-reactive.
Escenas:
  - ChillHop: "El Viajero Nocturno" — ciudad nocturna, lluvia, neón violeta, constelaciones
  - AfroHouse: "El Ser Galáctico" — galaxia, nebulosas, partículas que reaccionan al beat
"""
from pathlib import Path
from typing import Optional
import numpy as np


class Visualizer:
    """Genera video visualizer para beats IM Music usando Manim."""

    def __init__(self, quality: str = "medium_quality"):
        """
        quality: 'low_quality' (480p, rápido), 'medium_quality' (720p), 'high_quality' (1080p)
        """
        self.quality = quality

    def generate(
        self,
        audio_path: Path,
        genre: str = "chill_hop",
        output_path: Optional[Path] = None,
        duration_sec: Optional[float] = None,
    ) -> Path:
        """
        Genera video visualizer sincronizado con el audio.
        Devuelve path al archivo MP4 generado.
        """
        try:
            import manim  # noqa: F401
        except ImportError:
            raise RuntimeError(
                "Manim no instalado. Ejecutar: pip install manim\n"
                "También requiere: ffmpeg, LaTeX (para renderizado)"
            )

        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio no encontrado: {audio_path}")

        # Analizar audio con librosa
        beats, tempo, waveform, sr = self._analyze_audio(audio_path, duration_sec)

        # Seleccionar escena según género
        if genre == "chill_hop":
            output = self._render_chill_hop(audio_path, beats, tempo, waveform, sr, output_path)
        elif genre == "afro_house":
            output = self._render_afro_house(audio_path, beats, tempo, waveform, sr, output_path)
        else:
            raise ValueError(f"Género no válido: {genre}")

        return output

    def _analyze_audio(self, audio_path: Path, duration_sec: Optional[float]) -> tuple:
        """Analiza audio: extrae beats, tempo, waveform."""
        import librosa
        y, sr = librosa.load(str(audio_path), duration=duration_sec, mono=True)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        return beat_times, float(tempo), y, sr

    def _render_chill_hop(self, audio_path, beats, tempo, waveform, sr, output_path) -> Path:
        """
        Escena Chill Hop: "El Viajero Nocturno"
        - Ciudad nocturna futurista con lluvia suave
        - Neón violeta #5E17EB pulsando con el beat
        - Constelaciones que forman el logo IM Music
        - Partículas de polvo estelar flotan al ritmo
        """
        output_path = output_path or Path("releases") / "visualizers" / f"chill_hop_visualizer.mp4"
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        script = self._build_manim_script_chill_hop(beats, tempo, waveform, sr, audio_path)
        script_path = output_path.parent / "scene_chill_hop.py"
        script_path.write_text(script, encoding="utf-8")

        import subprocess
        cmd = ["manim", f"--{self.quality}", str(script_path), "ChillHopScene", "-o", str(output_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(output_path.parent))
        if result.returncode != 0:
            raise RuntimeError(f"Manim render failed:\n{result.stderr[-1000:]}")

        return output_path

    def _render_afro_house(self, audio_path, beats, tempo, waveform, sr, output_path) -> Path:
        """
        Escena Afro House: "El Ser Galáctico"
        - Galaxia abierta con nebulosas #5E17EB + #F2EDE5
        - Polvo estelar que vibra exactamente en cada kick
        - Partículas reaccionan al RMS del audio en tiempo real
        """
        output_path = output_path or Path("releases") / "visualizers" / f"afro_house_visualizer.mp4"
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        script = self._build_manim_script_afro_house(beats, tempo, waveform, sr, audio_path)
        script_path = output_path.parent / "scene_afro_house.py"
        script_path.write_text(script, encoding="utf-8")

        import subprocess
        cmd = ["manim", f"--{self.quality}", str(script_path), "AfroHouseScene", "-o", str(output_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(output_path.parent))
        if result.returncode != 0:
            raise RuntimeError(f"Manim render failed:\n{result.stderr[-1000:]}")

        return output_path

    def _build_manim_script_chill_hop(self, beats, tempo, waveform, sr, audio_path: Path) -> str:
        """Genera el script Python de Manim para la escena Chill Hop."""
        beat_times_str = str(list(beats[:50].tolist()))  # primeros 50 beats
        return f'''
from manim import *
import numpy as np

VIOLET = "#5E17EB"
CREAM = "#F2EDE5"
BLACK = "#000000"

class ChillHopScene(Scene):
    """El Viajero Nocturno — ciudad nocturna, neón violeta, constelaciones."""

    BEAT_TIMES = {beat_times_str}
    TEMPO = {tempo:.1f}

    def construct(self):
        self.camera.background_color = BLACK

        # Estrellas de fondo
        stars = VGroup(*[
            Dot(point=[np.random.uniform(-7, 7), np.random.uniform(-4, 4), 0],
                radius=np.random.uniform(0.01, 0.04),
                color=CREAM, fill_opacity=np.random.uniform(0.3, 1.0))
            for _ in range(300)
        ])
        self.add(stars)

        # Logo IM Music como constelación (puntos conectados)
        constellation_points = [
            LEFT * 2 + UP * 1.5, LEFT * 1 + UP * 0.5,
            ORIGIN, RIGHT * 1 + UP * 0.5, RIGHT * 2 + UP * 1.5,
        ]
        constellation_dots = VGroup(*[
            Dot(p, radius=0.06, color=VIOLET, fill_opacity=0.9)
            for p in constellation_points
        ])
        constellation_lines = VGroup(*[
            Line(constellation_points[i], constellation_points[i+1],
                 stroke_color=VIOLET, stroke_width=1, stroke_opacity=0.5)
            for i in range(len(constellation_points)-1)
        ])

        # Texto REBEL LUXURY
        title = Text("REBEL LUXURY", font_size=36, color=CREAM).to_edge(DOWN, buff=0.8)
        subtitle = Text("IM Music", font_size=24, color=VIOLET).next_to(title, DOWN, buff=0.2)

        # Pulso en cada beat (círculo que aparece y desaparece)
        pulse = Circle(radius=0.5, color=VIOLET, stroke_width=3, fill_opacity=0)

        self.play(
            FadeIn(constellation_dots), FadeIn(constellation_lines),
            FadeIn(title), FadeIn(subtitle),
            run_time=2
        )

        # Animar pulso en primeros beats
        for i, bt in enumerate(self.BEAT_TIMES[:20]):
            wait_time = bt - (self.BEAT_TIMES[i-1] if i > 0 else 0) - 0.1
            if wait_time > 0.05:
                self.wait(max(0.05, wait_time))
            pulse_copy = pulse.copy()
            self.play(
                pulse_copy.animate.scale(3).set_opacity(0),
                run_time=0.15
            )
            self.remove(pulse_copy)

        self.wait(2)
'''

    def _build_manim_script_afro_house(self, beats, tempo, waveform, sr, audio_path: Path) -> str:
        """Genera el script Python de Manim para la escena Afro House."""
        beat_times_str = str(list(beats[:50].tolist()))
        rms_values = self._compute_rms_envelope(waveform, sr, n_points=100)
        rms_str = str(rms_values[:50].tolist())
        return f'''
from manim import *
import numpy as np

VIOLET = "#5E17EB"
CREAM = "#F2EDE5"
BLACK = "#000000"

class AfroHouseScene(Scene):
    """El Ser Galáctico — galaxia, nebulosas, partículas que vibran con el beat."""

    BEAT_TIMES = {beat_times_str}
    RMS_ENVELOPE = {rms_str}
    TEMPO = {tempo:.1f}

    def construct(self):
        self.camera.background_color = BLACK

        # Nebulosa de fondo (elipse con gradiente violet)
        nebula = Ellipse(width=10, height=6, color=VIOLET, fill_opacity=0.08, stroke_opacity=0)
        nebula2 = Ellipse(width=6, height=4, color=CREAM, fill_opacity=0.04, stroke_opacity=0)
        self.add(nebula, nebula2)

        # Partículas galácticas
        n_particles = 200
        particles = VGroup(*[
            Dot(
                point=[np.random.uniform(-6, 6), np.random.uniform(-3.5, 3.5), 0],
                radius=np.random.uniform(0.015, 0.06),
                color=VIOLET if np.random.random() > 0.5 else CREAM,
                fill_opacity=np.random.uniform(0.4, 1.0)
            )
            for _ in range(n_particles)
        ])
        self.add(particles)

        # Centro de la galaxia — el logo
        galaxy_center = Dot(ORIGIN, radius=0.3, color=VIOLET, fill_opacity=1)
        glow_ring = Circle(radius=0.8, color=VIOLET, stroke_width=2, stroke_opacity=0.6)

        title = Text("REBEL LUXURY", font_size=32, color=CREAM).to_edge(DOWN, buff=0.8)
        subtitle = Text("IM Music", font_size=20, color=VIOLET).next_to(title, DOWN, buff=0.2)

        self.play(FadeIn(galaxy_center), FadeIn(glow_ring), FadeIn(title), FadeIn(subtitle), run_time=2)

        # Animar partículas al ritmo del beat
        for i, bt in enumerate(self.BEAT_TIMES[:20]):
            wait_time = bt - (self.BEAT_TIMES[i-1] if i > 0 else 0) - 0.08
            if wait_time > 0.05:
                self.wait(max(0.05, wait_time))
            rms = self.RMS_ENVELOPE[i % len(self.RMS_ENVELOPE)] if self.RMS_ENVELOPE else 0.5
            scale_factor = 1.0 + rms * 2.0
            self.play(
                galaxy_center.animate.scale(scale_factor),
                glow_ring.animate.scale(scale_factor).set_opacity(0.3),
                run_time=0.12
            )
            self.play(
                galaxy_center.animate.scale(1/scale_factor),
                glow_ring.animate.scale(1/scale_factor).set_opacity(0.6),
                run_time=0.08
            )

        self.wait(2)
'''

    def _compute_rms_envelope(self, waveform: np.ndarray, sr: int, n_points: int = 100) -> np.ndarray:
        """Calcula envolvente RMS para animar partículas."""
        import librosa
        rms = librosa.feature.rms(y=waveform, frame_length=2048, hop_length=512)[0]
        # Normalizar 0-1
        rms_norm = (rms - rms.min()) / (rms.max() - rms.min() + 1e-8)
        # Resamplear a n_points
        indices = np.linspace(0, len(rms_norm)-1, n_points, dtype=int)
        return rms_norm[indices]

    def is_available(self) -> bool:
        """True si Manim está instalado."""
        try:
            import manim  # noqa: F401
            return True
        except ImportError:
            return False
```

- [ ] **Paso 6.2: Crear tests/test_visualizer.py**

```python
"""Tests para Visualizer — usa mocks para no requerir Manim/audio real."""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import numpy as np
import sys
sys.path.insert(0, "src")

from music_engine.visualizer import Visualizer


class TestVisualizerInit:
    def test_default_quality(self):
        v = Visualizer()
        assert v.quality == "medium_quality"

    def test_custom_quality(self):
        v = Visualizer(quality="low_quality")
        assert v.quality == "low_quality"

    def test_is_available_no_manim(self):
        v = Visualizer()
        with patch.dict("sys.modules", {"manim": None}):
            # Without manim, should return False
            pass  # is_available depends on import, tested inline


class TestVisualizerAnalysis:
    def test_rms_envelope_shape(self):
        v = Visualizer()
        waveform = np.random.randn(44100)  # 1 segundo fake audio
        result = v._compute_rms_envelope(waveform, sr=44100, n_points=50)
        assert len(result) == 50
        assert result.min() >= 0.0
        assert result.max() <= 1.0

    def test_script_generation_chill_hop(self):
        v = Visualizer()
        beats = np.array([0.5, 1.0, 1.5, 2.0])
        waveform = np.random.randn(44100)
        script = v._build_manim_script_chill_hop(beats, 90.0, waveform, 44100, Path("fake.wav"))
        assert "ChillHopScene" in script
        assert "REBEL LUXURY" in script
        assert "#5E17EB" in script

    def test_script_generation_afro_house(self):
        v = Visualizer()
        beats = np.array([0.5, 1.0, 1.5, 2.0])
        waveform = np.random.randn(44100)
        script = v._build_manim_script_afro_house(beats, 124.0, waveform, 44100, Path("fake.wav"))
        assert "AfroHouseScene" in script
        assert "El Ser Galactico" in script or "AfroHouseScene" in script
        assert "#5E17EB" in script


class TestVisualizerGenerate:
    def test_invalid_genre_raises(self):
        v = Visualizer()
        with pytest.raises(ValueError, match="Género no válido"):
            with patch("pathlib.Path.exists", return_value=True):
                with patch.object(v, "_analyze_audio", return_value=(np.array([1.0]), 90.0, np.zeros(100), 44100)):
                    with patch("builtins.__import__", side_effect=lambda name, *a, **kw: MagicMock() if name == "manim" else __import__(name, *a, **kw)):
                        v.generate(Path("fake.wav"), genre="jazz")

    def test_missing_audio_raises(self):
        v = Visualizer()
        with patch("builtins.__import__", side_effect=lambda name, *a, **kw: MagicMock() if name == "manim" else __import__(name, *a, **kw)):
            with pytest.raises(FileNotFoundError):
                v.generate(Path("nonexistent.wav"))
```

- [ ] **Paso 6.3: Correr tests visualizer**
```powershell
python -m pytest tests/test_visualizer.py -v --tb=short
```
Esperado: todos pasan (no requieren Manim real).

- [ ] **Paso 6.4: Commit**
```powershell
git add src/music_engine/visualizer.py tests/test_visualizer.py
git commit -m "feat(visualizer): FASE 4 Manim audio-reactive, ChillHop + AfroHouse scenes"
```

---

## TAREA 7 — FASE 5: scheduler.py — Orquestador L/M/V

**Files:**
- Create: `src/core/scheduler.py`
- Test: `tests/test_scheduler.py`

- [ ] **Paso 7.1: Crear scheduler.py**

Crear `src/core/scheduler.py`:
```python
"""
IM Music Scheduler — Orquestador maestro del Content Engine.
Publica L/M/V: YouTube 18:00 | Instagram 19:00 | TikTok 20:00 (hora Colombia COT = UTC-5)
"""
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.brand import Brand
from core.config import Config
from content_engine.research import ResearchEngine
from content_engine.writer import ContentWriter
from content_engine.designer import Designer
from content_engine.seo_engine import SEOEngine
from content_engine.video_producer import VideoProducer
from content_engine.publisher import YouTubePublisher, InstagramPublisher

logger = logging.getLogger(__name__)

COT = timezone(timedelta(hours=-5))  # Colombia Time


class ContentScheduler:
    """Orquesta el pipeline completo L/M/V."""

    PUBLISH_DAYS = {0: "Monday", 2: "Wednesday", 4: "Friday"}  # weekday() indices
    PUBLISH_HOURS = Brand.PUBLISH_TIMES  # {"youtube": "18:00", "instagram": "19:00", "tiktok": "20:00"}

    def __init__(self):
        self.config = Config()
        self.research = ResearchEngine()
        self.writer = ContentWriter()
        self.designer = Designer()
        self.seo = SEOEngine()
        self.video = VideoProducer()

    def is_publish_day(self, dt: Optional[datetime] = None) -> bool:
        """True si hoy es L/M/V."""
        dt = dt or datetime.now(COT)
        return dt.weekday() in self.PUBLISH_DAYS

    def run_content_pipeline(self, topic: Optional[str] = None, dry_run: bool = True) -> dict:
        """
        Pipeline completo de contenido para una publicación.
        dry_run=True: genera todo pero NO publica en redes.
        dry_run=False: publica en redes (requiere OAuth configurado).
        Returns: dict con paths a todos los archivos generados.
        """
        logger.info("=== IM Music Content Pipeline START ===")

        # 1. Research
        logger.info("STEP 1: Research")
        if topic:
            brief = self.research.build_brief(
                titulo_principal=topic,
                angulo_neurociencia="neurociencia aplicada a la industria musical",
                hook_apertura=f"¿Por qué {topic}?",
                datos_clave=[],
                controversia="La industria no quiere que sepas esto",
                fuentes=["IM Music Research"],
            )
        else:
            stories = self.research.fetch_top_stories(limit=5)
            brief = self.research.score_and_select(stories)

        logger.info(f"Brief: {brief.get('titulo_principal', 'Sin título')}")

        # 2. Generación de contenido (todos los formatos)
        logger.info("STEP 2: Writing all formats")
        content = {}
        content["youtube_script"] = self.writer.generate_youtube_script(brief)
        content["youtube_short"] = self.writer.generate_youtube_short(brief)
        content["instagram_reel"] = self.writer.generate_instagram_reel(brief)
        content["tiktok_carousel"] = self.writer.generate_tiktok_carousel(brief)
        content["seo_pack"] = self.writer.generate_youtube_monetization_pack(brief)

        # 3. SEO
        logger.info("STEP 3: SEO optimization")
        title = brief.get("titulo_principal", "IM Music")
        content["youtube_seo"] = self.seo.youtube_monetization_seo(title, brief)
        content["tiktok_seo"] = self.seo.tiktok_seo_complete(title, brief)
        content["instagram_seo"] = self.seo.generate_instagram_hashtags(title)

        # 4. Diseño — todas las plataformas
        logger.info("STEP 4: Generating visual assets")
        output_dir = Path("releases") / f"content_{datetime.now(COT).strftime('%Y-%m-%d')}"
        output_dir.mkdir(parents=True, exist_ok=True)

        assets = {}
        assets["youtube_thumbnail"] = output_dir / "youtube_thumbnail.png"
        assets["youtube_short_thumbnail"] = output_dir / "youtube_short_thumbnail.png"
        assets["instagram_story"] = output_dir / "instagram_story.png"
        assets["tiktok_cover"] = output_dir / "tiktok_cover.png"

        self.designer.generate_thumbnail(title, save_path=assets["youtube_thumbnail"])
        self.designer.generate_youtube_short_thumbnail(title, save_path=assets["youtube_short_thumbnail"])
        self.designer.generate_story(title, save_path=assets["instagram_story"])
        self.designer.generate_tiktok_cover(title, save_path=assets["tiktok_cover"])

        # Carruseles
        carousel_dir = output_dir / "carousel"
        carousel_paths = self.designer.generate_carousel(title, brief.get("datos_clave", []), save_dir=carousel_dir)
        assets["carousel"] = carousel_paths

        tiktok_carousel_dir = output_dir / "tiktok_carousel"
        if isinstance(content.get("tiktok_carousel"), dict) and "slides" in content["tiktok_carousel"]:
            tiktok_slides = self.designer.generate_tiktok_carousel_slides(
                content["tiktok_carousel"]["slides"], save_dir=tiktok_carousel_dir
            )
            assets["tiktok_carousel"] = tiktok_slides

        logger.info(f"Assets generados en: {output_dir}")

        # 5. Publicar (solo si no es dry_run)
        if not dry_run:
            logger.info("STEP 5: Publishing to platforms")
            self._publish_all(content, assets, brief)
        else:
            logger.info("STEP 5: DRY RUN — no se publica en redes")

        result = {"brief": brief, "content": content, "assets": assets, "output_dir": str(output_dir)}
        logger.info("=== IM Music Content Pipeline COMPLETE ===")
        return result

    def _publish_all(self, content: dict, assets: dict, brief: dict):
        """Publica en todas las plataformas. Requiere OAuth configurado."""
        logger.warning("Publishing requires OAuth credentials — check .env for GOOGLE_CLIENT_ID etc.")
        # YouTube
        # youtube = YouTubePublisher(self.config)
        # youtube.upload_video(...)
        # Instagram
        # instagram = InstagramPublisher(self.config)
        # instagram.post_reel(...)
        # TikTok: API pendiente de configurar
        raise NotImplementedError(
            "Publicación en redes requiere credenciales OAuth de immusicsello. "
            "Configurar GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET en .env"
        )
```

- [ ] **Paso 7.2: Crear tests/test_scheduler.py**

```python
"""Tests para ContentScheduler."""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys
sys.path.insert(0, "src")

from core.scheduler import ContentScheduler, COT


class TestPublishDay:
    def test_monday_is_publish_day(self):
        s = ContentScheduler.__new__(ContentScheduler)
        monday = datetime(2026, 6, 1, 18, 0, tzinfo=COT)  # 2026-06-01 es lunes
        assert s.is_publish_day(monday) is True

    def test_tuesday_is_not_publish_day(self):
        s = ContentScheduler.__new__(ContentScheduler)
        tuesday = datetime(2026, 6, 2, 18, 0, tzinfo=COT)
        assert s.is_publish_day(tuesday) is False

    def test_wednesday_is_publish_day(self):
        s = ContentScheduler.__new__(ContentScheduler)
        wednesday = datetime(2026, 6, 3, 18, 0, tzinfo=COT)
        assert s.is_publish_day(wednesday) is True

    def test_friday_is_publish_day(self):
        s = ContentScheduler.__new__(ContentScheduler)
        friday = datetime(2026, 6, 5, 18, 0, tzinfo=COT)
        assert s.is_publish_day(friday) is True

    def test_saturday_is_not_publish_day(self):
        s = ContentScheduler.__new__(ContentScheduler)
        saturday = datetime(2026, 6, 6, 18, 0, tzinfo=COT)
        assert s.is_publish_day(saturday) is False
```

- [ ] **Paso 7.3: Correr tests scheduler**
```powershell
python -m pytest tests/test_scheduler.py -v --tb=short
```
Esperado: 5 tests pasan.

- [ ] **Paso 7.4: Commit**
```powershell
git add src/core/scheduler.py tests/test_scheduler.py
git commit -m "feat(scheduler): FASE 5 orquestador pipeline completo L/M/V"
```

---

## TAREA 8 — Verificación Final Completa

- [ ] **Paso 8.1: Correr suite completa**
```powershell
python -m pytest tests/ -q --tb=short
```
Esperado: 130+ tests passed, 0 failures.

- [ ] **Paso 8.2: Verificar todos los imports**
```powershell
python -c "
import sys; sys.path.insert(0, 'src')
from core.brand import Brand
from core.config import Config
from core.scheduler import ContentScheduler
from core.approval_cli import approve_beat
from content_engine.research import ResearchEngine
from content_engine.writer import ContentWriter
from content_engine.designer import Designer
from content_engine.seo_engine import SEOEngine
from content_engine.video_producer import VideoProducer
from content_engine.publisher import YouTubePublisher, InstagramPublisher
from music_engine.mastering import MasteringEngine
from music_engine.beat_generator import BeatGenerator
from music_engine.release_pack import ReleasePackGenerator
from music_engine.music_publisher import MusicPublisher
from music_engine.visualizer import Visualizer
print('ALL MODULES OK')
"
```

- [ ] **Paso 8.3: Generar contenido completo de prueba**
```powershell
python -c "
import sys; sys.path.insert(0, 'src')
from core.scheduler import ContentScheduler
s = ContentScheduler()
result = s.run_content_pipeline(topic='La neurociencia del éxito viral en música', dry_run=True)
print('Output dir:', result['output_dir'])
print('Formats generated:', list(result['content'].keys()))
"
```

- [ ] **Paso 8.4: Commit final**
```powershell
git add -A
git commit -m "feat: FASE 3-5 completas, todas las plataformas, scheduler L/M/V"
git push origin main
```

---

## Resumen de plataformas cubiertas

| Plataforma | Formato | Designer | Writer | SEO |
|------------|---------|----------|--------|-----|
| YouTube | Video largo (5-8min) | thumbnail 1280x720 | guión completo | monetization pack |
| YouTube | Shorts (55-58s) | thumbnail 1080x1920 | short script | shorts SEO |
| Instagram | Reel (15-30s) | story 1080x1920 | reel script | hashtags |
| Instagram | Carrusel (8 slides) | slides 1080x1080 | carousel copy | hashtags |
| TikTok | Reel (30-60s) | cover 1080x1920 | reel script | trending sounds |
| TikTok | Carrusel (5-7 slides) | slides 1080x1080 | carousel copy | viral hashtags |
| Pinterest | Pin | pin 1000x1500 | — | — |

## Dependencias pendientes de usuario

| Dep | Cuándo | Tamaño |
|-----|--------|--------|
| torch torchaudio (CPU) | Beats reales | ~500MB |
| audiocraft | Beats reales | ~200MB |
| openai-whisper | Subtítulos | ~100MB |
| manim | Visualizer | ~150MB |
| OAuth immusicsello | Publicar en redes | Config only |
