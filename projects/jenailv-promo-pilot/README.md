# 金耐力工业宣传片流程测试

状态：方案与制作契约已建立；用户已确认官网素材获授权用于本案例。16秒Blender机械视频样镜v004和两个本地Wan2.2受控写实化对照已完成；Blender版本可作概念动作交付，Wan候选尚未通过物料身份和写实质量门禁。55秒最终成片尚未制作。

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
- [连续故事分镜 v001](planning/continuous-storyboard-v001.md)
- [连续故事分镜数据表](planning/continuous-storyboard-v001.csv)
- [连续分镜独立评审 v001](reviews/independent-storyboard-review-v001.md)
- [物料身份卡 v001](docs/material-identity-v001.md)
- [S07→S08独立连续性复核 v002](reviews/independent-s07-s08-continuity-review-v002.md)
- [视频样镜审查 v001](reviews/video-sample-review-v001.md)
- [视频样镜独立评审 v001](reviews/independent-video-sample-review-v001.md)

## 当前结论

主片按用户确认只制作9:16工业品牌片，以“同一批松散废料从混乱进入生产线，经过连续压缩与受力推出，成为规整料包”为连续故事。Blender v004已完成16秒连续机械样镜并加入临时声轨。Wan2.2 Canny控制可跟随几何，但5B模型未锁住料包身份；下一步优先以确定性三维材质完成真实料包，再将生成限制在厂房、光线和表面细节层。

本项目可读取同级`aivideo`中的已验证本地环境，但不修改该仓库。角色镜头脚本`shot.py`不是本案直接入口；优先复用其中的Blender、FFmpeg、ComfyUI基线、哈希和验收方法，并为工业片另写镜头契约。
