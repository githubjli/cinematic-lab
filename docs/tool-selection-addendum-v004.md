# 工具选型补充 v004

更新日期：2026-10-14。本版汇总此前补充项并新增Anatomy；与`tool-selection-v001.md`、最新数学选型和技巧索引配合使用。优先级是研究建议，不代表安装或付费授权。

| 工具/资源 | 性质与来源 | 需求出现时考虑 | 输入→输出 | 本地与许可状态 | 关键边界 |
|---|---|---|---|---|---|
| LocalMiniDrama | [开源短剧工作流](https://github.com/xuanyustudio/LocalMiniDrama) | 多集剧本、资产、分镜与镜头管理 | 梗概/风格/API→脚本、参考资产、镜头、合成 | MIT；未运行 | 本地存储不等于全部推理离线；API和模型费用另核对 |
| Toonflow | [开源短剧画布工作台](https://github.com/HBAI-Ltd/Toonflow-app) | 剧本、资产、分镜、参考和视频节点集中管理 | 原文/资产/模型→画布节点和镜头文件 | 已保存`ae9e5f1`；MIT；未运行 | 当前主工作流不是固定六Agent；最终剪辑混音另验收 |
| OpenMontage | [制作流程编排](https://github.com/calesthio/OpenMontage) | 研究多阶段工具交接与自动化 | 创意/配置/素材→生产文件和渲染产物 | 已保存；AGPL-3.0；未运行 | 依赖与外部服务另核对；不推定“一句话完成” |
| Anatomy | [交互式原理图Agent Skill](https://github.com/wheresryan22/anatomy) | 机械原理、技术系统、交互科普与网页说明 | 事实/机制/部件→SVG、HTML或React组件，可加WebGL/3D | 已保存`e6600ffc`、147文件哈希；MIT；未安装/运行 | 不是CAD/物理仿真/图表库；3D为beta；成片需另做镜头、音频和编码 |
| MotionSites MCP | [网站设计提示词服务](https://motionsites.ai/mcp) | 网站视觉与动效参考 | 需求→检索参考/提示词→代理实现 | 未连接；许可未确认 | MCP不等于审美评测或自动验收 |
| GSAP Skills / GSAP | [技能资料](https://github.com/greensock/gsap-skills) / [许可](https://gsap.com/community/standard-license/) | 网页时间线、滚动、SVG和交互动效 | 页面需求→代码动效 | 未安装；技能与运行库许可分别核对 | 录制MP4需额外渲染；响应式、性能和减少动态效果需测试 |
| yihui-dev/awesome-opus5-5-videos | [案例/提示词合集](https://github.com/yihui-dev/awesome-opus5-5-videos) | 动效参考和技术路线比较 | 主题→案例/原帖/提示词 | 未下载 | 013候选来源；不保证完整源码公开 |
| TikBit.ai | 015推广平台线索 | 仅登记，需求明确后核验 | 服务机制未知 | 未连接；许可/费用/模型未知 | 不以宣传标签认定实际能力 |
| 数学动态模型课程 | 011成品参考 | 数学动画教学表现参考 | 问题→图形→变化→结论 | 制作工具未知 | Manim/SymPy只是建议实现路线 |

需要机械/系统交互解释时先比较Anatomy、Manim和通用Three.js：部件机构优先Anatomy；公式与数学变换优先Manim；自由三维场景优先Three.js/Blender。需要成片时再接Remotion、FFmpeg或人工剪辑工具。
