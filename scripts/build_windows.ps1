$ErrorActionPreference = "Stop"

$depsInstalled = $true
python -c "import PyQt5, PIL, PyInstaller" 2>$null
if ($LASTEXITCODE -ne 0) {
    $depsInstalled = $false
}

if (!$depsInstalled) {
    python -m pip install -r requirements.txt
}

New-Item -ItemType Directory -Force -Path "win-binaries" | Out-Null

$ffmpeg = Join-Path "win-binaries" "ffmpeg.exe"
$ffprobe = Join-Path "win-binaries" "ffprobe.exe"

if (!(Test-Path $ffmpeg)) {
    $pathFfmpeg = (Get-Command "ffmpeg.exe" -ErrorAction SilentlyContinue).Source
    if (!$pathFfmpeg) {
        throw "ffmpeg.exe was not found. Put ffmpeg.exe in win-binaries\ or install FFmpeg and add it to PATH."
    }
    Copy-Item $pathFfmpeg $ffmpeg
}

if (!(Test-Path $ffprobe)) {
    $pathFfprobe = (Get-Command "ffprobe.exe" -ErrorAction SilentlyContinue).Source
    if (!$pathFfprobe) {
        throw "ffprobe.exe was not found. Put ffprobe.exe in win-binaries\ or install FFmpeg and add it to PATH."
    }
    Copy-Item $pathFfprobe $ffprobe
}

$env:PYINSTALLER_CONFIG_DIR = if ($env:PYINSTALLER_CONFIG_DIR) { $env:PYINSTALLER_CONFIG_DIR } else { Join-Path (Get-Location) ".pyinstaller" }

pyinstaller `
    --noconfirm `
    --windowed `
    --name "Perfect Grid" `
    --distpath "dist_windows" `
    --workpath "build_windows" `
    --icon "icon.ico" `
    --add-data "presets_v2.json;." `
    --add-binary "win-binaries\ffmpeg.exe;." `
    --add-binary "win-binaries\ffprobe.exe;." `
    app.py

Write-Host "Windows build complete: dist_windows\Perfect Grid\Perfect Grid.exe"
