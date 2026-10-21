# 金耐力工业宣传片流程测试

状态：方案与制作契约已建立，尚未进行付费生成、GPU生成或成片渲染。

本项目以[金耐力官网](https://www.jenailv.net/)公开内容为研究输入，测试“事实核验 → 工业视觉设计 → 最难镜头Demo → 全片制作 → 独立盲审”的本地宣传片流程。官网文字和图片只作为内部分析参考；正式公开使用前仍需品牌方确认事实、商标、图片、视频、CAD和音乐等权利。

## 当前文件

- [制作方案 v001](planning/production-plan-v001.md)
- [镜头表 v001](planning/shotlist-v001.csv)
- [资产清单 v001](planning/asset-manifest-v001.csv)
- [官网快照来源记录](references/website/source-manifest-v001.md)
- [独立审评空白模板](reviews/review-template-v001.json)

## 当前结论

主片建议做成55秒、16:9、24fps的工业品牌片，以“松散废料被压缩成标准料包”为唯一视觉机制。首轮只制作10–12秒的高风险段：真实上料 → 液压压缩结构可视化 → 规整料包输出。该段通过质量门禁后再扩展全片和9:16版本。

本项目可读取同级`aivideo`中的已验证本地环境，但不修改该仓库。角色镜头脚本`shot.py`不是本案直接入口；优先复用其中的Blender、FFmpeg、ComfyUI基线、哈希和验收方法，并为工业片另写镜头契约。
