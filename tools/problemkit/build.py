"""从一个题目 spec 目录构建题包 zip，并在本地用四种语言跑一遍验证。

spec 目录：
  meta.json          元数据 + signature（见 codegen.py 的约定）
  statement.zh.md    中文题面
  statement.en.md    英文题面
  gen.py             def cases(): 返回 [{"id": "01", "input": "..."}, ...]
  solution.cpp / .py / .java / .cj   函数实现（只写 solve，不写 main）
  checker.cpp        可选：SPJ

用法：
  python build.py <spec-dir> [...] [--skip-verify] [--keep] [--out DIR] [--languages cpp,python]
"""
import argparse, json, os, pathlib, re, shutil, subprocess, sys, tempfile, zipfile

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TESTLIB = ROOT / 'third_party' / 'testlib'
EXT = {'cpp': 'cpp', 'cangjie': 'cj', 'python': 'py', 'java': 'java'}
LANG_ORDER = ['cpp', 'cangjie', 'python', 'java']
# 与 src/problems.cpp 的词表保持一致：题包校验会拒绝词表外的标签。
TAG_VOCAB = {'模拟', '枚举', '排序', '二分', '贪心', '构造', '前缀和', '差分', '双指针', '滑动窗口', '哈希', '栈',
             '队列', '单调栈', '堆', '并查集', '树状数组', '线段树', '字符串', 'Trie', 'KMP', '图论', '最短路',
             '最小生成树', '拓扑排序', '二分图', '网络流', '树', '最近公共祖先', '动态规划', '背包', '区间DP',
             '状压DP', '数位DP', '树形DP', '数学', '数论', '组合数学', '概率期望', '计算几何', '位运算', '分治',
             '记忆化搜索', '高精度', '交互'}


def validate_meta(meta, problem_id):
    problems = []
    if not re.match(r'^[a-z0-9][a-z0-9-]{1,47}$', problem_id):
        problems.append('id 不合法')
    tags = meta.get('tags') or []
    if not (1 <= len(tags) <= 3):
        problems.append('tags 需要 1–3 个')
    for tag in tags:
        if tag not in TAG_VOCAB:
            problems.append('未知标签 ' + str(tag))
    difficulty = meta.get('difficulty')
    if not isinstance(difficulty, int) or difficulty < 800 or difficulty > 3500 or difficulty % 100:
        problems.append('difficulty 必须是 800–3500 的整百')
    limits = meta.get('limits') or {}
    if not (100 <= int(limits.get('timeMs', 0)) <= 60000):
        problems.append('limits.timeMs 超出范围')
    if not (16 <= int(limits.get('memoryMb', 0)) <= 4096):
        problems.append('limits.memoryMb 超出范围')
    topic = meta.get('topic') or ''
    if not topic:
        problems.append('缺少 topic')
    source = meta.get('source') or {}
    if source:
        if source.get('platform') not in ('luogu', 'leetcode', 'codeforces', 'other'):
            problems.append('source.platform 不合法')
        if source.get('url') and not str(source['url']).startswith('https://'):
            problems.append('source.url 必须以 https:// 开头')
    samples = meta.get('samples') or []
    if not (1 <= len(samples) <= 5):
        problems.append('samples 需要 1–5 条')
    return problems


def find_tool(name, candidates=()):
    from shutil import which
    found = which(name)
    if found:
        return found
    for candidate in candidates:
        if candidate and pathlib.Path(candidate).is_file():
            return candidate
    return None


def toolchain():
    java_bins = []
    if os.environ.get('JAVA_HOME'):
        java_bins.append(str(pathlib.Path(os.environ['JAVA_HOME']) / 'bin'))
    adoptium = pathlib.Path(r'C:\Program Files\Eclipse Adoptium')
    if adoptium.is_dir():
        java_bins += [str(p / 'bin') for p in adoptium.glob('jdk-*')]
    tools = {
        'g++': find_tool('g++', [r'C:\msys64\ucrt64\bin\g++.exe']),
        'python': find_tool('python'),
        'javac': find_tool('javac', [str(pathlib.Path(p) / 'javac.exe') for p in java_bins]),
        'java': find_tool('java', [str(pathlib.Path(p) / 'java.exe') for p in java_bins]),
        'cjc': find_tool('cjc', [r'D:\Cangjie\cangjie\bin\cjc.exe']),
    }
    cangjie_home = str(pathlib.Path(tools['cjc']).resolve().parents[1]) if tools['cjc'] else None
    # g++ 需要它自己所在的 bin 在 PATH 上才能找到 cc1plus；javac/java 同理。
    prefix = []
    for key in ('g++', 'javac', 'java'):
        if tools[key]:
            directory = str(pathlib.Path(tools[key]).resolve().parent)
            if directory not in prefix:
                prefix.append(directory)
    if prefix:
        os.environ['PATH'] = os.pathsep.join(prefix + [os.environ.get('PATH', '')])
    return tools, cangjie_home


def run(command, cwd, stdin_bytes=None, timeout=20, env_extra=None):
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    if env_extra:
        env.update(env_extra)
    return subprocess.run(command, cwd=str(cwd), input=stdin_bytes, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=timeout, env=env)


def normalize(text):
    return text.replace('\r\n', '\n').replace('\r', '\n')


def tokens(text):
    return text.split()


def assemble(language, driver, solution, package, mode):
    if language == 'cpp':
        return {'Main.cpp': driver + '\n' + solution}
    if language == 'python':
        return {'main.py': solution + '\n\n' + driver}
    if language == 'java':
        return {'Main.java': "import java.util.*;\nimport java.io.*;\nimport java.math.*;\n\npublic class Main {\n"
                             + driver + '\n' + solution + "\n}\n"}
    if language == 'cangjie':
        if mode == 'function':
            return {'main.cj': driver, 'solution.cj': solution}
        imports, body = [], []
        for chunk in (driver, solution):
            for line in chunk.splitlines():
                stripped = line.strip()
                if stripped.startswith('package '):
                    continue
                if stripped.startswith('import '):
                    if stripped not in imports:
                        imports.append(stripped)
                    continue
                body.append(line)
        return {'main.cj': "package %s\n\n%s\n%s\n" % (package, "\n".join(imports), "\n".join(body))}
    raise ValueError(language)


class Prepared:
    def __init__(self, command, directory, env_extra):
        self.command, self.directory, self.env_extra = command, directory, env_extra

    def run(self, input_text, timeout=30):
        try:
            proc = run(self.command, self.directory, input_text.encode('utf-8'), timeout=timeout,
                       env_extra=self.env_extra)
        except subprocess.TimeoutExpired:
            return False, '', 'TLE'
        if proc.returncode != 0:
            return False, proc.stdout.decode('utf-8', 'replace'), 'RE exit=%d %s' % (
                proc.returncode, proc.stderr.decode('utf-8', 'replace')[:1500])
        return True, normalize(proc.stdout.decode('utf-8', 'replace')), ''


def prepare(language, files, directory, tools, cangjie_home):
    """写文件 + 编译一次，返回 (Prepared, 编译器日志) 或 (None, 失败日志)。"""
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (directory / name).write_text(content, encoding='utf-8')
    env_extra = {}
    if language == 'cpp':
        proc = run([tools['g++'], '-std=c++20', '-O2', '-pipe', '-fdiagnostics-color=never',
                    '-finput-charset=UTF-8', 'Main.cpp', '-o', 'Main.exe'], directory, timeout=180)
        if proc.returncode != 0:
            return None, (proc.stdout + proc.stderr).decode('utf-8', 'replace')
        return Prepared([str(directory / 'Main.exe')], directory, env_extra), ''
    if language == 'python':
        proc = run([tools['python'], '-X', 'utf8', '-m', 'py_compile', 'main.py'], directory, timeout=120)
        if proc.returncode != 0:
            return None, (proc.stdout + proc.stderr).decode('utf-8', 'replace')
        return Prepared([tools['python'], '-X', 'utf8', '-u', 'main.py'], directory, env_extra), ''
    if language == 'java':
        proc = run([tools['javac'], '-J-Dfile.encoding=UTF-8', '-encoding', 'UTF-8', '-d', '.', 'Main.java'],
                   directory, timeout=180)
        if proc.returncode != 0:
            return None, (proc.stdout + proc.stderr).decode('utf-8', 'replace')
        return Prepared([tools['java'], '-Dfile.encoding=UTF-8', '-Dstdout.encoding=UTF-8', '-Dstderr.encoding=UTF-8',
                         '-Xmx768m', '-cp', '.', 'Main'], directory, env_extra), ''
    if language == 'cangjie':
        env_extra['CANGJIE_HOME'] = cangjie_home
        env_extra['PATH'] = os.pathsep.join([
            str(pathlib.Path(cangjie_home) / 'runtime/lib/windows_x86_64_cjnative'),
            str(pathlib.Path(cangjie_home) / 'lib/windows_x86_64_cjnative'),
            str(pathlib.Path(cangjie_home) / 'tools/bin'),
            str(pathlib.Path(cangjie_home) / 'tools/lib'),
            str(pathlib.Path(tools['cjc']).parent),
            os.environ.get('PATH', '')])
        sources = sorted(p.name for p in directory.glob('*.cj'))
        sources.sort(key=lambda name: (name != 'main.cj', name))
        proc = run([tools['cjc'], *sources, '-o', 'Main.exe', '--diagnostic-format', 'noColor'], directory,
                   timeout=240, env_extra=env_extra)
        if proc.returncode != 0:
            return None, (proc.stdout + proc.stderr).decode('utf-8', 'replace')
        return Prepared([str(directory / 'Main.exe')], directory, env_extra), ''
    raise ValueError(language)


def default_groups(ids):
    groups = [{'name': 'sample', 'points': 1, 'cases': [ids[0]]}]
    rest = ids[1:]
    if not rest:
        groups[0]['points'] = 100
        return groups
    parts = min(3, len(rest))
    names = ['easy', 'medium', 'hard'][:parts] if parts > 1 else ['main']
    remaining, cursor = 99, 0
    for index in range(parts):
        count = len(rest) // parts + (1 if index < len(rest) % parts else 0)
        chunk = rest[cursor:cursor + count]
        cursor += count
        points = remaining if index == parts - 1 else remaining // (parts - index)
        remaining -= points
        groups.append({'name': names[index], 'points': points, 'cases': chunk})
    return groups


def build(spec_dir, out_dir, skip_verify=False, keep=False, languages=None, verbose=True):
    spec_dir = pathlib.Path(spec_dir)
    meta = json.loads((spec_dir / 'meta.json').read_text(encoding='utf-8'))
    problem_id = meta['id']
    problems = validate_meta(meta, problem_id)
    if problems:
        print('[%s] 元数据不合法：%s' % (problem_id, '；'.join(problems)))
        return None
    package = meta['signature'].get('package') or problem_id.replace('-', '_')
    meta['signature']['package'] = package
    sys.path.insert(0, str(HERE))
    import codegen

    meta['statement'] = {lang: (spec_dir / name).read_text(encoding='utf-8').strip() + '\n'
                         for lang, name in (('zh', 'statement.zh.md'), ('en', 'statement.en.md'))}
    meta.setdefault('schemaVersion', 2)

    drivers = codegen.generate(meta)
    signature_text = codegen.signature_text(meta['signature']['params'], meta['signature']['returns'])
    signature = {'zh': signature_text['cangjie'], 'en': meta['signature'].get('line', {}).get('en') or signature_text['python']}
    signature.update(signature_text)
    if meta['signature'].get('line', {}).get('zh'):
        signature['zh'] = meta['signature']['line']['zh']
    meta['function'] = {'package': package, 'signature': signature}

    solutions = {}
    for language in LANG_ORDER:
        path = spec_dir / ('solution.' + EXT[language])
        if path.is_file():
            solutions[language] = path.read_text(encoding='utf-8')
    if not solutions:
        raise SystemExit('spec 至少要有一个 solution.*')
    base_languages = [l for l in (languages or LANG_ORDER) if l in solutions]
    answer_language = 'python' if 'python' in solutions else base_languages[0]

    namespace = {'__file__': str(spec_dir / 'gen.py'), '__name__': 'gen'}
    exec(compile((spec_dir / 'gen.py').read_text(encoding='utf-8'), 'gen.py', 'exec'), namespace)
    cases = namespace['cases']()
    if not cases:
        raise SystemExit('gen.py 没有产出用例')
    for index, case in enumerate(cases):
        case.setdefault('id', '%02d' % (index + 1))
    ids = [c['id'] for c in cases]
    if len(set(ids)) != len(ids):
        raise SystemExit('用例 id 有重复')
    cases_by_id = {c['id']: c for c in cases}

    work = pathlib.Path(tempfile.mkdtemp(prefix='pb-' + problem_id + '-'))
    tools, cangjie_home = toolchain()
    if verbose:
        print('[%s] %d 个用例，答案语言 %s' % (problem_id, len(cases), answer_language))

    # 1. 用参考解算出每条用例的答案
    files = assemble(answer_language, drivers['main.' + EXT[answer_language]], solutions[answer_language], package, 'full')
    prepared, log = prepare(answer_language, files, work / 'answers', tools, cangjie_home)
    if prepared is None:
        print('[%s] 答案程序编译失败：\n%s' % (problem_id, log[:3000]))
        shutil.rmtree(work, ignore_errors=True)
        return None
    answers = {}
    for case in cases:
        ok, output, log = prepared.run(case['input'], timeout=60)
        if not ok:
            print('[%s] 答案程序在用例 %s 失败：%s' % (problem_id, case['id'], log[:1500]))
            shutil.rmtree(work, ignore_errors=True)
            return None
        answers[case['id']] = output

    # 2. SPJ
    checker_exe = None
    checker_source = None
    checker_path = spec_dir / 'checker.cpp'
    if checker_path.is_file():
        checker_source = checker_path.read_text(encoding='utf-8')
        checker_dir = work / 'checker'
        checker_dir.mkdir(parents=True, exist_ok=True)
        (checker_dir / 'checker.cpp').write_text(checker_source, encoding='utf-8')
        proc = run([tools['g++'], '-std=c++20', '-O2', '-I', str(TESTLIB), 'checker.cpp', '-o', 'checker.exe'],
                   checker_dir, timeout=180)
        if proc.returncode != 0:
            print('[%s] checker 编译失败：\n%s' % (problem_id, proc.stderr.decode('utf-8', 'replace')[:3000]))
            shutil.rmtree(work, ignore_errors=True)
            return None
        checker_exe = checker_dir / 'checker.exe'

    def check(case_id, output):
        if checker_exe:
            case_dir = work / 'check' / case_id
            case_dir.mkdir(parents=True, exist_ok=True)
            (case_dir / 'input.txt').write_text(cases_by_id[case_id]['input'], encoding='utf-8')
            (case_dir / 'output.txt').write_text(output, encoding='utf-8')
            (case_dir / 'answer.txt').write_text(answers[case_id], encoding='utf-8')
            proc = run([str(checker_exe), 'input.txt', 'output.txt', 'answer.txt'], case_dir, timeout=30)
            return proc.returncode == 0, (proc.stdout + proc.stderr).decode('utf-8', 'replace')[:400]
        return tokens(output) == tokens(answers[case_id]), ''

    # 3. 逐语言验证（函数式 + 完整式）；失败的语言降级掉，避免整包导入失败
    report, failed = {}, {}
    if not skip_verify:
        for language in base_languages:
            for mode in ('function', 'full'):
                files = assemble(language, drivers['main.' + EXT[language]], solutions[language], package, mode)
                target = work / ('run-%s-%s' % (language, mode))
                prepared, log = prepare(language, files, target, tools, cangjie_home)
                if prepared is None:
                    failed[language] = '编译失败：' + log[:600]
                    report[language + '/' + mode] = failed[language]
                    if verbose: print('  [%-7s %-8s] %s' % (language, mode, log[:800]))
                    break
                for case in cases:
                    ok, output, log = prepared.run(case['input'])
                    if not ok:
                        failed[language] = '用例 %s 运行失败：%s' % (case['id'], log[:400])
                        break
                    good, message = check(case['id'], output)
                    if not good:
                        failed[language] = '用例 %s 答案不符：%s' % (
                            case['id'], message or ('期望 %r 实际 %r' % (answers[case['id']][:120], output[:120])))
                        break
                report[language + '/' + mode] = failed.get(language, 'ok')
                if verbose:
                    print('  [%-7s %-8s] %s' % (language, mode, report[language + '/' + mode][:220]))
                if language in failed:
                    break

    chosen = [l for l in base_languages if l not in failed]
    if answer_language not in chosen:
        chosen.insert(0, answer_language) if answer_language not in failed else None
    if not chosen:
        print('[%s] 没有任何语言通过验证，放弃。' % problem_id)
        shutil.rmtree(work, ignore_errors=True)
        return None

    # 4. 打包
    package_dir = work / 'package'
    package_dir.mkdir(parents=True)
    meta.pop('groups', None)
    meta['modes'] = {l: ['function', 'full'] for l in chosen}
    meta['groups'] = default_groups(ids)
    allowed = {'schemaVersion', 'id', 'title', 'difficulty', 'tags', 'limits', 'modes', 'statement',
               'samples', 'groups', 'function', 'notes', 'topic', 'judgeType', 'source', 'selfJudge'}
    document = {key: meta[key] for key in allowed if key in meta}
    (package_dir / 'problem.json').write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n',
                                              encoding='utf-8')
    for case in cases:
        (package_dir / (case['id'] + '.in')).write_text(case['input'], encoding='utf-8')
        (package_dir / (case['id'] + '.ans')).write_text(answers[case['id']], encoding='utf-8')
    for key, content in drivers.items():
        (package_dir / key).write_text(content, encoding='utf-8')
    for language, content in solutions.items():
        (package_dir / ('solution.' + EXT[language])).write_text(content, encoding='utf-8')
    if checker_source:
        (package_dir / 'checker.cpp').write_text(checker_source, encoding='utf-8')

    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / (problem_id + '.zip')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(package_dir.iterdir()):
            zf.write(path, path.name)
    if verbose:
        print('[%s] 完成 %s（语言 %s%s）' % (problem_id, archive.name, ','.join(chosen),
                                            '，降级：' + ','.join(failed) if failed else ''))
    if not keep:
        shutil.rmtree(work, ignore_errors=True)
    return {'id': problem_id, 'archive': str(archive), 'report': report, 'languages': chosen, 'failed': failed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specs', nargs='+')
    parser.add_argument('--out', default=str(ROOT / 'build' / 'problemkit'))
    parser.add_argument('--skip-verify', action='store_true')
    parser.add_argument('--keep', action='store_true')
    parser.add_argument('--languages', default=None)
    args = parser.parse_args()
    languages = args.languages.split(',') if args.languages else None
    built = []
    for spec in args.specs:
        result = build(spec, args.out, args.skip_verify, args.keep, languages)
        if result:
            built.append(result)
    print(json.dumps({'built': [r['id'] for r in built]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
