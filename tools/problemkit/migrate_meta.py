"""给已有题包补 topic / judgeType / source（重写 zip 内的 problem.json，其余文件原样保留）。

用法：python tools/problemkit/migrate_meta.py [--dry-run]
"""
import argparse, json, os, pathlib, shutil, sys, tempfile, zipfile

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATABASE = ROOT / 'ProblemDatabase'

# id -> (专题, judgeType, source)
PLAN = {
    'cf1324d-pair-of-topics': ('哈希与计数', 'function',
                               {'platform': 'codeforces', 'id': '1324D',
                                'url': 'https://codeforces.com/problemset/problem/1324/D'}),
    'cf1338a-powered-addition': ('位运算与构造', 'function',
                                 {'platform': 'codeforces', 'id': '1338A',
                                  'url': 'https://codeforces.com/problemset/problem/1338/A'}),
    'cf1365c-rotation-matching': ('哈希与计数', 'function',
                                  {'platform': 'codeforces', 'id': '1365C',
                                   'url': 'https://codeforces.com/problemset/problem/1365/C'}),
    'cf1385d-a-good-string': ('分治与递归', 'function',
                              {'platform': 'codeforces', 'id': '1385D',
                               'url': 'https://codeforces.com/problemset/problem/1385/D'}),
    'cf1520d-same-differences': ('哈希与计数', 'function',
                                 {'platform': 'codeforces', 'id': '1520D',
                                  'url': 'https://codeforces.com/problemset/problem/1520/D'}),
    'ict-renjian-cihua': ('字符串与匹配', 'special', {'platform': 'other'}),
    'lc1911-alternating-sum': ('线性动态规划', 'function',
                               {'platform': 'leetcode', 'id': '1911',
                                'url': 'https://leetcode.cn/problems/maximum-alternating-subsequence-sum/'}),
    'lc1962-remove-stones': ('堆与优先队列', 'function',
                             {'platform': 'leetcode', 'id': '1962',
                              'url': 'https://leetcode.cn/problems/remove-stones-to-minimize-the-total/'}),
    'lc2270-split-array': ('前缀和与差分', 'function',
                           {'platform': 'leetcode', 'id': '2270',
                            'url': 'https://leetcode.cn/problems/number-of-ways-to-split-array/'}),
    'lc2300-successful-pairs': ('二分与二分答案', 'function',
                                {'platform': 'leetcode', 'id': '2300',
                                 'url': 'https://leetcode.cn/problems/successful-pairs-of-spells-and-potions/'}),
    'lc2461-distinct-subarrays': ('双指针与滑动窗口', 'function',
                                  {'platform': 'leetcode', 'id': '2461',
                                   'url': 'https://leetcode.cn/problems/maximum-sum-of-distinct-subarrays-with-length-k/'}),
}


def migrate(archive, dry_run=False):
    with zipfile.ZipFile(archive) as zf:
        entries = [(item, zf.read(item.filename)) for item in zf.infolist()]
    document = None
    for item, data in entries:
        if item.filename == 'problem.json':
            document = json.loads(data.decode('utf-8'))
    if document is None:
        return None
    problem_id = document.get('id')
    if problem_id not in PLAN:
        return None
    topic, judge_type, source = PLAN[problem_id]
    document['topic'] = topic
    document['judgeType'] = judge_type
    document['source'] = source
    print('%-28s %-12s %-11s %s' % (problem_id, topic, judge_type, source.get('url') or source['platform']))
    if dry_run:
        return problem_id
    payload = json.dumps(document, ensure_ascii=False, indent=2).encode('utf-8') + b'\n'
    handle, temp_name = tempfile.mkstemp(suffix='.zip')
    os.close(handle)
    pathlib.Path(temp_name).unlink(missing_ok=True)
    with zipfile.ZipFile(temp_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for item, data in entries:
            zf.writestr(item.filename, payload if item.filename == 'problem.json' else data)
    shutil.move(temp_name, archive)
    return problem_id


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    changed = []
    for archive in sorted(DATABASE.glob('*.zip')):
        if archive.name.startswith('proto-'):
            continue
        try:
            result = migrate(archive, args.dry_run)
        except Exception as error:
            print('skip', archive.name, error)
            continue
        if result:
            changed.append(result)
    print(json.dumps({'migrated': changed}, ensure_ascii=False))


if __name__ == '__main__':
    main()
