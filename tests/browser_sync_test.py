"""浏览器验证：全新空题库启动后，后台从 GitHub 同步，题单自动出现题目（不需要手动刷新）。"""
import os, pathlib, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.runtime/playwright'))
from playwright.sync_api import sync_playwright

work = ROOT / '.runtime' / 'sync-browser'
shutil.rmtree(work, ignore_errors=True)
work.mkdir(parents=True)
env = dict(os.environ)
env['JUDGEBOX_PROBLEM_DATABASE'] = str(work / 'ProblemDatabase')
env['JUDGEBOX_SYNC_REPO'] = 'Lyra-Lycoris/JudgeBox-SyncTest'
env.pop('JUDGEBOX_SYNC_OFF', None)

proc = subprocess.Popen([str(ROOT / 'JudgeBox.exe'), '--no-browser', '--data-dir', str(work / 'runs')],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', env=env)
base, token = proc.stdout.readline().strip().split('/#')
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
        page = browser.new_context(viewport={'width': 1500, 'height': 1000}).new_page()
        page.goto(base + '/#' + token)
        page.wait_for_timeout(300)
        start = time.perf_counter()
        page.goto(base + '/#/problems')
        page.wait_for_timeout(1500)
        print('同步中的提示:', page.locator('#pbListStats').inner_text())
        page.wait_for_selector('.pb-card', timeout=180000)
        print('题单自动出现 %.1f s 后，卡片数 %d' % (time.perf_counter() - start, page.locator('.pb-card').count()))
        page.screenshot(path=str(ROOT / 'build' / 'shots-sync.png'))
        browser.close()
finally:
    proc.terminate()
