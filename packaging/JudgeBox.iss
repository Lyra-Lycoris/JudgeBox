#ifndef StageDir
  #define StageDir "..\.runtime\release\JudgeBox"
#endif
#ifndef OutputDir
  #define OutputDir "..\dist"
#endif
[Setup]
AppId={{B5AE8D65-EB14-44CB-81CF-8653D73B62F3}
AppName=JudgeBox
AppVersion=1.1.2
AppPublisher=JudgeBox
DefaultDirName={localappdata}\Programs\JudgeBox
DefaultGroupName=JudgeBox
DisableProgramGroupPage=yes
AllowUNCPath=no
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0.22000
OutputDir={#OutputDir}
OutputBaseFilename=JudgeBox-Setup-1.1.2-x64
Compression=lzma2/fast
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMADictionarySize=16384
WizardStyle=modern
UninstallDisplayIcon={app}\JudgeBox.exe
SetupLogging=yes
CloseApplications=yes
[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; Flags: unchecked
[Files]
Source: "{#StageDir}\*"; DestDir: "{app}"; Excludes: "*.pyc,.judgebox-stage-owner"; Flags: ignoreversion recursesubdirs createallsubdirs
[InstallDelete]
Type: filesandordirs; Name: "{app}\runtimes"; Check: OwnsInstalledBundle
Type: filesandordirs; Name: "{app}\diagnostics"; Check: OwnsInstalledBundle
Type: filesandordirs; Name: "{app}\notices"; Check: OwnsInstalledBundle
Type: filesandordirs; Name: "{app}\validation"; Check: OwnsInstalledBundle
[Icons]
Name: "{group}\JudgeBox"; Filename: "{app}\JudgeBox.exe"; WorkingDir: "{app}"
Name: "{group}\Check Toolchains"; Filename: "{app}\Check-Toolchains.cmd"; WorkingDir: "{app}"
Name: "{autodesktop}\JudgeBox"; Filename: "{app}\JudgeBox.exe"; WorkingDir: "{app}"; Tasks: desktopicon
[Run]
Filename: "{app}\JudgeBox.exe"; Description: "Launch JudgeBox"; Flags: nowait postinstall skipifsilent
[Code]
var
  OwnershipChecked: Boolean;
  PreviouslyOwnedBundle: Boolean;

function OwnsInstalledBundle: Boolean;
var
  Identity: AnsiString;
begin
  if not OwnershipChecked then begin
    OwnershipChecked := True;
    PreviouslyOwnedBundle := LoadStringFromFile(ExpandConstant('{app}\runtimes\bundle-owner.txt'), Identity);
    if PreviouslyOwnedBundle then
      PreviouslyOwnedBundle := Trim(String(Identity)) = 'JudgeBox.OfflineToolchains';
  end;
  Result := PreviouslyOwnedBundle;
end;
