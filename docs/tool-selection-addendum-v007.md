# 工具选型补充 v007

更新日期：2026-10-19。本版新增音乐分轨工具；其他工具继续参考v006、`tool-selection-v001.md`、最新数学选型和技巧索引。

| 工具/资源 | 需求出现时考虑 | 输入→输出 | 本地与许可状态 | 关键边界 |
|---|---|---|---|---|
| 曲多多/BGMSkill分轨曲库 | 需要可授权音乐及更细的原生乐器组 | 曲目→Percussion/Pulses/Bass/Bells/Pads等可试听轨 | 视频中可见；未登录、未下载；开放源码未知，费用和逐曲许可待核 | 页面有分轨不证明AI分离；下载与同步授权按曲目核对 |
| Demucs | 本地批量四轨或实验六轨分离 | 混音→vocals/drums/bass/other，可加guitar/piano | [官方仓库](https://github.com/facebookresearch/demucs)，MIT；未安装 | 项目已归档且不再积极维护；细乐器分轨有限；会有串音和伪影 |
| Ultimate Vocal Remover GUI | Windows图形界面、多模型/集合分离 | 音频＋模型设置→分离stem | [官方仓库](https://github.com/Anjok07/ultimatevocalremovergui)，GUI代码MIT；未安装 | 权重和第三方组件分别记录；计算量和质量依硬件/模型变化 |
| FFmpeg | stem探测、统一格式、裁切、重组和响度 | 多轨音频→代理/混音/母版 | 已用于分析 | 不做源分离或听感判断 |

需要细到Pulses、Bells、Pads、Brass、Strings时优先原生stem；本地AI分离优先解决人声、鼓、贝斯、其他或有限六轨。任何分离只处理音频信号，不自动取得原曲使用权。
