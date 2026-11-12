@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if exist "C:\msys64\ucrt64\bin\g++.exe" set "PATH=C:\msys64\ucrt64\bin;%PATH%"
if not exist "build\CMakeCache.txt" (
    echo Configuring CMake...
    cmake -S . -B build -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
    if errorlevel 1 (
        echo CMake configuration failed.
        pause
        exit /b 1
    )
)
set "JBOX_JOBS=%NUMBER_OF_PROCESSORS%"
for /f %%J in ('powershell -NoProfile -Command "$logical = [int]$env:NUMBER_OF_PROCESSORS; if ($logical -lt 1) { $logical = 1 }; $bytes = (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory; $byRam = [Math]::Max(1, [int][Math]::Floor(($bytes / 1GB) - 2)); $jobs = [Math]::Min($logical, $byRam); Write-Output $jobs"') do set "JBOX_JOBS=%%J"
echo %JBOX_JOBS%| findstr /r "^[1-9][0-9]*$" >nul
if errorlevel 1 set "JBOX_JOBS=%NUMBER_OF_PROCESSORS%"
echo Building JudgeBox with -j %JBOX_JOBS%...
cmake --build build -j %JBOX_JOBS%
if errorlevel 1 (
    echo Build failed.
    pause
    exit /b 1
)
set "JBOX_DATA=%~dp0runs"
if exist "%JBOX_DATA%\" (
    rmdir /s /q "%JBOX_DATA%"
    if exist "%JBOX_DATA%\" (
        echo Cannot clear the previous JudgeBox data. Close other JudgeBox windows and try again.
        pause
        exit /b 1
    )
)
mkdir "%JBOX_DATA%"
if errorlevel 1 (
    echo Cannot create a clean JudgeBox data directory.
    pause
    exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -Command "$root = [IO.Path]::GetFullPath((Get-Location).Path); if (-not $root.EndsWith('\')) { $root += '\' }; $candidates = @('build\JudgeBox.exe', 'JudgeBox.exe') | ForEach-Object { $path = Join-Path $root.TrimEnd('\') $_; if (Test-Path -LiteralPath $path) { Get-Item -LiteralPath $path } }; if (-not $candidates) { Write-Host 'Build finished but JudgeBox.exe was not found.'; exit 1 }; $launch = @($candidates) | Sort-Object LastWriteTime, FullName -Descending | Select-Object -First 1; Get-CimInstance Win32_Process -Filter 'Name = ''JudgeBox.exe''' | Where-Object { $_.ExecutablePath -and [IO.Path]::GetFullPath($_.ExecutablePath).StartsWith($root, [StringComparison]::OrdinalIgnoreCase) } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }; Start-Sleep -Milliseconds 400; $dll = Join-Path $launch.DirectoryName 'WebView2Loader.dll'; $dllSource = Join-Path $root.TrimEnd('\') 'third_party\webview2\x64\WebView2Loader.dll'; if ((-not (Test-Path -LiteralPath $dll)) -and (Test-Path -LiteralPath $dllSource)) { Copy-Item -LiteralPath $dllSource -Destination $dll }; Write-Host ('Starting ' + $launch.FullName); $proc = Start-Process -FilePath $launch.FullName -ArgumentList @('--data-dir', $env:JBOX_DATA) -WorkingDirectory $launch.DirectoryName -Wait -PassThru; exit $proc.ExitCode"
if errorlevel 1 pause
