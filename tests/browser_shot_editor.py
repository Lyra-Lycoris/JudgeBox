import os
"""单独截一张「新建题目」对话框里测试数据区域的图，确认目录导入控件排版正常。"""
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
        page.goto(base + '/#' + token)
        page.wait_for_timeout(400)
        page.goto(base + '/#/problems')
        page.wait_for_selector('#pbNewProblem', timeout=60000)
        page.locator('#pbNewProblem').click()
        page.wait_for_selector('#pbEdId', timeout=10000)
        page.locator('.pb-ed-section', has_text='每一条是一对').locator('button:has-text("添加测试数据")').click()
        page.wait_for_timeout(300)
        page.locator('#pbEdDir').scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        page.screenshot(path=str(ROOT / 'build' / 'shots-case-dir.png'))
        print('目录导入控件:', page.locator('#pbEdDir').count(), page.locator('button:has-text("从目录导入测试数据")').count())
        browser.close()
finally:
    proc.terminate()
