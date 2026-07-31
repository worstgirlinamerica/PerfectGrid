# Perfect Grid
[![GitHub Release](https://img.shields.io/github/v/release/worstgirlinamerica/PerfectGrid?style=for-the-badge)](https://github.com/worstgirlinamerica/PerfectGrid/releases)
[![Downloads](https://img.shields.io/github/downloads/worstgirlinamerica/PerfectGrid/total?style=for-the-badge)](https://github.com/worstgirlinamerica/PerfectGrid/releases)
[![License](https://img.shields.io/github/license/worstgirlinamerica/PerfectGrid?style=for-the-badge)](LICENSE)

Perfect Grid is an Open Source, free desktop app for creating polished video contact sheets and preview thumbnails from local video files.

Drop in a video, customize the layout, metadata, and timecode styling, then export a high-quality PNG contact sheet. Designed for editors, collectors, archivists, and anyone who wants a quick visual summary of a video.

<p align="center">
  <img src="https://i.imgur.com/HVf0JjP.jpeg" alt="Example preview sheet made with Perfect Grid">
  <br>
  <em>Example contact sheet generated with Perfect Grid.</em>
</p>

<p align="center">
<a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/Perfect-Grid-macOS.zip">
  <img src="https://custom-icon-badges.demolab.com/badge/Download-macOS-000000?style=for-the-badge&logo=apple&logoColor=white" alt="Download for macOS">
  </a>
<a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/Perfect-Grid-Windows.zip">
  <img src="https://custom-icon-badges.demolab.com/badge/Download-Windows-0078D6?style=for-the-badge&logo=windows21&logoColor=white" alt="Download for Windows">
  </a>
</p>

## Features

- Generate high-quality PNG contact sheets
- Fully customizable grid layouts
- Optional timecode overlays
- Display video metadata (resolution, codecs, duration, file size, etc.)
- Smart frame selection with **Refine Picks**
- Save and reuse custom presets
- Batch processing support
- Native desktop app for Windows and macOS

## Basic Usage

1. Open Perfect Grid.
2. Drag a video into the window.
3. Choose your grid layout and styling.
4. (Optional) Click **Refine Picks** for smarter frame selection.
5. Click **Export PNG**.

## Download And Install

Download the latest release for your operating system.

### Windows

1. Download `Perfect-Grid-Windows.zip`.
2. Right-click the zip and choose **Extract All**.
3. Open the extracted folder.
4. Double-click `Perfect Grid.exe`.

Windows may show a SmartScreen warning because the app is not code-signed yet. Choose **More info**, then **Run anyway** if you trust the download.

### macOS

1. Download `Perfect-Grid-macOS.zip`.
2. Double-click the zip to extract it.
3. Open `Perfect Grid.app`.

If macOS blocks the unsigned app, right-click `Perfect Grid.app`, choose **Open**, then confirm.

## Privacy

Perfect Grid runs entirely on your computer.

- No analytics or telemetry
- No uploads or cloud processing
- No web API calls
- FFmpeg and FFprobe are bundled for local video processing

## Notes
> ## Supported Formats
Perfect Grid supports MP4, MOV, MKV, AVI, WebM, and most formats supported by FFmpeg.
- Very large videos may take longer to preview or export.
- AV1 and VP9 decoding may be slower on some systems.
- macOS builds are currently unsigned, so Gatekeeper may display a security prompt on first launch.

## For Developers

Perfect Grid is a Python/PyQt app.

Run from source:

```bash
python -m pip install -r requirements.txt
PYTHONPATH=src python -m perfect_grid.app
```

Build scripts are in `scripts/`. GitHub Actions builds Windows and macOS release zips.

## Contributing

Bug reports and feature requests are welcome. Useful bug reports include the operating system, video format, and whether the issue happened during preview, refine, export, or batch processing.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development notes.

## License

MIT. See [LICENSE](LICENSE).
