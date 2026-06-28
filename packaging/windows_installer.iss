[Setup]
AppId={{1F86F69C-A43B-4C26-8EE7-31D2F6D03E65}
AppName=Perfect Grid
AppVersion=1.0.0
AppPublisher=Perfect Grid
DefaultDirName={autopf}\Perfect Grid
DefaultGroupName=Perfect Grid
OutputDir=installer
OutputBaseFilename=PerfectGridSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "..\dist_windows\Perfect Grid\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Perfect Grid"; Filename: "{app}\Perfect Grid.exe"
Name: "{autodesktop}\Perfect Grid"; Filename: "{app}\Perfect Grid.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Run]
Filename: "{app}\Perfect Grid.exe"; Description: "Launch Perfect Grid"; Flags: nowait postinstall skipifsilent
