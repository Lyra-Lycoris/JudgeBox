import os
"""自判题（只有测试数据）的端到端检查：新建 → 提交正确解 100 分 → 错误解 0 分。

用法：python tests/selfjudge_api_test.py [build/JudgeBox.exe]
"""
import json, os, pathlib, random, shutil, subprocess, sys, tempfile, time, urllib.request, urllib.error
os.environ.setdefault("JUDGEBOX_SYNC_OFF", "1")  # 测试期间不跑 GitHub 题库同步
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
EXE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'build/JudgeBox.exe').resolve()
ROOT = pathlib.Path(__file__).resolve().parents[1]


def call(base, token, path, obj=None, method=None, timeout=300):
    data = None if obj is None else json.dumps(obj).encode('utf-8')
    req = urllib.request.Request(base + path, data=data, method=method or ('POST' if obj is not None else 'GET'),
                                 headers={'X-JudgeBox-Token': token, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print('HTTP', e.code, e.read().decode('utf-8', errors='replace')[:2000])
        raise


temp = pathlib.Path(tempfile.mkdtemp(prefix='JudgeBox selfjudge '))
database = temp / 'ProblemDatabase'; database.mkdir()
records = temp / 'solveRecord'
env = dict(os.environ)
env['JUDGEBOX_PROBLEM_DATABASE'] = str(database)
env['JUDGEBOX_SOLVE_RECORD'] = str(records)
proc = subprocess.Popen([str(EXE), '--no-browser', '--data-dir', str(temp / 'runs')],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', env=env)
line = proc.stdout.readline().strip()
base, token = line.split('/#')

try:
    cases = [{"id": "01", "input": "3\n1 2 3\n", "answer": "6\n"},
             {"id": "02", "input": "1\n-5\n", "answer": "-5\n"},
             {"id": "03", "input": "4\n1000000 2000000 -3 5\n", "answer": "3000002\n"}]
    problem = {
        "id": "selfjudge-sum", "title": {"zh": "自判求和", "en": "Self Judge Sum"}, "difficulty": 1200,
        "topic": "模拟与实现", "tags": ["模拟"], "limits": {"timeMs": 2000, "memoryMb": 256},
        "judgeType": "standard", "selfJudge": True,
        "source": {"platform": "luogu", "id": "P1001", "url": "https://www.luogu.com.cn/problem/P1001"},
        "statement": {"zh": "# 自判求和\n\n求 $n$ 个整数之和。\n", "en": "# Self Judge Sum\n\nSum $n$ integers.\n"},
        "samples": [{"input": "3\n1 2 3\n", "output": "6\n"}],
        "cases": cases
    }
    saved = call(base, token, '/api/problems/save', problem)
    print('save:', saved['ok'], saved['selfJudge'])
    detail = call(base, token, '/api/problems/selfjudge-sum')
    print('detail:', detail['judgeType'], detail['topic'], detail['limits'], detail['source'])

    good = """#include <bits/stdc++.h>
using namespace std;
int main(){int n; if(!(cin>>n)) return 0; long long s=0,x; for(int i=0;i<n;i++){cin>>x;s+=x;} cout<<s<<"\\n"; return 0;}
"""
    bad = """#include <bits/stdc++.h>
using namespace std;
int main(){int n; cin>>n; long long s=0,x; for(int i=0;i<n;i++){cin>>x;s-=x;} cout<<s<<"\\n"; return 0;}
"""
    def submit(source):
        r = call(base, token, '/api/submit', {"problemId": "selfjudge-sum", "language": "cpp", "mode": "full", "source": source})
        for _ in range(200):
            s = call(base, token, '/api/submit/status')
            if s.get('done'):
                return s
            time.sleep(0.2)
        raise RuntimeError('judge timeout')
    ok = submit(good)
    print('正确解:', ok['verdict'], ok['score'])
    ng = submit(bad)
    print('错误解:', ng['verdict'], ng['score'])

    cases_back = call(base, token, '/api/problems/selfjudge-sum/cases')
    print('测试数据条数:', cases_back['count'])

    # 编辑：只改难度与题面，测试数据保持
    edited = call(base, token, '/api/problems/save', {"id": "selfjudge-sum", "edit": True, "difficulty": 1400,
                                                     "statement": {"zh": "# 自判求和 v2\n\n求 $n$ 个整数之和。\n"}})
    print('edit:', edited['ok'], call(base, token, '/api/problems/selfjudge-sum')['difficulty'])
    print('编辑后测试数据:', call(base, token, '/api/problems/selfjudge-sum/cases')['count'])

    records_back = call(base, token, '/api/record/scaffold', {"problemId": "selfjudge-sum"})
    print('scaffold:', records_back['problem'])
    tree = sorted(str(p.relative_to(records)) for p in records.rglob('*') if p.is_file())
    print('solveRecord:', tree)

    # 从本地目录导入测试数据（成对的 .in/.ans）
    data_dir = temp / 'dataset'
    data_dir.mkdir(exist_ok=True)
    (data_dir / 'a.in').write_text('2\n7 8\n', encoding='utf-8')
    (data_dir / 'a.ans').write_text('15\n', encoding='utf-8')
    (data_dir / 'b.in').write_text('1\n-1\n', encoding='utf-8')
    (data_dir / 'b.ans').write_text('-1\n', encoding='utf-8')
    (data_dir / 'lonely.in').write_text('1\n1\n', encoding='utf-8')
    scanned = call(base, token, '/api/problems/scan-cases', {"directory": str(data_dir)})
    print('目录导入:', scanned['count'], [c['id'] for c in scanned['cases']])
    assert scanned['count'] == 2, scanned
finally:
    proc.terminate()
