param([switch]$SkipTests)
$ErrorActionPreference = 'Stop'
$projectDirectory = $PSScriptRoot
$gccBin = 'C:\msys64\ucrt64\bin'
if (Test-Path -LiteralPath (Join-Path $gccBin 'g++.exe')) {
    $env:PATH = $gccBin + ';' + $env:PATH
}
Push-Location -LiteralPath $projectDirectory
try {
    cmake -S . -B build -G 'MinGW Makefiles' -DCMAKE_BUILD_TYPE=Release
    if ($LASTEXITCODE -ne 0) { throw 'CMake configuration failed.' }
    cmake --build build -j 4
    if ($LASTEXITCODE -ne 0) { throw 'Build failed.' }
    if (-not $SkipTests) {
        ctest --test-dir build --output-on-failure
        if ($LASTEXITCODE -ne 0) { throw 'Tests failed.' }
    }
    Copy-Item -LiteralPath (Join-Path $projectDirectory 'third_party\webview2\x64\WebView2Loader.dll') -Destination (Join-Path $projectDirectory 'build\WebView2Loader.dll') -Force
    Copy-Item -LiteralPath (Join-Path $projectDirectory 'build\JudgeBox.exe') -Destination (Join-Path $projectDirectory 'JudgeBox.exe') -Force
    Copy-Item -LiteralPath (Join-Path $projectDirectory 'third_party\webview2\x64\WebView2Loader.dll') -Destination (Join-Path $projectDirectory 'WebView2Loader.dll') -Force
    New-Item -ItemType Directory -Force -Path (Join-Path $projectDirectory 'build\diagnostics') | Out-Null
    Copy-Item -LiteralPath (Join-Path $projectDirectory 'tests\toolchain_matrix.py') -Destination (Join-Path $projectDirectory 'build\diagnostics\toolchain_matrix.py') -Force
    Write-Host 'Ready: double-click JudgeBox.exe.'
} finally {
    Pop-Location
}
