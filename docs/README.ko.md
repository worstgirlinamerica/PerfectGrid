<p align="center">
  <img src="https://raw.githubusercontent.com/worstgirlinamerica/PerfectGrid/main/assets/icon.png" width="80" alt="Perfect Grid">
  <h1 align="center">Perfect Grid</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/worstgirlinamerica/PerfectGrid?color=E95420" alt="GitHub 릴리스">
  <img src="https://img.shields.io/github/downloads/worstgirlinamerica/PerfectGrid/total" alt="다운로드">
  <img src="https://img.shields.io/github/license/worstgirlinamerica/PerfectGrid" alt="라이선스">
</p>

<p align="center">
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.zh.md">중국어</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.pt.md">포르투갈어</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.es.md)">스페인어</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.ja.md">일본어</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.fr.md">프랑스어</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.de.md">독일어</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.ko.md">한국어</a> &nbsp;|&nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/blob/main/docs/README.ar.md">아랍어</a>
</p>

Perfect Grid는 로컬 동영상 파일로 동영상 콘택트 시트와 미리보기 썸네일을 생성할 수 있는 무료 오픈 소스 데스크톱 앱입니다. 동영상을 불러오고 레이아웃을 선택한 후 고화질 PNG 콘택트 시트로 내보내세요.

편집자, 수집가, 아카이브 담당자, 그리고 동영상의 빠른 시각적 요약을 원하는 모든 분을 위해 제작되었습니다.

<p align="center">
  <img src="https://i.imgur.com/HVf0JjP.jpeg" alt="Perfect Grid로 만든 예시 미리보기 시트">
  <br>
  <em>Perfect Grid로 생성된 예시 콘택트 시트.</em>
</p>

<p align="center">
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-macOS-000000?logo=apple&logoColor=white" alt="macOS용 다운로드">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Windows-0078D6?logo=windows11&logoColor=white" alt="Windows용 다운로드">
  </a>&#8203; &nbsp;
  <a href="https://github.com/worstgirlinamerica/PerfectGrid/releases/latest">
    <img src="https://custom-icon-badges.demolab.com/badge/Download-Linux-E95420?logo=linux&logoColor=white" alt="Linux용 다운로드">
  </a>
</p>
<p align="center"><sub>배지는 최신 릴리스로 연결됩니다. 사용 중인 OS(macOS의 경우 칩 종류도 포함)에 맞는 파일을 다운로드하세요.</sub></p>

## 기능

- 고급 비디오 메타데이터(해상도, 코덱, 재생 시간, 파일 크기 등)를 표시하는 고품질 콘택트 시트 생성
- 작업 공간을 넓혀주는 크기 조절 가능한 사이드바를 갖춘, 완전히 사용자 정의 가능한 그리드 레이아웃
- 선택 가능한 타임코드 오버레이
- **Refine Picks** 기능을 통한 스마트 프레임 선택
- 하드웨어 인식 미리보기 생성을 지원하는 PyAV 기반 추출 엔진으로, 다양한 CPU/아키텍처에서 빠른 미리보기 속도를 유지합니다
- 설정에서 초기 추출 단계의 품질을 조정할 수 있습니다
- 사용자 지정 프리셋을 저장하고 재사용할 수 있습니다
- 일괄 처리
- Windows, macOS, Linux에서 실행됩니다
> __어떤__ 오류가 발생하거나, 기능이 제대로 작동하지 않거나, 궁금한 점이 있다면 [이슈](https://github.com/worstgirlinamerica/PerfectGrid/issues/new)를 생성하여 신고해 주세요.

## 기본 사용법

1. Perfect Grid를 실행합니다.
2. 창 안으로 동영상을 드래그합니다.
3. 그리드 레이아웃과 스타일을 조정합니다. 레이아웃을 변경한 경우, **미리보기 새로 고침**을 클릭하여 썸네일을 다시 생성하세요.
4. 미리보기 화질은 의도적으로 낮게 설정되어 있습니다. 내보내기 시에는 항상 사용자가 선택한 화질 설정이 적용됩니다.
5. (선택 사항) **범위** 탭에서 **선택 항목 다듬기**를 사용하여 더 정교하게 프레임을 선택하세요.
6. **범위**에서 내보내기 화질을 선택하세요: **빠름 (1080p)**, **세부 (1440p)** 또는 **최대 (4K)**.
7. **PNG 내보내기**를 클릭하세요.

## 설치

[릴리스](https://github.com/worstgirlinamerica/PerfectGrid/releases/latest) 페이지에서 사용 중인 OS에 맞는 최신 릴리스를 다운로드하세요.

### macOS

1. 사용 중인 칩에 맞는 빌드를 다운로드하세요: `PerfectGrid-<버전>-macOS-arm64.zip` (Apple Silicon) 또는 `PerfectGrid-<버전>-macOS-x86_64.zip` (Intel). 어떤 칩을 사용 중인지 확실하지 않으신가요? Apple 메뉴 → **이 Mac에 관하여**를 확인하세요.
2. 파일을 두 번 클릭하여 압축을 풀고, Perfect Grid를 ‘응용 프로그램’ 폴더로 드래그하세요.
3. `Perfect Grid.app`을 실행하세요.

> macOS는 서명이 되어 있지 않은 앱이므로 첫 실행 시 차단합니다. 마우스 오른쪽 버튼 클릭 → **열기** → **열기**를 선택하여 차단 메시지를 해제하세요. 그래도 열리지 않으면 터미널에서 다음 명령을 실행하세요: `xattr -cr "/Applications/Perfect Grid.app"`

### Windows

1. `PerfectGrid-<버전>-Windows-x86_64.zip`을 다운로드하세요.
2. 마우스 오른쪽 버튼을 클릭 → **모두 추출**을 선택한 후, 폴더를 여세요.
3. `Perfect Grid.exe`를 더블 클릭하세요.

> 앱에 코드 서명이 되어 있지 않아 Windows SmartScreen에서 경고 메시지가 표시될 수 있습니다. **자세히 보기** → **어쨌든 실행**을 클릭하세요.

### 리눅스

1. `PerfectGrid-<버전>-Linux-x86_64.AppImage`를 다운로드하세요.
2. 실행 권한을 부여하고 실행합니다:
```bash
chmod +x PerfectGrid-<버전>-Linux-x86_64.AppImage
./PerfectGrid-<버전>-Linux-x86_64.AppImage
```

설치가 필요하지 않습니다. FFmpeg 및 모든 종속성이 포함되어 있습니다. 대부분의 x86_64 배포판(Ubuntu 22.04 이상, Fedora, Arch 등)에서 작동합니다.

> FUSE 오류가 발생하면: `sudo apt install fuse` (Debian/Ubuntu) 또는 `sudo dnf install fuse` (Fedora)를 실행하세요.

## 개인정보 보호

모든 작업은 로컬에서 실행됩니다. 분석, 원격 측정, 파일 업로드가 없습니다. FFmpeg와 FFprobe가 포함되어 있습니다.

## 현지화

앱 UI는 8개 언어로 제공됩니다. 시트 파일명 렌더링은 별도의 시스템으로, 내보낸 PNG 파일에 파일명을 픽셀로 그려 넣기 때문에 스크립트별 글꼴 처리가 필요합니다.

| 언어 | UI | 시트 내 |
|---|---|---|
| 영어 | 예 | 예 |
| 중국어 (中文) | 예 | 예 (macOS, Windows) |
| 포르투갈어 (PT) | 예 | 예 |
| 스페인어 (ES) | 예 | 예 |
| 일본어 (JA) | 예 | 예 (macOS, Windows) |
| 프랑스어 (FR) | 예 | 예 |
| 독일어 (DE) | 예 | 예 |
| 한국어 (KO) | 예 | 예 (macOS, Windows) |
| 아랍어 / RTL | — | 예 |
| 히브리어 | — | — |
| 태국어 | — | — |
| 데바나가리 (힌디어 등) | — | — |

> 현재 Linux에서 비-ASCII 파일 이름 표시는 지원되지 않습니다. 라틴 문자가 아닌 스크립트로 된 파일 이름은 사각형으로 표시됩니다. 이 문제는 다음 릴리스에서 수정될 예정입니다!

## 참고 사항

- MP4, MOV, MKV, AVI, WebM 및 FFmpeg가 읽을 수 있는 모든 형식을 지원합니다.
- 구형 하드웨어에서는 AV1 및 VP9 디코딩 속도가 느릴 수 있습니다.
- macOS 빌드는 서명되지 않았습니다 — 위의 설치 참고 사항을 확인하세요.

<details>
<summary>개발자용</summary>

```bash
python -m pip install -r requirements.txt
PYTHONPATH=src python -m perfect_grid.app
```

소스 코드에서 실행 시 아랍어/RTL 파일 이름을 완전히 지원하려면:

```bash
pip install arabic-reshaper python-bidi
```

빌드 스크립트는 `scripts/` 디렉터리에 있습니다. GitHub Actions는 태그가 지정된 푸시가 있을 때 Windows, Linux 및 macOS(arm64 + x86_64) 릴리스를 자동으로 빌드합니다.

</details>

## 기여

버그나 오류가 발생하면 [이슈](https://github.com/worstgirlinamerica/PerfectGrid/issues/new)를 생성하여 알려 주시기 바랍니다. 
포함하면 가장 유용한 정보는 사용 중인 OS, 비디오 형식, 그리고 문제가 미리보기, 다듬기, 내보내기 또는 일괄 처리 단계 중 어디에서 발생했는지입니다.

자세한 내용은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요.

## 라이선스

MIT. [LICENSE](LICENSE)를 참조하세요.
