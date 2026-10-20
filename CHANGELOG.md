# Changelog

## 0.2.0

- Replaced per-frame ffmpeg subprocess extraction with a persistent PyAV decode session — each extraction thread now opens a video once and seeks within it, instead of spawning (and on Intel, often double-spawning via a failed hwaccel attempt + software retry) a new ffmpeg process per thumbnail. Falls back to the old ffmpeg path automatically if PyAV can't handle a given file/codec.
- Fixed a bug where the "ultrafast" preview pool (used on Intel) had no buffer over the exact thumbnail count needed — a handful of failed extractions would silently exhaust it, causing the grid to reuse already-picked frames and show visible duplicate tiles
- Fixed an unbounded timeout on final frame export that could let a stuck hwaccel→software fallback hang the whole export on Intel
- Added a small version tag in the corner of the UI — shows the commit + a content hash of any uncommitted changes on dev/source runs, a clean version number on shipped builds

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
