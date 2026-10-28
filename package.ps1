param(
    [string]$Python = 'python',
    [string]$Msys = 'C:\msys64',
    [string]$Jdk = 'C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot',
    [string]$Cangjie = 'D:\Cangjie\cangjie',
    [switch]$SkipBuild,
    [switch]$SkipLocalMatrix,
    [switch]$SkipBundledMatrix,
    [switch]$SkipToInstall
)
$ErrorActionPreference = 'Stop'
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}
$utf8 = New-Object System.Text.UTF8Encoding $false
$projectDirectory = $PSScriptRoot
$stageDirectory = Join-Path $projectDirectory '.runtime\stage\JudgeBox'
$downloadDirectory = Join-Path $projectDirectory '.runtime\downloads'
$innoDirectory = Join-Path $projectDirectory '.runtime\inno'
$distDirectory = Join-Path $projectDirectory 'dist'
$artifactName = 'JudgeBox-Setup-1.1.2-x64.exe'
$artifact = Join-Path $distDirectory $artifactName
$unicodeDirName = -join @([char]0x4E2D, [char]0x6587, ' ', [char]0x5B89, [char]0x88C5)
$dataDirName = -join @([char]0x7528, [char]0x6237, [char]0x6570, [char]0x636E)
$installRoot = Join-Path $projectDirectory ".runtime\installer-test\$unicodeDirName"
$installDir = Join-Path $installRoot 'JudgeBox'
$dataDir = Join-Path $projectDirectory ".runtime\installer-test\$dataDirName"

function Invoke-Native {
    param([scriptblock]$Command, [string]$Failure)
    & $Command
    if ($LASTEXITCODE -ne 0) { throw $Failure }
}

function Test-StagedLayout {
    param([string]$Directory)
    $runtime = Join-Path $Directory 'runtimes'
    $required = @(
        'gcc\bin\g++.exe', 'python\python.exe', 'python\python314.zip', 'python\python314._pth',
        'jdk\bin\java.exe', 'jdk\bin\javac.exe', 'jdk\release', 'cangjie\bin\cjc.exe', 'manifest.json'
    )
    foreach ($relative in $required) {
        if (-not (Test-Path -LiteralPath (Join-Path $runtime $relative))) { return $false }
    }
    return $true
}

function Test-StagedVersions {
    param([string]$Directory)
    $runtime = Join-Path $Directory 'runtimes'
    $savedPath = $env:PATH
    $savedCangjie = $env:CANGJIE_HOME
    try {
        $gccBin = Join-Path $runtime 'gcc\bin'
        $env:PATH = $gccBin + ';' + $savedPath
        $gcc = (& (Join-Path $gccBin 'g++.exe') -dumpfullversion).Trim()
        if ($gcc -ne '16.1.0') { throw "Expected GCC 16.1.0, got $gcc" }
        $release = Get-Content -LiteralPath (Join-Path $runtime 'jdk\release') -Raw
        if ($release -notmatch 'JAVA_VERSION="21\.0\.11"') { throw 'Expected Temurin JDK 21.0.11' }
        $cangjieHome = Join-Path $runtime 'cangjie'
        $env:CANGJIE_HOME = $cangjieHome
        $env:PATH = (Join-Path $cangjieHome 'bin') + ';' + (Join-Path $cangjieHome 'runtime\lib\windows_x86_64_cjnative') + ';' + (Join-Path $cangjieHome 'lib\windows_x86_64_cjnative') + ';' + $savedPath
        $cangjie = (& (Join-Path $cangjieHome 'bin\cjc.exe') --version 2>&1 | Out-String)
        if ($cangjie -notmatch '1\.2\.0') { throw "Expected Cangjie 1.2.0, got $cangjie" }
        $embedded = Join-Path $runtime 'python\python.exe'
        $pythonVersion = (& $embedded -c 'import sys; print(sys.version.split()[0])').Trim()
        if ($pythonVersion -ne '3.14.9') { throw "Expected CPython 3.14.9, got $pythonVersion" }
    } finally {
        $env:PATH = $savedPath
        if ($null -eq $savedCangjie) { Remove-Item Env:CANGJIE_HOME -ErrorAction SilentlyContinue }
        else { $env:CANGJIE_HOME = $savedCangjie }
    }
}

function Test-EmbeddedPackages {
    param([string]$Directory)
    $embedded = Join-Path $Directory 'runtimes\python\python.exe'
    & $embedded -c "import importlib.metadata as metadata, sys; expected={'cyaron':'0.7.0','colorful':'0.5.8','colorama':'0.4.6','xeger':'0.4.0'}; found={item.metadata['Name'].lower(): item.version for item in metadata.distributions()}; missing={name: found.get(name) for name, version in expected.items() if found.get(name) != version}; print('ok' if not missing else missing); sys.exit(0 if not missing else 1)"
    return $LASTEXITCODE -eq 0
}

function Update-ApplicationFiles {
    param([string]$Directory)
    $runtime = Join-Path $Directory 'runtimes'
    New-Item -ItemType Directory -Force -Path (Join-Path $Directory 'diagnostics'), (Join-Path $Directory 'docs'), (Join-Path $Directory 'notices'), (Join-Path $runtime 'python\Lib\site-packages') | Out-Null
    Copy-Item -LiteralPath (Join-Path $projectDirectory 'build\JudgeBox.exe') -Destination (Join-Path $Directory 'JudgeBox.exe') -Force
    Copy-Item -LiteralPath (Join-Path $projectDirectory 'README.md') -Destination (Join-Path $Directory 'README.md') -Force
    $rule = @(Get-ChildItem -LiteralPath (Join-Path $projectDirectory 'docs') -File -Filter '*.md')
    if ($rule.Count -ne 1) { throw 'Expected exactly one Markdown document directly under docs.' }
    Copy-Item -LiteralPath $rule[0].FullName -Destination (Join-Path (Join-Path $Directory 'docs') $rule[0].Name) -Force
    Copy-Item -LiteralPath (Join-Path $projectDirectory 'tests\toolchain_matrix.py') -Destination (Join-Path $Directory 'diagnostics\toolchain_matrix.py') -Force
    Copy-Item -LiteralPath (Join-Path $projectDirectory 'third_party\json.LICENSE.MIT') -Destination (Join-Path $Directory 'notices\json.LICENSE.MIT') -Force
    [System.IO.File]::WriteAllText((Join-Path $Directory 'Check-Toolchains.cmd'), "@echo off`r`n`"%~dp0JudgeBox.exe`" --self-test`r`npause`r`n", [System.Text.Encoding]::ASCII)
    [System.IO.File]::WriteAllText((Join-Path $runtime 'bundle-owner.txt'), 'JudgeBox.OfflineToolchains', [System.Text.Encoding]::ASCII)
    [System.IO.File]::WriteAllText((Join-Path $runtime 'python\python314._pth'), "python314.zip`n.`nLib\site-packages`nimport site`n", [System.Text.Encoding]::ASCII)
    [System.IO.File]::WriteAllText((Join-Path $Directory '.judgebox-stage-owner'), 'JudgeBox stage v1', [System.Text.Encoding]::ASCII)
    $thirdParty = @"
JudgeBox invokes unmodified third-party tools as separate processes.

GCC and dependencies: original licenses are under runtimes/gcc/share/licenses and package descriptions under notices/msys2-packages. Exact source package locations and versions are recorded in runtimes/manifest.json. When redistributing binaries, also provide corresponding sources as required by each license; source locations alone do not replace those obligations.

Temurin OpenJDK: legal notices under runtimes/jdk/legal; source archive runtimes/jdk/lib/src.zip.
Cangjie: runtimes/cangjie/LICENSE and Open_Source_Software_Notice.docx.
Python: runtimes/python/LICENSE.txt.
Python packages: license metadata under runtimes/python/Lib/site-packages/*.dist-info.
"@
    [System.IO.File]::WriteAllText((Join-Path $Directory 'notices\THIRD-PARTY.txt'), $thirdParty.Replace("`r`n", "`n"), $utf8)
    $validation = Join-Path $Directory 'validation'
    if (Test-Path -LiteralPath $validation) { Remove-Item -LiteralPath $validation -Recurse -Force }
}

function Install-PythonPackages {
    param([string]$Directory)
    Invoke-Native { & $Python -m pip install --disable-pip-version-check --only-binary=:all: --no-compile --upgrade --target (Join-Path $Directory 'runtimes\python\Lib\site-packages') -r (Join-Path $projectDirectory 'packaging\python-requirements.txt') } 'Python package staging failed.'
    if (-not (Test-EmbeddedPackages $Directory)) { throw 'Embedded Python could not import the pinned packages.' }
}

function New-ToolchainStage {
    New-Item -ItemType Directory -Force -Path $downloadDirectory | Out-Null
    $pythonArchive = Join-Path $downloadDirectory 'python-3.14.9-embed-amd64.zip'
    if (-not (Test-Path -LiteralPath $pythonArchive)) {
        Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.14.9/python-3.14.9-embed-amd64.zip' -OutFile $pythonArchive
    }
    if ((Test-Path -LiteralPath $stageDirectory) -and ((Test-Path -LiteralPath (Join-Path $stageDirectory '.judgebox-stage-owner')) -or (Test-Path -LiteralPath (Join-Path $stageDirectory 'runtimes\gcc\bin\g++.exe')))) {
        Remove-Item -LiteralPath $stageDirectory -Recurse -Force
    }
    Invoke-Native { & $Python (Join-Path $projectDirectory 'scripts\stage_toolchains.py') --msys $Msys --jdk $Jdk --cangjie $Cangjie --python-zip $pythonArchive --output $stageDirectory } 'Toolchain staging failed.'
    Install-PythonPackages $stageDirectory
    Update-ApplicationFiles $stageDirectory
}

function Start-Quoted {
    param([string]$File, [string]$Arguments)
    $info = New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName = $File
    $info.Arguments = $Arguments
    $info.UseShellExecute = $false
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $info
    if (-not $process.Start()) { throw "Cannot start $File" }
    return $process
}

function Wait-SetupLog {
    param([string]$Log, [string]$SuccessPattern, [string]$TargetExe, [switch]$Absent)
    $deadline = (Get-Date).AddMinutes(8)
    do {
        $tail = ''
        try { if (Test-Path -LiteralPath $Log) { $tail = (Get-Content -LiteralPath $Log -Tail 40 -ErrorAction SilentlyContinue) -join "`n" } } catch { $tail = '' }
        $closed = $tail -match 'Log closed'
        $ok = $tail -match $SuccessPattern
        $present = Test-Path -LiteralPath $TargetExe
        $pathOk = if ($Absent) { -not $present } else { $present }
        if ($closed -and $ok -and $pathOk) { return }
        if ($closed -and -not $ok) { throw "Setup did not succeed. See $Log" }
        Start-Sleep -Milliseconds 400
    } while ((Get-Date) -lt $deadline)
    throw "Setup did not finish. See $Log"
}

function Uninstall-Directory {
    param([string]$Directory, [string]$Log)
    $uninstaller = Join-Path $Directory 'unins000.exe'
    $exe = Join-Path $Directory 'JudgeBox.exe'
    if (-not (Test-Path -LiteralPath $uninstaller)) {
        if (Test-Path -LiteralPath $exe) { throw "Installation at $Directory has JudgeBox.exe but no uninstaller." }
        return
    }
    Write-Host "Removing test installation: $Directory"
    if (Test-Path -LiteralPath $Log) { Remove-Item -LiteralPath $Log -Force }
    Start-Quoted -File $uninstaller -Arguments ('/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /LOG="' + $Log + '"') | Out-Null
    Wait-SetupLog -Log $Log -SuccessPattern 'Removed all\? Yes' -TargetExe $exe -Absent
}

function Uninstall-TestCopies {
    $root = Join-Path $projectDirectory '.runtime\installer-test'
    if (-not (Test-Path -LiteralPath $root)) { return }
    $uninstallers = @(Get-ChildItem -LiteralPath $root -Recurse -Filter 'unins000.exe' -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName)
    $index = 0
    foreach ($uninstaller in $uninstallers) {
        $index += 1
        Uninstall-Directory -Directory (Split-Path -Parent $uninstaller) -Log (Join-Path $root ("uninstall-$index.log"))
    }
}

function Install-Silent {
    param([string]$LogName)
    $log = Join-Path $projectDirectory ".runtime\installer-test\$LogName"
    if (Test-Path -LiteralPath $log) { Remove-Item -LiteralPath $log -Force }
    $exe = Join-Path $installDir 'JudgeBox.exe'
    Start-Quoted -File $artifact -Arguments ('/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /DIR="' + $installDir + '" /LOG="' + $log + '"') | Out-Null
    Wait-SetupLog -Log $log -SuccessPattern 'Installation process succeeded' -TargetExe $exe
    $owner = Get-Content -LiteralPath (Join-Path $installDir 'runtimes\bundle-owner.txt') -Raw
    if ($owner.Trim() -ne 'JudgeBox.OfflineToolchains') { throw 'Installed bundle owner marker is missing.' }
}

Push-Location -LiteralPath $projectDirectory
try {
    if ($SkipToInstall) {
        if (-not (Test-Path -LiteralPath $artifact)) { throw 'SkipToInstall requires the installer to already exist.' }
    } else {
    if (-not $SkipBuild) {
        Invoke-Native { & powershell -ExecutionPolicy Bypass -File (Join-Path $projectDirectory 'build.ps1') } 'Build or regression tests failed.'
    }
    if (-not (Test-Path -LiteralPath (Join-Path $projectDirectory 'build\JudgeBox.exe'))) { throw 'build\JudgeBox.exe is missing.' }
    if (-not $SkipLocalMatrix) {
        Invoke-Native { & $Python (Join-Path $projectDirectory 'tests\toolchain_matrix.py') (Join-Path $projectDirectory 'build\JudgeBox.exe') --report (Join-Path $projectDirectory 'build\toolchain-local-report.json') } 'Local toolchain matrix failed.'
    }
    $staleReport = Join-Path $projectDirectory 'build\toolchain-installed-unicode-report.json'
    if (Test-Path -LiteralPath $staleReport) { Move-Item -LiteralPath $staleReport -Destination ($staleReport + '.previous') -Force }

    if ((Test-StagedLayout $stageDirectory)) {
        Write-Host 'Refreshing application files on the existing toolchain stage'
        try { Test-StagedVersions $stageDirectory } catch {
            Write-Host "Staged toolchain versions are not reusable: $($_.Exception.Message)"
            New-ToolchainStage
        }
    } else {
        Write-Host 'Staging toolchains from the local SDKs'
        New-ToolchainStage
    }
    Update-ApplicationFiles $stageDirectory
    if (-not (Test-EmbeddedPackages $stageDirectory)) {
        Write-Host 'Installing pinned Python packages into the embedded runtime'
        Install-PythonPackages $stageDirectory
    }
    Test-StagedVersions $stageDirectory

    if (-not $SkipBundledMatrix) {
        Invoke-Native { & $Python (Join-Path $projectDirectory 'tests\toolchain_matrix.py') (Join-Path $stageDirectory 'JudgeBox.exe') --clean --bundled --report (Join-Path $projectDirectory 'build\toolchain-bundled-report.json') } 'Bundled matrix failed.'
    }
    Invoke-Native { & $Python (Join-Path $projectDirectory 'scripts\audit_dependencies.py') $stageDirectory --report (Join-Path $projectDirectory 'build\pe-dependencies-report.json') } 'Dependency audit failed.'
    Invoke-Native { & $Python (Join-Path $projectDirectory 'scripts\finalize_stage.py') $stageDirectory } 'Release inventory failed.'

    $innoCompiler = Join-Path $innoDirectory 'ISCC.exe'
    if (-not (Test-Path -LiteralPath $innoCompiler)) {
        $innoInstaller = Join-Path $downloadDirectory 'innosetup-6.7.3.exe'
        if (-not (Test-Path -LiteralPath $innoInstaller)) {
            Invoke-WebRequest -Uri 'https://github.com/jrsoftware/issrc/releases/download/is-6_7_3/innosetup-6.7.3.exe' -OutFile $innoInstaller
        }
        if ((Get-FileHash -LiteralPath $innoInstaller -Algorithm SHA256).Hash -ne '9C73C3BAE7ED48D44112A0F48E66742C00090BDB5BEF71D9D3C056C66E97B732') { throw 'Inno Setup checksum mismatch.' }
        if ((Get-AuthenticodeSignature -LiteralPath $innoInstaller).Status -ne 'Valid') { throw 'Inno Setup signature verification failed.' }
        $helper = Start-Process -FilePath $innoInstaller -ArgumentList @('/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART', '/CURRENTUSER', '/NOICONS', ('/DIR="' + $innoDirectory + '"')) -WindowStyle Hidden -PassThru -Wait
        if ($helper.ExitCode -ne 0) { throw 'Inno Setup helper installation failed.' }
    }
    New-Item -ItemType Directory -Force -Path $distDirectory | Out-Null
    Invoke-Native { & $innoCompiler /Q ('/DStageDir=' + $stageDirectory) ('/DOutputDir=' + $distDirectory) (Join-Path $projectDirectory 'packaging\JudgeBox.iss') } 'Installer compilation failed.'
    }
    if (-not (Test-Path -LiteralPath $artifact)) { throw 'Installer was not produced.' }

    $marker = Join-Path $env:LOCALAPPDATA 'JudgeBox\uninstall-keep-test.txt'
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $marker) | Out-Null
    [System.IO.File]::WriteAllText($marker, 'must survive uninstall', [System.Text.Encoding]::ASCII)
    New-Item -ItemType Directory -Force -Path $dataDir | Out-Null
    $keep = Join-Path $dataDir 'keep.txt'
    [System.IO.File]::WriteAllText($keep, 'must survive upgrade and uninstall', [System.Text.Encoding]::ASCII)
    Uninstall-TestCopies
    if (-not (Test-Path -LiteralPath $keep)) { throw 'Uninstall removed the explicit data directory.' }
    if ((Get-Content -LiteralPath $marker -Raw).Trim() -ne 'must survive uninstall') { throw 'Uninstall removed the user data marker.' }

    Write-Host 'Installing to a Unicode path'
    Install-Silent 'install-unicode.log'
    $installedExe = Join-Path $installDir 'JudgeBox.exe'
    Write-Host 'Running the installed self-test with embedded Python'
    Invoke-Native { & $installedExe --self-test --data-dir $dataDir } 'Installed self-test failed.'
    $selfTestReport = Join-Path $dataDir 'toolchain-self-test.json'
    if (-not (Test-Path -LiteralPath $selfTestReport)) { throw 'Self-test did not write a report.' }
    Copy-Item -LiteralPath $selfTestReport -Destination (Join-Path $projectDirectory 'build\toolchain-installed-unicode-report.json') -Force
    Copy-Item -LiteralPath $selfTestReport -Destination (Join-Path $distDirectory 'toolchain-installed-unicode-report.json') -Force
    $checker = Join-Path $projectDirectory 'build\check_installed_report.py'
    [System.IO.File]::WriteAllText($checker, "import json, sys`nreport = json.load(open(sys.argv[1], encoding='utf-8'))`nok = bool(report.get('passed')) and report.get('cleanEnvironment') is True and len(report.get('checks') or []) >= 30`nprint('installed report', 'PASS' if ok else 'FAIL', 'checks', len(report.get('checks') or []))`nsys.exit(0 if ok else 1)`n", $utf8)
    Invoke-Native { & $Python $checker $selfTestReport } 'Installed self-test report is incomplete.'

    Write-Host 'Reinstalling over the same directory'
    Install-Silent 'install-upgrade.log'
    if ((Get-Content -LiteralPath $keep -Raw).Trim() -ne 'must survive upgrade and uninstall') { throw 'Upgrade removed user data.' }
    Invoke-Native { & $installedExe --help } 'Upgraded JudgeBox.exe did not start.'
    Uninstall-TestCopies
    if ((Get-Content -LiteralPath $keep -Raw).Trim() -ne 'must survive upgrade and uninstall') { throw 'Final uninstall removed user data.' }
    if ((Get-Content -LiteralPath $marker -Raw).Trim() -ne 'must survive uninstall') { throw 'Final uninstall removed the user profile marker.' }
    if (Test-Path -LiteralPath (Join-Path $installDir 'runtimes\gcc\bin\g++.exe')) { throw 'Uninstall left the toolchain in place.' }
    Remove-Item -LiteralPath $marker -Force

    $shortcutDir = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\JudgeBox'
    if (Test-Path -LiteralPath $shortcutDir) {
        $shell = New-Object -ComObject WScript.Shell
        foreach ($shortcut in Get-ChildItem -LiteralPath $shortcutDir -Filter '*.lnk') {
            $target = $shell.CreateShortcut($shortcut.FullName).TargetPath
            $testRoot = Join-Path $projectDirectory '.runtime\installer-test'
            if ($target.StartsWith($testRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
                throw "Uninstall left a Start Menu shortcut to the test directory: $($shortcut.FullName)"
            }
        }
    }

    $hash = (Get-FileHash -LiteralPath $artifact -Algorithm SHA256).Hash.ToLowerInvariant()
    [System.IO.File]::WriteAllText($artifact + '.sha256', "$hash  $artifactName`n", [System.Text.Encoding]::ASCII)
    Write-Host "Offline installer ready: $artifact"
    Write-Host "SHA-256: $hash"
} finally {
    Pop-Location
}
