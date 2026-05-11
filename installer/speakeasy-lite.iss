[Setup]
AppName=Speakeasy Lite
AppVersion=1.0
AppPublisher=Speakeasy Lite
DefaultDirName={localappdata}\SpeakeasyLite
DefaultGroupName=Speakeasy Lite
OutputBaseFilename=SpeakeasyLite-Setup
OutputDir=..\
SetupIconFile=..\app\assets\icon.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
DisableProgramGroupPage=yes
DisableWelcomePage=no

[Files]
Source: "..\dist\SpeakeasyLite\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{autodesktop}\Speakeasy Lite";                         Filename: "{app}\SpeakeasyLite.exe"
Name: "{autoprograms}\Speakeasy Lite\Speakeasy Lite";         Filename: "{app}\SpeakeasyLite.exe"
Name: "{autoprograms}\Speakeasy Lite\Uninstall Speakeasy Lite"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\SpeakeasyLite.exe"; Description: "Launch Speakeasy Lite"; Flags: postinstall nowait skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\models"
Type: filesandordirs; Name: "{app}\temp"
Type: files;          Name: "{app}\speakeasy.log"
