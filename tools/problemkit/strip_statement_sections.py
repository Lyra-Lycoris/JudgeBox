"""删掉题面里的「两种提交方式 / 函数签名」小节（中文与英文两版都处理）。

用法：
  python tools/problemkit/strip_statement_sections.py            # 处理 ProblemDatabase 里的题包
  python tools/problemkit/strip_statement_sections.py --specs    # 同时处理 specs 里的 statement.*.md
  python tools/problemkit/strip_statement_sections.py --dry-run
"""
import argparse
import json
import os
import pathlib
import re
import shutil
import sys
import tempfile
import zipfile

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
HEADING = re.compile(r'^\s{0,3}(#{1,6})\s+')
DROPPED = re.compile(
    r'^\s{0,3}#{1,6}\s*(?:'
    r'两种提交方式|提交方式说明|提交方式|'
    r'函数签名(?:（按语言）)?|函数式签名|各语言签名|'
    r'two\s+submission\s+styles?|submission\s+styles?|'
    r'function\s+signatures?'
    r')',
    re.IGNORECASE)


def strip(text):
    if not text:
        return text
    lines = text.split('\n')
    out = []
    skipping = False
    for line in lines:
        if HEADING.match(line):
            if DROPPED.match(line):
                skipping = True
                continue
            skipping = False
        if skipping:
            continue
        out.append(line)
    result = '\n'.join(out)
    result = re.sub(r'\n{3,}', '\n\n', result)
    result = re.sub(r'[ \t]+\n', '\n', result)
    return result.strip() + '\n'


def patch_statement_files(specs_root, dry_run):
    changed = 0
    for path in sorted(specs_root.rglob('statement.*.md')):
        text = path.read_text(encoding='utf-8')
        cleaned = strip(text)
        if cleaned != text:
            changed += 1
            if not dry_run:
                path.write_text(cleaned, encoding='utf-8')
    return changed


def patch_archive(archive, dry_run):
    with zipfile.ZipFile(archive) as zf:
        items = [(item, zf.read(item.filename)) for item in zf.infolist()]
    document = None
    for item, data in items:
        if item.filename == 'problem.json':
            document = json.loads(data.decode('utf-8'))
    if document is None or not isinstance(document.get('statement'), dict):
        return False
    statement = document['statement']
    touched = False
    for language in ('zh', 'en'):
        if not isinstance(statement.get(language), str):
            continue
        cleaned = strip(statement[language])
        if cleaned != statement[language]:
            statement[language] = cleaned
            touched = True
    if not touched:
        return False
    if dry_run:
        return True
    payload = (json.dumps(document, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    handle, temp_name = tempfile.mkstemp(suffix='.zip')
    os.close(handle)
    pathlib.Path(temp_name).unlink(missing_ok=True)
    with zipfile.ZipFile(temp_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for item, data in items:
            zf.writestr(item.filename, payload if item.filename == 'problem.json' else data)
    shutil.move(temp_name, archive)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', default=str(ROOT / 'ProblemDatabase'))
    parser.add_argument('--specs', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    archives = files = 0
    for archive in sorted(pathlib.Path(args.database).glob('*.zip')):
        try:
            if patch_archive(archive, args.dry_run):
                archives += 1
        except Exception as error:
            print('skip', archive.name, error)
    if args.specs:
        files = patch_statement_files(ROOT / 'tools' / 'problemkit' / 'specs', args.dry_run)
    print(json.dumps({'archives': archives, 'statement_files': files, 'dry_run': args.dry_run}, ensure_ascii=False))


if __name__ == '__main__':
    main()
