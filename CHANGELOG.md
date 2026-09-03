# Changelog

## 0.1.2

- Rewrote all UI widgets from scratch — sliders, checkboxes, and dropdowns are now custom-painted to match the app theme instead of using default OS controls
- Added a localization system; the interface is now available in English, Chinese (中文), and Portuguese
- Fixed Arabic and RTL filenames showing as boxes on the contact sheet — GeezaPro is now checked first on macOS for Arabic text, with proper character reshaping and bidi reordering
- Faster previews — thumbnails are larger and sharper, frame extraction now uses all CPU cores
- Added debounce to preview — tweaking settings quickly no longer kicks off a bunch of redundant extractions
- Cache size is now capped so it doesn't grow forever during long sessions
- Added a Settings dialog (app menu) with theme/skin selection, default output folder, and default preset
- Linux build — ships as a self-contained AppImage, no install required

## 0.1.0

- Initial public release
- Windows and macOS builds via PyInstaller
- GitHub Actions CI with artifact uploads and tagged release publishing
- Bundled FFmpeg/FFprobe
- Settings and presets stored in per-user app data directories
