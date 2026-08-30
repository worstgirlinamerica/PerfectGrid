# Changelog

## 0.1.2

- Complete UI overhaul with custom-painted widgets (sliders, checkboxes, dropdowns) matching the app theme
- Added localization system — interface now available in English, Chinese (中文), and Portuguese
- Fixed Arabic and RTL filenames rendering as boxes on the contact sheet — GeezaPro is now prioritized on macOS for Arabic text, with proper reshaping and bidi support
- Faster and better-quality fast preview — preview thumbnails are now larger and sharper, and all CPU cores are used for frame extraction
- Added preview debounce — changing settings quickly no longer fires redundant extractions
- Added cache size cap to prevent unbounded disk use during long sessions
- Settings dialog with theme/skin selection, default output directory, and default preset
- Save and load named presets from the Presets tab
- Batch tab for processing multiple files
- Range tab reset button
- Linux support — ships as a self-contained AppImage, no install required

## 1.0.0

- Initial public release setup.
- Added Windows and macOS PyInstaller build scripts.
- Added GitHub Actions artifacts and tagged-release publishing.
- Bundled FFmpeg/FFprobe support for packaged apps.
- Moved settings and user presets into per-user app data directories.
