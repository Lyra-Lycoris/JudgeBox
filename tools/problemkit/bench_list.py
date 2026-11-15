import os
os.environ.setdefault("JUDGEBOX_SYNC_OFF", "1")  # 测试期间不跑 GitHub 题库同步
"""测量 /api/problems 冷启动与二次请求耗时。"""
import json, pathlib, subprocess, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
EXE = ROOT / 'JudgeBox.exe'


def main():
    proc = subprocess.Popen([str(EXE), '--no-browser', '--data-dir', str(ROOT / '.cache' / 'bench')],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    base, token = proc.stdout.readline().strip().split('/#')

    def call(path):
        request = urllib.request.Request(base + path, headers={'X-JudgeBox-Token': token})
        start = time.perf_counter()
        body = urllib.request.urlopen(request, timeout=600).read()
        return time.perf_counter() - start, body

    try:
        for index in range(3):
            seconds, body = call('/api/problems')
            print('第 %d 次 /api/problems: %.2f s（%d 字节）' % (index + 1, seconds, len(body)))
    finally:
        proc.terminate()


if __name__ == '__main__':
    main()
