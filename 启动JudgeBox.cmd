@echo off
setlocal
cd /d "%~dp0"
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
if exist "%~dp0JudgeBox.exe" (
    "%~dp0JudgeBox.exe" --data-dir "%JBOX_DATA%"
) else if exist "%~dp0build\JudgeBox.exe" (
    "%~dp0build\JudgeBox.exe" --data-dir "%JBOX_DATA%"
) else (
    echo JudgeBox.exe was not found. Run build.ps1 first.
    pause
    exit /b 1
)
if errorlevel 1 pause
