import os
"""为题库里的每道题准备 solveRecord 目录（4 语言 × 2 提交方式 + 工程骨架）。

用法：python tools/problemkit/scaffold_records.py [--exe JudgeBox.exe]
需要本地引擎能启动；它调用 /api/record/scaffold，保证目录命名与做题页保存时完全一致。
"""
import argparse, json, pathlib, subprocess, sys, urllib.error, urllib.request

try:
    os.environ.setdefault("JUDGEBOX_SYNC_OFF", "1")  # 测试期间不跑 GitHub 题库同步
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exe', default=str(ROOT / 'JudgeBox.exe'))
    args = parser.parse_args()
    proc = subprocess.Popen([args.exe, '--no-browser', '--data-dir', str(ROOT / '.cache' / 'scaffold')],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    line = proc.stdout.readline().strip()
    if not line.startswith('http://127.0.0.1:'):
        proc.terminate()
        raise SystemExit('引擎没有启动：' + line)
    base, token = line.split('/#')

    def call(path, obj=None):
        data = None if obj is None else json.dumps(obj).encode()
        request = urllib.request.Request(base + path, data=data, method='POST' if obj is not None else 'GET',
                                         headers={'X-JudgeBox-Token': token, 'Content-Type': 'application/json'})
        try:
            return json.loads(urllib.request.urlopen(request, timeout=120).read().decode())
        except urllib.error.HTTPError as error:
            print('HTTP', error.code, error.read().decode('utf-8', 'replace')[:400])
            raise

    try:
        problems = call('/api/problems')['problems']
        made = 0
        for problem in problems:
            try:
                result = call('/api/record/scaffold', {'problemId': problem['id']})
                made += 1
                if made % 20 == 0:
                    print('  ... %d / %d' % (made, len(problems)))
            except Exception as error:
                print('skip', problem['id'], error)
        print(json.dumps({'problems': len(problems), 'scaffolded': made}, ensure_ascii=False))
    finally:
        proc.terminate()


if __name__ == '__main__':
    main()
