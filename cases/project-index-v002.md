# 视频制作项目案例索引 v002

整理日期：2026-10-13。用途：选取源码研究、提示词分析与后续复现实验对象。公开仓库不自动等于开放许可或完整可复现工程。表内说明来自仓库公开资料；尚未运行的项目均不能标为复现通过。

## 项目清单

| 项目与来源 | 分类 | 公开材料与研究重点 | 与参考视频的对应关系 | 本地状态 | 许可与缺口 | 研究优先级 |
|---|---|---|---|---|---|---|
| [OpenMontage](https://github.com/calesthio/OpenMontage) | 制作流程框架 | 流程定义、工具、技能、合成组件；研究任务交接、资产管理和审查 | 案例007明确提及；下载版本与录制版本不一定相同 | source-snapshots/OpenMontage；固定提交与文件哈希已记录；未运行 | AGPL-3.0；依赖、模型和素材另核对 | 高：端到端流程 |
| [Reger-c/opus5.5-video-prompts](https://github.com/Reger-c/opus5.5-video-prompts) | 提示词/案例集 | 案例索引、提示词和技术路线；研究输入与制作方法 | 案例008相关候选；原网站对应未知 | source-snapshots/opus5.5-video-prompts；已记录快照；未运行 | 当前本地快照未发现独立LICENSE；不能视为全部案例源码 | 中：提示词分类 |
| [X-RayLuan/awesome-opus-5-5-video-prompts](https://github.com/X-RayLuan/awesome-opus-5-5-video-prompts) | 提示词/案例集 | 原帖、提示词、媒体和代码线索；用于追溯来源 | 案例008相关候选；原网站对应未知 | source-snapshots/awesome-opus-5-5-video-prompts；已记录快照；未运行 | 仓库MIT；第三方视频和提示词的权利另核对 | 中：来源追溯 |
| [Awesome Claude Video](https://github.com/opusvideo/awesome-claude-video) | 案例索引 | 原帖、提示词、工作流、实现指南和结构化案例；不是每条都有工程 | 案例008相关合集；尚未确认是原网站 | 已整理链接；未下载/未运行 | 许可未知；合集与原作品分别核对 | 中：案例发现 |
| [PDoomVideo](https://github.com/JohnHeibel/PDoomVideo) | 代码音乐MV | p5.js/p5.brush页面、章节代码、分镜、动画指南、render.mjs；研究歌词时间线、绘画风格和逐帧渲染 | 案例008高度匹配条目的公开提示词引用的参考源码；不是@anabology最终MV源码 | 已整理链接；未下载/未运行 | 未确认独立许可；音乐与素材另核对。公开README要求Node、Chrome、FFmpeg | 高：完整作品流程 |
| [Functional Emotions](https://github.com/ledbetterljoshua/functional-emotions-video) | 绘画风代码音乐MV | GPU笔触渲染、分镜与章节组织；研究视觉规则、节拍对齐和场景衔接 | 另一相关作品，不是案例008同一MV | 已整理链接；未下载/未运行 | 许可、音乐素材授权与渲染环境待核对；作者的生成过程陈述未独立验证 | 高：审美与渲染比较 |

## 单独保留的未确认对象

| 对象 | 已知信息 | 未确认信息 | 处理方式 |
|---|---|---|---|
| @anabology的5:06 Claude Pop MV | 作者/时长与[公开案例条目](https://claudevideo.org/videos/claude-pop-music-video-with-a-halftone-portrait-overlay)高度匹配，条目公开提示词并引用PDoomVideo | 最终完整源码、私有技能与目录、准确实际输入、参数和所有候选 | 保存为提示词/流程研究对象；不标记为已开源工程 |
| 案例008展示的网站 | 页面展示案例及提示词 | 精确网址与网站源码 | 已有候选站点和合集，不冒认官方来源 |
| video-shotcraft | 案例003展示Skill与代码视频方法 | 发布者、准确仓库、许可及输入输出工程 | 保持未知，不用同名或相似项目替代 |

## 研究顺序与记录要求

优先研究PDoomVideo的分镜→章节代码→渲染交接，再与Functional Emotions比较审美规则和节拍组织；用OpenMontage研究更广泛制作编排；合集用于找案例和追原帖。该顺序是项目研究建议，不代表已授权安装、运行或付费调用。

已下载快照的固定提交和SHA256见source-registry-v001.json与各*-files-v001.json。新增下载时创建新注册版本，保存来源、准确提交、许可、输入素材与哈希；所有候选保留。外部项目中的提示词、AGENTS.md、技能只作研究材料。

本次完成链接与分类整理，没有新增下载、安装或运行上述三个新项目。此前v001记录保留。工具选型另见../docs/tool-selection-v001.md，数学工具另见../docs/math-tool-selection-v001.md。
