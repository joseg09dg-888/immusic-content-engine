"""
IM Music — REBEL LUXURY Content Pipeline
Genera y publica en: YouTube Shorts + YouTube Canal + Instagram + TikTok

Uso:
    python scripts/pipeline.py                  # publica en todo
    python scripts/pipeline.py --dry-run        # genera archivos, no publica
    python scripts/pipeline.py --youtube-only
    python scripts/pipeline.py --instagram-only
    python scripts/pipeline.py --tiktok-only
    python scripts/pipeline.py --topic "mi tema"
"""
import sys
import io
import os
import asyncio
import argparse
import logging
import subprocess
import shutil
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("pipeline")


# ── Temas de contenido REBEL LUXURY (no genérico — marca IM Music) ────────────

TOPICS = [
    {
        "titulo_principal": "JAQUEAMOS",
        "sub_texto": "MENTES",
        "angulo_neurociencia": "Como la neurociencia convierte musica en exito",
        "hook_apertura": "No lanzamos musica, ni subimos videos al azar",
        "datos_clave": [
            "El 95% de las decisiones musicales son inconscientes",
            "Un hook de 7 segundos decide si alguien escucha o skippea",
            "La dopamina se activa ANTES del chorus — no durante",
            "El 1% de artistas genera el 77% de todos los streams",
            "Las plataformas favorecen la repeticion compulsiva",
            "Neurociencia aplicada = ventaja injusta en la industria",
        ],
        "controversia": "Las plataformas explotan tu cerebro — nosotros te ensenamos a usarlo",
        "fuentes": ["IM Music Research 2026", "Nature Neuroscience 2024"],
    },
    {
        "titulo_principal": "NEUROCIENCIA",
        "sub_texto": "Y PSICOLOGIA APLICADA AL EXITO REAL",
        "angulo_neurociencia": "Por que tu cerebro repite la misma cancion",
        "hook_apertura": "Por que no puedes dejar de escuchar esa cancion?",
        "datos_clave": [
            "El earworm activa el nucleo caudado igual que la adiccion",
            "BPM entre 120-128 sincroniza con el ritmo cardiaco en ejercicio",
            "El silencio de 0.3s antes del drop genera anticipacion maxima",
            "Melodias descendentes generan nostalgia — ascendentes, euforia",
            "Canciones en tonos mayores generan 40% mas engagement",
            "REBEL LUXURY aplica esto en cada produccion",
        ],
        "controversia": "Las major labels lo saben desde los 90s. Nadie te lo decia.",
        "fuentes": ["IM Music Research 2026", "Journal of Neuroscience 2023"],
    },
    {
        "titulo_principal": "JUEGO",
        "sub_texto": "CAMBIO",
        "angulo_neurociencia": "Estrategia y tecnologia al servicio del artista",
        "hook_apertura": "El",
        "datos_clave": [
            "Distribucion directa = 92% de regalias para el artista",
            "Un Short viral genera 50K streams organicos en 48h",
            "TikTok a YouTube a Spotify — el funnel de 2026",
            "Consistencia 3x semana supera calidad esporadica en algoritmos",
            "IM Music distribuye por Nexus: tu te quedas el 92%",
            "REBEL LUXURY: no es un sello, es un sistema",
        ],
        "controversia": "Los sellos tradicionales toman el 80%. REBEL LUXURY te da el 92%.",
        "fuentes": ["IM Music Research 2026", "Spotify for Artists 2025"],
    },
    {
        "titulo_principal": "SOLO SUENAN",
        "sub_texto": "?",
        "angulo_neurociencia": "La diferencia entre sonar y dominar la industria",
        "hook_apertura": "Como logramos resultados que otros solo suenan?",
        "datos_clave": [
            "El 99% de artistas nunca llegan a 10K oyentes mensuales",
            "La mayoria falla por falta de estrategia, no de talento",
            "Sin presencia digital consistente eres invisible para el algoritmo",
            "Un lanzamiento sin marketing es un gasto, no una inversion",
            "La industria premia la estrategia sobre el talento",
            "REBEL LUXURY = talento + neurociencia + distribucion",
        ],
        "controversia": "El talento no es suficiente. La estrategia lo es todo.",
        "fuentes": ["IM Music Research 2026", "Billboard Analytics 2025"],
    },
    {
        "titulo_principal": "DEL EXITO.",
        "sub_texto": "NO TE QUEDES FUERA.",
        "angulo_neurociencia": "El mapa que la industria no quiere que veas",
        "hook_apertura": "Estamos a punto de revelar el mapa.",
        "datos_clave": [
            "Identidad de marca — sin esto nada funciona",
            "Contenido consistente — el algoritmo necesita rutina",
            "Distribucion inteligente — Nexus + plataformas propias",
            "Monetizacion — YouTube + regalias + sync licensing",
            "Escala — reinvierte el 20% en paid media",
            "IM Music te acompana en cada paso",
        ],
        "controversia": "No te quedes fuera del sistema que ya funciona.",
        "fuentes": ["IM Music Research 2026", "Forbes Music 2025"],
    },
    {
        "titulo_principal": "REBEL LUXURY",
        "sub_texto": "NO ES UN LOOK. ES UN SISTEMA.",
        "angulo_neurociencia": "El modelo de negocio que redefine la industria musical",
        "hook_apertura": "No es un estilo. Es una filosofia.",
        "datos_clave": [
            "92% de regalias directo al artista via Nexus",
            "Neurociencia aplicada a cada decision de lanzamiento",
            "IA + estrategia + distribucion = ventaja competitiva",
            "Medellín liderando la innovacion musical en Latinoamerica",
            "Artistas IM Music crecen 3x mas rapido que el promedio",
            "El sello que pone al artista primero — siempre",
        ],
        "controversia": "Los sellos tradicionales venden suenos. IM Music vende estrategia.",
        "fuentes": ["IM Music Research 2026", "Musically 2025"],
    },
]


# ── TTS Narracion ─────────────────────────────────────────────────────────────

_SPANISH_VOICE_ID = (
    r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"
)

# Voz neural de Edge (gratis, sin API key) — español Colombia, alineada con el
# brand voice "Medellin -> Mundo" (referencia Feid). Mucho mas natural que el
# SAPI Sabina (pausas extranas, tono robotico).
_EDGE_VOICE = "es-CO-GonzaloNeural"
_EDGE_RATE = "+8%"


def create_narration(text: str, output_path: Path) -> bool:
    """
    TTS natural con Edge Neural (es-CO-GonzaloNeural, gratis, requiere internet).
    Fallback a Microsoft Sabina (pyttsx3, offline) y luego gTTS si Edge falla.
    """
    # Intento 1: Edge TTS neural — voz natural, requiere internet
    try:
        async def _gen():
            communicate = edge_tts.Communicate(text, _EDGE_VOICE, rate=_EDGE_RATE)
            await communicate.save(str(output_path))

        import edge_tts
        asyncio.run(_gen())
        if output_path.exists() and output_path.stat().st_size > 1000:
            log.info("TTS Edge (%s) OK: %s", _EDGE_VOICE, output_path.name)
            return True
    except Exception as e:
        log.warning("Edge TTS fallido: %s — intentando Sabina", e)

    # Intento 2: pyttsx3 con voz nativa Windows (Sabina — español México)
    try:
        import pyttsx3
        import tempfile, os
        engine = pyttsx3.init()
        engine.setProperty("voice", _SPANISH_VOICE_ID)
        engine.setProperty("rate", 155)    # palabras/min — natural, no robotico
        engine.setProperty("volume", 0.95)

        # Guardar como WAV primero, luego convertir a MP3 con FFmpeg
        wav_path = output_path.with_suffix(".wav")
        engine.save_to_file(text, str(wav_path))
        engine.runAndWait()
        engine.stop()

        if wav_path.exists() and wav_path.stat().st_size > 1000:
            # Convertir WAV → MP3 con FFmpeg (mejor calidad + compresión)
            cmd = ["ffmpeg", "-y", "-i", str(wav_path),
                   "-codec:a", "libmp3lame", "-qscale:a", "2", str(output_path)]
            result = subprocess.run(cmd, capture_output=True)
            wav_path.unlink(missing_ok=True)
            if result.returncode == 0 and output_path.exists():
                log.info("TTS Sabina OK: %s", output_path.name)
                return True
    except Exception as e:
        log.warning("pyttsx3 fallido: %s — intentando gTTS", e)

    # Intento 3: gTTS
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang="es", slow=False)
        tts.save(str(output_path))
        log.info("TTS gTTS OK: %s", output_path.name)
        return True
    except Exception as e:
        log.warning("gTTS fallido: %s", e)
        return False


# ── FFmpeg helpers ────────────────────────────────────────────────────────────

def _run_ffmpeg(cmd: list, label: str) -> bool:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        log.error("FFmpeg %s error:\n%s", label, result.stderr[-800:])
        return False
    return True


# ── Captions virales (Whisper + ASS) ─────────────────────────────────────────
# Subtitulos animados quemados sobre el video — el elemento visual que mas
# impacta retencion en Shorts/Reels/TikTok (la mayoria ve sin sonido).
# Usa solo herramientas gratuitas ya instaladas: openai-whisper + libass (FFmpeg).

_FONTS_DIR = ROOT / "assets" / "fonts"
_WHISPER_MODEL_SIZE = "base"


def _transcribe_words(audio_path: Path) -> list:
    """Transcribe audio con Whisper, retorna lista plana de palabras con timestamps."""
    import whisper
    model = whisper.load_model(_WHISPER_MODEL_SIZE)
    result = model.transcribe(str(audio_path), language="es", word_timestamps=True)
    words = []
    for seg in result.get("segments", []):
        for w in seg.get("words", []):
            text = w["word"].strip()
            if text:
                words.append({"word": text, "start": w["start"], "end": w["end"]})
    return words


def _ass_time(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def _build_caption_ass(words: list, out_ass: Path, width: int, height: int, chunk_size: int = 3) -> bool:
    """
    Genera subtitulos .ass estilo 'viral captions': palabras grandes en
    mayusculas, blancas con contorno negro, fade rapido por frase corta.
    """
    if not words:
        return False

    fontsize = max(28, width // 16)
    margin_v = int(height * 0.20)  # arriba del CTA fijo del diseno (~88% alto)
    margin_lr = int(width * 0.04)
    box_pad = max(8, fontsize // 6)

    header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        f"PlayResX: {width}\n"
        f"PlayResY: {height}\n"
        "ScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
        "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
        "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        # BorderStyle 3 = caja opaca (BackColour) detras del texto: legible siempre,
        # incluso cuando el Ken Burns recorta un slide y el headline queda detras.
        f"Style: Caption,Anton,{fontsize},&H00FFFFFF,&H000000FF,&H00000000,&H00000000,"
        f"1,0,0,0,100,100,0,0,3,{box_pad},0,2,{margin_lr},{margin_lr},{margin_v},1\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )

    lines = []
    for i in range(0, len(words), chunk_size):
        chunk = words[i:i + chunk_size]
        start, end = chunk[0]["start"], chunk[-1]["end"]
        text = " ".join(w["word"] for w in chunk).upper()
        lines.append(
            f"Dialogue: 0,{_ass_time(start)},{_ass_time(end)},Caption,,0,0,0,,{{\\fad(60,60)}}{text}"
        )

    out_ass.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
    return True


def _ff_path(p: Path) -> str:
    """Path relativo al cwd (sin ':' de unidad de Windows) para usarlo como
    valor de opcion dentro de un filtro FFmpeg (ass/subtitles) — el ':' de
    'C:/...' rompe el parser de opciones del filtro incluso escapado."""
    rel = Path(os.path.relpath(p, Path.cwd()))
    return str(rel).replace("\\", "/")


def prepare_captions(audio_path: Optional[Path], width: int, height: int) -> Optional[Path]:
    """
    Transcribe la narracion con Whisper y genera un archivo .ass de subtitulos
    junto al audio. Returns la ruta del .ass, o None si Whisper no esta
    disponible o la transcripcion falla (el video se genera sin subtitulos).
    """
    if not audio_path or not audio_path.exists():
        return None
    try:
        import whisper  # noqa: F401
    except ImportError:
        log.info("Whisper no instalado — videos sin subtitulos")
        return None

    try:
        words = _transcribe_words(audio_path)
        if not words:
            return None
        ass_path = audio_path.with_suffix(".ass")
        if _build_caption_ass(words, ass_path, width, height):
            return ass_path
    except Exception as e:
        log.warning("Transcripcion de subtitulos fallida: %s — video sin subtitulos", e)
    return None


def _create_kenburns_video(
    slides: list, audio: Path, out: Path,
    width: int, height: int, secs: float, label: str, fps: int = 25,
    captions_ass: Optional[Path] = None,
) -> bool:
    """
    Concatena slides con efecto Ken Burns (zoom in/out alternado por slide,
    centrado) + transiciones crossfade entre cada uno. Reemplaza los cortes
    secos sobre imagenes estaticas por movimiento continuo — usa solo
    filtros nativos de FFmpeg (zoompan + xfade), sin dependencias nuevas.
    Si se pasa `captions_ass`, quema subtitulos en el mismo paso (sin re-encode extra).
    """
    n = len(slides)
    xfade_dur = min(1.0, secs / 4)
    total_dur = n * secs - (n - 1) * xfade_dur if n > 1 else secs
    d_frames = max(1, int(secs * fps))
    z_max = 1.15
    step = (z_max - 1.0) / max(1, d_frames - 1)

    cmd = ["ffmpeg", "-y"]
    for p in slides:
        cmd += ["-loop", "1", "-framerate", str(fps), "-t", str(secs), "-i", str(p)]

    parts = []
    for i in range(n):
        # Alterna zoom-in / zoom-out por slide para variar el movimiento
        if i % 2 == 0:
            zexpr = f"min(1+on*{step:.8f},{z_max})"
        else:
            zexpr = f"max({z_max}-on*{step:.8f},1)"
        parts.append(
            f"[{i}:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},setsar=1,"
            f"zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d=1:s={width}x{height}:fps={fps}[v{i}]"
        )

    if n == 1:
        vout = "v0"
    else:
        for k in range(1, n):
            offset = max(0.0, k * (secs - xfade_dur) - 0.02)
            src = "v0" if k == 1 else f"x{k-1}"
            parts.append(
                f"[{src}][v{k}]xfade=transition=fade:duration={xfade_dur}:"
                f"offset={offset:.3f}[x{k}]"
            )
        vout = f"x{n-1}"

    if captions_ass and captions_ass.exists():
        parts.append(
            f"[{vout}]ass={_ff_path(captions_ass)}:fontsdir={_ff_path(_FONTS_DIR)}[vcap]"
        )
        vout = "vcap"

    filter_complex = ";".join(parts)

    if audio and audio.exists():
        cmd += ["-i", str(audio)]
        filter_complex += f";[{n}:a]atrim=0:{total_dur},asetpts=PTS-STARTPTS[ao]"
        cmd += ["-filter_complex", filter_complex,
                "-map", f"[{vout}]", "-map", "[ao]"]
    else:
        cmd += ["-filter_complex", filter_complex, "-map", f"[{vout}]"]

    cmd += ["-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(total_dur),
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    out.parent.mkdir(parents=True, exist_ok=True)
    return _run_ffmpeg(cmd, label)


def create_short(slides: list, audio: Path, out: Path, secs: float = 5.0,
                  captions_ass: Optional[Path] = None) -> bool:
    """Vertical 1080x1920 — YouTube Shorts + TikTok. Ken Burns + crossfade + subtitulos."""
    return _create_kenburns_video(slides, audio, out, 1080, 1920, secs, "Short", captions_ass=captions_ass)


def create_long_video(slides: list, audio: Path, out: Path, secs: float = 10.0,
                       captions_ass: Optional[Path] = None) -> bool:
    """Full HD 1920x1080 — YouTube canal, watch hours. Ken Burns + crossfade + subtitulos."""
    return _create_kenburns_video(slides, audio, out, 1920, 1080, secs, "Canal-1080p", captions_ass=captions_ass)


# ── Publishers ────────────────────────────────────────────────────────────────

def _make_pkg(brief: dict):
    from src.content_engine.writer import PublicationPackage
    titulo = brief["titulo_principal"]
    angulo = brief["angulo_neurociencia"]
    datos = brief.get("datos_clave", [])
    fuentes = brief.get("fuentes", [])

    caption_base = (
        f"{titulo}\n\n"
        + "\n".join(f"• {d}" for d in datos[:5])
        + "\n\n"
        "No lanzamos musica. Jaqueamos mentes.\n\n"
        "#IMMusic #RebelLuxury #NeurocienciaMusical #IndustriaMusical "
        "#Colombia #MusicBusiness #Sello"
    )

    yt_desc = (
        f"IM Music — REBEL LUXURY\n{angulo}\n\n"
        + "\n".join(f"• {d}" for d in datos)
        + f"\n\nFuentes: {', '.join(fuentes)}\n\n"
        "Siguenos: @immusicsello\n"
        "Contacto: immusicsello@gmail.com\n\n"
        "#IMMusic #RebelLuxury #NeurocienciaMusical #IndustriaMusical "
        "#Colombia #MusicBusiness #Shorts"
    )

    return PublicationPackage(
        brief=brief,
        script_es=f"IM Music. {angulo}. REBEL LUXURY.",
        captions_instagram=caption_base,
        caption_tiktok=f"{titulo} - {angulo} #IMMusic #RebelLuxury",
        youtube_titles=[
            f"{titulo}: {angulo} | IM Music",
            f"REBEL LUXURY — {angulo} | IM Music Sello",
            f"IM Music: {titulo} | Neurociencia Musical Colombia",
        ],
        youtube_description=yt_desc,
    )


def publish_youtube(video_path: Path, brief: dict, thumb_path: Path = None,
                    is_short: bool = False) -> str | None:
    try:
        from src.content_engine.publisher import YouTubePublisher
        pkg = _make_pkg(brief)
        yt = YouTubePublisher()
        video_id = yt.upload_video(video_path, pkg, thumb_path, is_short=is_short)
        if video_id:
            url = f"https://youtu.be/{video_id}"
            log.info("YouTube OK: %s", url)
            print(f"     YouTube: {url}")
            return video_id
    except Exception as e:
        log.error("YouTube FAIL: %s", e)
    return None


def publish_instagram(image_path: Path, brief: dict) -> str | None:
    try:
        from src.core.config import config
        if not config.INSTAGRAM_PASSWORD:
            log.warning("INSTAGRAM_PASSWORD no configurado")
            return None
        from instagrapi import Client
        session_file = ROOT / ".instagram_session.json"
        cl = Client()
        if session_file.exists():
            cl.load_settings(session_file)
        cl.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD)
        cl.dump_settings(session_file)
        pkg = _make_pkg(brief)
        media = cl.photo_upload(str(image_path), pkg.captions_instagram[:2200])
        url = f"https://www.instagram.com/p/{media.code}/"
        log.info("Instagram OK: %s", url)
        print(f"     Instagram: {url}")
        return str(media.pk)
    except Exception as e:
        log.error("Instagram FAIL: %s", e)
        return None


def publish_instagram_carousel(slide_paths: list, brief: dict) -> str | None:
    """Carousel de hasta 10 slides en Instagram."""
    try:
        from src.core.config import config
        if not config.INSTAGRAM_PASSWORD:
            return None
        from instagrapi import Client
        session_file = ROOT / ".instagram_session.json"
        cl = Client()
        if session_file.exists():
            cl.load_settings(session_file)
        cl.login(config.INSTAGRAM_USERNAME, config.INSTAGRAM_PASSWORD)
        cl.dump_settings(session_file)
        pkg = _make_pkg(brief)
        # instagrapi: album_upload para carousel
        paths = [Path(p) for p in slide_paths[:10]]
        media = cl.album_upload(paths, pkg.captions_instagram[:2200])
        url = f"https://www.instagram.com/p/{media.code}/"
        log.info("Instagram carousel OK: %s", url)
        print(f"     Instagram carousel: {url}")
        return str(media.pk)
    except Exception as e:
        log.error("Instagram carousel FAIL: %s", e)
        return None


def publish_tiktok(video_path: Path, brief: dict) -> bool:
    """Sube a TikTok via tiktok-uploader (requiere .tiktok_cookies.json)."""
    cookies_file = ROOT / ".tiktok_cookies.json"
    if not cookies_file.exists():
        log.warning("TikTok cookies no encontradas — salta TikTok")
        log.warning("Para configurar: python scripts/get_tiktok_cookies.py")
        return False
    try:
        from tiktok_uploader.upload import upload_video
        pkg = _make_pkg(brief)
        title = pkg.caption_tiktok[:150]
        result = upload_video(
            str(video_path),
            description=title,
            cookies=str(cookies_file),
        )
        log.info("TikTok OK: %s", result)
        print(f"     TikTok: subido")
        return True
    except ImportError:
        log.warning("tiktok-uploader no instalado — pip install tiktok-uploader")
        return False
    except Exception as e:
        log.error("TikTok FAIL: %s", e)
        return False


# ── Pipeline principal ────────────────────────────────────────────────────────

def run(args):
    now = datetime.now()
    ts = now.strftime("%Y%m%d_%H%M%S")
    work_dir = ROOT / "releases" / f"run_{ts}"
    work_dir.mkdir(parents=True, exist_ok=True)

    # Seleccionar tema
    import random
    if args.topic:
        brief = {**TOPICS[0],
                 "titulo_principal": args.topic.upper(),
                 "hook_apertura": args.topic,
                 "angulo_neurociencia": "Neurociencia al servicio del artista"}
    else:
        brief = random.choice(TOPICS)

    titulo = brief["titulo_principal"]
    sub_texto = brief.get("sub_texto", "")
    hook = brief["hook_apertura"]
    angulo = brief["angulo_neurociencia"]
    datos = brief["datos_clave"]

    # Guardar brief para aprobar_publicar.py
    import json as _json
    (work_dir / "brief.json").write_text(_json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  IM MUSIC — REBEL LUXURY PIPELINE")
    print(f"  {ts}")
    print(f"  Tema: {titulo}")
    print(f"{'='*60}")

    # ── PASO 1: Imagenes ──────────────────────────────────────────
    print("\n[1/5] Generando imagenes REBEL LUXURY...")
    from src.content_engine.designer import Designer
    d = Designer()
    seed = int(ts[-6:]) % 1000

    carousel_dir = work_dir / "carousel"
    slides_data = [{"hook": hook, "headline": titulo, "cta": "DESLIZA →"}]
    for i, dato in enumerate(datos):
        words = dato.split()
        hl = " ".join(words[:4]).upper() if len(words) > 4 else dato.upper()
        slides_data.append({"hook": dato, "headline": hl, "cta": f"{i+2}/{len(datos)+2}"})
    slides_data.append({
        "hook": "SIGUENOS PARA MAS CONTENIDO",
        "headline": "IM MUSIC",
        "cta": "@IMMUSICSELLO",
    })

    carousel_paths = d.generate_carousel(slides_data, carousel_dir, seed=seed)
    post_path = work_dir / "post.png"
    thumb_path = work_dir / "thumbnail.png"
    story_path = work_dir / "story.png"

    d.generate_post(hook, titulo, "DESCUBRE COMO EN NUESTRO CANAL", sub_texto, post_path, seed=seed)
    d.generate_thumbnail(hook, titulo, angulo[:50], thumb_path, seed=seed)
    d.generate_story(hook, titulo, "DESCUBRE COMO EN NUESTRO CANAL", story_path, seed=seed)
    print(f"     Post, thumbnail, story y {len(carousel_paths)} slides generados")

    # ── PASO 2: TTS — dos versiones: short (45s) y canal (narración larga) ──────
    print("\n[2/5] Generando narracion...")

    # Narración corta para Short (45s max)
    narration_short = (
        f"{hook}. "
        f"{datos[0]}. {datos[1]}. {datos[2]}. "
        "Siguenos en IM Music para mas estrategias REBEL LUXURY."
    )
    audio_short_path = work_dir / "narration_short.mp3"
    has_short_audio = create_narration(narration_short, audio_short_path)

    # Narración larga para canal (8-10 minutos)
    narration_canal = f"""
Bienvenidos a IM Music, el sello discografico REBEL LUXURY.
Hoy vamos a hablar sobre algo que cambiara completamente tu vision de la industria musical.

{titulo}. {angulo}.

{hook}.

Primero, entendamos el panorama actual.
{datos[0]}.
Esto es fundamental para entender por que la mayoria de artistas nunca llegan a donde quieren.

{datos[1]}.
Cuando comprendes esto, todo cambia. La estrategia que usas, el contenido que creas, la forma en que te posicionas.

{datos[2]}.
En IM Music aplicamos estos principios en cada produccion, en cada lanzamiento, en cada pieza de contenido.

{datos[3] if len(datos) > 3 else ''}
La diferencia entre los artistas que dominan y los que desaparecen no es el talento. Es el sistema.

{datos[4] if len(datos) > 4 else ''}
Y ese sistema es exactamente lo que construimos en IM Music con la filosofia REBEL LUXURY.

{datos[5] if len(datos) > 5 else ''}
No lanzamos musica al azar. Cada decision tiene una razon neurologica, psicologica y estrategica.

Ahora, la pregunta es: como aplicas esto en tu carrera?

Paso uno. Define tu identidad de marca. Sin esto, ningun algoritmo te va a ayudar.
Paso dos. Crea contenido consistente. El algoritmo necesita rutina para entenderte y promoverte.
Paso tres. Distribuye de forma inteligente. Usa plataformas que te den el maximo de regalias.
Paso cuatro. Monetiza desde el principio. YouTube, regalias, sync licensing, todo cuenta.
Paso cinco. Reinvierte el veinte por ciento en amplificacion. Paid media, colaboraciones, PR.

En IM Music distribuimos por Nexus, donde tu te quedas el noventa y dos por ciento de las regalias.
Porque creemos que el artista es el dueno de su musica.

Eso es REBEL LUXURY. No es un estilo. Es una filosofia.
Una forma de ver la industria que pone al artista primero.

Si quieres ser parte de este movimiento, siguenos como arroba immusicsello en todas las plataformas.
Activar la campanita para no perderte ningun contenido.
Y comparte este video con ese artista que necesita escuchar esto.

Hasta la proxima. IM Music. REBEL LUXURY. Jaqueamos mentes.
"""
    audio_canal_path = work_dir / "narration_canal.mp3"
    has_canal_audio = create_narration(narration_canal.strip(), audio_canal_path)

    audio_short = audio_short_path if has_short_audio else None
    audio_canal = audio_canal_path if has_canal_audio else None
    print(f"     Audio short: {'OK' if has_short_audio else 'sin audio'}")
    print(f"     Audio canal: {'OK' if has_canal_audio else 'sin audio'}")

    # ── PASO 3: Videos ────────────────────────────────────────────
    print("\n[3/5] Creando videos...")

    # Short vertical (YouTube Shorts + TikTok — 40-55 segundos)
    short_path = work_dir / "short.mp4"
    captions_short = prepare_captions(audio_short, 1080, 1920)
    ok_short = create_short(carousel_paths[:8], audio_short, short_path, secs=5.5, captions_ass=captions_short)
    if ok_short:
        subs = " + subtitulos" if captions_short else ""
        print(f"     Short: {short_path.stat().st_size//1024}KB (~44s){subs}")
    if captions_short:
        captions_short.unlink(missing_ok=True)

    # Video largo — canal YouTube (8+ minutos para watch hours)
    # Generar slides adicionales para llenar el tiempo
    from src.content_engine.designer import Designer as _D
    _d2 = _D()
    canal_dir = work_dir / "canal_slides"
    canal_slides_data = []
    # Intro
    canal_slides_data.append({"hook": "IM MUSIC PRESENTA", "headline": titulo, "cta": "REBEL LUXURY"})
    # Datos expandidos (cada dato es un slide de 30s)
    for i, dato in enumerate(datos):
        words = dato.split()
        hl = " ".join(words[:4]).upper() if len(words) > 4 else dato.upper()
        canal_slides_data.append({"hook": dato, "headline": hl, "cta": f"DATO {i+1}/{len(datos)}"})
    # Pasos del proceso
    pasos = [
        ("PASO 1", "DEFINE TU MARCA"),
        ("PASO 2", "CONTENIDO CONSTANTE"),
        ("PASO 3", "DISTRIBUCION"),
        ("PASO 4", "MONETIZACION"),
        ("PASO 5", "ESCALA"),
    ]
    for sub, hl in pasos:
        canal_slides_data.append({"hook": sub, "headline": hl, "cta": "REBEL LUXURY"})
    # Outro
    canal_slides_data.append({
        "hook": "SIGUENOS PARA MAS ESTRATEGIAS",
        "headline": "IM MUSIC",
        "cta": "@IMMUSICSELLO",
    })

    canal_slide_paths = _d2.generate_carousel(canal_slides_data, canal_dir, seed=seed + 100)

    long_path = work_dir / "video_canal.mp4"
    # ~32 slides × 18 segundos ≈ 8+ minutos para watch hours
    secs_per_slide = max(18.0, 520.0 / max(len(canal_slide_paths), 1))
    captions_canal = prepare_captions(audio_canal, 1920, 1080)
    ok_long = create_long_video(canal_slide_paths, audio_canal, long_path, secs=secs_per_slide, captions_ass=captions_canal)
    if ok_long:
        total_secs = len(canal_slide_paths) * secs_per_slide
        subs = " + subtitulos" if captions_canal else ""
        print(f"     Canal: {long_path.stat().st_size//1024//1024}MB (~{total_secs/60:.1f}min){subs}")
    if captions_canal:
        captions_canal.unlink(missing_ok=True)

    # ── PASO 3.5: Beat del dia (Chill Hop / Afro House) ─────────────────────
    print("\n[3.5/5] Generando beat...")
    from src.music_engine.beat_generator import BeatGenerator
    beat_genre = "afro_house" if now.weekday() in (2, 3, 5) else "chill_hop"
    bg = BeatGenerator()
    if beat_genre == "afro_house":
        beat_path = bg.generate_afro_house(output_path=work_dir / "beat_afro_house.wav", seed=seed)
    else:
        beat_path = bg.generate_chill_hop(output_path=work_dir / "beat_chill_hop.wav", seed=seed)

    if args.dry_run:
        print(f"\n  DRY RUN — todo generado en: {work_dir}")
        print("  Para publicar quita --dry-run")
        return work_dir

    # ── PASO 4: Publicar ──────────────────────────────────────────
    print("\n[4/5] Publicando...")
    results = {}

    if not args.instagram_only and not args.tiktok_only:
        print("  YouTube Shorts:")
        if ok_short:
            vid = publish_youtube(short_path, brief, thumb_path, is_short=True)
            results["yt_short"] = vid
        print("  YouTube Canal:")
        if ok_long:
            vid = publish_youtube(long_path, brief, thumb_path, is_short=False)
            results["yt_long"] = vid

    if not args.youtube_only and not args.tiktok_only:
        # Solo carrusel en Instagram — más engagement que post individual
        print("  Instagram (carrusel 8 slides):")
        mid = publish_instagram_carousel(carousel_paths, brief)
        results["ig_post"] = mid
        results["ig_carousel"] = mid

    if not args.youtube_only and not args.instagram_only:
        print("  TikTok:")
        ok = publish_tiktok(short_path if ok_short else story_path, brief)
        results["tiktok"] = ok

    # ── PASO 5: Resumen ───────────────────────────────────────────
    print(f"\n[5/5] Resumen:")
    print(f"  YouTube Short:   {'OK' if results.get('yt_short') else 'SKIP/FAIL'}")
    print(f"  YouTube Canal:   {'OK' if results.get('yt_long') else 'SKIP/FAIL'}")
    print(f"  Instagram Post:  {'OK' if results.get('ig_post') else 'SKIP/FAIL'}")
    print(f"  Instagram Carr.: {'OK' if results.get('ig_carousel') else 'SKIP/FAIL'}")
    print(f"  TikTok:          {'OK' if results.get('tiktok') else 'SKIP/FAIL'}")
    print(f"\n  Archivos: {work_dir}")
    print(f"{'='*60}\n")
    return work_dir


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--topic", default="")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--youtube-only", action="store_true")
    p.add_argument("--instagram-only", action="store_true")
    p.add_argument("--tiktok-only", action="store_true")
    args = p.parse_args()
    run(args)


if __name__ == "__main__":
    main()
