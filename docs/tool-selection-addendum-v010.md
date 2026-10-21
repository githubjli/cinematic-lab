# 工具选型补充 v010

更新日期：2026-10-21。本版新增开源机械资产与参数化零件库；详细说明见`mechanical-asset-libraries-v001.md`。

| 需求 | 优先考虑 | 备选/研究项 | 关键边界 |
|---|---|---|---|
| 现成可编辑机械零件 | FreeCAD Parts Library | NopSCADlib | 保存作者与CC BY署名；只下载所需分类 |
| 参数化机械零件 | CadQuery＋cq_warehouse | BOSL2、MCAD | 标准尺寸和装配接口需独立验证 |
| 资产树、BOM和来源编排 | PartCAD | Git＋自定义JSON清单 | 包中每个资产的许可分别判断 |
| PCB/电子元件三维模型 | KiCad Packages3D | 厂商单件STEP | KiCad集合重分发受CC BY-SA条款约束 |
| CAD几何学习/评测 | ABC Dataset | Fusion 360 Gallery | Fusion数据仅非商业研究 |
| 层级部件与关节运动 | PartNet/PartNet-Mobility | 自建URDF | 不是精密制造CAD；数据访问条款另核 |

本项目默认路线：`FreeCAD Parts Library现成件＋CadQuery参数件＋PartCAD资产树→Blender影视代理与动画`。尚未下载、安装或运行这些新增候选。
