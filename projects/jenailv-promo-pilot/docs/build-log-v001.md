# 制作记录 v001

## 2026-10-21：D2竖屏动态分镜

- 用户确认后续只制作9:16，横屏早期草稿保留为历史候选，不再迭代。
- 输入：`references/website/download-manifest-v001.csv`中的官网授权图片；使用顺序固化在`tools/build-animatic-v001.py`的`SHOTS`数组。
- 制作：Pillow生成10张独立竖屏镜头卡，FFmpeg 9.0.1编码各段并无重编码拼接。
- 准确命令：`C:\Users\76797\Desktop\chatgpt\aivideo\ComfyUI_windows_portable\python_embeded\python.exe -B -X utf8 projects\jenailv-promo-pilot\tools\build-animatic-v001.py`
- 输出：`outputs/animatic-v001/jenailv-animatic-v001-1080x1920-24-silent.mp4`
- SHA256：`039F518C70E3B8B3461561891B5091F361919A4D600CEA99DECD18D40135FD5B`
- 技术探测：H.264、1080×1920、24fps、1320帧、55.000秒、无音轨。
- 生成调用：无；未启动ComfyUI，未使用GPU，未产生费用。

审查状态：技术渲染通过；S03和S05竖屏关键卡已人工查看并调整长标题换行。尚未完成55秒连续节奏、声音、机械动作或独立盲审，因此不标记为视觉/运动/声音通过。

当前限制：全部运动仍为镜头时长占位；官网静态图不能证明上料、压缩、捆扎和出包动作。D3需连续实拍、CAD/三视图或明确授权使用的概念灰模。

## 2026-10-21：D3 Blender机械预演v002

- 目标：用可编辑三维灰模验证“进料 → 压缩 → 开门 → 出包”的空间关系与镜头运动，替代PPT式静态卡片。
- 工具：Blender 4.2.23，`BLENDER_WORKBENCH`，本地CPU/GPU具体分工未知；脚本由Python实现。
- 准确命令：`C:\Users\76797\Desktop\chatgpt\aivideo\tools\blender\blender-4.2.23-windows-x64\blender.exe --background --factory-startup --python C:\Users\76797\Desktop\chatgpt\cinematic-lab\projects\jenailv-promo-pilot\tools\blender-baler-demo-v002.py`
- 脚本：`tools/blender-baler-demo-v002.py`
- 输出视频：`outputs/blender-demo-v002/jenailv-baler-concept-v002-720x1280.mp4`
- 可编辑工程：`outputs/blender-demo-v002/jenailv-baler-concept-v002.blend`
- 视频SHA256：`5D708F84B3A5335068979B0E04F838D2B0DE71BA7DC555D0208BB7B1A2AD2771`
- 技术探测：H.264、720×1280、24fps、240帧、10.000秒、无音轨。
- 状态段：约0–2.5秒进料；2.5–6.5秒压板下行与料块收缩；6.5–10秒闸门开启、成品包显现并输出。
- 生成调用：无；未启动ComfyUI；未调用外部付费视频模型。

审查状态：抽查1.0、3.0、5.5、7.5、9.5秒画面，主体在9:16安全区内，四个机械状态可辨识，较v001去除地面说明牌并扩大环境交代。运动通过“概念预演”门禁；产品结构准确性、材质写实、完整连续看片、声音和独立盲审仍未通过。

已知限制：灰模根据官网外观与宣传需求抽象构建，没有CAD、液压原理图、精确尺寸或工程师确认。压缩过程是叙事可视化，不可作为设备内部结构、性能或安全操作证明。

## 2026-10-21：D3.1 独立审评与机械预演v003

- 独立审评结论：有条件通过。样张已摆脱PPT感；v002流程顺序可辨，但连续机械因果未达到正式制作门槛。
- 采用配比：A纪实与CG混合60%–70%；B英雄镜头20%–25%；C工程可视化10%–15%，且在CAD或工程师确认前冻结具体内部结构声明。
- v003修正：增加压缩中间态；成品包由小到大连续形成；出口门于第145–170帧开启；独立推出板与推杆于第176帧接触料包，至第226帧共同移动。
- 准确命令：`C:\Users\76797\Desktop\chatgpt\aivideo\tools\blender\blender-4.2.23-windows-x64\blender.exe --background --factory-startup --python C:\Users\76797\Desktop\chatgpt\cinematic-lab\projects\jenailv-promo-pilot\tools\blender-baler-demo-v003.py`
- 输出：`outputs/blender-demo-v003/jenailv-baler-concept-v003-720x1280.mp4`
- 可编辑工程：`outputs/blender-demo-v003/jenailv-baler-concept-v003.blend`
- SHA256：`21952A9C1B79607BE5D50BBDA487FCDDDB868A0F12FD56748C3015090C885CA8`
- 技术探测：H.264、720×1280、24fps、240帧、10.000秒、1,375,464字节、无音轨。
- 抽查：1.0、4.5、5.5、6.8、7.3、8.5、9.5秒，并由Python生成联系表。

审查状态：v003针对评审指出的“状态跳变”和“出包驱动力缺失”完成概念层修正。完整连续播放、真实产品结构、材质、声音和品牌方安全复核仍待完成，因此不标记为可发布。

## 2026-10-21：D4 电影化风格样张

- 工具：Codex内置ImageGen；模型版本、种子、采样器等服务端参数未返回，记为未知。
- 输入顺序：官网设备图`010` → 厂房图`025` → 成品料包图`016`。
- 输出：A纪实电影与CG、B高端工业英雄镜头、C工程可视化，共三张9:16候选；准确提示词、哈希和边界记录在`docs/style-direction-v001.md`。
- Python：`tools/build-style-contact-sheet-v001.py`生成三图对照联系表。
- 共同限制：生成图中的设备细节均可能失真；不生成或采用品牌字、型号、认证、参数和控制界面文字。
