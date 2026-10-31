$ErrorActionPreference = "Stop"

$depsInstalled = $true
python -c "import PyQt5, PIL, PyInstaller, av" 2>$null
if ($LASTEXITCODE -ne 0) {
    $depsInstalled = $false
}

if (!$depsInstalled) {
    python -m pip install -r requirements.txt
}

New-Item -ItemType Directory -Force -Path "win-binaries" | Out-Null

$ffmpeg = Join-Path "win-binaries" "ffmpeg.exe"
$ffprobe = Join-Path "win-binaries" "ffprobe.exe"

# NOTE: don't fall back to whatever ffmpeg.exe/ffprobe.exe happens to be on
# PATH here. If you installed FFmpeg via `choco install ffmpeg`, PATH
# resolves to a tiny *shim* launcher in chocolatey\bin, not a real binary —
# it redirects to chocolatey\lib at run time. Copying that shim into the
# bundle ships a launcher with nothing to redirect to once it leaves this
# machine: it fails silently, and because it's a console-subsystem exe
# started from our windowed app, Windows flashes a console window for it
# first (looks like "the app opens a terminal, then fails"). Put real
# binaries in win-binaries\ yourself (e.g. a static build from
# https://www.gyan.dev/ffmpeg/builds/), or let this script fetch one.
if (!(Test-Path $ffmpeg) -or !(Test-Path $ffprobe)) {
    Write-Host "ffmpeg.exe/ffprobe.exe not found in win-binaries\ — downloading a static build..."
    Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile "ffmpeg_dl.zip"
    Expand-Archive -Path "ffmpeg_dl.zip" -DestinationPath "ffmpeg_dl_extracted" -Force
    $binDir = Get-ChildItem -Path "ffmpeg_dl_extracted" -Directory | Select-Object -First 1
    Copy-Item (Join-Path $binDir.FullName "bin\ffmpeg.exe") $ffmpeg -Force
    Copy-Item (Join-Path $binDir.FullName "bin\ffprobe.exe") $ffprobe -Force
    Remove-Item "ffmpeg_dl.zip" -Force
    Remove-Item "ffmpeg_dl_extracted" -Recurse -Force
}

$env:PYINSTALLER_CONFIG_DIR = if ($env:PYINSTALLER_CONFIG_DIR) { $env:PYINSTALLER_CONFIG_DIR } else { Join-Path (Get-Location) ".pyinstaller" }

pyinstaller `
    --noconfirm `
    --windowed `
    --name "Perfect Grid" `
    --distpath "dist_windows" `
    --workpath "build_windows" `
    --icon "assets\icon.ico" `
    --add-data "src\perfect_grid\presets_v2.json;." `
    --add-binary "win-binaries\ffmpeg.exe;." `
    --add-binary "win-binaries\ffprobe.exe;." `
    --collect-all av `
    "src\perfect_grid\app.py"

Write-Host "Windows build complete: dist_windows\Perfect Grid\Perfect Grid.exe"
