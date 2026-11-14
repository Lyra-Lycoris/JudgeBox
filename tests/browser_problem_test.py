"""题目系统浏览器验收（阶段二）。依赖 .runtime/playwright 与本机 Chrome。

用法：python tests/browser_problem_test.py [build/JudgeBox.exe]
"""
import sys, json, time, pathlib, subprocess, tempfile, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.runtime/playwright'))
from playwright.sync_api import sync_playwright, expect

EXE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'build/JudgeBox.exe'
FIXTURE = ROOT / 'tests/fixtures/ict-renjian-cihua'
PID = 'ict-renjian-cihua'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'


def call(base, token, path, obj=None, method=None, timeout=30):
    data = None if obj is None else json.dumps(obj).encode('utf-8')
    req = urllib.request.Request(base + path, data=data, method=method or ('POST' if obj is not None else 'GET'),
                                 headers={'X-JudgeBox-Token': token, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))


def set_code(page, text):
    page.evaluate("t => { const a = document.getElementById('pbSource'); a.value = t; a.dispatchEvent(new Event('input', {bubbles: true})); }", text)


def submit_and_watch(page, label, shot=None, skip_after=None, close_with='click'):
    """点提交 → 等榜单出现 → 榜单播完后必须停留，直到点击 / Esc 才关闭。返回从出现到停稳的秒数。"""
    page.locator('#pbSubmit').click()
    expect(page.locator('#pbProgress')).to_be_visible()
    overlay = page.locator('.pb-reveal')
    overlay.wait_for(state='attached', timeout=120000)
    shown = time.monotonic()
    if skip_after is not None:
        page.wait_for_timeout(skip_after)
        overlay.click(position={'x': 10, 'y': 10})      # 播放中点击：快进到最终画面，不关闭
    page.locator('.pb-reveal.pb-reveal-settled').wait_for(state='attached', timeout=6000)
    settled = time.monotonic() - shown
    if shot:
        page.screenshot(path=str(ROOT / 'build' / shot))
    page.wait_for_timeout(1500)
    assert overlay.count() == 1, f'{label}: 榜单停稳后不应自动关闭'
    expect(page.locator('.pb-reveal-skip')).to_have_text('点击任意处关闭')
    if close_with == 'escape': page.keyboard.press('Escape')
    else: overlay.click(position={'x': 10, 'y': 10})
    overlay.wait_for(state='detached', timeout=2000)
    print(f'{label}: {settled:.2f} s 停稳，停留 1.5 s 仍在，{close_with} 关闭')
    return settled


document = json.loads((FIXTURE / 'problem.json').read_text(encoding='utf-8'))
# 题面加一行公式，覆盖 MathJax 路径（只改导入请求，不动 fixture 文件）。
document['statement']['zh'] += '\n\n规模：$1 \\le |verse| \\le 200$，且\n\n$$\\sum_{i=1}^{n} |w_i| \\le 2\\times 10^4$$\n'
document['statement']['en'] += '\n\nScale: $1 \\le |verse| \\le 200$ and\n\n$$\\sum_{i=1}^{n} |w_i| \\le 2\\times 10^4$$\n'
starter_cpp = document['function']['starter']['cpp']
wa_source = starter_cpp  # starter 本身就是“固定返回空数组”
ac_source = (FIXTURE / 'ac-solution.cj').read_text(encoding='utf-8')

with tempfile.TemporaryDirectory(prefix='JudgeBox problem ui ') as temp:
    proc = subprocess.Popen([str(EXE), '--no-browser', '--data-dir', temp], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, encoding='utf-8')
    url = proc.stdout.readline().strip()
    base, token = url.split('/#', 1)
    errors = []
    try:
        imported = call(base, token, '/api/problems/import', {'json': json.dumps(document, ensure_ascii=False)}, timeout=240)
        assert imported['ok'] and imported['id'] == PID, imported
        call(base, token, '/api/submissions/clear', {'problemId': PID})
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROME, headless=True)
            context = browser.new_context(viewport={'width': 1440, 'height': 960}, device_scale_factor=1)
            page = context.new_page()
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(url)
            # token 被收进 sessionStorage，hash 换成路由
            expect(page).to_have_url(base + '/#/problems')
            expect(page.locator('.pb-card')).to_have_count(1)
            expect(page.locator('#pbListStats')).to_have_text('已满分 0 / 共 1')
            page.screenshot(path=str(ROOT / 'build/problem-list.png'))

            page.locator('.pb-card').first.click()
            expect(page).to_have_url(base + f'/#/problem/{PID}')
            expect(page.locator('#pbStatement')).to_contain_text('人间词话')
            page.wait_for_function("document.querySelector('#pbStatement mjx-container, #pbStatement .math-fallback')", timeout=10000)
            mathjax = page.locator('#pbStatement mjx-container').count()
            fallback = page.locator('#pbStatement .math-fallback').count()
            print(f'公式：mjx-container={mathjax} 降级={fallback}')
            page.locator('.pb-segment [data-lang=en]').click()
            expect(page.locator('#pbStatement')).to_contain_text('Problem Description')
            page.wait_for_function("document.querySelector('#pbStatement mjx-container, #pbStatement .math-fallback')", timeout=10000)
            page.locator('.pb-segment [data-lang=zh]').click()
            expect(page.locator('#pbStatement')).to_contain_text('题目描述')
            page.screenshot(path=str(ROOT / 'build/problem-view.png'))

            # 0) 题目自测：默认带入 3 个样例；仓颉标准答案经 driver + checker 全部 AC
            expect(page.locator('#pbTabTest')).to_have_attribute('aria-selected', 'true')
            expect(page.locator('.pb-st-case')).to_have_count(len(document['samples']))
            page.locator('#pbLanguage').select_option('cangjie')
            set_code(page, ac_source)
            page.locator('#pbSelfRun').click()
            expect(page.locator('.pb-st-case[data-verdict=AC]')).to_have_count(len(document['samples']), timeout=60000)
            expect(page.locator('#pbSelfStatus')).to_contain_text('通过 3 / 3')
            # 改期望输出 → 本题 checker 判 WA 并给出原因；清空期望输出 → 只运行
            page.locator('.pb-st-case').nth(0).locator('textarea').nth(1).fill('1\n却是 荷池 跳雨\n')
            page.locator('.pb-st-case').nth(1).locator('textarea').nth(1).fill('')
            page.keyboard.press('Control+Shift+Enter')
            expect(page.locator('.pb-st-case').nth(0)).to_have_attribute('data-verdict', 'WA', timeout=60000)
            expect(page.locator('.pb-st-case').nth(0).locator('.pb-st-message')).to_contain_text('解的个数')
            expect(page.locator('.pb-st-case').nth(1)).to_have_attribute('data-verdict', 'OK')
            expect(page.locator('#pbSelfStatus')).to_contain_text('复用上次编译')
            page.screenshot(path=str(ROOT / 'build/problem-selftest.png'))
            # 包名写错 → 自测里直接看到编译错误与包名提示
            set_code(page, ac_source.replace('package ict02', 'package p2025P3', 1))
            page.locator('#pbSelfRun').click()
            expect(page.locator('.pb-st-compile')).to_contain_text('package ict02', timeout=60000)

            # 1) WA：固定返回空数组，自然播完（无点击）
            page.locator('#pbLanguage').select_option('cpp')
            set_code(page, wa_source)
            settled = submit_and_watch(page, 'WA', shot='reveal.png')
            assert 2.0 < settled < 4.0, f'动画 {settled:.2f}s 才停稳'
            expect(page.locator('#pbResultScore')).to_have_text('0')
            expect(page.locator('#pbResult .pb-result-meta .verdict')).to_have_text('WA')

            # 2) AC：仓颉标准答案；中途点击跳过
            page.locator('#pbLanguage').select_option('cangjie')
            set_code(page, ac_source)
            settled = submit_and_watch(page, 'AC(点击快进)', skip_after=600)
            assert settled < 1.5, f'快进后 {settled:.2f}s 才停稳'
            expect(page.locator('#pbResultScore')).to_have_text('100')
            status = call(base, token, '/api/submit/status')
            assert status['score'] == 100 and status['improved'] is True, status
            expect(page.locator('#pbResult .pb-result-compare')).to_contain_text('+100')
            expect(page.locator('#pbBest')).to_have_text('best 100/100')
            page.locator('#pbHistoryButton').click()
            expect(page.locator('.pb-history-item')).to_have_count(2)
            page.locator('.pb-history-item').first.click()
            expect(page.locator('.pb-history-panel .pb-code-lines')).to_contain_text('package')
            page.locator('#pbHistoryClose').click()

            # 草稿按语言分开保存；刷新后停在原题、代码仍在
            page.locator('#pbLanguage').select_option('cpp')
            expect(page.locator('#pbFileName')).to_have_text('solve.cpp')
            assert page.evaluate("document.getElementById('pbSource').value") == wa_source
            page.reload()
            expect(page).to_have_url(base + f'/#/problem/{PID}')
            expect(page.locator('#pbStatement')).to_contain_text('人间词话')

            # 3) reduced-motion：直接给静态结论，约 1.2 s 关闭
            page.emulate_media(reduced_motion='reduce')
            page.locator('#pbLanguage').select_option('cangjie')
            assert page.evaluate("document.getElementById('pbSource').value") == ac_source
            settled = submit_and_watch(page, 'reduced-motion', close_with='escape')
            assert settled < 1.0, settled
            page.emulate_media(reduced_motion='no-preference')

            # 题单状态更新
            page.locator('.pb-back').click()
            expect(page.locator('.pb-card[data-status=solved]')).to_have_count(1)
            page.locator('.pb-chip', has_text='未做').click()
            expect(page.locator('.pb-card')).to_have_count(0)
            page.locator('.pb-chip', has_text='已满分').click()
            expect(page.locator('.pb-card')).to_have_count(1)

            # 调试页仍在、草稿不受影响
            page.locator('.pb-nav-link[data-route=debug]').click()
            expect(page.locator('#runButton')).to_be_visible()
            expect(page.locator('#pbProblemsView')).to_be_hidden()

            # 移动端 390×844
            page.set_viewport_size({'width': 390, 'height': 844})
            page.goto(base + f'/#/problem/{PID}')
            expect(page.locator('#pbStatement')).to_contain_text('人间词话')
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'problem view mobile overflow'
            page.screenshot(path=str(ROOT / 'build/problem-mobile.png'), full_page=True)
            page.locator('.pb-mobile-tabs [data-pane=code]').click()
            expect(page.locator('#pbEditor')).to_be_visible()
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'code pane mobile overflow'
            page.goto(base + '/#/problems')
            expect(page.locator('.pb-card')).to_have_count(1)
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'list mobile overflow'

            # token 丢失：提示而不是白屏
            page.evaluate("sessionStorage.removeItem('judgebox-token')")
            page.reload()
            expect(page.locator('#pbBanner')).to_contain_text('会话已失效')

            browser.close()
        assert not errors, errors
        print('browser_problem_test: OK')
    finally:
        try:
            call(base, token, '/api/shutdown', {})
        except Exception:
            pass
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()
