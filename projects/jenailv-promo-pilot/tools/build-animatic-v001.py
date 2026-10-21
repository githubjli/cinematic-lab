from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


PROJECT = Path(__file__).resolve().parents[1]
ASSETS = PROJECT / "assets" / "source" / "website"
OUT = PROJECT / "outputs" / "animatic-v001"
CARDS = OUT / "cards"
CLIPS = OUT / "clips"
PORTRAIT_CARDS = OUT / "cards-9x16"
PORTRAIT_CLIPS = OUT / "clips-9x16"
FFMPEG = Path(r"C:\Users\76797\Desktop\chatgpt\aivideo\tools\avatar\Wan2GP\ffmpeg_bins\ffmpeg.exe")
FONT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")
W, H, FPS = 1920, 1080, 24

BLUE = (17, 72, 145)
CYAN = (17, 174, 213)
GREEN = (117, 181, 66)
INK = (235, 242, 248)
MUTED = (147, 170, 191)
BG = (8, 20, 34)


SHOTS = [
    {"id": "S01", "duration": 4, "title": "松散，占据的不只是空间", "sub": "问题建立｜废料体积与场地压力", "files": ["009-1790554983657413.jpg"]},
    {"id": "S02", "duration": 4, "title": "搬运、堆放、周转", "sub": "只表达流程低效，不使用未经确认的成本数字", "files": ["023-1790490330588939.jpg", "026-1790490244836255.jpg"]},
    {"id": "S03", "duration": 5, "title": "让废料处理回到简单、可靠、高效", "sub": "产品登场｜主推机型暂按全自动250型", "files": ["010-1790553932266631.jpg", "001-1790469943272760.png"]},
    {"id": "S04", "duration": 6, "title": "从上料开始，流程连续推进", "sub": "D3待替换：连续上料实拍或Blender灰模", "files": ["011-1790551663495432.jpg", "014-1790481873167824.jpg"]},
    {"id": "S05", "duration": 6, "title": "稳定液压，把松散体积压成规整密度", "sub": "D3核心：压板行程、受力方向、压缩腔剖切", "files": ["008-1790555112224865.jpg", "020-1790490444305335.jpg"]},
    {"id": "S06", "duration": 5, "title": "一包一包，便于堆放与周转", "sub": "D3待替换：捆扎、开门、推出与落位连续动作", "files": ["016-1790481828389271.jpg", "007-1790555845667730.jpg"]},
    {"id": "S07", "duration": 8, "title": "体积被重新组织，空间才开始产生效率", "sub": "同尺度前后对比｜压缩比例等待品牌数据", "files": ["009-1790554983657413.jpg", "016-1790481828389271.jpg"]},
    {"id": "S08", "duration": 7, "title": "不同物料，不同场地，匹配不同方案", "sub": "全自动｜半自动｜综合型｜工厂专用", "files": ["006-1790556029268605.jpg", "007-1790555845667730.jpg", "008-1790555112224865.jpg", "010-1790553932266631.jpg"]},
    {"id": "S09", "duration": 6, "title": "从现场，到交付", "sub": "现场分析｜方案匹配｜生产质检｜售后服务", "files": ["025-1790490274674288.jpg", "036-1792034396566064.jpg"]},
    {"id": "S10", "duration": 4, "title": "把体积，变成效率", "sub": "金耐力｜www.jenailv.net", "files": ["001-1790469943272760.png"]},
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REGULAR
    return ImageFont.truetype(str(path), size=size)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, text_font: ImageFont.FreeTypeFont, max_width: int) -> str:
    lines: list[str] = []
    current = ""
    for character in text:
        candidate = current + character
        if current and draw.textbbox((0, 0), candidate, font=text_font)[2] > max_width:
            lines.append(current)
            current = character
        else:
            current = candidate
    if current:
        lines.append(current)
    return "\n".join(lines)


def wrap_balanced_text(draw: ImageDraw.ImageDraw, text: str, text_font: ImageFont.FreeTypeFont, max_width: int) -> str:
    if draw.textbbox((0, 0), text, font=text_font)[2] <= max_width:
        return text
    midpoint = (len(text) + 1) // 2
    return text[:midpoint] + "\n" + text[midpoint:]


def cover(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
    return ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)


def add_gradient(image: Image.Image) -> Image.Image:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    pixels = overlay.load()
    for y in range(H):
        for x in range(W):
            alpha = int(220 * max(0.0, min(1.0, (x - 760) / 1160)))
            pixels[x, y] = (5, 14, 26, alpha)
    return Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")


def draw_card(shot: dict, index: int) -> Path:
    canvas = Image.new("RGB", (W, H), BG)
    files = [ASSETS / name for name in shot["files"]]
    if len(files) == 1:
        visual = cover(files[0], (W, H))
    elif len(files) == 2:
        visual = Image.new("RGB", (W, H), BG)
        visual.paste(cover(files[0], (W // 2, H)), (0, 0))
        visual.paste(cover(files[1], (W // 2, H)), (W // 2, 0))
    else:
        visual = Image.new("RGB", (W, H), BG)
        for n, path in enumerate(files[:4]):
            visual.paste(cover(path, (W // 2, H // 2)), ((n % 2) * W // 2, (n // 2) * H // 2))
    visual = ImageEnhance.Color(visual).enhance(0.78)
    visual = ImageEnhance.Contrast(visual).enhance(1.05)
    visual = add_gradient(visual)
    canvas.paste(visual)

    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((0, 0, W, 16), fill=BLUE + (255,))
    draw.rectangle((0, 16, int(W * (index + 1) / len(SHOTS)), 24), fill=GREEN + (255,))
    draw.rectangle((1040, 0, W, H), fill=(4, 14, 27, 145))
    draw.rectangle((1090, 176, 1110, 540), fill=CYAN + (255,))

    draw.text((90, 70), "JENAILV  /  INDUSTRIAL FILM", font=font(28, True), fill=INK)
    draw.text((90, 116), "D2 动态分镜 · 非最终画面", font=font(24), fill=MUTED)
    draw.text((1135, 178), shot["id"], font=font(34, True), fill=GREEN)
    title_font = font(60, True)
    sub_font = font(28)
    draw.multiline_text((1135, 246), wrap_text(draw, shot["title"], title_font, 680), font=title_font, fill=INK, spacing=18)
    draw.multiline_text((1138, 500), wrap_text(draw, shot["sub"], sub_font, 680), font=sub_font, fill=MUTED, spacing=12)

    draw.rounded_rectangle((1135, 790, 1740, 892), radius=16, fill=(17, 72, 145, 210))
    draw.text((1170, 817), f"{shot['duration']:02d}s   ·   1920×1080   ·   24fps", font=font(25), fill=INK)
    draw.text((90, 1000), "官网授权素材 / 内部流程测试 / 画面运动与机械动作尚未验证", font=font(22), fill=(210, 220, 228))

    path = CARDS / f"{index + 1:02d}-{shot['id']}.png"
    canvas.save(path)
    return path


def draw_portrait_card(shot: dict, index: int) -> Path:
    width, height = 1080, 1920
    canvas = Image.new("RGB", (width, height), BG)
    files = [ASSETS / name for name in shot["files"]]
    if len(files) == 1:
        visual = cover(files[0], (width, 1120))
    elif len(files) == 2:
        visual = Image.new("RGB", (width, 1120), BG)
        visual.paste(cover(files[0], (width, 560)), (0, 0))
        visual.paste(cover(files[1], (width, 560)), (0, 560))
    else:
        visual = Image.new("RGB", (width, 1120), BG)
        for n, path in enumerate(files[:4]):
            visual.paste(cover(path, (width // 2, 560)), ((n % 2) * width // 2, (n // 2) * 560))
    visual = ImageEnhance.Color(visual).enhance(0.78)
    visual = ImageEnhance.Contrast(visual).enhance(1.05)
    canvas.paste(visual, (0, 0))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay, "RGBA")
    for y in range(760, 1220):
        alpha = int(235 * (y - 760) / 460)
        odraw.rectangle((0, y, width, y + 1), fill=(5, 14, 26, alpha))
    odraw.rectangle((0, 1120, width, height), fill=BG + (255,))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle((0, 0, width, 18), fill=BLUE + (255,))
    draw.rectangle((0, 18, int(width * (index + 1) / len(SHOTS)), 28), fill=GREEN + (255,))
    draw.text((68, 68), "JENAILV / INDUSTRIAL FILM", font=font(26, True), fill=INK)
    draw.text((68, 108), "D2 竖屏动态分镜 · 非最终画面", font=font(22), fill=(220, 230, 238))
    draw.rectangle((68, 1165, 84, 1575), fill=CYAN + (255,))
    draw.text((116, 1165), shot["id"], font=font(32, True), fill=GREEN)
    title_font = font(58, True)
    sub_font = font(29)
    draw.multiline_text((116, 1230), wrap_balanced_text(draw, shot["title"], title_font, 870), font=title_font, fill=INK, spacing=20)
    draw.multiline_text((116, 1480), wrap_text(draw, shot["sub"], sub_font, 860), font=sub_font, fill=MUTED, spacing=14)
    draw.rounded_rectangle((116, 1690, 964, 1794), radius=18, fill=(17, 72, 145, 225))
    draw.text((154, 1722), f"{shot['duration']:02d}s  ·  1080×1920  ·  24fps", font=font(27), fill=INK)
    draw.text((68, 1842), "官网授权素材 / 内部流程测试 / 机械动作尚未验证", font=font(20), fill=(190, 205, 218))
    path = PORTRAIT_CARDS / f"{index + 1:02d}-{shot['id']}-9x16.png"
    canvas.save(path)
    return path


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main() -> None:
    PORTRAIT_CARDS.mkdir(parents=True, exist_ok=True)
    PORTRAIT_CLIPS.mkdir(parents=True, exist_ok=True)
    portrait_cards = [draw_portrait_card(shot, index) for index, shot in enumerate(SHOTS)]

    portrait_clips: list[Path] = []
    for shot, card in zip(SHOTS, portrait_cards):
        clip = PORTRAIT_CLIPS / f"{shot['id']}-9x16.mp4"
        run([
            str(FFMPEG), "-y", "-loop", "1", "-i", str(card), "-t", str(shot["duration"]),
            "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-an", str(clip),
        ])
        portrait_clips.append(clip)
    portrait_concat = OUT / "concat-9x16-v001.txt"
    portrait_concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in portrait_clips), encoding="utf-8")
    portrait_master = OUT / "jenailv-animatic-v001-1080x1920-24-silent.mp4"
    run([
        str(FFMPEG), "-y", "-f", "concat", "-safe", "0", "-i", str(portrait_concat),
        "-c", "copy", str(portrait_master),
    ])

    report = {
        "version": "v001",
        "status": "technical_render_only_not_visual_approval",
        "source_manifest": "references/website/download-manifest-v001.csv",
        "shot_count": len(SHOTS),
        "duration_seconds": sum(s["duration"] for s in SHOTS),
        "fps": FPS,
        "resolution": [1080, 1920],
        "audio": False,
        "output": {"layout": "9:16", "file": str(portrait_master.relative_to(PROJECT)).replace("\\", "/"), "sha256": sha256(portrait_master)},
        "notes": [
            "Static website images are proxies; no equipment motion is claimed.",
            "Main product assumption: automatic 250 model, pending brand confirmation.",
            "No paid or GPU generation was invoked.",
            "9:16 is the only active delivery layout; the earlier 16:9 draft is retained as history only.",
        ],
    }
    (OUT / "render-report-v001.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
