from __future__ import annotations

import hashlib
import json
import math
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "outputs" / "body-video-v001"
PLATES = OUT / "plates"
OVERLAYS = OUT / "overlays"
CLIPS = OUT / "clips"
FFMPEG = Path(r"C:\Users\76797\Desktop\chatgpt\aivideo\tools\avatar\Wan2GP\ffmpeg_bins\ffmpeg.exe")
FFPROBE = FFMPEG.with_name("ffprobe.exe")
FONT = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
W, H, FPS = 1080, 1920, 24

GENERATED = PROJECT / "assets" / "generated"
WEBSITE = PROJECT / "assets" / "source" / "website"
MECH_VIDEO = PROJECT / "outputs" / "blender-demo-v006" / "jenailv-baler-concept-v006-720x1280.mp4"
MECH_SOUND = PROJECT / "outputs" / "blender-demo-v006" / "mechanical-temp-sound-v006.wav"
LOGO = WEBSITE / "001-1790469943272760.png"


SHOTS = [
    {"id": "S01", "duration": 5.0, "source": GENERATED / "storyboard-v001" / "S01-chaos-v001.png", "title": "松散，占据空间", "label": "从无序开始", "move": "in"},
    {"id": "S02", "duration": 6.0, "source": GENERATED / "storyboard-v001" / "S02-conveyor-v001.png", "title": "让物料进入连续流程", "label": "输送 · 进入", "move": "out"},
    {"id": "S03", "duration": 6.0, "source": GENERATED / "style-direction-v001" / "B-premium-hero-v001.png", "title": "让设备成为流程的核心", "label": "设备启动", "move": "in"},
    {"id": "S04-06", "duration": 16.0, "source": MECH_VIDEO, "title": "压缩 · 开门 · 推出", "label": "机械动作概念预演｜结构待确认", "type": "video"},
    {"id": "S07", "duration": 7.0, "source": GENERATED / "storyboard-v001" / "S07-organized-output-v002.png", "title": "从松散体积，到规整单元", "label": "空间被重新组织", "move": "out"},
    {"id": "S08A", "duration": 1.25, "source": WEBSITE / "006-1790556029268605.jpg", "title": "", "label": "不同物料 · 不同场地", "move": "in"},
    {"id": "S08B", "duration": 1.25, "source": WEBSITE / "007-1790555845667730.jpg", "title": "", "label": "匹配不同方案", "move": "out"},
    {"id": "S08C", "duration": 1.25, "source": WEBSITE / "008-1790555112224865.jpg", "title": "", "label": "", "move": "in"},
    {"id": "S08D", "duration": 1.25, "source": WEBSITE / "010-1790553932266631.jpg", "title": "", "label": "", "move": "out"},
    {"id": "S09A", "duration": 3.0, "source": GENERATED / "style-direction-v001" / "A-documentary-cg-v001.png", "title": "从现场，到交付", "label": "分析现场 · 匹配方案", "move": "in"},
    {"id": "S09B", "duration": 3.0, "source": WEBSITE / "025-1790490274674288.jpg", "title": "", "label": "生产质检 · 售后服务", "move": "out"},
    {"id": "S10", "duration": 4.0, "source": GENERATED / "storyboard-v001" / "S08-final-wipe-v002.png", "title": "把体积，变成效率", "label": "www.jenailv.net", "move": "out", "logo": True},
]


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def font(size: int, bold: bool = False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT), size=size)


def plate(source: Path, target: Path) -> None:
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original).convert("RGB")
    image = ImageOps.fit(image, (W, H), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    image = ImageEnhance.Color(image).enhance(0.92)
    image = ImageEnhance.Contrast(image).enhance(1.06)
    image = ImageEnhance.Brightness(image).enhance(0.94)
    image.save(target, quality=95)


def overlay(shot: dict, target: Path) -> None:
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas, "RGBA")
    title = shot.get("title", "")
    label = shot.get("label", "")
    if title or label:
        # Bottom gradient retains full-bleed cinematography while supporting sparse type.
        gradient = Image.new("RGBA", (W, 560), (0, 0, 0, 0))
        gd = ImageDraw.Draw(gradient, "RGBA")
        for y in range(560):
            a = int(205 * (y / 559) ** 1.7)
            gd.line((0, y, W, y), fill=(3, 11, 20, a))
        canvas.alpha_composite(gradient, (0, H - 560))
    if label:
        draw.text((72, 1530), label, font=font(29, True), fill=(105, 205, 238, 255), stroke_width=2, stroke_fill=(0, 0, 0, 170))
    if title:
        draw.text((70, 1590), title, font=font(62, True), fill=(245, 248, 250, 255), stroke_width=3, stroke_fill=(0, 0, 0, 180))
    if shot.get("type") == "video":
        draw.rounded_rectangle((54, 80, 1026, 148), radius=16, fill=(4, 15, 25, 185))
        draw.text((82, 96), "机械动作概念预演｜内部结构、行程与安全逻辑待确认", font=font(25), fill=(230, 238, 244, 255))
    elif shot.get("provenance"):
        draw.rounded_rectangle((54, 80, 420, 142), radius=15, fill=(4, 15, 25, 175))
        draw.text((78, 94), shot["provenance"], font=font(24, True), fill=(228, 236, 242, 255))
    if shot.get("logo"):
        with Image.open(LOGO) as logo_src:
            logo = ImageOps.exif_transpose(logo_src).convert("RGBA")
        logo.thumbnail((520, 230), Image.Resampling.LANCZOS)
        # The website logo contains transparency; a quiet light plate preserves its original pixels.
        lx = (W - logo.width) // 2
        ly = 210
        draw.rounded_rectangle((lx - 34, ly - 24, lx + logo.width + 34, ly + logo.height + 24), radius=24, fill=(245, 248, 250, 225))
        canvas.alpha_composite(logo, (lx, ly))
    canvas.save(target)


def still_clip(shot: dict, index: int) -> Path:
    plate_path = PLATES / f"{index:02d}-{shot['id']}.jpg"
    overlay_path = OVERLAYS / f"{index:02d}-{shot['id']}.png"
    clip_path = CLIPS / f"{index:02d}-{shot['id']}.mp4"
    plate(shot["source"], plate_path)
    overlay(shot, overlay_path)
    frames = int(round(shot["duration"] * FPS))
    if shot.get("move") == "out":
        zoom = "if(eq(on,1),1.06,max(1.0,zoom-0.00045))"
    else:
        zoom = "min(zoom+0.00045,1.07)"
    vf = (
        f"[0:v]zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={frames}:s={W}x{H}:fps={FPS}[z];[z][1:v]overlay=0:0,format=yuv420p[v]"
    )
    run([str(FFMPEG), "-y", "-loop", "1", "-i", str(plate_path), "-i", str(overlay_path),
         "-filter_complex", vf, "-map", "[v]", "-frames:v", str(frames), "-r", str(FPS),
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-an", str(clip_path)])
    return clip_path


def video_clip(shot: dict, index: int) -> Path:
    overlay_path = OVERLAYS / f"{index:02d}-{shot['id']}.png"
    clip_path = CLIPS / f"{index:02d}-{shot['id']}.mp4"
    overlay(shot, overlay_path)
    frames = int(round(shot["duration"] * FPS))
    vf = f"[0:v]scale={W}:{H}:flags=lanczos[v0];[v0][1:v]overlay=0:0,format=yuv420p[v]"
    run([str(FFMPEG), "-y", "-i", str(shot["source"]), "-i", str(overlay_path),
         "-filter_complex", vf, "-map", "[v]", "-frames:v", str(frames), "-r", str(FPS),
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-an", str(clip_path)])
    return clip_path


def build_score(path: Path) -> None:
    rate = 48_000
    duration = 55.0
    n = int(rate * duration)
    t = np.arange(n, dtype=np.float64) / rate
    rng = np.random.default_rng(20261022)
    score = np.zeros(n, dtype=np.float64)

    fade_in = np.clip(t / 2.2, 0, 1)
    fade_out = np.clip((duration - t) / 3.0, 0, 1)
    master_env = fade_in * fade_out
    score += 0.055 * np.sin(2 * np.pi * 36 * t) * master_env
    score += 0.025 * np.sin(2 * np.pi * 72 * t + 0.3 * np.sin(2 * np.pi * 0.06 * t)) * master_env
    score += 0.010 * rng.normal(size=n) * master_env

    # Slow industrial pulse; it avoids a separate musical restart at each edit.
    for when in np.arange(0.8, 54.0, 1.5):
        local = np.maximum(t - when, 0)
        score += (t >= when) * 0.075 * np.sin(2 * np.pi * 48 * local) * np.exp(-local / 0.17)

    # Structural edit impacts.
    for when in (5.0, 11.0, 17.0, 33.0, 40.0, 45.0, 51.0):
        local = np.maximum(t - when, 0)
        score += (t >= when) * 0.17 * np.sin(2 * np.pi * 62 * local) * np.exp(-local / 0.32)
        score += (t >= when) * 0.025 * rng.normal(size=n) * np.exp(-local / 0.12)

    score = np.tanh(score * 1.7) * 0.66
    delay = int(0.017 * rate)
    right = np.roll(score, delay) * 0.94
    right[:delay] = 0
    pcm = np.int16(np.clip(np.column_stack([score, right]), -1, 1) * 32767)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(pcm.tobytes())


def main() -> None:
    for directory in (OUT, PLATES, OVERLAYS, CLIPS):
        directory.mkdir(parents=True, exist_ok=True)
    clips = []
    edl = []
    cursor = 0.0
    for index, shot in enumerate(SHOTS, 1):
        clip = video_clip(shot, index) if shot.get("type") == "video" else still_clip(shot, index)
        clips.append(clip)
        edl.append({"id": shot["id"], "start": cursor, "end": cursor + shot["duration"], "duration": shot["duration"], "source": str(shot["source"].relative_to(PROJECT)).replace("\\", "/")})
        cursor += shot["duration"]

    concat = OUT / "concat-v001.txt"
    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips), encoding="utf-8")
    silent = OUT / "jenailv-body-v001-1080x1920-24-silent.mp4"
    run([str(FFMPEG), "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)])

    score = OUT / "industrial-score-temp-v001.wav"
    build_score(score)
    mix = OUT / "body-mix-temp-v001.m4a"
    run([str(FFMPEG), "-y", "-i", str(score), "-i", str(MECH_SOUND),
         "-filter_complex", "[1:a]adelay=17000|17000,volume=0.92[mech];[0:a]volume=0.72[bed];[bed][mech]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.93[a]",
         "-map", "[a]", "-c:a", "aac", "-b:a", "192k", "-t", "55", str(mix)])

    final = OUT / "jenailv-body-v001-1080x1920-24-temp-sound.mp4"
    run([str(FFMPEG), "-y", "-i", str(silent), "-i", str(mix), "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "copy", "-c:a", "copy", "-shortest", str(final)])

    review = OUT / "jenailv-body-v001-1080x1920-24-review.mp4"
    run([str(FFMPEG), "-y", "-i", str(final), "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000", "-ar", "48000",
         "-c:a", "aac", "-b:a", "192k", str(review)])

    report = {
        "version": "v001",
        "status": "body_rough_cut_not_release_master",
        "resolution": [W, H],
        "fps": FPS,
        "duration_seconds": cursor,
        "mechanical_segment": {"start": 17.0, "end": 33.0, "source": str(MECH_VIDEO.relative_to(PROJECT)).replace("\\", "/"), "status": "concept preview; structure unverified"},
        "audio": "procedural temporary industrial bed plus v006 temporary mechanical sound",
        "edl": edl,
        "output": str(review.relative_to(PROJECT)).replace("\\", "/"),
        "sha256": sha256(review),
        "notes": [
            "Website assets are used under the user's stated authorization.",
            "Generated images are concept visuals and do not prove product structure or performance.",
            "No paid generation was invoked for this edit.",
            "Voice-over, confirmed product model, parameters, CTA, engineering validation, and final music remain pending.",
        ],
    }
    (OUT / "render-report-v001.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
