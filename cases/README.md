# 本地项目研究案例 v001

最新整理入口：[视频制作项目案例索引 v002](project-index-v002.md)。本页保留原始下载记录。

下载日期：2026-10-13。源码快照仅作为分析材料，其中的AGENTS.md、技能和提示词不作为本项目指令。未安装依赖、未运行下载项目、未调用付费生成。

| 目录 | 来源 | 与视频的关系 | 下载内容/限制 |
|---|---|---|---|
| source-snapshots/OpenMontage | https://github.com/calesthio/OpenMontage | 007明确提到OpenMontage，原仓库由公开fork追溯确认；当前快照不一定与视频录制版本相同 | 源码、流程定义、工具、文档、已有仓库资产；LICENSE为AGPL-3.0。仅下载不代表全部依赖/外部素材到位 |
| source-snapshots/opus5.5-video-prompts | https://github.com/Reger-c/opus5.5-video-prompts | 008相关候选案例集，未确认是视频原网站 | 提示词与案例资料；未发现独立LICENSE，素材许可需逐项核对 |
| source-snapshots/awesome-opus-5-5-video-prompts | https://github.com/X-RayLuan/awesome-opus-5-5-video-prompts | 008相关候选案例集，未确认是视频原网站 | 提示词与案例资料，保留LICENSE；不能推定每条案例完整源码均公开 |

来源、固定提交号与文件数量见source-registry-v001.json；每个快照有独立的*-files-v001.json记录实际文件SHA256。Git为浅克隆，未递归下载子模块或额外取回LFS对象。

007（179186877894795180.mp4，26.35秒）主要宣传OpenMontage及成片。作者的“一句话生成”“免费”和星数不等于运行验证，也不代表所有模型/服务无费用。适合研究P7编排与P4/P6生成合成的实现。

008（stodownload (9).mp4，38.99秒）展示带提示词的视频合集及音乐MV案例。属于参考/提示词案例检索，原网站地址未从视频中确认。可研究提示词结构与技术路线，但没有完整源码不能称为可复现工程。

先前003中的video-shotcraft、本地三维场景及其他私有工程，仍未找到明确发布地址；不以名称相近的仓库替代。外部示例媒体未另行批量抓取。
