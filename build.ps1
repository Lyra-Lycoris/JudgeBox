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
    Copy-Item -LiteralPath (Join-Path $projectDirectory 'build\JudgeBox.exe') -Destination (Join-Path $projectDirectory 'JudgeBox.exe') -Force
    Write-Host 'Ready: double-click JudgeBox.exe.'
} finally {
    Pop-Location
}
