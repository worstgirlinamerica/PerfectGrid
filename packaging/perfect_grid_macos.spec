# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ["src/perfect_grid/app.py"],
    pathex=[],
    binaries=[("/usr/local/bin/ffmpeg", "."), ("/usr/local/bin/ffprobe", ".")],
    datas=[("src/perfect_grid/presets_v2.json", ".")],
    hiddenimports=[],
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
