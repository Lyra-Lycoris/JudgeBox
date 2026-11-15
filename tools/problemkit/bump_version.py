"""把 1.4.0 版本号统一升到 1.5.0（源代码、安装包脚本、README 链接）。"""
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
EDITS = {
    'packaging/JudgeBox.iss': [
        ('AppVersion=1.4.0', 'AppVersion=1.5.0'),
        ('AppVerName=JudgeBox 1.4.0', 'AppVerName=JudgeBox 1.5.0'),
        ('VersionInfoVersion=1.4.0.0', 'VersionInfoVersion=1.5.0.0'),
        ('VersionInfoProductVersion=1.4.0', 'VersionInfoProductVersion=1.5.0'),
        ('OutputBaseFilename=JudgeBox-Setup-1.4.0-x64', 'OutputBaseFilename=JudgeBox-Setup-1.5.0-x64'),
    ],
    'src/main.cpp': [('JudgeBox 1.4.0', 'JudgeBox 1.5.0')],
    'src/resources.rc': [
        ('VALUE "FileVersion", "1.4.0.0"', 'VALUE "FileVersion", "1.5.0.0"'),
        ('VALUE "ProductVersion", "1.4.0"', 'VALUE "ProductVersion", "1.5.0"'),
    ],
    'src/server.cpp': [('{"version","1.4.0"}', '{"version","1.5.0"}')],
    'package.json': [('"version": "1.4.0"', '"version": "1.5.0"')],
    'package.ps1': [("$artifactName = 'JudgeBox-Setup-1.4.0-x64.exe'", "$artifactName = 'JudgeBox-Setup-1.5.0-x64.exe'")],
    'README.md': [
        ('[JudgeBox-Setup-1.4.0-x64.exe](https://github.com/Lyra-Lycoris/JudgeBox/releases/download/v1.4.0/JudgeBox-Setup-1.4.0-x64.exe)',
         '[JudgeBox-Setup-1.5.0-x64.exe](https://github.com/Lyra-Lycoris/JudgeBox/releases/download/v1.5.0/JudgeBox-Setup-1.5.0-x64.exe)'),
        ('[SHA-256](https://github.com/Lyra-Lycoris/JudgeBox/releases/download/v1.4.0/JudgeBox-Setup-1.4.0-x64.exe.sha256)',
         '[SHA-256](https://github.com/Lyra-Lycoris/JudgeBox/releases/download/v1.5.0/JudgeBox-Setup-1.5.0-x64.exe.sha256)'),
    ],
}


def main():
    for name, pairs in EDITS.items():
        path = ROOT / name
        text = path.read_text(encoding='utf-8')
        for old, new in pairs:
            if old not in text:
                print('MISS', name, old[:40])
                continue
            text = text.replace(old, new)
        path.write_text(text, encoding='utf-8')
        print('patched', name)


if __name__ == '__main__':
    main()
