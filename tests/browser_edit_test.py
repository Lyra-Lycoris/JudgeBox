"""新建 / 编辑题目、做题页四张卡片、solveRecord 落盘的浏览器验收。

用法：python tests/browser_edit_test.py [build/JudgeBox.exe]
"""
import os, sys, json, shutil, subprocess, tempfile, pathlib, time, urllib.request
os.environ.setdefault("JUDGEBOX_SYNC_OFF", "1")  # 测试期间不跑 GitHub 题库同步
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.runtime/playwright'))
from playwright.sync_api import sync_playwright, expect

EXE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'build/JudgeBox.exe'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
SHOTS = ROOT / 'build'


def start():
    temp = pathlib.Path(tempfile.mkdtemp(prefix='JudgeBox browser edit '))
    database = temp / 'ProblemDatabase'
    database.mkdir()
    for zip_path in (ROOT / 'ProblemDatabase').glob('*.zip'):
        shutil.copy2(zip_path, database / zip_path.name)
    records = temp / 'solveRecord'
    env = dict(os.environ)
    env['JUDGEBOX_PROBLEM_DATABASE'] = str(database)
    env['JUDGEBOX_SOLVE_RECORD'] = str(records)
    data = temp / 'runs'
    proc = subprocess.Popen([str(EXE), '--no-browser', '--data-dir', str(data)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', env=env)
    line = proc.stdout.readline().strip()
    if not line.startswith('http://127.0.0.1:'):
        proc.terminate()
        raise RuntimeError('server did not announce URL: ' + line)
    base, token = line.split('/#')
    return proc, base, token, database, records, temp


proc, base, token, database, records, temp = start()
errors = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True)
        context = browser.new_context(viewport={'width': 1500, 'height': 1000}, device_scale_factor=1)
        page = context.new_page()
        page.on('pageerror', lambda e: errors.append('pageerror: ' + str(e)))
        page.on('console', lambda m: errors.append('console: ' + m.text) if m.type == 'error' else None)

        page.goto(base + '/#' + token)
        page.wait_for_timeout(500)
        page.goto(base + '/#/problems')
        page.wait_for_selector('.pb-card', timeout=30000)
        page.wait_for_timeout(800)
        page.screenshot(path=str(SHOTS / 'ui-list.png'))
        print('题目卡片数:', page.locator('.pb-card').count())
        print('专题筛选数量:', page.locator('.pb-filter-group[aria-label="专题"] .pb-chip').count())

        # ---- 新建题目（只带测试数据，自判） ----
        page.locator('#pbNewProblem').click()
        page.wait_for_selector('#pbEdId', timeout=10000)
        page.wait_for_timeout(300)
        page.screenshot(path=str(SHOTS / 'ui-editor-new.png'))
        page.fill('#pbEdId', 'ui-demo-range-sum')
        page.fill('#pbEdTitleZh', '区间求和演示')
        page.fill('#pbEdTitleEn', 'Range Sum Demo')
        page.fill('#pbEdTopic', '前缀和与差分')
        page.click('.pb-ed-chips button:has-text("前缀和")')
        areas = page.locator('#pbEditorBody textarea')
        areas.nth(0).fill('# 区间求和演示\n\n给定 $n$ 个数，回答 $q$ 次区间和。\n\n### 输入\n\n第一行 $n$；第二行 $n$ 个整数；第三行 $q$。\n')
        areas.nth(1).fill('# Range Sum Demo\n\nGiven $n$ numbers, answer $q$ range-sum queries.\n')
        page.locator('.pb-ed-section', has_text='样例').first.locator('button:has-text("添加样例")').click()
        page.wait_for_timeout(200)
        page.locator('.pb-ed-case[data-sample="0"] textarea[data-role="input"]').fill('3\n1 2 3\n1\n')
        page.locator('.pb-ed-case[data-sample="0"] textarea[data-role="output"]').fill('6\n')
        data_section = page.locator('.pb-ed-section', has_text='每一条是一对')
        data_section.locator('button:has-text("添加测试数据")').click()
        page.wait_for_timeout(200)
        page.locator('.pb-ed-case[data-case-id="01"] textarea[data-role="input"]').fill('3\n1 2 3\n1\n')
        page.locator('.pb-ed-case[data-case-id="01"] textarea[data-role="answer"]').fill('6\n')
        data_section.locator('button:has-text("添加测试数据")').click()
        page.wait_for_timeout(200)
        page.locator('.pb-ed-case[data-case-id="02"] textarea[data-role="input"]').fill('1\n-5\n2\n')
        page.locator('.pb-ed-case[data-case-id="02"] textarea[data-role="answer"]').fill('-5\n')
        page.screenshot(path=str(SHOTS / 'ui-editor-filled.png'))
        page.locator('#pbEditorSave').click()
        page.wait_for_timeout(2500)
        page.screenshot(path=str(SHOTS / 'ui-editor-saved.png'))
        print('保存状态:', page.locator('#pbEditorStatus').inner_text())
        page.wait_for_timeout(2000)
        page.wait_for_selector('.pb-card:has-text("区间求和演示")', timeout=20000)
        print('新题已出现在题单')

        # ---- 做题页：四张卡片 ----
        page.locator('.pb-card:has-text("区间求和演示")').click()
        page.wait_for_selector('#pbTimeLimit', timeout=15000)
        page.wait_for_timeout(700)
        print('时间卡片:', page.locator('#pbTimeLimit').inner_text(),
              '| 内存卡片:', page.locator('#pbMemoryLimit').inner_text(),
              '| 评判方式:', page.locator('#pbJudgeType').inner_text(),
              '| 来源:', page.locator('#pbSourceCard').inner_text())
        page.screenshot(path=str(SHOTS / 'ui-problem.png'))

        # ---- 写代码 → solveRecord ----
        page.evaluate("""() => {
            const a = document.getElementById('pbSource');
            a.value = 'import sys\\n\\n\\ndef main():\\n    data = sys.stdin.buffer.read().split()\\n\\n\\nmain()\\n';
            a.dispatchEvent(new Event('input', {bubbles: true}));
        }""")
        page.wait_for_timeout(2500)
        print('record 状态:', page.locator('#pbRecordState').inner_text())
        found = [p for p in records.rglob('*') if p.is_file()] if records.exists() else []
        print('solveRecord 目录:', sorted(str(p.relative_to(records)) for p in found))

        # ---- 编辑已有题目 ----
        page.goto(base + '/#/problems')
        page.wait_for_selector('.pb-card', timeout=15000)
        card = page.locator('.pb-card:has-text("区间求和演示")')
        card.locator('.pb-card-menu-btn').click()
        card.locator('.pb-card-menu button:has-text("编辑题目")').click()
        page.wait_for_selector('#pbEdId', timeout=10000)
        page.wait_for_timeout(500)
        print('编辑时 id 可改:', not page.locator('#pbEdId').is_disabled())
        print('编辑载入测试数据条数:', page.locator('.pb-ed-section:has-text("测试数据") .pb-ed-case').count())
        page.fill('#pbEdDifficulty', '1300')
        page.locator('#pbEditorSave').click()
        page.wait_for_timeout(2500)
        print('编辑保存状态:', page.locator('#pbEditorStatus').inner_text())
        page.screenshot(path=str(SHOTS / 'ui-editor-edit.png'))
        page.wait_for_timeout(1500)
        detail = json.loads(urllib.request.urlopen(urllib.request.Request(
            base + '/api/problems/ui-demo-range-sum', headers={'X-JudgeBox-Token': token})).read())
        print('保存后难度:', detail['difficulty'], '专题:', detail['topic'], '评判:', detail['judgeType'])
        browser.close()
finally:
    proc.terminate()
    print('页面错误:', errors if errors else 'none')
    print('临时目录:', temp)
