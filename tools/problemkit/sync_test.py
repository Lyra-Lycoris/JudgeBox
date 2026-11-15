import os
"""验证 GitHub 题库静默增量同步：首次拉全量、二次不重复下载、新增题包能增量拉取。"""
import json, os, pathlib, shutil, subprocess, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
REPO = 'Lyra-Lycoris/JudgeBox-SyncTest'


def start(database, data, extra_env):
    env = dict(os.environ)
    env.update(extra_env)
    env['JUDGEBOX_PROBLEM_DATABASE'] = str(database)
    proc = subprocess.Popen([str(ROOT / 'JudgeBox.exe'), '--no-browser', '--data-dir', str(data)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', env=env)
    base, token = proc.stdout.readline().strip().split('/#')
    return proc, base, token


def call(base, token, path):
    request = urllib.request.Request(base + path, headers={'X-JudgeBox-Token': token})
    return json.loads(urllib.request.urlopen(request, timeout=120).read().decode())


def wait_sync(base, token, timeout=180):
    deadline = time.time() + timeout
    while time.time() < deadline:
        status = call(base, token, '/api/sync/status')
        if not status.get('running'):
            return status
        time.sleep(0.3)
    return {'error': 'sync timeout'}


def run(label, database, data, extra_env, timeout=180):
    local_start = time.perf_counter()
    proc, base, token = start(database, data, extra_env)
    try:
        first_list = time.perf_counter() - local_start
        listing = call(base, token, '/api/problems')
        status = wait_sync(base, token, timeout)
        after = call(base, token, '/api/problems')
        print('%s: 首次列表 %.2f s / %d 题；同步结果 added=%s updated=%s skipped=%s error=%s；同步后 %d 题' % (
            label, first_list, len(listing['problems']), status.get('added'), status.get('updated'),
            status.get('skipped'), (status.get('error') or '')[:80], len(after['problems'])))
        return status
    finally:
        proc.terminate()
        proc.wait()


def main():
    temp = pathlib.Path(r'E:\JudgeBox\.runtime\synctest-work')
    shutil.rmtree(temp, ignore_errors=True)
    temp.mkdir(parents=True)
    database = temp / 'ProblemDatabase'      # 故意不存在：模拟全新安装
    data = temp / 'runs'
    env = {'JUDGEBOX_SYNC_REPO': REPO}
    run('首次（空目录，远端 2 题）', database, data, env)
    print('  zip 落地:', sorted(p.name for p in database.glob('*.zip')))
    run('第二次（应零下载）', database, data, env)

    # 远端新增一个题包（挑一个还没在测试仓库里的）
    repo_dir = pathlib.Path(r'E:\JudgeBox\.runtime\synctest-repo')
    existing = {p.name for p in repo_dir.glob('*.zip')}
    source = next(p for p in sorted((ROOT / 'ProblemDatabase').glob('t03-*.zip')) if p.name not in existing)
    shutil.copy2(source, repo_dir / source.name)
    subprocess.run(['git', 'add', '-A'], cwd=repo_dir, check=True)
    subprocess.run(['git', '-c', 'user.name=Lycoris', '-c', 'user.email=yeling114514@gmail.com',
                    'commit', '-q', '-m', 'test: add problem'], cwd=repo_dir, check=True)
    subprocess.run(['git', 'push', '-q', 'origin', 'main'], cwd=repo_dir, check=True)
    # GitHub 的 contents 接口有几十秒的 CDN 缓存，push 后立刻读可能还是旧列表；
    # 这里最多等 60 秒再重试，验证「下一次启动能增量拉到」。
    for attempt in range(6):
        status = run('远端新增 1 题后（第 %d 次）' % (attempt + 1), database, data, env)
        if status.get('added') or status.get('updated'):
            break
        time.sleep(10)
    print('  最终 zip:', sorted(p.name for p in database.glob('*.zip')))


if __name__ == '__main__':
    main()
