"""界面截图：题单（专题筛选）、做题页四张卡片、新建题目对话框。

用法：python tests/browser_shots.py [build/JudgeBox.exe]
"""
import os, sys, json, subprocess, tempfile, pathlib, urllib.request
os.environ.setdefault("JUDGEBOX_SYNC_OFF", "1")  # 测试期间不跑 GitHub 题库同步
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.runtime/playwright'))
from playwright.sync_api import sync_playwright

EXE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'JudgeBox.exe'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
SHOTS = ROOT / 'build'

proc = subprocess.Popen([str(EXE), '--no-browser', '--data-dir', str(ROOT / '.cache' / 'shots')],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
line = proc.stdout.readline().strip()
base, token = line.split('/#')
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True)
        page = browser.new_context(viewport={'width': 1500, 'height': 1000}).new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(base + '/#' + token)
        page.wait_for_timeout(400)
        page.goto(base + '/#/problems')
        page.wait_for_selector('.pb-card', timeout=120000)
        page.wait_for_timeout(800)
        page.screenshot(path=str(SHOTS / 'shots-list.png'))
        print('卡片数', page.locator('.pb-card').count())
        print('专题筛选', page.locator('.pb-filter-group[aria-label="专题"] .pb-chip').count())
        # 筛选一个专题
        page.locator('.pb-filter-group[aria-label="专题"] .pb-chip', has_text='图论与搜索').first.click()
        page.wait_for_timeout(400)
        page.screenshot(path=str(SHOTS / 'shots-topic.png'))
        print('图论与搜索题数', page.locator('.pb-card').count())
        # 打开一道 Codeforces 来源的题
        page.goto(base + '/#/problem/cf1324d-pair-of-topics')
        page.wait_for_selector('#pbTimeLimit', timeout=30000)
        page.wait_for_timeout(700)
        print('卡片', page.locator('#pbTimeLimit').inner_text(), page.locator('#pbMemoryLimit').inner_text(),
              page.locator('#pbJudgeType').inner_text(), page.locator('#pbSourceCard').inner_text())
        page.screenshot(path=str(SHOTS / 'shots-problem.png'))
        # 新建题目对话框
        page.goto(base + '/#/problems')
        page.wait_for_selector('#pbNewProblem', timeout=30000)
        page.locator('#pbNewProblem').click()
        page.wait_for_selector('#pbEdId', timeout=10000)
        page.wait_for_timeout(400)
        page.screenshot(path=str(SHOTS / 'shots-editor.png'))
        print('页面错误', errors or 'none')
        browser.close()
finally:
    proc.terminate()
