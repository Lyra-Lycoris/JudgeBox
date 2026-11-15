"""批量构建 specs 目录下的全部题目，并可选安装进 ProblemDatabase。

用法：
  python tools/problemkit/build_all.py [--topics a,b] [--install] [--skip-verify] [--jobs 1]
"""
import argparse, concurrent.futures, pathlib, sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import build as builder  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topics', default=None)
    parser.add_argument('--install', action='store_true')
    parser.add_argument('--skip-verify', action='store_true')
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--out', default=str(ROOT / 'build' / 'problemkit'))
    args = parser.parse_args()
    specs_root = HERE / 'specs'
    topics = args.topics.split(',') if args.topics else [p.name for p in sorted(specs_root.iterdir()) if p.is_dir()]
    specs = []
    for topic in topics:
        topic_dir = specs_root / topic
        if not topic_dir.is_dir():
            continue
        for spec in sorted(topic_dir.iterdir()):
            if spec.is_dir() and (spec / 'meta.json').is_file():
                specs.append(spec)
    print('待构建 %d 个 spec' % len(specs))
    results, failures = [], []
    if args.jobs <= 1:
        for spec in specs:
            result = builder.build(spec, args.out, args.skip_verify, False, None, verbose=True)
            if result:
                results.append(result)
            else:
                failures.append(spec.name)
    else:
        def one(spec):
            return spec, builder.build(spec, args.out, args.skip_verify, False, None, verbose=False)
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            for spec, result in pool.map(one, specs):
                if result:
                    results.append(result)
                    print('  ok   %s (%s)' % (result['id'], ','.join(result['languages'])))
                else:
                    failures.append(spec.name)
                    print('  FAIL %s' % spec.name)
    print('成功 %d，失败 %d' % (len(results), len(failures)))
    if failures:
        print('失败列表：' + ', '.join(failures))
    degraded = [r['id'] for r in results if r.get('failed')]
    if degraded:
        print('降级（缺语言）：' + ', '.join(degraded))
    if args.install:
        import install
        database = ROOT / 'ProblemDatabase'
        for result in results:
            target = install.install(pathlib.Path(result['archive']), database)
            print('installed', target.name)
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
