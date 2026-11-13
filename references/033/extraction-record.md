# 案例033 本地读取记录

工具：项目已有`.tools/python/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe`，FFmpeg7.1。未安装新依赖；系统python别名不可执行，因此直接使用已存在的FFmpeg二进制。

输入、拷贝、规格与SHA-256见`provenance.json`。保留Downloads原文件，另存本地研究副本，未修改源视频。输出图像用于分析而非生成或编辑创作素材。

## 实际操作参数

- 技术探测：`-hide_banner -i <输入>`；未指定输出时返回“At least one output file must be specified”为预期探测行为，不是生成失败。
- 12秒总览24：`-vf "fps=1/12,scale=320:-1,tile=7x5" -frames:v 1 contact_24.jpg`
- 12秒总览25：`-vf "fps=1/12,scale=240:-1,tile=6x3" -frames:v 1 contact_25.jpg`
- 3秒详细24：`-vf "fps=1/3,scale=384:-1,tile=5x6" -fps_mode vfr frames/24_sheet_%02d.jpg`
- 3秒详细25：`-vf "fps=1/3,scale=230:-1,tile=5x4" -fps_mode vfr frames/25_sheet_%02d.jpg`
- 场景变化候选，两片分别运行：`-vf "select='gt(scene,0.30)',showinfo" -an -fps_mode vfr -f null NUL`，stderr保存在scene24.log/scene25.log；pts_time导出scene-candidates.json。24为181个、25为99个候选，不是已确认镜头数。
- 24局部动作：输入前`-ss 120`，输出前`-t 9 -vf "fps=4,scale=320:-1,tile=6x6" -frames:v 1 frames/24_motion120.jpg`
- 25局部动作：输入前`-ss 114`，输出前`-t 9 -vf "fps=4,scale=200:-1,tile=6x6" -frames:v 1 frames/25_motion114.jpg`
- 24高潮字幕：输入前`-ss 264`，输出前`-t 54 -vf "fps=1,scale=420:-1,tile=6x9" -frames:v 1 frames/24_honesty264.jpg`

上述输出命令均加`-hide_banner -loglevel error -i <输入>`，scene检测使用`-hide_banner -i <输入>`以保留showinfo日志。没有替原作者推测或记录任何未知生成参数。

## 导航与限制

拼图按从左到右、从上到下排列。3秒详细24每页覆盖约90秒，25每页约60秒；最后一页空黑格为tile补齐，不代表源片存在黑场。fps为重新取样，实际所选源帧与网格标称时刻有采样/舍入偏移，因此正文时间用于导航，不作精确EDL或剪辑入出点。

`derivatives-manifest.csv`记录本轮图像与变化候选JSON的实际哈希。派生图像与原片留本地；Git只归档可追溯文本和哈希。声轨存在不代表已听审，密集抽样不代表连续运动通过。
