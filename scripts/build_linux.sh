#!/usr/bin/env bash
set -euo pipefail

if ! python3 - <<'PY'
import PyQt5, PIL, PyInstaller
PY
then
  python3 -m pip install -r requirements.txt
fi

FFMPEG_BIN="${FFMPEG_BIN:-}"
FFPROBE_BIN="${FFPROBE_BIN:-}"
if [[ -z "${FFMPEG_BIN}" ]]; then
  FFMPEG_BIN="$(command -v ffmpeg || true)"
fi
if [[ -z "${FFPROBE_BIN}" ]]; then
  FFPROBE_BIN="$(command -v ffprobe || true)"
fi

if [[ -z "${FFMPEG_BIN}" || -z "${FFPROBE_BIN}" ]]; then
  echo "ffmpeg and ffprobe are required. Install them with: sudo apt install ffmpeg" >&2
  exit 1
fi

export PYINSTALLER_CONFIG_DIR="${PYINSTALLER_CONFIG_DIR:-$(pwd)/.pyinstaller}"

# Step 1: PyInstaller one-folder build
pyinstaller \
  --noconfirm \
  --onedir \
  --name "perfect-grid" \
  --distpath dist_linux \
  --workpath build_linux \
  --add-data "src/perfect_grid/presets_v2.json:." \
  --add-binary "${FFMPEG_BIN}:." \
  --add-binary "${FFPROBE_BIN}:." \
  src/perfect_grid/app.py

# Step 2: Download appimagetool
wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" \
  -O appimagetool
chmod +x appimagetool

# Step 3: Assemble AppDir
APPDIR="AppDir"
rm -rf "${APPDIR}"
mkdir -p "${APPDIR}/usr/bin"
mkdir -p "${APPDIR}/usr/share/icons/hicolor/256x256/apps"

cp -r dist_linux/perfect-grid/* "${APPDIR}/usr/bin/"

cat > "${APPDIR}/AppRun" << 'APPRUN'
#!/usr/bin/env bash
HERE="$(dirname "$(readlink -f "$0")")"
export LD_LIBRARY_PATH="${HERE}/usr/bin:${LD_LIBRARY_PATH:-}"
exec "${HERE}/usr/bin/perfect-grid" "$@"
APPRUN
chmod +x "${APPDIR}/AppRun"

cat > "${APPDIR}/perfect-grid.desktop" << 'DESKTOP'
[Desktop Entry]
Name=Perfect Grid
Exec=perfect-grid
Icon=perfect-grid
Type=Application
Categories=Graphics;Video;
Comment=Create detailed preview sheets from video files
DESKTOP

# Convert icon: icns -> png via Pillow (already installed)
if [[ -f "assets/icon.icns" ]]; then
  python3 -c "
from PIL import Image
img = Image.open('assets/icon.icns')
img.save('AppDir/usr/share/icons/hicolor/256x256/apps/perfect-grid.png')
"
else
  python3 -c "
from PIL import Image
Image.new('RGBA', (256, 256), (30, 30, 30, 255)).save(
  'AppDir/usr/share/icons/hicolor/256x256/apps/perfect-grid.png'
)
"
fi
cp "${APPDIR}/usr/share/icons/hicolor/256x256/apps/perfect-grid.png" \
   "${APPDIR}/perfect-grid.png"

# Step 4: Build AppImage
ARCH=x86_64 ./appimagetool "${APPDIR}" "Perfect-Grid-x86_64.AppImage"

echo "AppImage complete: Perfect-Grid-x86_64.AppImage"
