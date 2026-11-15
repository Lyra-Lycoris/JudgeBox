"""把构建好的题包 zip 安装到 ProblemDatabase，并按平台的命名规则改名。

用法：
  python tools/problemkit/install.py [zip ...] [--database DIR] [--dry-run]
不给 zip 时安装 build/problemkit 下的全部 zip。
"""
import argparse, json, pathlib, shutil, sys, zipfile

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def safe_title(text):
    out = []
    for char in text:
        if char in '\\/:*?"<>|' or ord(char) < 0x20:
            out.append('-')
        else:
            out.append(char)
    text = ''.join(out)
    while text and text[-1] in ' .-':
        text = text[:-1]
    return text[:40] or 'problem'


def install(archive, database, dry_run=False):
    with zipfile.ZipFile(archive) as zf:
        meta = json.loads(zf.read('problem.json').decode('utf-8'))
    problem_id = meta['id']
    title = safe_title((meta.get('title') or {}).get('zh') or (meta.get('title') or {}).get('en') or 'problem')
    target = database / ('%s_%s_.zip' % (problem_id, title))
    if dry_run:
        print('%s -> %s' % (archive.name, target.name))
        return target
    database.mkdir(parents=True, exist_ok=True)
    # 同 id 的旧题包先删掉（文件名可能变了）
    for old in database.glob('*.zip'):
        try:
            with zipfile.ZipFile(old) as zf:
                if json.loads(zf.read('problem.json').decode('utf-8')).get('id') == problem_id:
                    old.unlink()
        except Exception:
            continue
    shutil.copy2(archive, target)
    return target


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('archives', nargs='*')
    parser.add_argument('--database', default=str(ROOT / 'ProblemDatabase'))
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    archives = [pathlib.Path(p) for p in args.archives] or sorted((ROOT / 'build' / 'problemkit').glob('*.zip'))
    database = pathlib.Path(args.database)
    for archive in archives:
        target = install(archive, database, args.dry_run)
        print('installed', target.name)
    print(json.dumps({'installed': len(archives)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
