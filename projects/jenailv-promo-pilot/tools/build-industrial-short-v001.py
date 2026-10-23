from pathlib import Path
import hashlib
import json
import subprocess

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / "outputs" / "industrial-short-v001"
OUT.mkdir(parents=True, exist_ok=True)
FFMPEG = Path(r"C:\Users\76797\Desktop\chatgpt\aivideo\tools\avatar\Wan2GP\ffmpeg_bins\ffmpeg.exe")
VIDEO = PROJECT / "outputs" / "blender-demo-v007" / "jenailv-baler-concept-v007-720x1280.mp4"
SOUND = PROJECT / "outputs" / "blender-demo-v006" / "mechanical-temp-sound-v006.wav"
LOGO = PROJECT / "assets" / "source" / "website" / "001-1790469943272760.png"
FONT = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
W, H = 720, 1280


def font(size: int, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT), size=size)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay, "RGBA")
draw.rounded_rectangle((24, 26, 696, 74), radius=12, fill=(3, 12, 22, 174))
draw.text((42, 37), "机械动作概念预演｜内部结构、行程与安全逻辑待确认", font=font(17), fill=(236, 241, 245, 255))
overlay_path = OUT / "concept-label.png"
overlay.save(overlay_path)

# Use the actual rendered last frame as the only static closing background.
last_frame = OUT / "last-frame.png"
subprocess.run([str(FFMPEG), "-y", "-sseof", "-0.05", "-i", str(VIDEO), "-frames:v", "1", "-update", "1", str(last_frame)], check=True)
with Image.open(last_frame) as src:
    end = ImageOps.fit(src.convert("RGB"), (W, H), method=Image.Resampling.LANCZOS).convert("RGBA")
end = ImageEnhance.Brightness(end).enhance(0.34)
shade = Image.new("RGBA", (W, H), (2, 10, 18, 102))
end = Image.alpha_composite(end, shade)
ed = ImageDraw.Draw(end, "RGBA")
with Image.open(LOGO) as logo_src:
    logo = ImageOps.exif_transpose(logo_src).convert("RGBA")
logo.thumbnail((420, 180), Image.Resampling.LANCZOS)
lx, ly = (W - logo.width) // 2, 360
ed.rounded_rectangle((lx - 24, ly - 18, lx + logo.width + 24, ly + logo.height + 18), radius=20, fill=(248, 250, 252, 232))
end.alpha_composite(logo, (lx, ly))
title = "把体积，变成效率"
bbox = ed.textbbox((0, 0), title, font=font(42, True))
ed.text(((W - (bbox[2] - bbox[0])) / 2, 650), title, font=font(42, True), fill=(248, 250, 252, 255))
url = "www.jenailv.net"
bbox = ed.textbbox((0, 0), url, font=font(24))
ed.text(((W - (bbox[2] - bbox[0])) / 2, 730), url, font=font(24), fill=(164, 205, 229, 255))
end_path = OUT / "end-frame.png"
end.convert("RGB").save(end_path)

final = OUT / "jenailv-industrial-short-v001-720x1280-26s.mp4"
filter_graph = (
    "[0:v][1:v]overlay=0:0[vmain];"
    "[2:v]fps=24,format=yuv420p[vend];"
    "[vmain][vend]concat=n=2:v=1:a=0[v];"
    "[3:a]atempo=0.6666667,apad=pad_dur=2,atrim=0:26,afade=t=out:st=24:d=2,alimiter=limit=0.93[a]"
)
subprocess.run([
    str(FFMPEG), "-y", "-i", str(VIDEO), "-i", str(overlay_path), "-loop", "1", "-t", "2", "-i", str(end_path), "-i", str(SOUND),
    "-filter_complex", filter_graph, "-map", "[v]", "-map", "[a]", "-r", "24", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(final)
], check=True)

report = {
    "version": "v001",
    "status": "rapid review candidate; not release master",
    "direction": "Jenailv industrial documentary",
    "duration_seconds": 26,
    "resolution": [W, H],
    "fps": 24,
    "body": "24-second deterministic Blender v007 animation with four motivated cameras",
    "ending": "2-second static brand frame derived from the final rendered frame",
    "audio": "v006 temporary mechanical sound time-stretched to 24 seconds plus 2-second fade",
    "output": str(final.relative_to(PROJECT)).replace("\\", "/"),
    "sha256": sha256(final),
    "limitations": [
        "Mechanical structure remains an unverified concept proxy.",
        "Factory set and materials are cinematic proxies, not a verified customer site.",
        "Temporary sound is programmatic and not recorded from the real machine.",
    ],
}
(OUT / "render-report-v001.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
