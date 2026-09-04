<p align="center">
  <img src="assets/icon.png" width="80" alt="Perfect Grid">
  <h1 align="center">Perfect Grid</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/worstgirlinamerica/PerfectGrid" alt="GitHub 发布">
  <img src="https://img.shields.io/github/downloads/worstgirlinamerica/PerfectGrid/total" alt="下载">
  <img src="https://img.shields.io/github/license/worstgirlinamerica/PerfectGrid" alt="许可证">
</p>

Perfect Grid 是一款免费的开源桌面应用程序，用于从本地视频文件中创建视频接触表和预览缩略图。只需导入视频、选择布局，即可导出高质量的 PNG 接触表。

专为剪辑师、收藏家、档案管理员以及任何希望快速直观地概览视频内容的人士打造。

<p align="center">
  <img src="https://i.imgur.com/HVf0JjP.jpeg" alt="使用 Perfect Grid 制作的预览样张示例">
  <br>
  <em>使用 Perfect Grid 生成的联系表示例。</em>
</p>

<p align="center">
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-macos-universal.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-macOS-000000?logo=apple&logoColor=white" alt="下载 macOS 版本">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-Windows-x86_64.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Windows-0078D6?logo=windows11&logoColor=white" alt="Windows 版下载">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-Linux-x86_64.AppImage">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Linux-E95420?logo=linux&logoColor=white" alt="下载 Linux 版">
  </a>
</p>

## 功能

- 生成高质量的联系表，并显示高级视频元数据（分辨率、编解码器、时长、文件大小等）
- 完全可自定义的网格布局
- 可选的时间码叠加
- 通过 **“优化选择”** 实现智能帧选择
- 保存并重复使用自定义预设
- 批量处理
- 支持 Windows、macOS 和 Linux 系统
> 如果您遇到 __任何__ 错误、功能无法正常运行，或有任何疑问，请创建一个 [问题报告](https://github.com/worstgirlinamerica/PerfectGrid/issues/new) 进行反馈。

## 本地化

该应用的用户界面支持 8 种语言。工作表文件名的渲染采用独立机制——它将文件名以像素形式绘制在导出的 PNG 文件上，这需要脚本特有的字体处理机制。

| 语言 | 界面 | 工作表 |
|---|---|---|
| 英语 | 是 | 是 |
| 中文 | 是 | 是（macOS、Windows） |
| 葡萄牙语（PT） | 是 | 是 |
| 西班牙语（ES） | 是 | 是 |
| 日语（JA） | 是 | 是（macOS、Windows） |
| 法语 (FR) | 是 | 是 |
| 德语 (DE) | 是 | 是 |
| 韩语 (KO) | 是 | 是 (macOS、Windows) |
| 阿拉伯语 / 从右到左 (RTL) | — | 是 |
| 希伯来语 | — | — |
| 泰语 | — | — |
| 天城文（印地语等） | — | — |

> 目前不支持 Linux 系统中非 ASCII 文件名的渲染——非拉丁字母脚本的文件名将显示为方块。此问题将在下一个版本中修复！

## 基本用法

1. 打开 Perfect Grid。
2. 将视频拖拽到窗口中。
3. 调整网格布局和样式。如果更改了布局，请点击 **刷新预览** 以重新生成缩略图。
4. 预览画质故意设置得较低 — 导出时始终采用您选择的画质设置。
5. （可选）在**范围**选项卡下，使用**优化选帧**功能进行更智能的帧选择。
6. 在 **范围** 下选择导出质量：**快速 (1080p)**、**精细 (1440p)** 或 **最高 (4K)**。
7. 点击 **导出 PNG**。

## 安装

请从 [版本发布](https://github.com/worstgirlinamerica/PerfectGrid/releases/latest) 页面下载适用于您操作系统的最新版本。

### macOS

1. 下载 `PerfectGrid-v0.1.2-macos-universal.zip`。
2. 双击解压，然后将 Perfect Grid 拖拽到“应用程序”文件夹中。
3. 打开 `Perfect Grid.app`。

> 由于该应用未签名，macOS 会在首次启动时阻止其运行。请右键点击 → **打开** → **打开** 以绕过此限制。 如果仍然无法打开，请在终端中运行以下命令：`xattr -cr "/Applications/Perfect Grid.app"`

### Windows

1. 下载 `PerfectGrid-v0.1.2-Windows-x86_64.zip`。
2. 右键单击 → **全部解压**，然后打开该文件夹。
3. 双击 `Perfect Grid.exe`。

> 由于该应用未进行代码签名，Windows SmartScreen 可能会发出警告。点击 **更多信息** → **仍要运行**。

### Linux

1. 下载 `PerfectGrid-v0.1.2-Linux-x86_64.AppImage`。
2. 赋予其可执行权限并运行：
```bash
chmod +x PerfectGrid-v0.1.2-Linux-x86_64.AppImage
./PerfectGrid-v0.1.2-Linux-x86_64.AppImage
```

无需安装——FFmpeg 及所有依赖项均已打包。可在大多数 x86_64 发行版上运行（Ubuntu 22.04 及以上、Fedora、Arch 等）。

> 若遇到 FUSE 错误：请执行 `sudo apt install fuse`（Debian/Ubuntu）或 `sudo dnf install fuse`（Fedora）。

## 隐私

所有操作均在本地进行。无分析、无遥测、无上传。FFmpeg 和 FFprobe 已打包其中。

## 注意事项

- 支持 MP4、MOV、MKV、AVI、WebM 以及 FFmpeg 能读取的任何格式。
- 在较旧的硬件上，AV1 和 VP9 的解码速度可能较慢。
- macOS 版本未签名 —— 请参阅上文的安装说明。

<details>
<summary>开发者专区</summary>

```bash
python -m pip install -r requirements.txt
PYTHONPATH=src python -m perfect_grid.app
```

若从源代码运行并需完整支持阿拉伯语/从右到左（RTL）文件名，请执行：

```bash
pip install arabic-reshaper python-bidi
```

构建脚本位于 `scripts/` 目录中。GitHub Actions 会在推送带标签的代码时自动构建 Windows 和 Linux 版本。macOS 版本需手动构建。

</details>

## 贡献

如果您遇到任何错误或问题，请通过创建 [问题](https://github.com/worstgirlinamerica/PerfectGrid/issues/new) 告知我们。
请务必提供以下关键信息：您的操作系统、视频格式，以及问题发生在预览、精修、导出还是批量处理阶段。

更多详情请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可协议

MIT 许可。请参阅 [LICENSE](LICENSE)。
