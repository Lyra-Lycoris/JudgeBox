"""把题库里的题包文件名规范成 `<id>_<题目名>_.zip`（题目名取 title.zh）。"""
import json
import pathlib
import sys
import zipfile

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
FORBIDDEN = '\\/:*?"<>|'


def safe_title(text):
    out = []
    for char in text:
        out.append('-' if (char in FORBIDDEN or ord(char) < 0x20) else char)
    text = ''.join(out)
    while text and text[-1] in ' .-':
        text = text[:-1]
    return text[:40] or 'problem'


def main():
    database = ROOT / 'ProblemDatabase'
    moved = 0
    for archive in sorted(database.glob('*.zip')):
        try:
            with zipfile.ZipFile(archive) as zf:
                meta = json.loads(zf.read('problem.json').decode('utf-8'))
        except Exception as error:
            print('skip', archive.name, error)
            continue
        title = safe_title((meta.get('title') or {}).get('zh') or (meta.get('title') or {}).get('en') or 'problem')
        target = database / ('%s_%s_.zip' % (meta['id'], title))
        if archive.name != target.name:
            if target.exists():
                target.unlink()
            archive.rename(target)
            moved += 1
            print('%s -> %s' % (archive.name, target.name))
    print('renamed', moved)


if __name__ == '__main__':
    main()
