# -*- mode: python ; coding: utf-8 -*-

# NOTE: this .spec is a secondary entry point — scripts/build_macos.sh is
# the one CI/the build docs actually call, and it invokes pyinstaller via
# CLI flags (including --collect-all av) rather than this file. If you
# build from this .spec directly instead, use PyInstaller's
# Analysis(..., module_collection_mode={"av": "py+so"}) or run
# `pyi-makespec --collect-all av ...` to regenerate it, or av's bundled
# libav .dylibs won't get picked up.
#
# Also: /usr/local/bin is Homebrew's default prefix on Intel Macs only —
# Apple Silicon Homebrew installs to /opt/homebrew/bin. This hardcoded
# path will silently resolve to nothing (or someone else's stray binary)
# on an arm64 build machine. build_macos.sh handles this correctly via
# `command -v ffmpeg` / $FFMPEG_BIN; this .spec does not.

a = Analysis(
    ["src/perfect_grid/app.py"],
    pathex=[],
    binaries=[("/usr/local/bin/ffmpeg", "."), ("/usr/local/bin/ffprobe", ".")],
    datas=[("src/perfect_grid/presets_v2.json", ".")],
    hiddenimports=["av"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Perfect Grid",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=["assets/icon.icns"],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Perfect Grid",
)
app = BUNDLE(
    coll,
    name="Perfect Grid.app",
    icon="assets/icon.icns",
    bundle_identifier="app.perfectgrid.desktop",
)
