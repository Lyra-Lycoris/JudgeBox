import os
os.environ.setdefault("JUDGEBOX_SYNC_OFF", "1")  # 测试期间不跑 GitHub 题库同步
"""验证题库索引缓存：冷启动 / 有索引 / 新增题包 / 改动题包 / 删除题包 都拿到正确结果。"""
import json, pathlib, shutil, subprocess, sys, tempfile, time, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[2]


def start(exe, database, data):
    proc = subprocess.Popen([str(exe), '--no-browser', '--data-dir', str(data)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8',
                            env={**__import__('os').environ, 'JUDGEBOX_PROBLEM_DATABASE': str(database)})
    base, token = proc.stdout.readline().strip().split('/#')
    return proc, base, token


def call(base, token, path, obj=None, method=None):
    data = None if obj is None else json.dumps(obj).encode()
    request = urllib.request.Request(base + path, data=data, method=method or ('POST' if obj else 'GET'),
                                     headers={'X-JudgeBox-Token': token, 'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(request, timeout=600).read().decode())


def timed(base, token):
    start_time = time.perf_counter()
    listing = call(base, token, '/api/problems')
    return time.perf_counter() - start_time, listing


def main():
    temp = pathlib.Path(tempfile.mkdtemp(prefix='JudgeBox index '))
    database = temp / 'ProblemDatabase'
    shutil.copytree(ROOT / 'ProblemDatabase', database, ignore=shutil.ignore_patterns('*.md'))
    total = len(list(database.glob('*.zip')))
    print('题库题包数', total)

    data = temp / 'runs'
    exe = ROOT / 'JudgeBox.exe'

    # 1) 冷启动（无索引）
    proc, base, token = start(exe, database, data)
    seconds, listing = timed(base, token)
    print('冷启动: %.2f s, 题目 %d' % (seconds, len(listing['problems'])))
    proc.terminate(); proc.wait()

    # 2) 有索引
    proc, base, token = start(exe, database, data)
    seconds, listing = timed(base, token)
    first = {p['id']: p['difficulty'] for p in listing['problems']}
    print('有索引: %.2f s, 题目 %d' % (seconds, len(listing['problems'])))
    proc.terminate(); proc.wait()

    # 3) 新增一个题包（复制一份改 id 与难度）
    import zipfile
    source = sorted(database.glob('t01-date-after_*.zip'))[0]
    with zipfile.ZipFile(source) as zf:
        items = [(i, zf.read(i.filename)) for i in zf.infolist()]
    document = None
    for item, payload in items:
        if item.filename == 'problem.json':
            document = json.loads(payload.decode('utf-8'))
    document['id'] = 'zz-index-probe'
    document['title'] = {'zh': '索引探针', 'en': 'Index Probe'}
    document['difficulty'] = 2300
    probe = database / 'zz-index-probe_索引探针_.zip'
    with zipfile.ZipFile(probe, 'w', zipfile.ZIP_DEFLATED) as zf:
        for item, payload in items:
            zf.writestr(item.filename, (json.dumps(document, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
                        if item.filename == 'problem.json' else payload)

    proc, base, token = start(exe, database, data)
    seconds, listing = timed(base, token)
    found = [p for p in listing['problems'] if p['id'] == 'zz-index-probe']
    print('新增后: %.2f s, 题目 %d, 新题难度 %s' % (seconds, len(listing['problems']), found[0]['difficulty'] if found else '缺失'))
    proc.terminate(); proc.wait()

    # 4) 改难度（模拟编辑题包）
    document['difficulty'] = 1900
    with zipfile.ZipFile(probe, 'w', zipfile.ZIP_DEFLATED) as zf:
        for item, payload in items:
            zf.writestr(item.filename, (json.dumps(document, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
                        if item.filename == 'problem.json' else payload)
    time.sleep(0.05)
    proc, base, token = start(exe, database, data)
    seconds, listing = timed(base, token)
    found = [p for p in listing['problems'] if p['id'] == 'zz-index-probe']
    print('改动后: %.2f s, 新题难度 %s（应为 1900）' % (seconds, found[0]['difficulty'] if found else '缺失'))
    proc.terminate(); proc.wait()

    # 5) 删除
    probe.unlink()
    proc, base, token = start(exe, database, data)
    seconds, listing = timed(base, token)
    found = [p for p in listing['problems'] if p['id'] == 'zz-index-probe']
    print('删除后: %.2f s, 题目 %d, 探针还在？%s' % (seconds, len(listing['problems']), bool(found)))
    proc.terminate(); proc.wait()

    # 6) 索引文件名与内容
    indexes = list((ROOT / '.cache' / 'problemdb').glob('index-*.json'))
    print('索引文件', [(p.name, p.stat().st_size) for p in indexes[-3:]])
    shutil.rmtree(temp, ignore_errors=True)


if __name__ == '__main__':
    main()
