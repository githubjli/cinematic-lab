from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "generated" / "style-direction-v001"
OUT = ROOT / "reviews" / "style-direction-contact-sheet-v001.jpg"
ITEMS = [
    ("A  DOCUMENTARY + CG", SRC / "A-documentary-cg-v001.png"),
    ("B  PREMIUM HERO", SRC / "B-premium-hero-v001.png"),
    ("C  ENGINEERING CUTAWAY", SRC / "C-engineering-cutaway-v001.png"),
]

thumb_w, thumb_h = 400, 711
margin, gap, header = 36, 24, 92
canvas = Image.new("RGB", (margin * 2 + thumb_w * 3 + gap * 2, header + thumb_h + margin), "#08111e")
draw = ImageDraw.Draw(canvas)
font = ImageFont.load_default(size=24)

for i, (label, path) in enumerate(ITEMS):
    image = Image.open(path).convert("RGB")
    image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    x = margin + i * (thumb_w + gap)
    y = header
    tile = Image.new("RGB", (thumb_w, thumb_h), "#111827")
    tile.paste(image, ((thumb_w - image.width) // 2, (thumb_h - image.height) // 2))
    canvas.paste(tile, (x, y))
    draw.text((x, 34), label, fill="#f4f7fb", font=font)

OUT.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT, quality=92, subsampling=0)
print(OUT)
