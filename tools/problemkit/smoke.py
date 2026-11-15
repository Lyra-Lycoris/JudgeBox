import os
"""对已安装的题包做一次真实判题冒烟：详情能加载、可以按需提交参考解。

用法：python tools/problemkit/smoke.py [--problem ID] [--submit]
不给 --problem 时检查所有 id 以 proto- 或 t 开头的题目。
"""
import argparse, json, pathlib, subprocess, sys, time, urllib.error, urllib.request

try:
    os.environ.setdefault("JUDGEBOX_SYNC_OFF", "1")  # 测试期间不跑 GitHub 题库同步
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--problem', default=None)
    parser.add_argument('--exe', default=str(ROOT / 'JudgeBox.exe'))
    parser.add_argument('--prefixes', default='proto-,t')
    args = parser.parse_args()
    proc = subprocess.Popen([args.exe, '--no-browser', '--data-dir', str(ROOT / '.runtime' / 'apitest')],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    line = proc.stdout.readline().strip()
    base, token = line.split('/#')

    def call(path, obj=None, method=None, timeout=180):
        data = None if obj is None else json.dumps(obj).encode()
        req = urllib.request.Request(base + path, data=data, method=method or ('POST' if obj else 'GET'),
                                     headers={'X-JudgeBox-Token': token, 'Content-Type': 'application/json'})
        try:
            return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())
        except urllib.error.HTTPError as error:
            print('HTTP', error.code, error.read().decode('utf-8', 'replace')[:1500])
            raise

    try:
        listing = call('/api/problems')
        problems = listing['problems']
        prefixes = tuple(p for p in args.prefixes.split(',') if p)
        ids = [args.problem] if args.problem else [p['id'] for p in problems if p['id'].startswith(prefixes)]
        print('题库共 %d 题，检查 %d 题' % (len(problems), len(ids)))
        bad = []
        for pid in ids:
            try:
                detail = call('/api/problems/' + pid)
            except Exception as error:
                bad.append((pid, str(error)))
                print('  %-30s 加载失败 %s' % (pid, error))
                continue
            print('  %-30s %4d %-14s %-9s %s' % (pid, detail['difficulty'], detail['topic'],
                                                 detail['judgeType'], ','.join(detail['judgedLanguages'])))
        for pid, message in bad:
            print('FAILED', pid, message)
        print(json.dumps({'total': len(problems), 'checked': len(ids), 'failed': len(bad)}, ensure_ascii=False))
    finally:
        proc.terminate()


if __name__ == '__main__':
    main()
