<p align="center">
  <img src="https://raw.githubusercontent.com/worstgirlinamerica/PerfectGrid/main/assets/icon.png" width="80" alt="Perfect Grid">
  <h1 align="center">Perfect Grid</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/worstgirlinamerica/PerfectGrid?color=E95420" alt="GitHub-Veröffentlichung">
  <img src="https://img.shields.io/github/downloads/worstgirlinamerica/PerfectGrid/total" alt="Downloads">
  <img src="https://img.shields.io/github/license/worstgirlinamerica/PerfectGrid" alt="Lizenz">
</p>

<p align="center">
  <a href="docs/README.zh.md">Chinesisch</a> &nbsp;|&nbsp;
  <a href="docs/README.pt.md">Portugiesisch</a> &nbsp;|&nbsp;
  <a href="docs/README.es.md">Español</a> &nbsp;|&nbsp;
  <a href="docs/README.ja.md">日本語</a> &nbsp;|&nbsp;
  <a href="docs/README.fr.md">Französisch</a> &nbsp;|&nbsp;
  <a href="docs/README.de.md">Deutsch</a> &nbsp;|&nbsp;
  <a href="docs/README.ko.md">Koreanisch</a> &nbsp;|&nbsp;
  <a href="docs/README.ar.md">Arabisch</a>
</p>

Perfect Grid ist eine kostenlose Open-Source-Desktop-Anwendung zum Erstellen von Video-Kontaktabzügen und Vorschaubildern aus lokalen Videodateien. Laden Sie ein Video hoch, wählen Sie Ihr Layout aus und exportieren Sie einen hochwertigen PNG-Kontaktabzug.

Entwickelt für Cutter, Sammler, Archivare und alle, die sich einen schnellen visuellen Überblick über ein Video verschaffen möchten.

<p align="center">
  <img src="https://i.imgur.com/HVf0JjP.jpeg" alt="Beispiel für ein mit Perfect Grid erstelltes Vorschaublatt">
  <br>
  <em>Beispiel für ein mit Perfect Grid erstelltes Kontaktblatt.</em>
</p>

<p align="center">
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-macos-universal.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-macOS-000000?logo=apple&logoColor=white" alt="Download für macOS">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-Windows-x86_64.zip">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Windows-0078D6?logo=windows11&logoColor=white" alt="Download für Windows">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest/download/PerfectGrid-v0.1.2-Linux-x86_64.AppImage">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Linux-E95420?logo=linux&logoColor=white" alt="Für Linux herunterladen">
  </a>
</p>

## Funktionen

- Erstellen Sie hochwertige Kontaktabzüge mit erweiterter Anzeige von Video-Metadaten (Auflösung, Codecs, Dauer, Dateigröße usw.)
- Vollständig anpassbare Rasterlayouts
- Optionale Timecode-Einblendungen
- Intelligente Bildauswahl mit **„Refine Picks“**
- Speichern und Wiederverwenden benutzerdefinierter Voreinstellungen
- Stapelverarbeitung
- Läuft unter Windows, macOS und Linux
> Sollten Sie __irgendwelche__ Fehler feststellen, sollte etwas nicht funktionieren oder sollten Sie Fragen haben, erstellen Sie bitte ein [Issue](https://github.com/worstgirlinamerica/PerfectGrid/issues/new), um dies zu melden.

## Grundlegende Verwendung

1. Öffne Perfect Grid.
2. Ziehe ein Video in das Fenster.
3. Passe das Rasterlayout und das Design an. Wenn du das Layout änderst, klicke auf **Vorschau aktualisieren**, um die Miniaturansichten neu zu generieren.
4. Die Vorschauen sind absichtlich in geringerer Qualität – beim Export wird immer die von dir gewählte Qualitätseinstellung verwendet.
5. (Optional) Verwenden Sie auf der Registerkarte **Bereich** die Funktion **Auswahl verfeinern** für eine intelligentere Auswahl der Einzelbilder.
6. Wählen Sie unter **Bereich** eine Exportqualität aus: **Schnell (1080p)**, **Detail (1440p)** oder **Maximal (4K)**.
7. Klicken Sie auf **PNG exportieren**.

## Installation

Laden Sie die neueste Version für Ihr Betriebssystem von der Seite [Veröffentlichungen](https://github.com/worstgirlinamerica/PerfectGrid/releases/latest) herunter.

### macOS

1. Laden Sie `PerfectGrid-v0.1.2-macos-universal.zip` herunter.
2. Doppelklicken Sie zum Entpacken darauf und ziehen Sie „Perfect Grid“ anschließend in den Ordner „Programme“.
3. Öffnen Sie `Perfect Grid.app`.

> macOS blockiert die App beim ersten Start, da sie nicht signiert ist. Klicken Sie mit der rechten Maustaste darauf → **Öffnen** → **Öffnen**, um diese Sperre zu umgehen. Falls sich die App immer noch nicht öffnen lässt, führen Sie folgenden Befehl im Terminal aus: `xattr -cr "/Applications/Perfect Grid.app"`

### Windows

1. Laden Sie `PerfectGrid-v0.1.2-Windows-x86_64.zip` herunter.
2. Rechtsklick → **Alle extrahieren**, dann den Ordner öffnen.
3. Doppelklick auf `Perfect Grid.exe`.

> Windows SmartScreen zeigt möglicherweise eine Warnung an, da die App nicht codesigniert ist. Klicken Sie auf **Weitere Informationen** → **Trotzdem ausführen**.

### Linux

1. Lade `PerfectGrid-v0.1.2-Linux-x86_64.AppImage` herunter.
2. Mach die Datei ausführbar und führe sie aus:
```bash
chmod +x PerfectGrid-v0.1.2-Linux-x86_64.AppImage
./PerfectGrid-v0.1.2-Linux-x86_64.AppImage
```

Keine Installation erforderlich – FFmpeg und alle Abhängigkeiten sind im Paket enthalten. Funktioniert auf den meisten x86_64-Distributionen (Ubuntu 22.04+, Fedora, Arch usw.).

> Falls ein FUSE-Fehler auftritt: `sudo apt install fuse` (Debian/Ubuntu) oder `sudo dnf install fuse` (Fedora).

## Datenschutz

Alles läuft lokal. Keine Analysen, keine Telemetrie, keine Uploads. FFmpeg und FFprobe sind im Paket enthalten.

## Lokalisierung

Die Benutzeroberfläche der App ist in 8 Sprachen verfügbar. Die Darstellung der Dateinamen auf dem Blatt erfolgt über ein separates System – dabei werden die Dateinamen als Pixel auf das exportierte PNG gezeichnet, was eine skriptspezifische Schriftartverarbeitung erfordert.

| Sprache | Benutzeroberfläche | Auf dem Blatt |
|---|---|---|
| Englisch | Ja | Ja |
| Chinesisch (中文) | Ja | Ja (macOS, Windows) |
| Portugiesisch (PT) | Ja | Ja |
| Spanisch (ES) | Ja | Ja |
| Japanisch (JA) | Ja | Ja (macOS, Windows) |
| Französisch (FR) | Ja | Ja |
| Deutsch (DE) | Ja | Ja |
| Koreanisch (KO) | Ja | Ja (macOS, Windows) |
| Arabisch / RTL | — | Ja |
| Hebräisch | — | — |
| Thailändisch | — | — |
| Devanagari (Hindi usw.) | — | — |

> Die Darstellung von Nicht-ASCII-Dateinamen unter Linux wird derzeit nicht unterstützt – Dateinamen in nicht-lateinischen Schriften werden als Quadrate angezeigt. Dies wird in der nächsten Version behoben!

## Hinweise

- Unterstützt MP4, MOV, MKV, AVI, WebM und alles, was FFmpeg lesen kann.
- Die Dekodierung von AV1 und VP9 kann auf älterer Hardware langsam sein.
- Die macOS-Builds sind nicht signiert – siehe Installationshinweis oben.

<details>
<summary>Für Entwickler</summary>

```bash
python -m pip install -r requirements.txt
PYTHONPATH=src python -m perfect_grid.app
```

Für vollständige Unterstützung arabischer/RTL-Dateinamen bei der Ausführung aus dem Quellcode:

```bash
pip install arabic-reshaper python-bidi
```

Die Build-Skripte befinden sich in `scripts/`. GitHub Actions erstellt Windows- und Linux-Versionen automatisch bei getaggten Pushes. Die macOS-Version wird manuell erstellt.

</details>

## Mitwirken

Bitte teilen Sie uns Fehler oder Probleme mit, indem Sie ein [Issue](https://github.com/worstgirlinamerica/PerfectGrid/issues/new) erstellen. 
Die hilfreichsten Informationen sind Ihr Betriebssystem, das Videoformat und ob das Problem bei der Vorschau, der Verfeinerung, dem Export oder der Stapelverarbeitung aufgetreten ist.

Weitere Informationen finden Sie in [CONTRIBUTING.md](CONTRIBUTING.md).

## Lizenz

MIT. Siehe [LICENSE](LICENSE).
