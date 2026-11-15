"""给测试脚本统一加上 JUDGEBOX_SYNC_OFF=1，避免测试期间触发 GitHub 题库同步。"""
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGETS = [
    'tests/api_test.py', 'tests/problem_api_test.py', 'tests/selfjudge_api_test.py',
    'tests/browser_problem_test.py', 'tests/browser_edit_test.py', 'tests/browser_shots.py',
    'tests/browser_judge_card_test.py', 'tests/browser_shot_editor.py', 'tests/browser_sync_test.py',
    'tools/problemkit/smoke.py', 'tools/problemkit/submit_check.py', 'tools/problemkit/scaffold_records.py',
    'tools/problemkit/bench_index.py', 'tools/problemkit/bench_list.py', 'tools/problemkit/sync_test.py',
]
LINE = 'os.environ.setdefault("JUDGEBOX_SYNC_OFF", "1")  # 测试期间不跑 GitHub 题库同步\n'


def main():
    for name in TARGETS:
        path = ROOT / name
        if not path.is_file():
            print('missing', name)
            continue
        text = path.read_text(encoding='utf-8')
        if 'JUDGEBOX_SYNC_OFF' in text:
            print('skip  ', name)
            continue
        if '\nimport os' not in text and not text.startswith('import os'):
            text = 'import os\n' + text
        marker = 'sys.stdout.reconfigure(encoding'
        if marker in text:
            text = text.replace(marker, LINE + marker, 1)
        else:
            text = text.replace('import os\n', 'import os\n' + LINE, 1)
        path.write_text(text, encoding='utf-8')
        print('patched', name)


if __name__ == '__main__':
    main()
