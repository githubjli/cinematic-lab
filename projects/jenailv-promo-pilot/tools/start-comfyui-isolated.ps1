$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$runtimeRoot = Join-Path $projectRoot 'runtime\comfyui'
$sharedRoot = 'C:\Users\76797\Desktop\chatgpt\aivideo\ComfyUI_windows_portable'
$python = Join-Path $sharedRoot 'python_embeded\python.exe'
$main = Join-Path $sharedRoot 'ComfyUI\main.py'

if (-not (Test-Path -LiteralPath $python)) { throw "Shared Python not found: $python" }
if (-not (Test-Path -LiteralPath $main)) { throw "Shared ComfyUI not found: $main" }

$userDir = Join-Path $runtimeRoot 'user'
$inputDir = Join-Path $runtimeRoot 'input'
$outputDir = Join-Path $runtimeRoot 'output'
$tempDir = Join-Path $runtimeRoot 'temp'
@($userDir, $inputDir, $outputDir, $tempDir) | ForEach-Object {
    New-Item -ItemType Directory -Force -Path $_ | Out-Null
}

& $python -s $main `
    --listen 127.0.0.1 `
    --port 8189 `
    --disable-auto-launch `
    --user-directory $userDir `
    --input-directory $inputDir `
    --output-directory $outputDir `
    --temp-directory $tempDir
