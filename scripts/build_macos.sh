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
  echo "ffmpeg and ffprobe are required. Install them with: brew install ffmpeg" >&2
  exit 1
fi

export PYINSTALLER_CONFIG_DIR="${PYINSTALLER_CONFIG_DIR:-$(pwd)/.pyinstaller}"

pyinstaller \
  --noconfirm \
  --windowed \
  --name "Perfect Grid" \
  --distpath dist_mac \
  --workpath build_mac \
  --icon assets/icon.icns \
  --add-data "src/perfect_grid/presets_v2.json:." \
  --add-binary "${FFMPEG_BIN}:." \
  --add-binary "${FFPROBE_BIN}:." \
  src/perfect_grid/app.py

echo "macOS build complete: dist_mac/Perfect Grid.app"
