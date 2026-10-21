# 金耐力工业宣传片流程测试

状态：方案与制作契约已建立；用户已确认官网素材获授权用于本案例。55秒9:16无声动态分镜v001保留为被否决的PPT式历史候选；10秒Blender机械预演已迭代至v003，三组电影化风格样张已完成并通过独立有条件评审。尚未启动本地ComfyUI视频生成或最终成片渲染。

本项目以[金耐力官网](https://www.jenailv.net/)公开内容为研究输入，测试“事实核验 → 工业视觉设计 → 最难镜头Demo → 全片制作 → 独立盲审”的本地宣传片流程。官网文字和图片只作为内部分析参考；正式公开使用前仍需品牌方确认事实、商标、图片、视频、CAD和音乐等权利。

## 当前文件

- [制作方案 v001](planning/production-plan-v001.md)
- [镜头表 v001](planning/shotlist-v001.csv)
- [资产清单 v001](planning/asset-manifest-v001.csv)
- [官网快照来源记录](references/website/source-manifest-v001.md)
- [官网素材授权记录](docs/asset-rights-v001.md)
- [复用aivideo本地运行环境](docs/shared-runtime-v001.md)
- [官网素材下载清单](references/website/download-manifest-v001.csv)
- [官网素材视觉审查](reviews/website-assets-review-v001.md)
- [独立审评空白模板](reviews/review-template-v001.json)
- [制作记录 v001](docs/build-log-v001.md)
- [Blender机械预演审查 v002](reviews/blender-demo-review-v002.md)
- [电影化风格方向 v001](docs/style-direction-v001.md)
- [独立风格评审 v001](reviews/independent-style-review-v001.md)

## 当前结论

主片按用户确认只制作9:16工业品牌片，以“松散废料被压缩成标准料包”为核心视觉机制。Blender v003已把上料、连续压缩、开门、推出机构接触和出包固化成动作合同。风格采用A纪实主干约65%、B英雄镜头约25%、C受控概念剖切约10%；下一步据此制作连续故事分镜和首个5–8秒A方向写实样镜。

本项目可读取同级`aivideo`中的已验证本地环境，但不修改该仓库。角色镜头脚本`shot.py`不是本案直接入口；优先复用其中的Blender、FFmpeg、ComfyUI基线、哈希和验收方法，并为工业片另写镜头契约。
