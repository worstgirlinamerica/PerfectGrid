<p align="center">
  <img src="assets/icon.png" width="80" alt="Perfect Grid">
  <h1 align="center">Perfect Grid</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/worstgirlinamerica/PerfectGrid" alt="GitHub Release">
  <img src="https://img.shields.io/github/downloads/worstgirlinamerica/PerfectGrid/total" alt="ダウンロード">
  <img src="https://img.shields.io/github/license/worstgirlinamerica/PerfectGrid" alt="ライセンス">
</p>

<p align="center">
  <a href="docs/README.zh.md">中国語</a> &nbsp;|&nbsp;
  <a href="docs/README.pt.md">ポルトガル語</a> &nbsp;|&nbsp;
  <a href="docs/README.es.md">スペイン語</a> &nbsp;|&nbsp;
  <a href="docs/README.ja.md">日本語</a> &nbsp;|&nbsp;
  <a href="docs/README.fr.md">フランス語</a> &nbsp;|&nbsp;
  <a href="docs/README.de.md">ドイツ語</a> &nbsp;|&nbsp;
  <a href="docs/README.ko.md">韓国語</a> &nbsp;|&nbsp;
  <a href="docs/README.ar.md">アラビア語</a>
</p>

Perfect Gridは、ローカルの動画ファイルから動画コンタクトシートやプレビューサムネイルを作成するための、無料のオープンソースデスクトップアプリです。動画をドラッグ＆ドロップし、レイアウトを選択するだけで、高品質なPNG形式のコンタクトシートをエクスポートできます。

編集者、コレクター、アーキビスト、そして動画の概要を素早く視覚的に把握したいすべての方のために開発されました。

<p align="center">
  <img src="https://i.imgur.com/HVf0JjP.jpeg" alt="Perfect Gridで作成されたプレビューシートの例">
  <br>
  <em>Perfect Gridで生成されたコンタクトシートの例。</em>
</p>

<p align="center">
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-macos-universal.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-macOS-000000?logo=apple&logoColor=white" alt="macOS用ダウンロード">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-Windows-x86_64.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Windows-0078D6?logo=windows11&logoColor=white" alt="Windows用をダウンロード">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-Linux-x86_64.AppImage">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Linux-E95420?logo=linux&logoColor=white" alt="Linux版をダウンロード">
  </a>
</p>

## 機能

- 高度な動画メタデータ（解像度、コーデック、再生時間、ファイルサイズなど）を表示した高品質なコンタクトシートを生成
- 完全にカスタマイズ可能なグリッドレイアウト
- オプションでタイムコードのオーバーレイ表示
- **Refine Picks** によるスマートなフレーム選択
- カスタムプリセットの保存と再利用
- バッチ処理
- Windows、macOS、Linux で動作
> __いかなる__エラーが発生した場合、動作しない箇所がある場合、またはご質問がある場合は、[Issue](https://github.com/worstgirlinamerica/PerfectGrid/issues/new) を作成して報告してください。

## ローカライズ

アプリの UI は 8 言語に対応しています。シートのファイル名の表示は別のシステムで処理されており、エクスポートされた PNG ファイル上にファイル名をピクセルとして描画するため、スクリプト独自のフォント処理が必要となります。

| 言語 | UI | シート上 |
|---|---|---|
| 英語 | 対応 | 対応 |
| 中国語 (中文) | 対応 | 対応 (macOS、Windows) |
| ポルトガル語 (PT) | 対応 | 対応 |
| スペイン語 (ES) | 対応 | 対応 |
| 日本語 (JA) | 対応 | 対応 (macOS、Windows) |
| フランス語 (FR) | はい | はい |
| ドイツ語 (DE) | はい | はい |
| 韓国語 (KO) | はい | はい (macOS、Windows) |
| アラビア語 / RTL | — | はい |
| ヘブライ語 | — | — |
| タイ語 | — | — |
| デーヴァナーガリー文字（ヒンディー語など） | — | — |

> 現在、Linux における非 ASCII ファイル名の表示はサポートされていません。ラテン文字以外の文字で書かれたファイル名は四角いボックスとして表示されます。これは次回のリリースで修正される予定です！

## 基本的な使い方

1. Perfect Grid を起動します。
2. 動画をウィンドウにドラッグします。
3. グリッドのレイアウトとスタイルを調整します。レイアウトを変更した場合は、**プレビューの更新** をクリックしてサムネイルを再生成してください。
4. プレビューの画質は意図的に低く設定されています。エクスポート時には、選択した画質設定が常に適用されます。
5. （オプション）**範囲**タブで、**選択範囲の絞り込み**を使用すると、より的確にフレームを選択できます。
6. **Range** タブで、エクスポート画質を **Fast (1080p)**、**Detail (1440p)**、または **Maximum (4K)** から選択します。
7. **Export PNG** をクリックします。

## インストール

[リリース](https://github.com/worstgirlinamerica/PerfectGrid/releases/latest)ページから、お使いのOSに対応した最新バージョンをダウンロードしてください。

### macOS

1. `PerfectGrid-v0.1.2-macos-universal.zip`をダウンロードします。
2. ダブルクリックして解凍し、Perfect Grid を「アプリケーション」フォルダにドラッグします。
3. `Perfect Grid.app` を開きます。

> 署名がないため、macOS は初回起動時にアプリをブロックします。右クリック → **開く** → **開く** を選択してブロックを解除してください。 それでも開かない場合は、ターミナルで `xattr -cr "/Applications/Perfect Grid.app"` を実行してください。

### Windows

1. `PerfectGrid-v0.1.2-Windows-x86_64.zip` をダウンロードします。
2. 右クリック → **すべて展開** を選択し、フォルダを開きます。
3. `Perfect Grid.exe` をダブルクリックします。

> アプリはコード署名されていないため、Windows SmartScreen から警告が表示される場合があります。**詳細** → **それでも実行** をクリックしてください。

### Linux

1. `PerfectGrid-v0.1.2-Linux-x86_64.AppImage` をダウンロードします。
2. 実行可能にして実行します：
```bash
chmod +x PerfectGrid-v0.1.2-Linux-x86_64.AppImage
./PerfectGrid-v0.1.2-Linux-x86_64.AppImage
```

インストールは不要です。FFmpeg およびすべての依存関係が同梱されています。ほとんどの x86_64 ディストリビューション（Ubuntu 22.04 以降、Fedora、Arch など）で動作します。

> FUSEエラーが発生した場合は、`sudo apt install fuse`（Debian/Ubuntu）または`sudo dnf install fuse`（Fedora）を実行してください。

## プライバシー

すべての処理はローカルで行われます。分析、テレメトリ、アップロードは一切行われません。FFmpegとFFprobeが同梱されています。

## 注意事項

- MP4、MOV、MKV、AVI、WebM、および FFmpeg が読み込めるすべての形式に対応しています。
- 古いハードウェアでは、AV1 および VP9 のデコードに時間がかかる場合があります。
- macOS 版は署名されていません。上記のインストールに関する注意事項を参照してください。

<details>
<summary>開発者向け</summary>

```bash
python -m pip install -r requirements.txt
PYTHONPATH=src python -m perfect_grid.app
```

ソースから実行する際、アラビア語/RTLファイル名を完全にサポートするには：

```bash
pip install arabic-reshaper python-bidi
```

ビルドスクリプトは `scripts/` ディレクトリにあります。GitHub Actions では、タグ付きプッシュが行われると Windows および Linux 版が自動的にビルドされます。macOS 版は手動でビルドしてください。

</details>

## 貢献について

バグやエラーが発生した場合は、[Issue](https://github.com/worstgirlinamerica/PerfectGrid/issues/new) を作成してご連絡ください。
記載していただくと特に役立つ情報として、お使いのOS、動画形式、および問題が「プレビュー」「リファイン」「エクスポート」、あるいは「バッチ」のどの段階で発生したかなどがあります。

詳細は [CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

## ライセンス

MIT ライセンスです。[LICENSE](LICENSE) をご覧ください。
