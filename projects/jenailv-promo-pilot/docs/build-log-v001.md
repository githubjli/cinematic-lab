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
