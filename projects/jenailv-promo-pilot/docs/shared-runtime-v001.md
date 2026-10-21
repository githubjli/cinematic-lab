# 复用 aivideo 本地运行环境 v001

核对日期：2026-10-21。原则：`aivideo`只作为程序与模型的只读来源，案例输入、缓存、用户数据库、临时文件和输出全部写入当前项目。

## 可直接使用

| 工具 | 路径 | 使用方式 |
|---|---|---|
| FFmpeg 9.0.1 | `C:\Users\76797\Desktop\chatgpt\aivideo\tools\avatar\Wan2GP\ffmpeg_bins\ffmpeg.exe` | 可直接处理当前项目媒体，显式指定输入输出 |
| Blender 4.2.23 | `C:\Users\76797\Desktop\chatgpt\aivideo\tools\blender\blender-4.2.23-windows-x64\blender.exe` | 使用`--background --factory-startup`，脚本和输出放当前项目 |
| ComfyUI 0.36.0 | `C:\Users\76797\Desktop\chatgpt\aivideo\ComfyUI_windows_portable` | 使用本项目隔离启动脚本；程序和模型只读复用 |

## ComfyUI隔离要求

当前版本已确认支持`--user-directory`、`--input-directory`、`--output-directory`和`--temp-directory`。启动脚本把四个目录都指向`projects/jenailv-promo-pilot/runtime/comfyui/`，端口使用8189，以免与`aivideo`默认8188冲突。

不要运行`aivideo`中的升级脚本、依赖安装、模型下载或工作流准备脚本。需要修改的工作流先复制到当前项目。运行前确认没有另一个GPU任务；停止服务后再启动其他Wan2GP或ComfyUI任务。

## 当前验证边界

- 已静态确认程序文件和ComfyUI参数存在；FFmpeg版本命令运行成功。
- 尚未启动本案例ComfyUI服务，也没有提交GPU生成任务。
- 复用程序不代表复用所有模型的商业许可；具体模型仍按候选输出逐项核对。
