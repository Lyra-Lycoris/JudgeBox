"""Optional real Chrome UI smoke test. Install playwright into .runtime/playwright first."""
import sys, pathlib, subprocess, tempfile, json, urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.runtime/playwright'))
from playwright.sync_api import sync_playwright, expect

with tempfile.TemporaryDirectory(prefix='JudgeBox browser ') as temp:
    proc=subprocess.Popen([str(ROOT/'build/JudgeBox.exe'),'--no-browser','--data-dir',temp],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8')
    url=proc.stdout.readline().strip()
    errors=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
            page=browser.new_page(viewport={'width':1440,'height':1080},device_scale_factor=1)
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(url)
            expect(page.locator('#connectionState')).to_have_text('本地引擎就绪')
            page.screenshot(path=str(ROOT/'build/judgebox-workspace.png'),full_page=True)
            page.locator('#runButton').click()
            expect(page.locator('#overallBadge')).to_have_text('AC',timeout=30000)
            expect(page.locator('#detailOutput')).to_contain_text('15')
            page.locator('#caseExpected').fill('14')
            page.locator('#runButton').click()
            expect(page.locator('#overallBadge')).to_have_text('WA',timeout=30000)
            expect(page.locator('#detailMessage')).to_contain_text('token')
            page.locator('#caseExpected').fill('15')
            page.locator('[data-mode="generated"]').click()
            page.locator('#previewButton').click()
            expect(page.locator('#usePreviewButton')).to_be_enabled()
            preview=page.locator('#preview').inner_text()
            assert preview.strip()
            page.locator('#usePreviewButton').click()
            expect(page.locator('#caseInput')).to_have_value(preview)
            expect(page.locator('#hasExpected')).not_to_be_checked()
            page.locator('#runButton').click()
            expect(page.locator('#overallBadge')).to_have_text('RUN',timeout=30000)
            page.locator('[data-mode="stress"]').click()
            page.locator('#language').select_option('python')
            page.locator('#source').fill('print(0)')
            page.locator('#count').fill('5')
            page.locator('#runButton').click()
            expect(page.locator('#overallBadge')).to_have_text('WA',timeout=30000)
            expect(page.locator('#detailExpected')).not_to_have_text('0')
            page.screenshot(path=str(ROOT/'build/judgebox-stress.png'),full_page=True)
            with page.expect_download() as d:
                page.locator('#counterexampleButton').click()
            data=json.loads(pathlib.Path(d.value.path()).read_text(encoding='utf-8'))
            assert data['verdict']=='WA' and data['input']
            with page.expect_download() as d:
                page.locator('#exportButton').click()
            workspace=pathlib.Path(temp)/'workspace.json'; d.value.save_as(workspace)
            page.locator('#source').fill('draft that must be restored')
            page.locator('#workspaceFile').set_input_files(workspace)
            expect(page.locator('#source')).to_have_value('print(0)')
            page.wait_for_timeout(1000)
            page.reload()
            expect(page.locator('#connectionState')).to_have_text('本地引擎就绪')
            expect(page.locator('#source')).to_have_value('print(0)')
            page.locator('#settingsButton').click(); expect(page.locator('#settingsDialog')).to_be_visible()
            page.keyboard.press('Escape'); expect(page.locator('#settingsDialog')).not_to_be_visible()
            page.set_viewport_size({'width':390,'height':844})
            page.locator('#mobileMode').select_option('generated')
            expect(page.locator('#generationPanel')).to_be_visible()
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'mobile horizontal overflow'
            page.screenshot(path=str(ROOT/'build/judgebox-mobile.png'),full_page=True)
            assert not errors,errors
            browser.close()
        print('Browser tests passed: manual AC/WA, generated RUN, stress counterexample, downloads, workspace import, draft reload, dialog, mobile layout.')
    finally:
        try:
            base,token=url.split('/#')
            req=urllib.request.Request(base+'/api/shutdown',data=b'{}',headers={'Content-Type':'application/json','X-JudgeBox-Token':token})
            urllib.request.urlopen(req,timeout=5).close()
            proc.wait(timeout=10)
        except Exception:
            proc.terminate();proc.wait(timeout=10)
        proc.stdout.close();proc.stderr.close()
