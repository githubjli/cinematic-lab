"""Extract original frames and typeset a single annotated storyboard board.

No image generation or retouching; source frame pixels are fitted without cropping.
Run with a Python environment containing Pillow. Output is local, ignored media.
"""
from pathlib import Path
import csv
import hashlib
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = ROOT / 'references/033/storyboard-v001'
OUT.mkdir(parents=True, exist_ok=True)
FFMPEG = ROOT / '.tools/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
ITEMS = json.loads((HERE / 'storyboard-keyframes.json').read_text(encoding='utf-8'))
FONT = 'C:/Windows/Fonts/msyh.ttc'
BOLD = 'C:/Windows/Fonts/msyhbd.ttc'

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def tc(seconds):
    return f'{int(seconds)//60:02d}:{seconds%60:04.1f}'

commands, records = [], []
for item in ITEMS:
    src = ROOT / f"references/033/source-{item['source']}.mp4"
    dest = OUT / f"{item['id']}-ep{1 if item['source']=='25' else 2}-{item['time']:06.1f}.png"
    cmd = [str(FFMPEG), '-hide_banner', '-loglevel', 'error', '-ss', str(item['time']),
           '-i', str(src), '-frames:v', '1', '-y', str(dest)]
    subprocess.run(cmd, check=True)
    commands.append(cmd)
    item['frame'] = str(dest)
    records.append(dict(id=item['id'], source=str(src.relative_to(ROOT)), source_sha256=sha(src),
                        requested_time_seconds=item['time'], frame=str(dest.relative_to(ROOT)),
                        frame_sha256=sha(dest), dialogue=item['dialogue']))

W, M, GAP, CW, CH = 3600, 72, 24, 846, 810
HEADER, RH, FOOTER = 270, 76, 160
H = HEADER + 5*(RH+CH+24) + FOOTER
canvas = Image.new('RGB', (W, H), '#101823')
d = ImageDraw.Draw(canvas)
WHITE, MUTED, GOLD = '#f1f4f8', '#aab8c9', '#f1bd6b'
d.text((M, 45), '角色反差 → 信息揭示 → 自主选择', font=font(60, True), fill=WHITE)
d.text((M, 128), 'MY CAT IS RICHER THAN ME  ·  双集故事分镜看板', font=font(34), fill=GOLD)
d.text((M, 191), '阅读顺序  左 → 右， 上 → 下    |    原片关键帧 · 20个叙事节点 · 含剧透', font=font(28), fill=MUTED)

def wrap(text, width, f):
    lines, line = [], ''
    for char in text:
        if char == '\n':
            lines.append(line); line = ''; continue
        if line and d.textlength(line+char, font=f) > width:
            lines.append(line); line = char
        else:
            line += char
    if line:
        lines.append(line)
    return lines

def block(x, y, label, body, width, size=27):
    d.text((x,y), label, font=font(23,True), fill=GOLD)
    y += 37
    f = font(size)
    for line in wrap(body, width, f):
        d.text((x,y), line, font=f, fill=WHITE)
        y += size+13
    return y+17

stages = [
    ('EPISODE 01 · 起', '憧憬城市 → 碰到规则 → 遭遇损失 → 获得资源'),
    ('EPISODE 01 · 承', '条件交换 → 冷暖转变 → 同住关系 → 身份悬念'),
    ('EPISODE 02 · 起', '建立环境 → 明确目标 → 提出难题 → 展示解法'),
    ('EPISODE 02 · 转', '社会压力升级 → 暂时过关 → 更高门槛 → 群体标准'),
    ('EPISODE 02 · 合', '拒绝冒充 → 坦诚选择 → 价值翻转 → 关系收束'),
]
for row, (stage, desc) in enumerate(stages):
    y = HEADER + row*(RH+CH+24)
    d.text((M,y+9), stage, font=font(29,True), fill=GOLD)
    d.text((M+435,y+12), desc, font=font(27), fill=MUTED)
    for col in range(4):
        item = ITEMS[row*4+col]
        x, cy = M+col*(CW+GAP), y+RH
        d.rounded_rectangle((x,cy,x+CW,cy+CH), radius=20, fill='#1c2838')
        d.text((x+24,cy+18), f"{item['id']}  {item['title']}", font=font(32,True), fill=WHITE)
        label = f"EP{1 if item['source']=='25' else 2}  {tc(item['time'])}"
        d.text((x+CW-245,cy+24), label, font=font(24), fill=MUTED)
        im = Image.open(item['frame']).convert('RGB')
        if item['source'] == '25':
            fitted = ImageOps.contain(im, (344,612), Image.Resampling.LANCZOS)
            ix, iy = x+24+(344-fitted.width)//2, cy+80
            canvas.paste(fitted,(ix,iy))
            tx, ty, tw = x+392, cy+83, CW-416
            ty = block(tx,ty,'镜头',item['shot'],tw)
            ty = block(tx,ty,'表情 / 姿态',item['expression'],tw)
            ty = block(tx,ty,'对话细节',item['dialogue'],tw,26)
            if ty > cy+690:
                raise ValueError(f"Portrait annotation overflow {item['id']}: {ty-cy}")
            fy = cy+710
        else:
            fitted = ImageOps.contain(im,(CW-48,449),Image.Resampling.LANCZOS)
            canvas.paste(fitted,(x+24+(CW-48-fitted.width)//2,cy+80))
            fy = cy+550
            f = font(25)
            for label, val in [('镜头',item['shot']),('表情',item['expression']),('对话',item['dialogue'])]:
                lines = wrap(label+'  '+val,CW-48,f)
                for line in lines:
                    d.text((x+24,fy),line,font=f,fill=WHITE)
                    fy += 37
                fy += 8
            if fy > cy+712:
                raise ValueError(f"Landscape annotation overflow {item['id']}: {fy-cy}")
            fy = cy+714
        d.line((x+24,fy-12,x+CW-24,fy-12),fill='#3b4b60',width=2)
        pf=font(25)
        for line in wrap('叙事作用  '+item['purpose'],CW-48,pf):
            d.text((x+24,fy),line,font=pf,fill=GOLD)
            fy += 37
        if fy > cy+CH-12:
            raise ValueError(f"Purpose overflow {item['id']}")

fy = H-FOOTER+25
d.text((M,fy),'注：镜头为研究重排编号，非原作者镜号；时间码为源视频定位值；原画面保留，不裁切、不重绘。',font=font(26),fill=MUTED)
d.text((M,fy+44),'“字幕”是可见文字摘录；“相邻字幕”来自同段邻帧；“场面概述”是研究归纳。导演意图属推断，原制作工具未知。',font=font(25),fill=MUTED)
d.text((M,fy+87),'CINEMATIC LAB  /  CASE 033  /  STORYBOARD v001  /  2026-11-13',font=font(24),fill=MUTED)
full = OUT / 'case033-storyboard-board-v001.png'
canvas.save(full)
preview = OUT / 'case033-storyboard-board-v001-preview.jpg'
small = canvas.copy(); small.thumbnail((1800,2600),Image.Resampling.LANCZOS); small.save(preview,quality=94)
with (HERE/'storyboard-frame-manifest.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=records[0].keys()); writer.writeheader(); writer.writerows(records)
(HERE/'storyboard-extraction-commands.json').write_text(json.dumps(commands,ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'storyboard-output-manifest.json').write_text(json.dumps({
    'board':str(full.relative_to(ROOT)), 'board_sha256':sha(full), 'width':W,'height':H,
    'preview':str(preview.relative_to(ROOT)),'preview_sha256':sha(preview),
    'renderer':'Pillow '+Image.__version__, 'font':FONT,'font_sha256':sha(Path(FONT)),
    'bold_font':BOLD,'bold_font_sha256':sha(Path(BOLD)),
    'review':'layout checked by geometry; visual and subtitle verification pending'
},ensure_ascii=False,indent=2),encoding='utf-8')
print(full)
print(preview)
