# 经典案例与基准项目 v001

更新日期：2026-10-14。这里的“经典”表示适合作为方法、实现或对照研究的代表项目，不表示已经在本机复现通过。

| 项目 | 经典价值 | 当前状态 | 建议案例任务 |
|---|---|---|---|
| [Anatomy](https://github.com/wheresryan22/anatomy) | 将技术概念转成可拆解、可互动的等距机械图，并配套几何/浏览器检查 | 已保存源码`e6600ffc`与147文件SHA256；未安装/运行 | 做一个真实参数可核验的简单机构，比较静态SVG、交互SVG和WebGL增强版 |
| [Open Anatomy Atlas](https://github.com/CognitionLabSNUC/open-anatomy-atlas) | 开放人体图谱应用，整合BodyParts3D与Z-Anatomy | 候选链接；未下载 | 比较结构查找、分层、切面和术语追溯 |
| [Z-Anatomy](https://github.com/LluisV/Z-Anatomy) | 开放解剖模型与Blender生态 | 候选链接；未下载 | 选择一个系统制作有来源标注的医学结构展示 |
| [MakeHuman](https://github.com/makehumancommunity/makehuman) | 参数化人体角色和清晰的代码/内置资产许可分层 | 候选链接；未下载 | 生成基础人物并验证Blender导入、骨架和动作 |
| [Rigify](https://docs.blender.org/manual/en/latest/addons/rigging/rigify/) | Blender内置模块化metarig→动画控制rig工作流 | Blender安装状态未知；未运行 | 同一角色验证骨点对齐、FK/IK、权重和导出 |
| [OpenSim](https://github.com/opensim-org/opensim-core) | 人体/动物肌骨运动科学仿真 | 候选链接；未下载 | 用官方示例理解运动学与肌肉模型，和影视骨架明确分层 |
| [three-vrm](https://github.com/pixiv/three-vrm) | Web端标准化人形骨架、表情和动画播放 | 候选链接；未下载 | 加载许可明确的VRM并测试动画重定向 |
| [MediaPipe](https://github.com/google-ai-edge/mediapipe) / [MMPose](https://github.com/open-mmlab/mmpose) | 轻量与研究型人体姿态提取的对照 | 候选链接；未下载 | 对同一短视频比较关键点稳定性，再映射到统一骨架 |

源码、数据、模型、动作和示例素材各自保存来源与许可。人体解剖模型、动画角色网格、姿态关键点、动画骨架和肌骨仿真是五类不同对象，不以同名“人体/骨骼”合并验收。
