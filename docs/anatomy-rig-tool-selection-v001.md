# 人体解剖模型与动画骨骼开源项目选型 v001

更新日期：2026-10-14。用途：为科学可视化、人体角色、骨骼绑定、动作捕捉和动画重定向选择开源参考。项目代码、模型数据、预训练权重、示例资产与输出许可分别核对；“能打开”不等于解剖、蒙皮或动作通过审查。

## 选型表

| 项目 | 类别 | 最适合的任务 | 输入→输出 | 许可与状态 | 主要限制 |
|---|---|---|---|---|---|
| [Open Anatomy Atlas](https://github.com/CognitionLabSNUC/open-anatomy-atlas) | 交互式3D人体解剖图谱 | 教学、结构检索、系统剥离、切面观察和测验 | BodyParts3D/Z-Anatomy数据→可旋转、点选和切面的桌面/网页图谱 | 应用代码MIT；数据许可独立；未下载/运行 | 医学显示优先，不是动画角色网格；需同时引用软件和数据来源 |
| [Z-Anatomy](https://github.com/LluisV/Z-Anatomy) | 开放人体解剖模型/图谱 | 器官、肌肉、神经、血管等分层结构与术语参考 | 解剖网格/命名→Blender/图谱资产 | 模型主要为CC BY-SA 4.0，并继承BodyParts3D来源要求；未下载 | ShareAlike与署名要求；密集分件不等于可变形蒙皮；医学正确性需版本核验 |
| [BodyParts3D](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html) | 人体结构数据集 | 成人男性全身结构、FMA术语和高/低分辨率网格 | 数据集→解剖表面模型 | 数据许可按DBCLS发布条款核对，常见为CC BY-SA 2.1 Japan | 是数据源，不是完整制作软件；人群代表性和版本范围有限 |
| [OpenSim](https://github.com/opensim-org/opensim-core) | 肌骨动力学与生物力学仿真 | 关节、肌肉、步态和运动学/动力学研究 | 肌骨模型、运动/力数据→仿真和分析 | 核心Apache-2.0；模型/插件各自许可；未下载 | 科学仿真，不负责影视角色外观；模型假设和实验数据决定可信度 |
| [MakeHuman](https://github.com/makehumancommunity/makehuman) | 参数化人体角色生成 | 生成可绑定/可导出的基础人体角色，供Blender与动画试验 | 身体参数、资产和骨架→角色网格/导出文件 | 程序AGPL；官方内置图形资产CC0；第三方资产另查；未下载 | 不是医学解剖图谱；面部、衣物、拓扑和目标平台骨架需实际检查 |
| [Rigify](https://docs.blender.org/manual/en/latest/addons/rigging/rigify/) | Blender自动绑定系统 | 给人物/动物建立控制器、FK/IK和变形骨骼 | 调整后的metarig→控制/机制/变形rig | Blender内置，GPL；未运行 | 需要手工对齐骨点、权重和变形修正；生成rig不等于动画可直接复用 |
| [three-vrm](https://github.com/pixiv/three-vrm)＋[VRM Animation](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm_animation-1.0/README.md) | Web端人形骨架与动画标准 | Three.js加载VRM、表情、视线、骨骼控制及跨角色动画 | VRM/glTF模型和动画→WebGL角色播放 | three-vrm MIT；具体VRM模型与动作许可另查；未部署 | 适合标准化人形，不解决建模/权重质量；重定向仍受rest pose和比例影响 |
| [MediaPipe Pose](https://github.com/google-ai-edge/mediapipe) | 轻量人体姿态估计 | 从单人视频提取实时/近实时姿态关键点 | 图像/视频→2D/3D姿态landmarks | 代码Apache-2.0；具体任务模型包再核对；未部署 | 关键点不是动画；遮挡、快速运动、多人和深度会出错，模型包再分许可 |
| [MMPose](https://github.com/open-mmlab/mmpose) | 研究型姿态估计工具箱 | 比较多人、手、脸、全身等模型和数据集 | 图像/视频、模型配置→关键点/评测 | 代码Apache-2.0；权重/数据集各自条款；未部署 | 环境较重；需要选择模型和格式；输出必须清洗、跟踪和重定向 |
| [Godot Skeleton3D](https://docs.godotengine.org/en/stable/classes/class_skeleton3d.html) | 实时骨骼播放/重定向/布娃娃 | 在开源引擎中驱动3D角色、共享动画和物理骨骼 | glTF骨架/动画→实时角色 | Godot MIT；角色和动作资产另查；未部署 | 是运行时骨架系统，不生成角色或动作；不同rest pose需要重定向配置 |

MB-Lab可作为Blender参数化人物的次级候选，但在正式选型前应固定维护中的准确仓库、Blender兼容版本及代码/输出许可，不与MakeHuman的CC0输出政策混用。

## 按需求选择

| 目标 | 优先组合 | 不应混淆 |
|---|---|---|
| 人体器官/肌肉教学互动 | Open Anatomy Atlas＋Z-Anatomy/BodyParts3D | 不把解剖分件网格直接当可动画角色 |
| 关节和肌肉运动科学 | OpenSim＋实验/文献数据 | 不把影视骨骼动画当生物力学结论 |
| 创建可动画基础人物 | MakeHuman→Blender→Rigify | 不把参数化外形当医学准确模型 |
| 网页虚拟人/数字角色 | VRM模型＋three-vrm＋VRM Animation | 模型许可、表情和弹簧骨另查 |
| 从真人视频提取动作 | MediaPipe Pose（轻量）或MMPose（研究/多模型）→清洗→骨骼重定向 | 关键点输出不是动作成品 |
| 游戏/实时角色 | Blender/Rigify制作→glTF→Godot Skeleton3D | 导出骨架、动画轨和引擎rest pose必须对齐 |
| 科普成片 | 解剖/角色资产→Blender/Three.js/Anatomy→Remotion/FFmpeg/剪辑 | 网页交互、实时角色和最终视频是不同交付物 |

## 推荐研究顺序

1. 先用Open Anatomy Atlas在线版评估医学结构、命名和交互，不先下载大型数据。
2. 用MakeHuman＋Rigify做一个低风险基础人物，验证导出、骨架、权重和动作。
3. 用同一段短动作比较MediaPipe Pose与MMPose，记录丢点、抖动、遮挡和重定向误差。
4. 若需要网页展示，再验证three-vrm；若需要肌肉和关节科学结论，再单独进入OpenSim。

正式试验必须保存源视频/模型哈希、骨架定义、rest pose、帧率、尺度、坐标系、重定向映射、滤波参数、所有候选及视觉/运动审查。医学用途还需保存数据版本、术语来源和专业复核状态。
