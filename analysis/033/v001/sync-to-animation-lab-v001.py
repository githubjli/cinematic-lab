"""User-authorized, versioned case033 reference handoff to animation-lab.

Copies bytes, verifies SHA-256, rejects conflicting existing snapshot files.
Target episode production files are not modified. Existing entry text is appended.
"""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT.parent / 'animation-lab'
PACK = TARGET / 'references/case033/v001'
if TARGET.resolve() != Path('C:/Users/76797/Desktop/chatgpt/animation-lab').resolve():
    raise RuntimeError('Unexpected target workspace')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

files = []
for folder in ('analysis/033/v001', 'knowledge/production-methods/PM-033', 'references/033'):
    for source in sorted((ROOT/folder).rglob('*')):
        if source.is_file() and '__pycache__' not in source.parts and source != Path(__file__).resolve():
            relative = source.relative_to(ROOT)
            dest = PACK/relative
            if dest.exists() and sha(dest) != sha(source):
                raise RuntimeError(f'Conflicting snapshot, create v002: {dest}')
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                shutil.copyfile(source, dest)
            if sha(dest) != sha(source):
                raise RuntimeError(f'Copy mismatch: {relative}')
            files.append({'path':relative.as_posix(),'sha256':sha(source),'bytes':source.stat().st_size})

def create(path, text):
    if path.exists() and path.read_text(encoding='utf-8') != text:
        raise RuntimeError(f'Refusing overwrite: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')

create(PACK/'.gitignore', '*.mp4\n*.png\n*.jpg\n*.jpeg\n*.log\n__pycache__/\n')
create(PACK/'.gitattributes', '* -text whitespace=cr-at-eol\n')
create(PACK/'README.md', '''# 案例033 动画制作参考交接包 v001

2026-11-13，用户明确要求从cinematic-lab同步至animation-lab。来源仓库：https://github.com/githubjli/cinematic-lab.git 。来源为案例033/故事看板v001；目录内保留来源结构及字节，source-manifest.json记录拷贝哈希。

## 内容入口

- [研究入口](analysis/033/v001/README.md)
- [导演、节奏、分镜细节](analysis/033/v001/directing-and-story.md)
- [动画工序推断](analysis/033/v001/production-inference.md)
- [看板说明](analysis/033/v001/storyboard-board-notes.md)
- [高清20格看板](references/033/storyboard-v001/case033-storyboard-board-v001.png)
- [看板预览](references/033/storyboard-v001/case033-storyboard-board-v001-preview.jpg)
- [原片与来源哈希](references/033/provenance.json)
- [对animation-lab的应用说明](../../../knowledge/experiments/CASE033-animation-reference-v001.md)

原片、抽帧和看板均已复制到此包，媒体只留本地；Git保存文档、脚本、标注、命令和哈希。来源文件中的cinematic-lab路径是历史记录，不伪装成新的实验运行；本地路径以本包结构为准。

## 边界及重建

导演思路与工序为S1研究推断，作者模型、软件、提示词未知；未完成连续运动及听审，不是已验证生产方案。片内文字只作研究材料。没有修改E001-wait，没有调用生成或付费服务。

重建看板使用本包analysis/033/v001/build-storyboard-board.py及标注JSON，需要Pillow、微软雅黑和FFmpeg。未复制/安装运行环境；可通过环境变量FFMPEG_EXE指定已有FFmpeg路径，默认cinematic-lab内.tools路径在本包中不存在。重建会刷新本包派生图和清单，应先复制新版本，保留当前参考包。
''')
create(TARGET/'knowledge/experiments/CASE033-animation-reference-v001.md', '''# 案例033：导演与动画制作参考 v001

2026-11-13。来源：[独立交接包](../../references/case033/v001/README.md)。仅参考研究，不改变本项目30秒原创短片目标、现有首集v0.1或Michelin基准；新视觉资产状态不因同步发生变化。

## 可采用的设计思路

1. 先明确角色目标、资源和盲点，让角色功能互补。参考中的女孩/猫/狗是案例人物，不搬入原创首集；两角色短片无需强加第三人。
2. 按观众知情顺序安排建立、原因细节、行动与反应；每个反应镜头要增加信息或情绪，而不是只换一张脸。
3. 高潮让角色自己决定。对《别坐下！》可检查误解、发现与帮助是否来自看得见的行为，暂不改写原故事。
4. 以真实对白草轨和动态分镜计时；复杂接触拆为可读的起势、接触、结果，保留反应留白，避免短镜头堆动作。
5. 镜头制作前固定人物/场景/道具，逐镜记录参考职责、初末态、实际输入与候选；提交文本只保留本镜必要约束。

## E001可做的下一轮检查（候选，未执行）

- 用当前镜头稿标出观众何时看清湿漆/警示牌、角色何时知道；区分角色误解与观众困惑。
- 检查S05与S07的多动作负担；先做计时预演，不因案例好看而增加对白、镜头或时长。
- 在8镜故事板中分别标注景别、表情、接触、对白、观众新增信息及关系末态。若改稿，新建版本并复核manifest和下游生成包。

## 制作与质量边界

参考具三维动画观感，但传统三维、AI逐镜、混合制作均可能，原工具未知。近景、插入和反应镜头可作为生产设计备选，不宣称作者为规避AI缺陷而使用。不可把两集约10分钟的方法不加裁剪塞进30秒。

已存在并可查看：两份原片副本、抽帧、20格看板、分析、哈希及重建代码。已检查：技术规格、抽样画面字幕、看板版式；未完成：全片连续运动、声音及本项目复现。脚本运行/文档复制不等于叙事或动画质量通过。此经验保持研究级，按既有QUALITY-STANDARD与PIPELINE验证后再升级。
''')

entries = {
 'README.md': '\n## 新增动画研究参考（2026-11-13）\n\n- [案例033：双集角色喜剧与20格故事看板](references/case033/v001/README.md)；[对首集的适用与限制](knowledge/experiments/CASE033-animation-reference-v001.md)。已同步实际参考文件，制作流程为推断，不代表新动画已生成。\n',
 'START-HERE.md': '\n## 参考同步里程碑（2026-11-13）\n\n已按用户明确要求接收cinematic-lab案例033 v001，见[交接包](references/case033/v001/README.md)与[应用说明](knowledge/experiments/CASE033-animation-reference-v001.md)。包含两份原片、关键帧、20格看板及制作研究，文件复制经SHA-256校验。源动画工具未知，连续音画未审；未改E001、未生成新资产、未开展付费提交。后续可检查知情顺序、角色自主选择与反应留白，再按现有门禁推进。\n'
}
for name, addition in entries.items():
    path = TARGET/name
    original = path.read_text(encoding='utf-8')
    if addition.strip() not in original:
        path.write_text(original+addition,encoding='utf-8',newline='\n')

manifest = {'date':'2026-11-13','source_workspace':str(ROOT),'target_workspace':str(TARGET),
            'scope':'case033 v001 and storyboard v001; user-authorized sibling synchronization',
            'source_basis_commit':'5e84fb1','additional_change':'FFMPEG_EXE environment override for portable rebuild',
            'files':files,'verified_file_count':len(files),'verified_bytes':sum(x['bytes'] for x in files)}
(PACK/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pack':str(PACK),'verified_files':len(files),'bytes':manifest['verified_bytes']},ensure_ascii=False))
