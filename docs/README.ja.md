# Perfect Grid

[![GitHub Release](https://img.shields.io/github/v/release/worstgirlinamerica/PerfectGrid?)](https://github.com/worstgirlinamerica/PerfectGrid/releases)
[![Downloads](https://img.shields.io/github/downloads/worstgirlinamerica/PerfectGrid/total?)](https://github.com/worstgirlinamerica/PerfectGrid/releases)
[![License](https://img.shields.io/github/license/worstgirlinamerica/PerfectGrid?)](LICENSE)

Perfect Grid は、ローカルの動画ファイルからコンタクトシートとサムネイルを作成するための、無料・オープンソースのデスクトップアプリです。

動画をドロップしてレイアウトを選ぶだけで、高品質なPNGコンタクトシートを書き出せます。映像編集者、コレクター、アーカイビスト、動画をひと目で把握したいすべての人向けに作られています。

<p align="center">
  <img src="https://i.imgur.com/HVf0JjP.jpeg" alt="Perfect Grid で生成したコンタクトシートの例">
  <br>
  <em>Perfect Grid で生成したコンタクトシートの例。</em>
</p>

<p align="center">
<a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-macos-universal.zip">
  <img src="https://custom-icon-badges.demolab.com/badge/Download-macOS-000000?style=for-the-badge&logo=apple&logoColor=white" alt="macOS 版をダウンロード">
</a>
<a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/Perfect-Grid-Windows.zip">
  <img src="https://custom-icon-badges.demolab.com/badge/Download-Windows-0078D6?style=for-the-badge&logo=windows21&logoColor=white" alt="Windows 版をダウンロード">
</a>
<a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/Perfect-Grid-x86_64.AppImage">
  <img src="https://custom-icon-badges.demolab.com/badge/Download-Linux-E95420?style=for-the-badge&logo=linux&logoColor=white" alt="Linux 版をダウンロード">
</a>
</p>

## 機能

- 高品質な PNG コンタクトシートを生成
- グリッドレイアウトを自由にカスタマイズ
- タイムコードオーバーレイ（任意）
- 動画メタデータ表示（解像度、コーデック、再生時間、ファイルサイズ等）
- **フレームを絞り込む** によるスマートなフレーム選択
- カスタムプリセットの保存と再利用
- 一括処理
- 英語・中国語・ポルトガル語・スペイン語・日本語・フランス語・ドイツ語・韓国語の UI 対応
- アラビア語・CJK・その他の非ラテン文字ファイル名を正しく表示
- Windows、macOS、Linux 対応

## 基本的な使い方

1. Perfect Grid を開く。
2. 動画ウィンドウにドロップする。
3. グリッドレイアウトとスタイルを調整。レイアウトを変更した場合は **プレビューを更新** をクリック。
4. プレビューは意図的に低品質 — 書き出しは常に選択した品質設定が使われます。
5. （任意）**範囲** タブで **フレームを絞り込む** を使うと、よりスマートなフレーム選択ができます。
6. **範囲** タブで書き出し品質を選択：**高速 (1080p)**、**詳細 (1440p)**、**最高画質 (4K)**。
7. **PNG 書き出し** をクリック。

## ダウンロードとインストール

[Releases](https://github.com/worstgirlinamerica/PerfectGrid/releases/latest) ページから最新版をダウンロードしてください。

### macOS

1. `PerfectGrid-v0.1.2-macos-universal.zip` をダウンロード。
2. 展開して Perfect Grid をアプリケーションフォルダにドラッグ。
3. 初回起動時に macOS がブロックした場合、ターミナルで以下を実行：

```bash
xattr -cr "/Applications/Perfect Grid.app"
```

### Windows

1. `Perfect-Grid-Windows.zip` をダウンロード。
2. 任意のフォルダに展開。
3. `Perfect Grid.exe` を実行。

### Linux

1. `Perfect-Grid-x86_64.AppImage` をダウンロード。
2. 実行権限を付与して起動：

```bash
chmod +x Perfect-Grid-x86_64.AppImage
./Perfect-Grid-x86_64.AppImage
```

FFmpeg は同梱されています — 別途インストール不要。

## ライセンス

MIT。詳細は [LICENSE](../LICENSE) を参照してください。
