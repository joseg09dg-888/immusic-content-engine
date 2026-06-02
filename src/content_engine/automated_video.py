"""
IM Music Automated Video Producer — REBEL LUXURY
Crea videos completos SIN intervención humana:
  - Voz en español (gTTS / ElevenLabs)
  - Texto en pantalla con animación
  - Imágenes de marca (grabados vintage + violeta)
  - Transiciones entre clips
  - Música de fondo (cuando haya beats)

Formatos:
  - Reel Instagram: 9:16, 15-45s
  - TikTok: 9:16, 21-90s
  - YouTube Short: 9:16, max 58s

Uso:
    producer = AutomatedVideoProducer()
    producer.create_reel(brief, "outputs/reel.mp4")
    producer.create_tiktok(brief, "outputs/tiktok.mp4")
    producer.create_youtube_short(brief, "outputs/short.mp4")
"""
import logging
import subprocess
import shutil
import tempfile
from pathlib import Path
from typing import Optional, List
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps

logger = logging.getLogger(__name__)

_ASSETS  = Path(__file__).resolve().parent.parent.parent / "assets"
_OUTPUTS = Path(__file__).resolve().parent.parent.parent / "outputs"

VIOLET = (94, 23, 235)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)

# Rebel Brain Method — 5 momentos con voz y texto
# Cada escena = slide visual + narración + texto en pantalla

def _font(size: int) -> ImageFont.FreeTypeFont:
    for name in ["Anton-Regular.ttf", "impact.ttf"]:
        for base in [_ASSETS / "fonts", Path(r"C:\Windows\Fonts")]:
            p = base / name
            if p.exists():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default(size=size)


def _pick_engraving(idx: int) -> Optional[Path]:
    from src.content_engine.designer import _pick_engraving as _pick
    return _pick(seed=idx * 17 + 5)


def _make_slide_image(
    headline: str,
    context: str = "",
    subtitle: str = "",
    size: tuple = (1080, 1920),
    engraving_idx: int = 0,
) -> Image.Image:
    """Genera un frame de fondo con grabado + texto para el video."""
    w, h = size

    # Fondo violeta + grabado
    img = Image.new("RGB", size, VIOLET)
    eng_path = _pick_engraving(engraving_idx)
    if eng_path and eng_path.exists():
        try:
            eng = Image.open(eng_path).convert("L")
            ew, eh = eng.size
            scale  = max(h * 0.85 / eh, w / ew)
            eng    = eng.resize((int(ew * scale), int(eh * scale)), Image.LANCZOS)
            eng    = ImageEnhance.Contrast(eng).enhance(1.8)
            inv    = ImageOps.invert(eng)
            rgba   = Image.new("RGBA", eng.size, (0, 0, 0, 255))
            rgba.putalpha(inv)
            img    = img.convert("RGBA")
            img.paste(rgba, ((w - eng.width) // 2, 0), rgba)
            img    = img.convert("RGB")
        except Exception:
            pass

    draw = ImageDraw.Draw(img)

    # Context (pequeño, 48% vertical)
    if context:
        ctx_f = _font(max(28, w // 36))
        bx    = draw.textbbox((0, 0), context.upper(), font=ctx_f)
        draw.text(((w - (bx[2]-bx[0])) // 2, int(h * 0.46)), context.upper(), font=ctx_f, fill=WHITE)

    # HEADLINE MASIVO (53% vertical)
    if headline:
        head_sz = max(80, w // 8)
        for _ in range(6):
            head_f = _font(head_sz)
            lines  = _wrap(draw, headline.upper(), head_f, int(w * 0.90))
            lh     = int(head_sz * 0.96)
            total  = lh * len(lines)
            if total <= int(h * 0.22):
                break
            head_sz = int(head_sz * 0.88)

        y = int(h * 0.52)
        for ln in lines:
            bx = draw.textbbox((0, 0), ln, font=head_f)
            x  = (w - (bx[2]-bx[0])) // 2
            draw.text((x+3, y+3), ln, font=head_f, fill=BLACK)
            draw.text((x,   y),   ln, font=head_f, fill=WHITE)
            y += lh

    # Subtitle
    if subtitle:
        sub_f = _font(max(26, w // 38))
        bx    = draw.textbbox((0, 0), subtitle.upper(), font=sub_f)
        y_sub = int(h * 0.77)
        draw.text(((w - (bx[2]-bx[0])) // 2, y_sub), subtitle.upper(), font=sub_f, fill=WHITE)

    return img


def _wrap(draw, text: str, font, max_w: int) -> List[str]:
    words, lines, line = text.split(), [], ""
    for w in words:
        test = (line + " " + w).strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= max_w:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def _synthesize_voice(text: str, output_mp3: Path, lang: str = "es") -> bool:
    """Genera audio con gTTS (Google TTS). Retorna True si OK."""
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(str(output_mp3))
        return True
    except Exception as e:
        logger.warning(f"gTTS failed: {e}")
        return False


def _image_to_video(img: Image.Image, duration: float, output: Path, size: tuple, fps: int = 30) -> Path:
    """Convierte una imagen en un clip de video de duración fija."""
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp_img = output.parent / f"_tmp_{output.stem}.png"
    img.save(tmp_img)

    # Fade in/out
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duration), "-i", str(tmp_img),
        "-vf", f"scale={size[0]}:{size[1]},setsar=1,fps={fps},fade=t=in:st=0:d=0.3,fade=t=out:st={max(0,duration-0.3)}:d=0.3",
        "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p",
        str(output)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    tmp_img.unlink(missing_ok=True)
    if r.returncode != 0:
        raise RuntimeError(f"image_to_video failed: {r.stderr[-200:]}")
    return output


def _combine_video_audio(video: Path, audio: Path, output: Path) -> Path:
    """Combina video + audio, ajusta duración al video."""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video), "-i", str(audio),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"combine_video_audio failed: {r.stderr[-200:]}")
    return output


def _concat_videos(video_paths: List[Path], output: Path) -> Path:
    """Concatena múltiples clips en uno solo."""
    list_file = output.parent / "_concat_list.txt"
    list_file.write_text("\n".join(f"file '{p.resolve()}'" for p in video_paths))
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p",
        str(output)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    list_file.unlink(missing_ok=True)
    if r.returncode != 0:
        raise RuntimeError(f"concat_videos failed: {r.stderr[-200:]}")
    return output


class AutomatedVideoProducer:
    """
    Produce videos automatizados completos para IM Music.
    Sin intervención humana: investigación → guión → voz → video → listo.
    """

    def _build_scenes(self, brief: dict) -> List[dict]:
        """
        Construye las escenas del Rebel Brain Method desde el brief.
        Cada escena = headline + narración + duración.
        """
        titulo   = brief.get("titulo_principal", "")
        datos    = brief.get("datos_clave", [""])
        fuente   = brief.get("fuentes", [{}])[0].get("source", "fuente verificada")
        tema     = brief.get("tema_categoria", "")

        dato = datos[0][:200] if datos else ""

        return [
            # Escena 1 — PATTERN INTERRUPT (0-5s)
            {
                "headline":  "SPOTIFY NO PAGA",
                "context":   "Lo que nadie te dice.",
                "subtitle":  "por streams.",
                "narration": "Spotify no paga por streams. Paga por familiaridad. Y eso lo cambia todo.",
                "duration":  5.0,
                "engraving": 0,
            },
            # Escena 2 — TENSION BUILDER (5-14s)
            {
                "headline":  "LA INDUSTRIA",
                "context":   f"Fuente: {fuente}",
                "subtitle":  "lo sabe hace años.",
                "narration": f"Mira esto. {dato[:150]} Y siguieron vendiendo como si nada.",
                "duration":  9.0,
                "engraving": 1,
            },
            # Escena 3 — CREDIBILITY ANCHOR (14-24s)
            {
                "headline":  "MERE EXPOSURE",
                "context":   "Robert Zajonc, 1968.",
                "subtitle":  "El cerebro confunde familiaridad con calidad.",
                "narration": "El Mere Exposure Effect. Zajonc, 1968. Mientras más veces escuchas algo, más te gusta. Aunque sea de fondo. El cerebro confunde familiaridad con calidad.",
                "duration":  10.0,
                "engraving": 2,
            },
            # Escena 4 — INSIGHT REVELATION (24-38s)
            {
                "headline":  "TikTok ES",
                "context":   "Esto no es opinión.",
                "subtitle":  "una máquina de familiaridad.",
                "narration": "TikTok no es entretenimiento. Es una máquina de crear familiaridad masiva a costo casi cero. Cada vez que alguien usa tu canción de fondo, tu cerebro entra al subconsciente de millones.",
                "duration":  14.0,
                "engraving": 3,
            },
            # Escena 5 — REBEL REFRAME (38-48s)
            {
                "headline":  "ES BIOLOGIA",
                "context":   "La pregunta correcta.",
                "subtitle":  "cuántos te escuchan sin saberlo.",
                "narration": "La pregunta no es cómo hacer una canción buena. La pregunta es cuántas personas van a escucharla sin darse cuenta de que la están escuchando. Esas son las que pagan. IM Music, Rebel Luxury.",
                "duration":  10.0,
                "engraving": 4,
            },
        ]

    def create_reel(
        self,
        brief: dict,
        output_path: Path,
        size: tuple = (1080, 1920),
        with_voice: bool = True,
    ) -> Path:
        """Crea un Reel completo con voz, texto y grabados."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_dir = output_path.parent / f"_tmp_{output_path.stem}"
        tmp_dir.mkdir(exist_ok=True)

        scenes    = self._build_scenes(brief)
        clip_paths = []

        print(f"  Generando {len(scenes)} escenas...")
        for i, scene in enumerate(scenes):
            print(f"    Escena {i+1}/{len(scenes)}: {scene['headline']}", end=" ")

            # 1. Frame visual
            img = _make_slide_image(
                headline=scene["headline"],
                context=scene.get("context", ""),
                subtitle=scene.get("subtitle", ""),
                size=size,
                engraving_idx=scene.get("engraving", i),
            )

            # 2. Voz
            narration = scene.get("narration", "")
            audio_path = tmp_dir / f"voice_{i:02d}.mp3"
            has_voice = False
            if with_voice and narration:
                has_voice = _synthesize_voice(narration, audio_path)

            # 3. Video del frame
            clip_silent = tmp_dir / f"clip_{i:02d}_silent.mp4"
            _image_to_video(img, scene["duration"], clip_silent, size)

            # 4. Combinar con voz
            if has_voice and audio_path.exists():
                clip_with_audio = tmp_dir / f"clip_{i:02d}.mp4"
                try:
                    _combine_video_audio(clip_silent, audio_path, clip_with_audio)
                    clip_paths.append(clip_with_audio)
                    print("voz+imagen OK")
                except Exception as e:
                    logger.warning(f"Combine failed: {e}")
                    clip_paths.append(clip_silent)
                    print("solo imagen OK")
            else:
                clip_paths.append(clip_silent)
                print("imagen OK")

        # 5. Concatenar todo
        print(f"  Concatenando {len(clip_paths)} clips...")
        _concat_videos(clip_paths, output_path)

        # Limpieza
        shutil.rmtree(tmp_dir, ignore_errors=True)
        size_kb = output_path.stat().st_size // 1024
        print(f"  [OK] {output_path.name}  {size_kb}KB  {sum(s['duration'] for s in scenes):.0f}s")
        return output_path

    def create_tiktok(self, brief: dict, output_path: Path) -> Path:
        """TikTok: misma estructura, 9:16, max 90s."""
        return self.create_reel(brief, output_path, size=(1080, 1920))

    def create_youtube_short(self, brief: dict, output_path: Path) -> Path:
        """YouTube Short: max 58s — usa solo primeras 3 escenas."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_dir = output_path.parent / f"_tmp_{output_path.stem}"
        tmp_dir.mkdir(exist_ok=True)

        scenes     = self._build_scenes(brief)[:3]  # Solo 3 escenas para ~24s
        clip_paths = []
        size       = (1080, 1920)

        for i, scene in enumerate(scenes):
            img   = _make_slide_image(scene["headline"], scene.get("context",""), scene.get("subtitle",""), size, scene.get("engraving",i))
            audio = tmp_dir / f"voice_{i:02d}.mp3"
            _synthesize_voice(scene.get("narration",""), audio)
            clip_s = tmp_dir / f"clip_{i:02d}_s.mp4"
            _image_to_video(img, scene["duration"], clip_s, size)
            if audio.exists():
                clip_a = tmp_dir / f"clip_{i:02d}.mp4"
                try:
                    _combine_video_audio(clip_s, audio, clip_a)
                    clip_paths.append(clip_a)
                except Exception:
                    clip_paths.append(clip_s)
            else:
                clip_paths.append(clip_s)

        _concat_videos(clip_paths, output_path)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return output_path

    def produce_all_videos(self, brief: dict, out_dir: Path) -> dict:
        """Produce TODOS los videos automatizados del brief."""
        out_dir.mkdir(parents=True, exist_ok=True)
        results = {}

        print("PRODUCCION AUTOMATIZADA — IM MUSIC REBEL LUXURY")
        print(f"Tema: {brief.get('titulo_principal','')[:60]}")
        print()

        print("[1/3] Reel Instagram (9:16, 48s con voz)...")
        try:
            p = self.create_reel(brief, out_dir / "reel_instagram.mp4")
            results["reel_instagram"] = str(p)
        except Exception as e:
            print(f"  [FAIL] {e}")

        print("[2/3] TikTok (9:16, 48s con voz)...")
        try:
            p = self.create_tiktok(brief, out_dir / "tiktok.mp4")
            results["tiktok"] = str(p)
        except Exception as e:
            print(f"  [FAIL] {e}")

        print("[3/3] YouTube Short (9:16, 24s con voz)...")
        try:
            p = self.create_youtube_short(brief, out_dir / "youtube_short.mp4")
            results["youtube_short"] = str(p)
        except Exception as e:
            print(f"  [FAIL] {e}")

        print()
        print("VIDEOS LISTOS:")
        for k, v in results.items():
            p = Path(v)
            print(f"  {k}: {p.name}  {p.stat().st_size//1024}KB")

        return results
