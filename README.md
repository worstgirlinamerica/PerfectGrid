# Perfect Grid
[![GitHub Release](https://img.shields.io/github/v/release/worstgirlinamerica/PerfectGrid?style=for-the-badge)](https://github.com/worstgirlinamerica/PerfectGrid/releases)
[![Downloads](https://img.shields.io/github/downloads/worstgirlinamerica/PerfectGrid/total?style=for-the-badge)](https://github.com/worstgirlinamerica/PerfectGrid/releases)
[![License](https://img.shields.io/github/license/worstgirlinamerica/PerfectGrid?style=for-the-badge)](LICENSE)

Perfect Grid makes polished video preview sheets from local video files.

Drop in a video, choose a layout, adjust the metadata and timecode styling, then export a clean PNG contact sheet. It is built for editors, collectors, archivists, and anyone who wants quick visual summaries of video files without opening a full editing app.

<p align="center">
  <img src="https://i.imgur.com/HVf0JjP.jpeg" alt="Example preview sheet made with Perfect Grid">
</p>

<p align="center">
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/download/v1.0.0/Perfect-Grid-macOS.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-macOS-000000?style=for-the-badge&logo=apple&logoColor=white" alt="Download for macOS">
  </a>
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/download/v1.0.0/Perfect-Grid-Windows.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Windows-0078D6?style=for-the-badge&logo=windows21&logoColor=white" alt="Download for Windows">
  </a>
</p>

## Features
- Creates PNG preview sheets from videos
- Lets you choose rows, columns, spacing, margins, and scaling
- Shows useful file details like filename, size, resolution, duration, video codec, and audio codec
- Adds optional timecode labels to each frame
- Offers fast previews and refined frame picking
- Saves custom presets
- Supports batch processing
- Runs as a desktop app on Windows and macOS

## Download And Install

Go to the Releases page and download the build for your system.

> ### Windows

1. Download `Perfect-Grid-Windows.zip`.
2. Right-click the zip and choose **Extract All**.
3. Open the extracted folder.
4. Double-click `Perfect Grid.exe`.

Windows may show a SmartScreen warning because the app is not code-signed yet. Choose **More info**, then **Run anyway** if you trust the download.

> ### macOS

1. Download `Perfect-Grid-macOS.zip`.
2. Double-click the zip to extract it.
3. Open `Perfect Grid.app`.

If macOS blocks the unsigned app, right-click `Perfect Grid.app`, choose **Open**, then confirm.

## Privacy

Perfect Grid works locally on your computer.

- It does not include analytics or telemetry.
- It does not upload your videos.
- It does not call any web APIs.
- Packaged builds include FFmpeg and FFprobe so video metadata and frames can be processed locally.

## Basic Use

1. Open Perfect Grid.
2. Drag a video into the preview area.
3. Adjust the grid, text, timecode, and range settings.
4. Use **Refine Picks** if you want a smarter frame selection pass.
5. Click **Export PNG**.

## Supported Files

Perfect Grid uses FFmpeg for video reading, so common formats such as MP4, MOV, MKV, AVI, and WebM should work. Some unusual codecs may be slower or less reliable depending on the system.

## Notes

- Very large videos can take longer to preview or export.
- AV1 and VP9 files may use software decoding and can be slower.
- The macOS app is currently unsigned, so macOS may show a security prompt the first time it opens.

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
