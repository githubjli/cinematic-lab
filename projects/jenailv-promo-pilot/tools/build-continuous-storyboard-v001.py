from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reviews" / "continuous-storyboard-v001.jpg"
FONT_PATH = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD_PATH = Path(r"C:\Windows\Fonts\msyhbd.ttc")

PANELS = [
    ("S01  0–5s", "混乱有体积", "生成关键帧", ROOT / "assets/generated/storyboard-v001/S01-chaos-v001.png"),
    ("S02  5–11s", "进入秩序", "生成关键帧", ROOT / "assets/generated/storyboard-v001/S02-conveyor-v001.png"),
    ("S03  11–17s", "机器苏醒", "B风格代理", ROOT / "assets/generated/style-direction-v001/B-premium-hero-v001.png"),
    ("S04  17–24s", "落料入腔", "A风格代理", ROOT / "assets/generated/style-direction-v001/A-documentary-cg-v001.png"),
    ("S05  24–32s", "连续压缩", "C概念代理", ROOT / "assets/generated/style-direction-v001/C-engineering-cutaway-v001.png"),
    ("S06  32–40s", "开门推包", "Blender运动合同", ROOT / "outputs/blender-demo-v003/review/t085.jpg"),
    ("S07  40–49s", "空间重组", "官网事实素材", ROOT / "assets/source/website/016-1790481828389271.jpg"),
    ("S08  49–55s", "机器与结果", "B风格代理", ROOT / "assets/generated/style-direction-v001/B-premium-hero-v001.png"),
]

canvas_w, canvas_h = 1440, 2560
margin, gutter, header = 54, 32, 156
cell_w = (canvas_w - margin * 2 - gutter) // 2
cell_h = (canvas_h - header - margin - gutter * 3) // 4
image_h = cell_h - 96

canvas = Image.new("RGB", (canvas_w, canvas_h), "#07111f")
draw = ImageDraw.Draw(canvas)
title_font = ImageFont.truetype(str(FONT_BOLD_PATH), 48)
shot_font = ImageFont.truetype(str(FONT_BOLD_PATH), 27)
caption_font = ImageFont.truetype(str(FONT_PATH), 25)
badge_font = ImageFont.truetype(str(FONT_PATH), 18)

draw.text((margin, 46), "金耐力 · 9:16连续故事分镜 v001", fill="#f5f7fb", font=title_font)
draw.text((margin, 108), "同一批物料：混乱 → 输送 → 压缩 → 推出 → 有序", fill="#8da4c0", font=caption_font)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    x = (resized.width - target_w) // 2
    y = (resized.height - target_h) // 2
    return resized.crop((x, y, x + target_w, y + target_h))


for index, (shot, caption, badge, path) in enumerate(PANELS):
    row, col = divmod(index, 2)
    x = margin + col * (cell_w + gutter)
    y = header + row * (cell_h + gutter)
    image = cover(Image.open(path).convert("RGB"), (cell_w, image_h))
    canvas.paste(image, (x, y))
    draw.rectangle((x, y + image_h, x + cell_w, y + cell_h), fill="#0f2034")
    draw.text((x + 18, y + image_h + 12), shot, fill="#ffffff", font=shot_font)
    draw.text((x + 18, y + image_h + 50), caption, fill="#d5e2ee", font=caption_font)
    badge_box = draw.textbbox((0, 0), badge, font=badge_font)
    badge_w = badge_box[2] - badge_box[0] + 24
    bx = x + cell_w - badge_w - 14
    by = y + image_h + 47
    draw.rounded_rectangle((bx, by, bx + badge_w, by + 32), radius=8, fill="#1e5e91")
    draw.text((bx + 12, by + 4), badge, fill="#ffffff", font=badge_font)

OUT.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT, quality=93, subsampling=0)
print(OUT)
