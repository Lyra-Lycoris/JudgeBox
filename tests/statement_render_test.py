"""题面渲染验收：Markdown + MathJax 的字号与排版（对真实可执行文件跑）。

用法：python tests/statement_render_test.py [build/JudgeBox.exe]

守护的回归点（v1.4.0 曾出现）：
  * 图标样式 `svg { width:17px; height:17px; fill:none }` 命中 MathJax 的 <svg>，
    行内公式被撑大、长公式被压成看不清的一条、字形只剩描边。
  * 题面里 $…$ / $$…$$ 配对失败时整段公式退化成原文。
"""
import json, os, pathlib, shutil, subprocess, sys, tempfile, unittest, urllib.error, urllib.request, zipfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.runtime/playwright'))
from playwright.sync_api import sync_playwright, expect

EXE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else str(ROOT / 'build/JudgeBox.exe')).resolve()
sys.argv = sys.argv[:1]
PACKAGE = ROOT / 'tests/fixtures/ict-renjian-cihua'
PROBLEM_ID = 'ict-renjian-cihua'
CHROMES = [pathlib.Path(os.environ.get('JUDGEBOX_CHROME', '')) if os.environ.get('JUDGEBOX_CHROME') else None,
           pathlib.Path(r'C:\Program Files\Google\Chrome\Application\chrome.exe'),
           pathlib.Path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')]

EXTRA_ZH = '\n\n规模：$1 \\le |verse| \\le 200$，且\n\n$$\\sum_{i=1}^{n} |w_i| \\le 2\\times 10^4$$\n'
EXTRA_EN = '\n\nScale: $1 \\le |verse| \\le 200$ and\n\n$$\\sum_{i=1}^{n} |w_i| \\le 2\\times 10^4$$\n'


def make_zip(folder, archive):
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(folder.iterdir()):
            if path.is_file():
                zf.write(path, path.name)
    return archive


class StatementRender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tempfile.TemporaryDirectory(prefix='JudgeBox statement ')
        data = pathlib.Path(cls.root.name) / 'runs'
        # 问题库放到临时目录，测试不会碰本机题单。
        database = pathlib.Path(cls.root.name) / 'ProblemDatabase'
        database.mkdir()
        env = dict(os.environ)
        env['JUDGEBOX_PROBLEM_DATABASE'] = str(database)
        cls.proc = subprocess.Popen([str(EXE), '--no-browser', '--data-dir', str(data)],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                    encoding='utf-8', env=env)
        line = cls.proc.stdout.readline().strip()
        if not line.startswith('http://127.0.0.1:'):
            cls.proc.terminate()
            raise RuntimeError('服务没有公布地址：' + line)
        cls.start_url = line                        # 带 token 的启动地址
        cls.url, cls.token = line.split('/#')
        cls.chrome = next((path for path in CHROMES if path and path.is_file()), None)
        if not cls.chrome:
            cls.proc.kill()
            raise unittest.SkipTest('需要本机 Chrome 或 Edge 才能跑题面渲染验收')

        package = pathlib.Path(cls.root.name) / 'statement.zip'
        folder = pathlib.Path(cls.root.name) / 'statement'
        shutil.copytree(PACKAGE, folder)
        document = json.loads((PACKAGE / 'problem.json').read_text(encoding='utf-8'))
        document['statement']['zh'] += EXTRA_ZH
        document['statement']['en'] += EXTRA_EN
        (folder / 'problem.json').write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')
        cls.package = make_zip(folder, package)
        status, body = cls.request('/api/problems/import', {'zipPath': str(cls.package)}, timeout=240)
        assert status == 200 and body.get('ok'), body

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

    def test_statement_math_renders_at_text_size(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=str(self.chrome), headless=True)
            context = browser.new_context(viewport={'width': 1440, 'height': 960}, device_scale_factor=2)
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(self.start_url)                 # 启动地址里带 token，先落题单页
            page.wait_for_url('**/#/problems')
            page.locator('.pb-card', has_text='人间词话').first.click()
            expect(page.locator('#pbStatement')).to_contain_text('人间词话')
            page.wait_for_selector('#pbStatement mjx-container', timeout=30000)
            page.wait_for_timeout(800)

            # 1) 公式全部由 MathJax 渲染，没有退回原文
            self.assertEqual(page.locator('#pbStatement .math-fallback').count(), 0, '公式退化成原文')

            # 2) 每个公式的 <svg> 宽度 = 它自带的 ex 宽度，没有被 17px 图标规则压扁/撑大
            metrics = page.evaluate("""() => [...document.querySelectorAll('#pbStatement .math, #pbStatement .math-block')]
                .map(node => {
                    const svg = node.querySelector('svg');
                    if (!svg) return null;
                    const ex = Number.parseFloat(svg.getAttribute('width'));
                    const rect = svg.getBoundingClientRect();
                    const style = getComputedStyle(svg);
                    return {ex, width: rect.width, height: rect.height,
                            ratio: rect.width / ex,
                            exPixel: Number.parseFloat(getComputedStyle(node).fontSize) * 0.5,
                            fill: style.fill, stroke: style.stroke};
                }).filter(Boolean)""")
            self.assertGreaterEqual(len(metrics), 2, metrics)
            for item in metrics:
                self.assertAlmostEqual(item['ratio'] / item['exPixel'], 1, delta=0.08,
                                       msg=f'公式宽度不符合字号：{item}')
                self.assertNotEqual(item['fill'], 'none', f'公式只剩描边：{item}')

            # 3) 行内公式与正文同量级，块级公式完整可见（旧 bug 里两者都被塞进 17×17）
            inline = page.evaluate("""() => {
                const node = document.querySelector('#pbStatement .math');
                return node ? node.getBoundingClientRect() : null;
            }""")
            self.assertIsNotNone(inline)
            self.assertLess(inline['height'], 26, inline)
            display = page.evaluate("""() => {
                const node = document.querySelector('#pbStatement .math-block mjx-container');
                return node ? node.getBoundingClientRect() : null;
            }""")
            self.assertIsNotNone(display)
            self.assertGreater(display['width'], 100, display)
            self.assertGreater(display['height'], 30, display)

            # 4) 题面不出现横向溢出（超宽公式在块内滚动，不撑破面板）
            overflow = page.evaluate("""() => {
                const pane = document.querySelector('.pb-statement-pane');
                return {client: pane.clientWidth, scroll: pane.scrollWidth};
            }""")
            self.assertLessEqual(overflow['scroll'], overflow['client'] + 1, overflow)

            # 5) 标题、小节标题、列表、代码块都按 Markdown 结构渲染
            for selector in ('#pbStatement h1', '#pbStatement .pb-md-h2', '#pbStatement .pb-md-h3',
                             '#pbStatement ul li', '#pbStatement pre.pb-md-code'):
                self.assertGreater(page.locator(selector).count(), 0, f'缺少 {selector} 结构')

            page.screenshot(path=str(ROOT / 'build' / 'statement-view.png'))

            # 6) 切到英文：题面换成英文，公式仍然完整
            page.locator('.pb-segment [data-lang=en]').click()
            expect(page.locator('#pbStatement')).to_contain_text('Problem Description')
            page.wait_for_selector('#pbStatement article[lang=en]')
            page.wait_for_selector('#pbStatement mjx-container', timeout=30000)
            self.assertEqual(page.locator('#pbStatement .math-fallback').count(), 0, '英文题面公式退化成原文')
            page.screenshot(path=str(ROOT / 'build' / 'statement-view-en.png'))

            self.assertEqual(errors, [], '页面脚本报错')
            browser.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
