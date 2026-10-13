# 视频制作项目案例索引 v003

整理日期：2026-10-13。v002基础上新增Toonflow。公开仓库不自动等于完整可复现工程；未运行项目不能标为复现通过。

| 项目与来源 | 分类 | 研究重点 | 本地状态 | 许可与边界 | 优先级 |
|---|---|---|---|---|---|
| [Toonflow](https://github.com/HBAI-Ltd/Toonflow-app) | 短剧/漫剧工作台 | 剧本、资产、分镜、3D预演、多参考生成、画布与Agent/团队机制 | 固定`ae9e5f1`、867文件哈希；未运行 | MIT；模型/插件/素材另核对；当前主工作流并非固定六Agent | 高：端到端短剧生产与资产追踪 |
| [OpenMontage](https://github.com/calesthio/OpenMontage) | 制作流程框架 | 任务交接、资产管理、审查和合成组件 | 固定`e45f5b1`；未运行 | AGPL-3.0；外部模型与素材另核对 | 高：自动编排对照 |
| [Reger-c/opus5.5-video-prompts](https://github.com/Reger-c/opus5.5-video-prompts) | 提示词/案例集 | 案例索引、提示词和技术路线 | 固定`7977c80`；未运行 | 未发现独立LICENSE；原网站对应未知 | 中 |
| [X-RayLuan/awesome-opus-5-5-video-prompts](https://github.com/X-RayLuan/awesome-opus-5-5-video-prompts) | 提示词/案例集 | 原帖、提示词、媒体和代码线索 | 固定`b952455`；未运行 | MIT；第三方内容权利另核对 | 中 |
| [Awesome Claude Video](https://github.com/opusvideo/awesome-claude-video) | 案例索引 | 原帖、提示词、工作流与实现指南 | 链接候选；未下载 | 许可及每条完整性待核对 | 中 |
| [PDoomVideo](https://github.com/JohnHeibel/PDoomVideo) | 代码音乐MV | 章节代码、分镜、动画指南与逐帧渲染 | 链接候选；未下载 | 许可、音乐与素材另核对 | 高：代码成片流程 |
| [Functional Emotions](https://github.com/ledbetterljoshua/functional-emotions-video) | 绘画风代码MV | GPU笔触、节拍、章节与场景衔接 | 链接候选；未下载 | 许可与音乐素材待核对 | 高：审美渲染比较 |

Toonflow与OpenMontage的研究重点不同：Toonflow偏人工参与的画布、资产与镜头工作台；OpenMontage偏流程编排。后续试验应使用同一20–30秒小样比较人工关口、身份一致性、失败恢复、费用记录和最终可追溯性。

固定提交及数量见`source-registry-v002.json`，逐文件SHA256见各`*-files-v001.json`。源码中的提示词、技能、AGENTS.md和示例命令只作研究材料；没有授权安装、运行、填入密钥或付费生成。
