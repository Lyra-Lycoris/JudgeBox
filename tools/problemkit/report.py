"""统计题库：专题分布、难度分布、语言/裁判覆盖，顺便检查题包可读性。

用法：python tools/problemkit/report.py [--database DIR]
"""
import argparse, collections, json, pathlib, sys, zipfile

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', default=str(ROOT / 'ProblemDatabase'))
    args = parser.parse_args()
    database = pathlib.Path(args.database)
    topics = collections.Counter()
    difficulties = collections.Counter()
    judges = collections.Counter()
    languages = collections.Counter()
    problems = []
    broken = []
    for archive in sorted(database.glob('*.zip')):
        try:
            with zipfile.ZipFile(archive) as zf:
                meta = json.loads(zf.read('problem.json').decode('utf-8'))
        except Exception as error:
            broken.append((archive.name, str(error)))
            continue
        problems.append(meta)
        topics[meta.get('topic') or '（未分类）'] += 1
        difficulties[meta.get('difficulty', 0)] += 1
        judges[meta.get('judgeType') or 'auto'] += 1
        for language in (meta.get('modes') or {}):
            languages[language] += 1
    print('题包总数：%d，损坏：%d' % (len(problems), len(broken)))
    for name, error in broken:
        print('  损坏', name, error)
    print('\n专题分布（%d 个专题）：' % len(topics))
    for name, count in sorted(topics.items(), key=lambda item: (-item[1], item[0])):
        print('  %-16s %d' % (name, count))
    print('\n难度分布：')
    for difficulty in sorted(difficulties):
        print('  %4d  %s %d' % (difficulty, '#' * difficulties[difficulty], difficulties[difficulty]))
    print('\n裁判方式：')
    for name, count in judges.most_common():
        print('  %-10s %d' % (name, count))
    print('\n语言覆盖：')
    for name, count in languages.most_common():
        print('  %-8s %d' % (name, count))
    ids = [p['id'] for p in problems]
    duplicated = [item for item, count in collections.Counter(ids).items() if count > 1]
    if duplicated:
        print('\n重复 id：' + ', '.join(duplicated))
    titles = collections.Counter((p.get('title') or {}).get('zh', '') for p in problems)
    repeated = [item for item, count in titles.items() if count > 1 and item]
    if repeated:
        print('重复标题：' + ', '.join(repeated))
    print('\n总题数：%d' % len(problems))


if __name__ == '__main__':
    main()
