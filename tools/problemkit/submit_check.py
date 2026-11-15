import os
"""用题包自带的参考解，对若干题目在各语言下真实提交一次，确认平台能判 AC。

用法：python tools/problemkit/submit_check.py --problems t04-lower-bound,t24-big-add [--modes function,full]
不给 --problems 时随机挑 4 道。
"""
import argparse, json, pathlib, random, subprocess, sys, time, urllib.error, urllib.request

try:
    os.environ.setdefault("JUDGEBOX_SYNC_OFF", "1")  # 测试期间不跑 GitHub 题库同步
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
EXT = {'cpp': 'cpp', 'cangjie': 'cj', 'python': 'py', 'java': 'java'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--problems', default=None)
    parser.add_argument('--modes', default='function')
    parser.add_argument('--languages', default='cpp,cangjie,python,java')
    parser.add_argument('--exe', default=str(ROOT / 'JudgeBox.exe'))
    args = parser.parse_args()
    specs = {}
    for meta in (ROOT / 'tools' / 'problemkit' / 'specs').rglob('meta.json'):
        document = json.loads(meta.read_text(encoding='utf-8'))
        specs[document['id']] = meta.parent
    ids = args.problems.split(',') if args.problems else random.sample(sorted(specs), 4)
    modes = args.modes.split(',')
    languages = args.languages.split(',')

    proc = subprocess.Popen([args.exe, '--no-browser', '--data-dir', str(ROOT / '.cache' / 'submitcheck')],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    line = proc.stdout.readline().strip()
    if not line.startswith('http://127.0.0.1:'):
        proc.terminate()
        raise SystemExit('引擎没有启动：' + line)
    base, token = line.split('/#')

    def call(path, obj=None, timeout=300):
        data = None if obj is None else json.dumps(obj).encode()
        request = urllib.request.Request(base + path, data=data, method='POST' if obj is not None else 'GET',
                                         headers={'X-JudgeBox-Token': token, 'Content-Type': 'application/json'})
        return json.loads(urllib.request.urlopen(request, timeout=timeout).read().decode())

    failures = []
    try:
        for problem_id in ids:
            spec = specs.get(problem_id)
            if not spec:
                print('找不到 spec', problem_id)
                continue
            for language in languages:
                path = spec / ('solution.' + EXT[language])
                if not path.is_file():
                    continue
                source = path.read_text(encoding='utf-8')
                for mode in modes:
                    result = call('/api/submit', {'problemId': problem_id, 'language': language,
                                                  'mode': mode, 'source': source})
                    for _ in range(600):
                        status = call('/api/submit/status')
                        if status.get('done'):
                            break
                        time.sleep(0.2)
                    ok = status.get('verdict') == 'AC' and status.get('score') == 100
                    print('  %-28s %-7s %-8s %-6s %3s %s' % (problem_id, language, mode, status.get('verdict'),
                                                            status.get('score'), '' if ok else (status.get('message') or '')[:120]))
                    if not ok:
                        failures.append((problem_id, language, mode, status.get('verdict'), status.get('message')))
    finally:
        proc.terminate()
    print(json.dumps({'checked': len(ids), 'failures': len(failures)}, ensure_ascii=False))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
