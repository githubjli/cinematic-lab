# 工具选型补充 v006

更新日期：2026-10-14。本版新增Vibe Knowledge Film；其他工具继续参考v005、`tool-selection-v001.md`和最新数学/技巧文档。

| 工具/资源 | 需求出现时考虑 | 输入→输出 | 本地与许可状态 | 关键边界 |
|---|---|---|---|---|
| Vibe Knowledge Film | 无旁白、16:9、字幕驱动的知识短片 | 题目/文案→事实表、分镜、Canvas工程、程序音效、MP4 | [官方仓库](https://github.com/HeyChengC/vibe-knowledge-film)；引擎/脚本/方法MIT；本地保存`62d5150`；未安装/运行 | 参考片内容和部分示例排除在MIT之外；只支持两类风格和16:9；需Chrome、Playwright、FFmpeg、NumPy/SciPy/Pillow |
| Remotion＋SVG | 参数化科普与竖屏/横屏多规格 | facts/镜头JSON/React组件→视频 | 既有候选 | 更适合组件化产品工程；事实与声音仍需独立控制 |
| Manim＋SymPy | 公式和数学推演为主 | 符号表达/场景代码→动画 | 既有候选 | 生活寓言、复杂声音和剪辑需另做 |

选择建议：需要“无旁白＋底部字幕＋画面把动词演出来”时优先研究Vibe Knowledge Film；需要竖屏、React组件生态或多规格输出时优先Remotion；公式变换占主导时优先Manim。是否安装要根据实际题材、Windows兼容性和所需交付再决定。
