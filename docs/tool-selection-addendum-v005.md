# 工具选型补充 v005

更新日期：2026-10-14。本版在v004基础上新增声音库、场景灰模、B-roll工程和数据驱动科普动画候选。需同时参考`tool-selection-v001.md`、`math-tool-selection-v002.md`和`workflow-techniques-v003.md`。未声明安装或付费授权。

| 工具/资源 | 优先需求 | 输入→输出 | 本地与许可状态 | 关键边界 |
|---|---|---|---|---|
| Microsoft CLAP | 音效语义检索、自动描述 | 音频/文字→嵌入、相似度、描述 | [官方仓库](https://github.com/microsoft/CLAP)，MIT；未安装 | 检索模型，不生成声音；中文效果与权重条件需实测 |
| AudioCraft AudioGen | 本地文本生成短音效 | 描述/时长/种子→音频候选 | [官方文档](https://github.com/facebookresearch/audiocraft/blob/main/docs/AUDIOGEN.md)；未安装；代码MIT、权重CC-BY-NC 4.0 | medium文档建议至少16GB GPU；权重不默认可商用 |
| AudioLDM | 文本/参考音频生成与转换 | 描述或音频→候选音频 | [官方仓库](https://github.com/haoheliu/AudioLDM)；未安装 | 检查点许可另核；生成必须听审 |
| FFmpeg＋SQLite | 本地音效库最小底座 | 文件→元数据、代理、裁切、索引 | FFmpeg已用于分析；数据库未实现 | 不做语义/审美判断；原件只读 |
| Blender/Three.js灰模 | 固定场景空间与摄影机 | 平面/参考→低模空间、相机截图 | 既有候选；本案例未运行 | 灰模不证明材质、物理和最终画面通过 |
| Erduo B-roll Loop Engineering | SRT驱动口播B-roll多阶段生产 | SRT/design/素材→逐镜源码、媒体、预览和审查记录 | [MIT开源](https://github.com/erduo1998-cell/erduo-broll-loop-engineering)；未安装 | 官方列Windows未验证；HyperFrames/Remotion路径不同；重型流程 |
| Remotion | 参数化科普、帧级声画编排 | facts/镜头JSON/组件/音频→MP4 | 案例023容器记录4.0.529；本项目未复现 | 元数据只证明渲染器；数学和审美另验收 |
| Manim＋SymPy | 公式推导与数学动画 | 符号表达/场景代码→动画 | 既有数学工具候选 | 历史叙事、配音和最终剪辑需另接 |

本地音效库首选先实现FFmpeg＋SQLite＋文本标签，再加CLAP，最后才加音频生成模型。科普片首选用结构化事实驱动SVG/Remotion或Manim，不把关键数字交给图像/视频生成模型自由绘制。
