# 开源机械结构与CAD资产库选型 v001

更新日期：2026-10-21。用途：为机械产品片、爆炸动画、工程科普、机器人/载具资产规划和SKY-001式层级结构研究选择参考库。

这里区分三类内容：**现成模型资产**可直接导入修改；**参数化零件库**用代码按尺寸生成；**研究数据集**用于训练、评测或结构分析。软件开源不代表库中每个第三方资产都自动获得相同许可，正式使用仍保存来源、作者、版本和单件许可。

## 首选清单

| 项目 | 类型与内容 | 适合本项目 | 格式/工作流 | 许可与边界 | 优先级 |
|---|---|---|---|---|---|
| [FreeCAD Parts Library](https://github.com/FreeCAD/FreeCAD-library) | 大型社区机械零件库，含轴承、紧固件、齿轮、机电、管件等分类 | 直接找可编辑零件、产品片道具、装配与爆炸图原型 | `.FCStd`＋STEP，部分STL；可进入FreeCAD后导出glTF/Blender | 资产CC BY 3.0，需按git历史/文件属性署名作者；约5GB，不建议无选择全量下载 | **首选现成资产** |
| [NopSCADlib](https://github.com/nophead/NopSCADlib) | OpenSCAD零件、vitamins、打印件、装配与BOM框架 | 3D打印机、机架、皮带、轴承、电机、紧固件和装配步骤 | OpenSCAD源码→STL/渲染/装配图 | GPL-3.0；复用和发布前评估派生作品义务 | **首选机械装配参考** |
| [BOSL2](https://github.com/BelfrySCAD/BOSL2) | 大型OpenSCAD建模库；形状、变换、连接、轴承等 | AI生成可读参数脚本、机械形状与连接系统 | `.scad`参数→网格/动画帧 | BSD-2-Clause；项目仍标Beta，固定版本并跑回归 | **首选代码建模基础** |
| [OpenSCAD MCAD](https://github.com/openscad/MCAD) | 常用机械组件：渐开线/锥齿轮、轴承、电机座、螺母螺栓等 | 快速做机构原理图、低成本机械Demo | OpenSCAD内置/子模块→STL | LGPL-2.1；部分API未稳定，逐文件看作者说明 | 轻量备选 |
| [CadQuery](https://github.com/CadQuery/cadquery)＋[cq_warehouse](https://github.com/gumyr/cq_warehouse) | Python参数化实体与装配；扩展含轴承、链条、紧固件、链轮、螺纹 | 用代码生成高质量STEP、版本化零件、自动做尺寸变体 | Python→STEP/DXF/STL/3MF/glTF | CadQuery Apache-2.0；cq_warehouse许可按所用版本仓库核对；实际标准尺寸仍需工程验证 | **首选Python路线** |
| [PartCAD](https://github.com/partcad/partcad) | 硬件包管理与数字线程；组合CadQuery、OpenSCAD、build123d、FreeCAD等 | 建立`资产树＋BOM＋制造/验证文档`，很接近案例030所需控制层 | 包配置＋代码/STEP等→零件、装配、文档、BOM | 核心Apache-2.0；包内资产许可分别核对 | **首选资产编排** |
| [KiCad Packages3D](https://gitlab.com/kicad/libraries/kicad-packages3D) | 官方电子元件三维模型，覆盖连接器、IC、开关、电池等 | PCB、电子设备内部结构、科技产品爆炸图 | STEP 1:1毫米＋WRL；源文件/脚本另库保存 | CC BY-SA 4.0加KiCad例外；项目中使用较宽松，重分发库集合需保留相同许可和署名 | **首选电子零件** |

## 研究与结构数据集

| 数据集 | 内容 | 最适合 | 许可/限制 | 不适合直接做什么 |
|---|---|---|---|---|
| [ABC Dataset](https://deep-geometry.github.io/abc-dataset/) | 超过100万高质量CAD模型，含参数曲面、patch分解、锐边和微分属性 | 几何学习、曲面/边特征评测、大规模CAD候选 | 论文称MIT；下载按分块，保存版本和具体数据条款 | 缺少丰富语义装配，不是整理好的影视资产库 |
| [Fusion 360 Gallery Dataset](https://github.com/AutodeskAILab/Fusion360GalleryDataset) | 8,625个人类设计CAD程序，含Sketch＋Extrude构建序列 | 学习“从草图到实体”的操作时间线，最接近SKY-001构造序列 | 仅限非商业研究；不得整体再分发 | 不能直接用于商业影视资产或产品库 |
| [PartNet](https://partnet.cs.stanford.edu/)／PartNet-Mobility | 细粒度层级部件标注；Mobility含关节、URDF与OBJ网格 | 资产树、门/抽屉/轮子等可动部件、机器人仿真原型 | 访问和数据许可按官方申请/单项条款核对；来源模型可能有各自限制 | 不是精密CAD或制造数据，拓扑和尺度需清洗 |

## 按需求选择

| 目标 | 推荐组合 | 原因 |
|---|---|---|
| 快速做机械爆炸动画 | FreeCAD Parts Library→FreeCAD/Blender | 有现成STEP与参数文件，易拆件和设枢轴 |
| 生成齿轮、轴承、螺栓、支架 | CadQuery＋cq_warehouse，或OpenSCAD＋BOSL2/MCAD | 参数明确，可批量生成尺寸变体并保存源码 |
| 做完整机架/3D打印装配 | NopSCADlib | 自带vitamins、BOM、装配和说明书思路 |
| 建立SKY-001式资产树 | PartCAD＋CadQuery/FreeCAD资产 | 可把需求、零件、装配、BOM、验证和来源放在一个包中 |
| PCB与电子设备内部 | KiCad Packages3D→STEP→FreeCAD/Blender | 元件与封装对齐，适合电子产品可视化 |
| 研究构造步骤模型 | Fusion 360 Gallery＋ABC | 一个有操作序列，一个有大规模几何基准 |
| 研究关节和可动物体 | PartNet-Mobility→URDF/Blender/Godot | 已有部件和关节关系，适合交互与运动原型 |

## 对影视制作的统一导入流程

`源资产＋许可 → CAD单位/坐标检查 → 修复实体/法线 → 建父子层级与枢轴 → 简化渲染网格 → UV/材质 → 爆炸/装配状态 → 镜头与声音事件 → 审查`

每个资产至少记录：来源URL、仓库提交或数据版本、原始文件哈希、作者、许可、单位、坐标系、零件ID、父级ID、原始CAD与影视代理的映射。CAD源件、简化代理和最终渲染网格分别保存，避免把不可逆的三角化网格当作工程原件。

## 验收边界

- “可下载”或“免费”不等于开放许可；GrabCAD、厂商CAD目录等应按单件条款判断，未列为默认开放资产源。
- STEP/FCStd能打开不代表尺寸、螺纹、公差、材料或装配正确。
- 用于影视时可以简化隐藏结构，但必须标记“视觉代理”；用于工程说明时不得用虚构内部结构。
- 进入Blender后重点检查单位、轴向、法线、曲面细分、枢轴、层级、实例化和材质，不直接破坏原始CAD。

建议第一批只下载FreeCAD Parts Library中的目标子目录，并安装CadQuery＋cq_warehouse做一个“轴承—轴—齿轮—紧固件”的小型装配Demo；通过层级、爆炸动画和许可记录后，再决定是否引入大数据集。
