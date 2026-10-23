from pathlib import Path


PROJECT = Path(r"C:\Users\76797\Desktop\chatgpt\cinematic-lab\projects\jenailv-promo-pilot")
source_path = PROJECT / "tools" / "build-body-video-v001.py"
target_path = PROJECT / "tools" / "build-body-video-v002.py"
source = source_path.read_text(encoding="utf-8")

source = source.replace('"body-video-v001"', '"body-video-v002"')
source = source.replace('jenailv-body-v001', 'jenailv-body-v002')
source = source.replace('industrial-score-temp-v001.wav', 'industrial-score-temp-v002.wav')
source = source.replace('body-mix-temp-v001.m4a', 'body-mix-temp-v002.m4a')
source = source.replace('concat-v001.txt', 'concat-v002.txt')
source = source.replace('"version": "v001"', '"version": "v002"')

start = source.index("SHOTS = [")
end = source.index("\n\n\ndef run", start)
shots = '''SHOTS = [
    {"id": "S01", "duration": 3.0, "source": GENERATED / "storyboard-v001" / "S01-chaos-v001.png", "title": "松散，占据空间", "label": "从无序开始", "move": "in", "provenance": "概念视觉"},
    {"id": "S02", "duration": 3.0, "source": GENERATED / "storyboard-v001" / "S02-conveyor-v001.png", "title": "让物料进入连续流程", "label": "输送 · 进入", "move": "out", "provenance": "概念视觉"},
    {"id": "S03", "duration": 4.0, "source": GENERATED / "style-direction-v001" / "B-premium-hero-v001.png", "title": "让设备成为流程的核心", "label": "设备启动", "move": "in", "provenance": "概念视觉"},
    {"id": "S04-BRIDGE", "duration": 2.0, "source": GENERATED / "style-direction-v001" / "C-engineering-cutaway-v001.png", "title": "看见压缩发生", "label": "从外观进入动作解释", "move": "in", "provenance": "概念剖切｜结构待确认"},
    {"id": "S04-06", "duration": 16.0, "source": MECH_VIDEO, "title": "压缩 · 开门 · 推出", "label": "机械动作概念预演｜结构待确认", "type": "video"},
    {"id": "S07", "duration": 5.0, "source": GENERATED / "storyboard-v001" / "S07-organized-output-v002.png", "title": "从松散体积，到规整单元", "label": "空间被重新组织", "move": "out", "provenance": "概念视觉"},
    {"id": "S08", "duration": 2.0, "source": WEBSITE / "010-1790553932266631.jpg", "title": "", "label": "官网产品素材", "move": "in", "provenance": "官网授权素材"},
    {"id": "S09", "duration": 2.0, "source": WEBSITE / "025-1790490274674288.jpg", "title": "从现场，到交付", "label": "分析现场 · 匹配方案", "move": "out", "provenance": "官网授权素材"},
    {"id": "S10", "duration": 5.0, "source": GENERATED / "storyboard-v001" / "S08-final-wipe-v002.png", "title": "把体积，变成效率", "label": "www.jenailv.net", "move": "out", "logo": True, "provenance": "概念视觉"},
]'''
source = source[:start] + shots + source[end:]

source = source.replace('"start": 17.0, "end": 33.0', '"start": 12.0, "end": 28.0')
source = source.replace('adelay=17000|17000', 'adelay=12000|12000')
source = source.replace('"-t", "55"', '"-t", "42"')
source = source.replace('duration = 55.0', 'duration = 42.0')
source = source.replace('np.arange(0.8, 54.0, 1.5)', 'np.arange(0.8, 41.0, 1.5)')
source = source.replace('(5.0, 11.0, 17.0, 33.0, 40.0, 45.0, 51.0)', '(3.0, 6.0, 10.0, 12.0, 28.0, 33.0, 35.0, 37.0)')
source = source.replace('"procedural temporary industrial bed plus v006 temporary mechanical sound"', '"42-second procedural temporary industrial bed plus v006 temporary mechanical sound"')

target_path.write_text(source, encoding="utf-8")
print(target_path)
