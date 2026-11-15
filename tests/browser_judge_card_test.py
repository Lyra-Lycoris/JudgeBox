import os
"""检查：题面里没有「两种提交方式 / 函数签名」，标题下没有 time limit 行，裁判卡片跟随提交方式。"""
import pathlib, subprocess, sys
os.environ.setdefault("JUDGEBOX_SYNC_OFF", "1")  # 测试期间不跑 GitHub 题库同步
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.runtime/playwright'))
from playwright.sync_api import sync_playwright

EXE = ROOT / 'JudgeBox.exe'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
proc = subprocess.Popen([str(EXE), '--no-browser', '--data-dir', str(ROOT / '.cache' / 'shots')],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
base, token = proc.stdout.readline().strip().split('/#')
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, headless=True)
        page = browser.new_context(viewport={'width': 1500, 'height': 1000}).new_page()
        page.goto(base + '/' + '#' + token)
        page.wait_for_timeout(300)
        page.goto(base + '/#/problem/t01-date-after')
        page.wait_for_selector('#pbTimeLimit', timeout=60000)
        page.wait_for_function("() => document.getElementById('pbTitle').textContent.includes('日期')", timeout=60000)
        page.wait_for_timeout(400)
        statement = page.locator('#pbStatement').inner_text()
        print('题面含“两种提交方式”:', '两种提交方式' in statement)
        print('题面含“函数签名”:', '函数签名' in statement)
        print('题面含 time limit:', 'time limit' in statement.lower())
        print('初始裁判:', page.locator('#pbJudgeType').inner_text())
        page.select_option('#pbMode', 'full')
        page.wait_for_timeout(400)
        print('切到完整程序后:', page.locator('#pbJudgeType').inner_text())
        page.screenshot(path=str(ROOT / 'build' / 'shots-statement-clean.png'))
        page.select_option('#pbMode', 'function')
        page.wait_for_timeout(300)
        print('切回函数式后:', page.locator('#pbJudgeType').inner_text())
        # 特殊裁判题保持 special
        page.goto(base + '/#/problem/ict-renjian-cihua')
        page.wait_for_selector('#pbJudgeType', timeout=30000)
        page.wait_for_function("() => document.getElementById('pbTitle').textContent.includes('人间')", timeout=60000)
        page.wait_for_timeout(400)
        print('SPJ 题裁判:', page.locator('#pbJudgeType').inner_text())
        browser.close()
finally:
    proc.terminate()
