@echo off
setlocal
cd /d "%~dp0"
if exist "%~dp0JudgeBox.exe" (
    "%~dp0JudgeBox.exe" --data-dir "%~dp0runs"
) else if exist "%~dp0build\JudgeBox.exe" (
    "%~dp0build\JudgeBox.exe" --data-dir "%~dp0runs"
) else (
    echo JudgeBox.exe was not found. Run build.ps1 first.
    pause
    exit /b 1
)
if errorlevel 1 pause
