"""End-to-end tests for the problem subsystem (规格 §10.1), against the real executable."""
import json, subprocess, tempfile, time, urllib.request, urllib.error, pathlib, unittest, sys, os

EXE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'build/JudgeBox.exe').resolve()
sys.argv = sys.argv[:1]
FIXTURE = pathlib.Path(__file__).resolve().parent / 'fixtures' / 'ict-renjian-cihua'
PROBLEM_ID = 'ict-renjian-cihua'


class ProblemAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Data dir is <root>/runs, so problems land in <root>/problems and the run is hermetic.
        cls.root = tempfile.TemporaryDirectory(prefix='JudgeBox problem ')
        cls.data = pathlib.Path(cls.root.name) / 'runs'
        env = dict(os.environ)
        env['PATH'] = ';'.join(p for p in env['PATH'].split(';') if 'msys64' not in p.lower() and 'cangjie' not in p.lower())
        cls.proc = subprocess.Popen([str(EXE), '--no-browser', '--data-dir', str(cls.data)],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                    encoding='utf-8', env=env)
        line = cls.proc.stdout.readline().strip()
        if not line.startswith('http://127.0.0.1:'):
            cls.proc.terminate()
            raise RuntimeError('Server did not announce URL: ' + line)
        cls.url, cls.token = line.split('/#')
        cls.document = json.loads((FIXTURE / 'problem.json').read_text(encoding='utf-8'))
        cls.ac_source = (FIXTURE / 'ac-solution.cj').read_text(encoding='utf-8')
        cls.wa_source = cls.document['function']['starter']['cpp']

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

    def submit(self, language, source):
        body = self.ok('/api/submit', {'problemId': PROBLEM_ID, 'language': language, 'source': source})
        self.assertTrue(body['ok'], body)
        self.assertTrue(body['submissionId'])
        return body['submissionId']

    def wait_done(self, deadline=120):
        finish = time.monotonic() + deadline
        while time.monotonic() < finish:
            status = self.ok('/api/submit/status')
            if status['done']:
                return status
            time.sleep(0.25)
        self.fail('submission did not finish within %ss' % deadline)

    # 1. 导入 fixture → 200，参考答案满分
    def test_01_import(self):
        status, body = self.request('/api/problems/import', {'path': str(FIXTURE / 'problem.json')}, timeout=180)
        self.assertEqual(status, 200, body)
        self.assertTrue(body['ok'])
        self.assertEqual(body['id'], PROBLEM_ID)
        verification = body['verification']
        self.assertEqual(verification['cases'], 8)
        self.assertEqual(verification['checkerCompiled'], True)
        self.assertEqual(verification['drivers']['cpp'], True)
        self.assertEqual(verification['drivers']['cangjie'], True)
        self.assertEqual(verification['solutions']['cangjie']['score'], 100)
        self.assertEqual(verification['solutions']['cangjie']['verdict'], 'AC')
        self.assertEqual(len(verification['groups']), 4)
        self.assertTrue(all(group['passed'] for group in verification['groups']), verification['groups'])
        self.assertTrue((pathlib.Path(self.root.name) / 'problems' / PROBLEM_ID / 'problem.json').is_file())
        self.assertTrue((pathlib.Path(self.root.name) / 'problems' / PROBLEM_ID / 'data.zip').is_file())
        stored = json.loads((pathlib.Path(self.root.name) / 'problems' / PROBLEM_ID / 'problem.json').read_text(encoding='utf-8'))
        self.assertNotIn('tests', stored)
        self.assertIn('storedAt', stored)
        # 判题之前状态是空转，不能是 404。
        state = self.ok('/api/submit/status')
        self.assertEqual(state['done'], True)
        self.assertEqual(state['verdict'], 'READY')
        self.ok('/api/submissions/clear', {})

    # 2. 题单：totalPoints 100，未做过排前面
    def test_02_list(self):
        body = self.ok('/api/problems')
        self.assertEqual(len(body['problems']), 1, body)
        problem = body['problems'][0]
        self.assertEqual(problem['id'], PROBLEM_ID)
        self.assertEqual(problem['totalPoints'], 100)
        self.assertEqual(problem['judgeMode'], 'function')
        self.assertEqual(problem['difficulty'], 1700)
        self.assertIsNone(problem['bestScore'])
        self.assertEqual(problem['attempts'], 0)
        self.assertIsNone(problem['lastVerdict'])
        self.assertIsNone(problem['lastSubmittedAt'])
        self.assertEqual(problem['limits'], {'timeMs': 2000, 'memoryMb': 512})

    # 3. 详情字段齐全
    def test_03_detail(self):
        body = self.ok('/api/problems/' + PROBLEM_ID)
        self.assertTrue(body['statement']['zh'])
        self.assertTrue(body['statement']['en'])
        self.assertEqual(len(body['samples']), 3)
        self.assertEqual(body['samples'][0]['input'].splitlines()[0], '1')
        self.assertIn('signature', body)
        self.assertTrue(body['signature']['zh'])
        self.assertEqual(sorted(body['starter'].keys()), ['cangjie', 'cpp'])
        self.assertEqual(sorted(body['drivers'].keys()), ['cangjie', 'cpp'])
        self.assertEqual(body['judgedLanguages'], ['cpp', 'cangjie'])
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

    # 5. 正确答案：score 100 / AC / improved，且并发提交被 409 拒绝
    def test_05_accepted(self):
        submission = self.submit('cangjie', self.ac_source)
        status, body = self.request('/api/submit', {'problemId': PROBLEM_ID, 'language': 'cangjie', 'source': self.ac_source})
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

    # 6. 历史：两条，明细带 source
    def test_06_submissions(self):
        body = self.ok('/api/submissions?problemId=' + PROBLEM_ID)
        self.assertEqual(len(body['submissions']), 2, body)
        newest, oldest = body['submissions']
        self.assertEqual(newest['verdict'], 'AC')
        self.assertEqual(newest['score'], 100)
        self.assertEqual(newest['cases'], 8)
        self.assertEqual(newest['passed'], 8)
        self.assertEqual(newest['language'], 'cangjie')
        self.assertEqual(oldest['verdict'], 'WA')
        self.assertEqual(oldest['passed'], 0)
        self.assertGreaterEqual(newest['sourceBytes'], len(self.ac_source))
        detail = self.ok('/api/submissions/' + newest['id'])
        self.assertEqual(detail['source'], self.ac_source)
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

    # 8. 坏题包：分值 98 → 400 且 details 可用
    def test_08_invalid_package(self):
        document = json.loads(json.dumps(self.document))
        document['groups'][1]['points'] = 18
        status, body = self.request('/api/problems/import', {'json': json.dumps(document, ensure_ascii=False)}, timeout=60)
        self.assertEqual(status, 400, body)
        self.assertTrue(body['details'], body)
        self.assertIn('100', body['details'][0]['message'])
        self.assertIn('98', body['details'][0]['message'])
        self.assertEqual(body['error'], '题包校验失败')
        # 未知字段同样要拦下来
        document = json.loads(json.dumps(self.document))
        document['freeStyle'] = 1
        document['groups'][1]['points'] = 18
        status, body = self.request('/api/problems/import', {'json': json.dumps(document, ensure_ascii=False)}, timeout=60)
        self.assertEqual(status, 400, body)
        self.assertTrue(any('未知字段' in item['message'] for item in body['details']), body)

    # 10. 外部 data.zip（testsZipPath）导入；缺 .ans 要报出可定位的信息
    def test_10_zip_package(self):
        folder = pathlib.Path(self.root.name) / 'zip-package'
        cases = folder / 'cases'
        cases.mkdir(parents=True)
        document = json.loads(json.dumps(self.document))
        entries = document.pop('tests')
        for case in entries:
            (cases / (case['id'] + '.in')).write_bytes(case['input'].encode('utf-8'))
            (cases / (case['id'] + '.ans')).write_bytes(case['answer'].encode('utf-8'))
        archive = folder / 'data.zip'
        self.make_zip(archive, cases)
        document['testsZipPath'] = str(archive)
        package = folder / 'problem.json'
        package.write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')
        body = self.ok('/api/problems/import', {'path': str(package)}, timeout=180)
        self.assertEqual(body['verification']['cases'], 8)
        self.assertEqual(body['verification']['solutions']['cangjie']['score'], 100)
        self.assertTrue((pathlib.Path(self.root.name) / 'problems' / PROBLEM_ID / 'data.zip').is_file())
        (cases / '05.ans').unlink()
        self.make_zip(archive, cases)
        status, failure = self.request('/api/problems/import', {'path': str(package)}, timeout=120)
        self.assertEqual(status, 400, failure)
        self.assertTrue(any('05.ans' in item['message'] for item in failure['details']), failure)

    @staticmethod
    def make_zip(archive, folder):
        import zipfile
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for path in sorted(folder.iterdir()):
                zip_file.write(path, path.name)

    # 9. 重复导入是幂等的；删除接口同时清掉该题提交
    def test_09_replace_and_delete(self):
        body = self.ok('/api/problems/import', {'path': str(FIXTURE / 'problem.json')}, timeout=180)
        self.assertTrue(body['ok'])
        self.assertEqual(body.get('replaced'), True)
        self.assertEqual(len(self.ok('/api/problems')['problems']), 1)
        self.ok('/api/submit', {'problemId': PROBLEM_ID, 'language': 'cpp', 'source': self.wa_source})
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

    # 11. 判题中途 /api/cancel → CANCELLED，且之后还能正常判题
    def test_11_cancel(self):
        self.ok('/api/submissions/clear', {})
        self.submit('cangjie', self.ac_source)
        time.sleep(0.4)
        self.ok('/api/cancel', {})
        result = self.wait_done(120)
        self.assertEqual(result['verdict'], 'CANCELLED')
        self.assertEqual(result['score'], 0)
        self.assertEqual([group['earned'] for group in result['groups']], [0, 0, 0, 0])
        saved = self.ok('/api/submissions?problemId=' + PROBLEM_ID)['submissions']
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0]['verdict'], 'CANCELLED')
        self.assertEqual(saved[0]['score'], 0)
        self.submit('cangjie', self.ac_source)
        self.assertEqual(self.wait_done()['verdict'], 'AC')


if __name__ == '__main__':
    unittest.main(verbosity=2)
