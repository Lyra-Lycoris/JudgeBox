import os
os.environ.setdefault("JUDGEBOX_SYNC_OFF", "1")  # 测试期间不跑 GitHub 题库同步
"""End-to-end tests for the problem subsystem (题包 v2：四语言 × 两提交方式), against the real executable."""
import base64, json, os, pathlib, shutil, subprocess, sys, tempfile, time, unittest, urllib.request, urllib.error, zipfile

EXE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'build/JudgeBox.exe').resolve()
sys.argv = sys.argv[:1]
FIXTURES = pathlib.Path(__file__).resolve().parent / 'fixtures'
PACKAGE = FIXTURES / 'ict-renjian-cihua'
AC_SOURCE = FIXTURES / 'ict-renjian-cihua-ac.cj'
PROBLEM_ID = 'ict-renjian-cihua'
LANGUAGES = ['cpp', 'cangjie', 'python', 'java']
BOTH = ['function', 'full']


def make_zip(folder, archive):
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(folder.iterdir()):
            if path.is_file():
                zf.write(path, path.name)
    return archive


class ProblemAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Data dir is <root>/runs, so problems land in <root>/problems and the run is hermetic.
        cls.root = tempfile.TemporaryDirectory(prefix='JudgeBox problem ')
        cls.data = pathlib.Path(cls.root.name) / 'runs'
        env = dict(os.environ)
        env['PATH'] = ';'.join(p for p in env['PATH'].split(';') if 'msys64' not in p.lower() and 'cangjie' not in p.lower())
        cls.database = pathlib.Path(cls.root.name) / 'ProblemDatabase'
        cls.database.mkdir()
        env['JUDGEBOX_PROBLEM_DATABASE'] = str(cls.database)
        cls.proc = subprocess.Popen([str(EXE), '--no-browser', '--data-dir', str(cls.data)],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                    encoding='utf-8', env=env)
        line = cls.proc.stdout.readline().strip()
        if not line.startswith('http://127.0.0.1:'):
            cls.proc.terminate()
            raise RuntimeError('Server did not announce URL: ' + line)
        cls.url, cls.token = line.split('/#')
        cls.package = make_zip(PACKAGE, pathlib.Path(cls.root.name) / 'ict-renjian-cihua.zip')
        cls.ac_source = AC_SOURCE.read_text(encoding='utf-8')
        cls.wa_source = (PACKAGE / 'starter.cpp').read_text(encoding='utf-8')

    @classmethod
    def tearDownClass(cls):
        try:
            cls.request('/api/shutdown', {})
        finally:
            cls.proc.wait(timeout=10)
            cls.proc.stdout.close()
            cls.proc.stderr.close()
            cls.root.cleanup()

    @classmethod
    def request(cls, path, obj=None, timeout=30):
        request = urllib.request.Request(cls.url + path, data=None if obj is None else json.dumps(obj).encode(),
                                         headers={'Content-Type': 'application/json', 'X-JudgeBox-Token': cls.token})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            with error:
                return error.code, json.load(error)

    def ok(self, path, obj=None, timeout=30):
        status, body = self.request(path, obj, timeout)
        self.assertEqual(status, 200, body)
        return body

    def variant(self, name, mutate):
        """Copy the fixture package, let mutate() edit it, return the zipped path."""
        folder = pathlib.Path(self.root.name) / ('variant-' + name)
        shutil.copytree(PACKAGE, folder)
        mutate(folder)
        return make_zip(folder, pathlib.Path(self.root.name) / ('variant-' + name + '.zip'))

    def submit(self, language, source, mode='function'):
        body = self.ok('/api/submit', {'problemId': PROBLEM_ID, 'language': language, 'mode': mode, 'source': source})
        self.assertTrue(body['ok'], body)
        self.assertTrue(body['submissionId'])
        return body['submissionId']

    def wait_done(self, deadline=180):
        finish = time.monotonic() + deadline
        while time.monotonic() < finish:
            status = self.ok('/api/submit/status')
            if status['done']:
                return status
            time.sleep(0.25)
        self.fail('submission did not finish within %ss' % deadline)

    # 1. 导入题包 zip → 200，四种语言两种方式的参考答案都满分，源码落盘
    def test_01_import(self):
        status, body = self.request('/api/problems/import', {'zipPath': str(self.package)}, timeout=600)
        self.assertEqual(status, 200, body)
        self.assertTrue(body['ok'])
        self.assertEqual(body['id'], PROBLEM_ID)
        verification = body['verification']
        self.assertEqual(verification['cases'], 8)
        self.assertEqual(verification['checker'], 'custom')
        self.assertEqual(verification['checkerCompiled'], True)
        self.assertEqual(sorted(verification['drivers']), sorted(LANGUAGES))
        self.assertTrue(all(verification['drivers'].values()), verification['drivers'])
        self.assertEqual(sorted(verification['solutions']), sorted(LANGUAGES))
        for language in LANGUAGES:
            self.assertEqual(verification['solutions'][language]['score'], 100, language)
            self.assertEqual(verification['solutions'][language]['verdict'], 'AC', language)
            self.assertEqual(verification['full'][language], True, language)
        self.assertEqual(len(verification['groups']), 4)
        self.assertTrue(all(group['passed'] for group in verification['groups']), verification['groups'])
        files = [path.name for path in self.database.glob('*.zip')]
        self.assertEqual(files, ['ict-renjian-cihua_人间词话_.zip'], files)
        self.assertEqual(body['file'], 'ict-renjian-cihua_人间词话_.zip')
        # 判题之前状态是空转，不能是 404。
        state = self.ok('/api/submit/status')
        self.assertEqual(state['done'], True)
        self.assertEqual(state['verdict'], 'READY')
        self.ok('/api/submissions/clear', {})

    # 2. 题单：totalPoints 100，未做过排前面，卡片带 modes
    def test_02_list(self):
        body = self.ok('/api/problems')
        self.assertEqual(len(body['problems']), 1, body)
        problem = body['problems'][0]
        self.assertEqual(problem['id'], PROBLEM_ID)
        self.assertEqual(problem['totalPoints'], 100)
        self.assertEqual(problem['judgedLanguages'], LANGUAGES)
        self.assertEqual(problem['modes'], {language: BOTH for language in LANGUAGES})
        self.assertEqual(problem['difficulty'], 1700)
        self.assertIsNone(problem['bestScore'])
        self.assertEqual(problem['attempts'], 0)
        self.assertIsNone(problem['lastVerdict'])
        self.assertIsNone(problem['lastSubmittedAt'])
        self.assertEqual(problem['limits'], {'timeMs': 2000, 'memoryMb': 512})
        self.assertEqual(problem['title']['zh'], '人间词话')
        self.assertEqual(problem['file'], 'ict-renjian-cihua_人间词话_.zip')

    # 3. 详情字段齐全
    def test_03_detail(self):
        body = self.ok('/api/problems/' + PROBLEM_ID)
        self.assertTrue(body['statement']['zh'])
        self.assertTrue(body['statement']['en'])
        self.assertEqual(len(body['samples']), 3)
        self.assertEqual(body['samples'][0]['input'].splitlines()[0], '1')
        self.assertIn('signature', body)
        self.assertTrue(body['signature']['zh'])
        self.assertTrue(body['signature']['python'])
        self.assertEqual(sorted(body['starter'].keys()), sorted(LANGUAGES))
        self.assertEqual(sorted(body['drivers'].keys()), sorted(LANGUAGES))
        self.assertEqual(body['judgedLanguages'], LANGUAGES)
        self.assertEqual(body['modes'], {language: BOTH for language in LANGUAGES})
        self.assertEqual(body['package'], 'ict02')
        self.assertEqual([group['name'] for group in body['groups']], ['sample', 'simple', 'boundary', 'long'])
        self.assertEqual(sum(group['caseCount'] for group in body['groups']), 8)
        self.assertEqual([group['points'] for group in body['groups']], [1, 20, 29, 50])

    # 4. 错误答案：score 0 / WA / 每组首个用例失败即换组
    def test_04_wrong_answer(self):
        submission = self.submit('cpp', self.wa_source)
        status = self.wait_done()
        self.assertEqual(status['submissionId'], submission)
        self.assertEqual(status['verdict'], 'WA')
        self.assertEqual(status['score'], 0)
        self.assertEqual(status['total'], 8)
        self.assertEqual(status['completed'], 4)
        self.assertEqual([case['verdict'] for case in status['cases']], ['WA', 'WA', 'WA', 'WA'])
        self.assertEqual([case['caseId'] for case in status['cases']], ['00', '02', '04', '07'])
        self.assertEqual([group['state'] for group in status['groups']], ['failed'] * 4)
        self.assertEqual([group['earned'] for group in status['groups']], [0, 0, 0, 0])
        self.assertTrue(status['message'])
        self.assertIn('improved', status)
        self.assertFalse(status['improved'])
        self.assertTrue(status['finishedAt'].endswith('Z'))
        self.assertEqual(status['language'], 'cpp')
        self.assertEqual(status['mode'], 'function')

    # 5. 正确答案：score 100 / AC / improved，且并发提交被 409 拒绝
    def test_05_accepted(self):
        submission = self.submit('cangjie', self.ac_source)
        status, body = self.request('/api/submit', {'problemId': PROBLEM_ID, 'language': 'cangjie', 'mode': 'function', 'source': self.ac_source})
        self.assertEqual(status, 409, body)
        self.assertIn('已有提交正在判题', body['error'])
        result = self.wait_done()
        self.assertEqual(result['submissionId'], submission)
        self.assertEqual(result['verdict'], 'AC')
        self.assertEqual(result['score'], 100)
        self.assertEqual(result['completed'], 8)
        self.assertEqual([group['earned'] for group in result['groups']], [1, 20, 29, 50])
        self.assertEqual([group['state'] for group in result['groups']], ['passed'] * 4)
        self.assertTrue(result['improved'])
        self.assertEqual(result['previousBest'], 0)
        self.assertEqual(result['best'], 100)
        problems = self.ok('/api/problems')['problems']
        self.assertEqual(problems[0]['bestScore'], 100)
        self.assertEqual(problems[0]['attempts'], 2)
        self.assertEqual(problems[0]['lastVerdict'], 'AC')
        self.assertTrue(problems[0]['lastSubmittedAt'].endswith('Z'))

    # 6. 历史：两条，明细带 source / language / mode
    def test_06_submissions(self):
        body = self.ok('/api/submissions?problemId=' + PROBLEM_ID)
        self.assertEqual(len(body['submissions']), 2, body)
        newest, oldest = body['submissions']
        self.assertEqual(newest['verdict'], 'AC')
        self.assertEqual(newest['score'], 100)
        self.assertEqual(newest['cases'], 8)
        self.assertEqual(newest['passed'], 8)
        self.assertEqual(newest['language'], 'cangjie')
        self.assertEqual(newest['mode'], 'function')
        self.assertEqual(oldest['verdict'], 'WA')
        self.assertEqual(oldest['passed'], 0)
        self.assertGreaterEqual(newest['sourceBytes'], len(self.ac_source))
        detail = self.ok('/api/submissions/' + newest['id'])
        self.assertEqual(detail['source'], self.ac_source)
        self.assertEqual(detail['mode'], 'function')
        self.assertEqual(len(detail['cases']), 8)
        self.assertEqual(len(detail['groups']), 4)
        self.assertTrue(detail['id'])
        status, missing = self.request('/api/submissions/20990101-000000-abcdef')
        self.assertEqual(status, 404, missing)

    # 7. 清空缓存：提交没了，题目还在
    def test_07_clear(self):
        body = self.ok('/api/submissions/clear', {'problemId': PROBLEM_ID})
        self.assertTrue(body['ok'])
        self.assertEqual(body['removed'], 2)
        self.assertEqual(self.ok('/api/submissions?problemId=' + PROBLEM_ID)['submissions'], [])
        problems = self.ok('/api/problems')['problems']
        self.assertEqual(len(problems), 1)
        self.assertIsNone(problems[0]['bestScore'])
        self.assertEqual(problems[0]['attempts'], 0)

    # 8. 坏题包：只改 zip 里的东西，全部 400 且 details 可定位
    def test_08_invalid_package(self):
        def bad_points(folder):
            document = json.loads((folder / 'problem.json').read_text(encoding='utf-8'))
            document['groups'][1]['points'] = 18
            (folder / 'problem.json').write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')

        status, body = self.request('/api/problems/import', {'zipPath': str(self.variant('points', bad_points))}, timeout=600)
        self.assertEqual(status, 400, body)
        self.assertTrue(body['details'], body)
        self.assertIn('100', body['details'][0]['message'])
        self.assertIn('98', body['details'][0]['message'])
        self.assertEqual(body['error'], '题包校验失败')

        def unknown_field(folder):
            document = json.loads((folder / 'problem.json').read_text(encoding='utf-8'))
            document['freeStyle'] = 1
            (folder / 'problem.json').write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')

        status, body = self.request('/api/problems/import', {'zipPath': str(self.variant('unknown', unknown_field))}, timeout=600)
        self.assertEqual(status, 400, body)
        self.assertTrue(any('未知字段' in item['message'] for item in body['details']), body)

        def missing_answer(folder):
            (folder / '05.ans').unlink()

        status, body = self.request('/api/problems/import', {'zipPath': str(self.variant('noans', missing_answer))}, timeout=600)
        self.assertEqual(status, 400, body)
        self.assertTrue(any('05.ans' in item['message'] for item in body['details']), body)

        def drop_python_driver(folder):
            (folder / 'main.py').unlink()

        status, body = self.request('/api/problems/import', {'zipPath': str(self.variant('nopy', drop_python_driver))}, timeout=600)
        self.assertEqual(status, 400, body)
        self.assertTrue(any('main.py' in item['message'] for item in body['details']), body)

        # 不存在的 zip / 不是 zip
        status, body = self.request('/api/problems/import', {'zipPath': str(pathlib.Path(self.root.name) / 'nope.zip')}, timeout=30)
        self.assertEqual(status, 400, body)
        broken = pathlib.Path(self.root.name) / 'broken.zip'
        broken.write_bytes(b'not a zip')
        status, body = self.request('/api/problems/import', {'zipPath': str(broken)}, timeout=30)
        self.assertEqual(status, 400, body)
        self.assertEqual(len(list(self.database.glob('*.zip'))), 1, '坏题包不能进题库')

    # 9. 重复导入是幂等的；删除接口同时清掉该题提交
    def test_09_replace_and_delete(self):
        body = self.ok('/api/problems/import', {'zipPath': str(self.package)}, timeout=600)
        self.assertTrue(body['ok'])
        self.assertEqual(body.get('replaced'), True)
        self.assertEqual(len(self.ok('/api/problems')['problems']), 1)
        self.ok('/api/submit', {'problemId': PROBLEM_ID, 'language': 'cpp', 'mode': 'function', 'source': self.wa_source})
        self.wait_done()
        self.assertEqual(len(self.ok('/api/submissions?problemId=' + PROBLEM_ID)['submissions']), 1)
        request = urllib.request.Request(self.url + '/api/problems/' + PROBLEM_ID, method='DELETE',
                                         headers={'Content-Type': 'application/json', 'X-JudgeBox-Token': self.token})
        with urllib.request.urlopen(request, timeout=30) as response:
            self.assertEqual(json.load(response), {'ok': True})
        self.assertEqual(self.ok('/api/problems')['problems'], [])
        status, body = self.request('/api/problems/' + PROBLEM_ID)
        self.assertEqual(status, 404, body)
        self.assertEqual(self.ok('/api/submissions?problemId=' + PROBLEM_ID)['submissions'], [])
        self.assertEqual(list(self.database.glob('*.zip')), [])

    # 10. base64 上传同一份题包（浏览器走这条）
    def test_10_base64_import(self):
        encoded = base64.b64encode(pathlib.Path(self.package).read_bytes()).decode('ascii')
        body = self.ok('/api/problems/import', {'zip': encoded}, timeout=600)
        self.assertEqual(body['id'], PROBLEM_ID)
        self.assertEqual(body['verification']['solutions']['cangjie']['score'], 100)
        self.assertEqual(body['verification']['full']['java'], True)
        status, rejected = self.request('/api/problems/import', {'zip': '!!!not-base64!!!'}, timeout=30)
        self.assertEqual(status, 400, rejected)

    # 11. 判题中途 /api/cancel → CANCELLED，且之后还能正常判题
    def test_11_cancel(self):
        self.ok('/api/submissions/clear', {})
        self.submit('cangjie', self.ac_source)
        time.sleep(0.4)
        self.ok('/api/cancel', {})
        result = self.wait_done(180)
        self.assertEqual(result['verdict'], 'CANCELLED')
        self.assertEqual(result['score'], 0)
        self.assertEqual([group['earned'] for group in result['groups']], [0, 0, 0, 0])
        saved = self.ok('/api/submissions?problemId=' + PROBLEM_ID)['submissions']
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]['verdict'], 'CANCELLED')
        self.assertEqual(saved[0]['score'], 0)
        self.submit('cangjie', self.ac_source)
        self.assertEqual(self.wait_done()['verdict'], 'AC')

    # 12. 只有 C++ 的 v2 题包：完整式和函数式都能提交；没有 checker 时用内置 token 比较
    def test_12_builtin_checker_and_subset_modes(self):
        folder = pathlib.Path(self.root.name) / 'builtin'
        folder.mkdir()
        document = {
            'schemaVersion': 2, 'id': 'demo-builtin',
            'title': {'zh': '内置判分示例', 'en': 'Builtin checker demo'},
            'difficulty': 800, 'tags': ['模拟'],
            'limits': {'timeMs': 1000, 'memoryMb': 128},
            'modes': {'cpp': ['function', 'full']},
            'statement': {'zh': '# A+B\n\n读两个整数输出和。\n', 'en': '# A+B\n\nRead two integers and print the sum.\n'},
            'samples': [{'input': '2 3\n', 'output': '5\n'}],
            'groups': [{'name': 'sample', 'points': 1, 'cases': ['01']},
                       {'name': 'main', 'points': 99, 'cases': ['02']}],
            'function': {'package': 'demo', 'signature': {'zh': 'func solve(a: Int64, b: Int64): Int64', 'en': 'solve(a, b) -> a + b'}},
        }
        (folder / 'problem.json').write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')
        function_source = 'long long solve(long long a, long long b) { return a + b; }\n'
        full = '#include <cstdio>\nint main() { long long a, b; scanf("%lld %lld", &a, &b); printf("%lld\\n", a + b); }\n'
        (folder / 'main.cpp').write_text('#include <cstdio>\nlong long solve(long long a, long long b);\nint main() { long long a, b; scanf("%lld %lld", &a, &b); printf("%lld\\n", solve(a, b)); }\n', encoding='utf-8')
        (folder / 'starter.cpp').write_text('long long solve(long long a, long long b) { return 0; }\n', encoding='utf-8')
        (folder / 'solution.cpp').write_text(function_source, encoding='utf-8')
        (folder / '01.in').write_text('2 3\n', encoding='utf-8')
        (folder / '01.ans').write_text('5\n', encoding='utf-8')
        (folder / '02.in').write_text('1000000000 7\n', encoding='utf-8')
        (folder / '02.ans').write_text('1000000007\n', encoding='utf-8')
        archive = make_zip(folder, pathlib.Path(self.root.name) / 'builtin.zip')
        imported = self.ok('/api/problems/import', {'zipPath': str(archive)}, timeout=300)
        self.assertEqual(imported['verification']['checker'], 'builtin')
        self.assertEqual(imported['verification']['checkerCompiled'], False)
        self.assertEqual(imported['verification']['solutions']['cpp']['score'], 100)
        self.assertEqual(imported['verification']['full']['cpp'], True)
        self.assertEqual(len(list(self.database.glob('*.zip'))), 2)
        cards = {item['id']: item for item in self.ok('/api/problems')['problems']}
        self.assertEqual(cards['demo-builtin']['title']['zh'], '内置判分示例')
        self.assertEqual(cards['demo-builtin']['modes'], {'cpp': ['function', 'full']})
        for mode, source in [('function', function_source), ('full', full)]:
            self.ok('/api/submit', {'problemId': 'demo-builtin', 'language': 'cpp', 'mode': mode, 'source': source})
            result = self.wait_done()
            self.assertEqual(result['verdict'], 'AC', result)
            self.assertEqual(result['score'], 100)
        # 未声明的语言/方式要被拒绝
        status, rejected = self.request('/api/submit', {'problemId': 'demo-builtin', 'language': 'python', 'mode': 'function', 'source': 'def solve(a, b):\n    return a + b\n'})
        self.assertEqual(status, 400, rejected)
        status, rejected = self.request('/api/problems/demo-builtin/run', {'language': 'cpp', 'mode': 'python', 'source': function_source,
                                                                           'tests': [{'input': '2 3\n', 'expected': '5\n'}]})
        self.assertEqual(status, 400, rejected)

    # 13. 直接把题包丢进题库目录（不走导入接口）也会出现，标题取自 problem.json 而不是文件名
    def test_13_manual_drop(self):
        template = pathlib.Path(__file__).resolve().parent.parent / 'CreateProblemGuide' / '模板'
        folder = pathlib.Path(self.root.name) / 'manual-package'
        shutil.copytree(template, folder)
        archive = make_zip(folder, pathlib.Path(self.root.name) / 'whatever.zip')
        shutil.copyfile(archive, self.database / 'zzz-random-name.zip')
        cards = {item['id']: item for item in self.ok('/api/problems')['problems']}
        self.assertIn('a-plus-b', cards)
        self.assertEqual(cards['a-plus-b']['title']['zh'], 'A+B 问题')
        self.assertEqual(cards['a-plus-b']['difficulty'], 800)
        self.assertEqual(cards['a-plus-b']['modes'], {language: BOTH for language in LANGUAGES})
        detail = self.ok('/api/problems/a-plus-b')
        self.assertEqual(detail['package'], 'demo')
        self.assertEqual(sorted(detail['drivers'].keys()), sorted(LANGUAGES))
        request = urllib.request.Request(self.url + '/api/problems/a-plus-b', method='DELETE',
                                         headers={'Content-Type': 'application/json', 'X-JudgeBox-Token': self.token})
        with urllib.request.urlopen(request, timeout=30) as response:
            self.assertEqual(json.load(response), {'ok': True})
        self.assertFalse((self.database / 'zzz-random-name.zip').exists())

    # 14. 模板题：四种语言 × 两种方式各提交一次，全部 AC
    def test_14_all_eight_combinations(self):
        template = pathlib.Path(__file__).resolve().parent.parent / 'CreateProblemGuide' / '模板'
        archive = make_zip(template, pathlib.Path(self.root.name) / 'plus.zip')
        self.ok('/api/problems/import', {'zipPath': str(archive)}, timeout=300)
        sources = {
            ('cpp', 'function'): 'long long solve(long long a, long long b) { return a + b; }\n',
            ('cpp', 'full'): '#include <iostream>\nint main() { long long a, b; std::cin >> a >> b; std::cout << a + b << \'\\n\'; }\n',
            ('python', 'function'): 'def solve(a: int, b: int) -> int:\n    return a + b\n',
            ('python', 'full'): 'import sys\ndata = sys.stdin.buffer.read().split()\nprint(int(data[0]) + int(data[1]))\n',
            ('java', 'function'): '    static long solve(long a, long b) { return a + b; }\n',
            ('java', 'full'): 'import java.util.*;\npublic class Main { public static void main(String[] args) { Scanner s = new Scanner(System.in); System.out.println(s.nextLong() + s.nextLong()); } }\n',
            ('cangjie', 'function'): 'package demo\n\nfunc solve(a: Int64, b: Int64): Int64 {\n    return a + b\n}\n',
            ('cangjie', 'full'): 'package demo\n\nimport std.convert.Parsable\n\nmain(): Unit {\n    let a = Int64.parse(readln().trimAscii())\n    let b = Int64.parse(readln().trimAscii())\n    println(a + b)\n}\n',
        }
        for (language, mode), source in sources.items():
            self.ok('/api/submit', {'problemId': 'a-plus-b', 'language': language, 'mode': mode, 'source': source})
            result = self.wait_done()
            self.assertEqual(result['verdict'], 'AC', (language, mode, result))
            self.assertEqual(result['score'], 100, (language, mode, result))
            self.assertEqual(result['language'], language)
            self.assertEqual(result['mode'], mode)
        request = urllib.request.Request(self.url + '/api/problems/a-plus-b', method='DELETE',
                                         headers={'Content-Type': 'application/json', 'X-JudgeBox-Token': self.token})
        with urllib.request.urlopen(request, timeout=30) as response:
            self.assertEqual(json.load(response), {'ok': True})


if __name__ == '__main__':
    unittest.main(verbosity=2)
