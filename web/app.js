'use strict';
const $ = id => document.getElementById(id);
const token = location.hash.slice(1) || sessionStorage.getItem('judgebox-token') || '';
if (token) sessionStorage.setItem('judgebox-token', token);
let mode = 'manual', cases = [{input:'5\n1 2 3 4 5\n', expected:'15\n'}], activeCase = 0;
let loaded = false, running = false, tools = {}, currentResult = null, selectedDetail = null;
let previewIndex = 0, previewInput = null, saveTimer, pollTimer, savePromise = Promise.resolve();
const samples = {
  cpp: '#include <iostream>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    int n;\n    if (!(cin >> n)) return 0;\n    long long sum = 0, x;\n    for (int i = 0; i < n; ++i) {\n        cin >> x;\n        sum += x;\n    }\n    cout << sum << "\\n";\n    return 0;\n}\n',
  python: 'n = int(input())\na = list(map(int, input().split()))\nprint(sum(a[:n]))\n',
  java: 'import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner in = new Scanner(System.in);\n        int n = in.nextInt();\n        long sum = 0;\n        for (int i = 0; i < n; i++) sum += in.nextLong();\n        System.out.println(sum);\n    }\n}\n',
  cangjie: '// 仓颉最小运行示例；测试答案填 15\nmain() {\n    println("15")\n}\n'
};
const pythonExample = 'import sys, random\n\nseed = int(sys.argv[1])\nindex = int(sys.argv[2])\nrng = random.Random(seed + index)\nn = rng.randint(1, 8)\nprint(n)\nprint(*[rng.randint(-10, 10) for _ in range(n)])\n\n# 安装 CYaRon 后可以：from cyaron import Graph\n# 再用 print(Graph.tree(n)) 输出树的边\n';
const inputIds = ['language','source','referenceLanguage','reference','timeMs','memoryMb','checker','tolerance','outputKb','referenceTimeMs','count','seed','strategy','template','sizeMin','sizeMax','valueMin','valueMax','alphabet','weighted','rule','generatorMode','generatorSource','stopOnFailure'];
const modeInfo = {
  manual: {name:'手动测试', data:'测试数据', run:'运行'},
  generated: {name:'生成测试', data:'输入生成器', run:'运行'},
  stress: {name:'随机对拍', data:'参考程序与输入', run:'开始对拍'}
};
function notice(message = '') { $('notice').textContent = message; $('notice').hidden = !message; }
async function api(path, body) {
  const options = {headers:{'X-JudgeBox-Token':token}};
  if (body !== undefined) { options.method = 'POST'; options.headers['Content-Type'] = 'application/json'; options.body = JSON.stringify(body); }
  const response = await fetch(path, options);
  let result; try { result = await response.json(); } catch { throw new Error('本地引擎没有返回有效响应，请检查启动窗口。'); }
  if (!response.ok) throw new Error(result.error || `请求失败：${response.status}`);
  return result;
}
function handle(action) { return async event => { try { await action(event); } catch (e) { notice(e.message || String(e)); } }; }
function number(id, min, max) {
  const field = $(id), n = Number(field.value);
  if (!field.value.trim() || !Number.isFinite(n) || n < min || n > max || !Number.isInteger(n)) {
    field.setAttribute('aria-invalid','true'); field.focus(); throw new Error(`${field.closest('label')?.textContent.trim() || id}：请填写 ${min} 到 ${max} 的整数。`);
  }
  field.removeAttribute('aria-invalid'); return n;
}
function make(tag, text, className) { const e = document.createElement(tag); if (text !== undefined) e.textContent = text; if (className) e.className = className; return e; }
function badge(v) { const e = make('span',v,'verdict'); e.dataset.verdict = v; return e; }
function syncSource() {
  const lines = $('source').value.split('\n').length;
  $('sourceLines').textContent = Array.from({length:Math.min(lines,10000)},(_,i) => i+1).join('\n');
  $('sourceFileName').textContent = {cpp:'Main.cpp',python:'main.py',java:'Main.java',cangjie:'main.cj'}[$('language').value];
}
function rememberCase() {
  if (!cases[activeCase]) return;
  cases[activeCase] = {input:$('caseInput').value, expected:$('hasExpected').checked ? $('caseExpected').value : null};
}
function renderCase() {
  const list = $('caseTabs'); list.replaceChildren();
  cases.forEach((c,i) => { const b = make('button',`#${String(i+1).padStart(2,'0')}`,`case-tab${i === activeCase ? ' active' : ''}`); b.setAttribute('aria-pressed',String(i === activeCase)); b.onclick = () => { rememberCase(); activeCase = i; renderCase(); }; list.append(b); });
  const c = cases[activeCase]; $('caseInput').value = c.input; $('caseExpected').value = c.expected ?? ''; $('hasExpected').checked = c.expected !== null;
  expectedState(); $('removeCase').disabled = cases.length <= 1; $('addCase').disabled = cases.length >= 200;
}
function expectedState() {
  $('caseExpected').disabled = !$('hasExpected').checked;
  $('expectedHelp').textContent = $('hasExpected').checked ? '空文本按空答案比较。' : '仅运行，不比较答案。';
}
function switchMode(next, save = true) {
  if (!modeInfo[next]) return;
  rememberCase(); mode = next;
  $('mobileMode').value = next;
  document.querySelectorAll('.mode-btn').forEach(b => { const active = b.dataset.mode === mode; b.classList.toggle('active',active); b.setAttribute('aria-pressed',String(active)); });
  const info = modeInfo[mode];
  $('dataTitle').textContent = info.data;
  $('runLabel').textContent = running ? '运行中' : info.run;
  $('manualPanel').hidden = mode !== 'manual'; $('generationPanel').hidden = mode === 'manual'; $('referencePanel').hidden = mode !== 'stress';
  $('stopOnFailure').disabled = mode === 'stress';
  if (save) queueSave();
}
function preset() {
  const kind = $('template').value; if (kind === 'custom') return;
  const nmin = number('sizeMin',1,1000), nmax = number('sizeMax',1,1000), low = number('valueMin',-1000000000,1000000000), high = number('valueMax',-1000000000,1000000000);
  if (nmin > nmax || low > high) throw new Error('最小值不能大于最大值。');
  const n = {type:'int',name:'n',min:nmin,max:nmax}, arr = {type:'array',count:'n',min:low,max:high};
  let steps;
  if (kind === 'array') steps = [n,arr];
  if (kind === 'pair') steps = [{type:'line',items:[{name:'a',min:low,max:high},{name:'b',min:low,max:high}]}];
  if (kind === 'matrix') steps = [{type:'line',items:[{name:'n',min:nmin,max:nmax},{name:'m',min:nmin,max:nmax}]},{type:'matrix',rows:'n',cols:'m',min:low,max:high}];
  if (kind === 'string') steps = [n,{type:'string',length:'n',alphabet:$('alphabet').value}];
  if (kind === 'tree') steps = [n,{type:'tree',nodes:'n',weighted:$('weighted').checked,min:low,max:high}];
  if (kind === 'graph') steps = [{type:'line',items:[{name:'n',min:nmin,max:nmax},{name:'m',min:'n-1',max:'n*(n-1)/2'}]},{type:'graph',nodes:'n',edges:'m',weighted:$('weighted').checked,min:low,max:high}];
  if (kind === 'multi') steps = [{type:'int',name:'T',min:1,max:3},{type:'repeat',count:'T',steps:[n,arr]}];
  $('rule').value = JSON.stringify({steps},null,2); resetPreview();
}
function templateState() {
  const value = $('template').value;
  $('visualParams').hidden = value === 'custom'; $('alphabetField').hidden = value !== 'string'; $('weightField').hidden = !['tree','graph'].includes(value);
  $('ruleDetails').open = value === 'custom';
  $('sizeMinLabel').textContent = value === 'matrix' ? '行 / 列最小值' : 'n 最小值';
  $('sizeMaxLabel').textContent = value === 'matrix' ? '行 / 列最大值' : 'n 最大值';
}
function generatorState() { const python = $('generatorMode').value === 'python'; $('ruleControls').hidden = python; $('pythonControls').hidden = !python; $('strategy').disabled = python; resetPreview(); }
function resetPreview() { previewIndex = 0; previewInput = null; $('usePreviewButton').disabled = true; $('preview').textContent = '未生成'; $('previewIndex').textContent = `种子 ${$('seed').value} · 第 1 组`; }
function generatorPayload() {
  const p = {generatorMode:$('generatorMode').value,seed:number('seed',0,Number.MAX_SAFE_INTEGER),strategy:$('strategy').value,tools:readTools()};
  if (p.generatorMode === 'python') { p.generatorSource = $('generatorSource').value; if (!p.generatorSource.trim()) throw new Error('请填写 Python 生成器源码。'); }
  else {
    try { p.generator = JSON.parse($('rule').value); $('rule').removeAttribute('aria-invalid'); }
    catch(e) { $('ruleDetails').open = true; $('rule').setAttribute('aria-invalid','true'); $('rule').focus(); throw new Error('JSON 生成规则格式错误：'+e.message); }
  }
  return p;
}
function readTools() { const result = {...tools}; document.querySelectorAll('[data-tool]').forEach(e => { result[e.dataset.tool] = e.value.trim(); }); return result; }
function payload() {
  rememberCase();
  const p = {source:$('source').value,language:$('language').value,mode,timeMs:number('timeMs',10,60000),memoryMb:number('memoryMb',16,4096),outputKb:number('outputKb',1,4096),checker:$('checker').value,tolerance:Number($('tolerance').value),stopOnFailure:$('stopOnFailure').checked,tools:readTools()};
  if (!p.source.trim()) { $('source').focus(); throw new Error('请先粘贴待测程序。'); }
  if (p.checker === 'float' && (!Number.isFinite(p.tolerance) || p.tolerance < 0 || p.tolerance > 1)) throw new Error('浮点容差须在 0 到 1 之间。');
  if (mode === 'manual') p.cases = cases.map(c => ({...c}));
  else Object.assign(p,generatorPayload(),{count:number('count',1,1000)});
  if (mode === 'stress') { p.reference = $('reference').value; p.referenceLanguage = $('referenceLanguage').value; p.referenceTimeMs = number('referenceTimeMs',10,60000); if (!p.reference.trim()) { $('reference').focus(); throw new Error('请填写参考程序。'); } }
  return p;
}
function draft() {
  rememberCase(); const fields = {}; inputIds.forEach(id => { fields[id] = $(id).type === 'checkbox' ? $(id).checked : $(id).value; });
  return {version:1,mode,fields,cases:cases.map(c => ({...c})),tools:readTools()};
}
async function saveDraft() {
  if (!loaded) return;
  clearTimeout(saveTimer);
  const snapshot = draft(); $('saveState').textContent = '保存中…';
  savePromise = savePromise.catch(() => {}).then(async () => {
    try { await api('/api/draft',snapshot); $('saveState').textContent = '已保存'; }
    catch(e) { $('saveState').textContent = '保存失败'; throw e; }
  });
  return savePromise;
}
function queueSave() { if (!loaded) return; clearTimeout(saveTimer); saveTimer = setTimeout(() => saveDraft().catch(e => notice(e.message)),650); }
function applyDraft(data) {
  if (!data || !data.fields) return;
  if (Array.isArray(data.cases) && data.cases.length && data.cases.length <= 200) {
    cases = data.cases.map(c => { if (typeof c.input !== 'string' || !(c.expected === null || typeof c.expected === 'string')) throw new Error('工作区测试点格式不正确。'); return {input:c.input,expected:c.expected}; });
  }
  inputIds.forEach(id => { if (data.fields[id] !== undefined) { if ($(id).type === 'checkbox') $(id).checked = Boolean(data.fields[id]); else $(id).value = String(data.fields[id]); } });
  if (data.tools) { tools = {...tools,...data.tools}; renderTools(); }
  activeCase = 0; renderCase(); templateState(); generatorState(); syncSource(); switchMode(data.mode || 'manual',false); $('floatField').hidden = $('checker').value !== 'float';
}
function download(name, text, type = 'text/plain;charset=utf-8') { const url = URL.createObjectURL(new Blob([text],{type})); const a = make('a'); a.href = url; a.download = name; document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url),1000); }
function addManual(input, expected = null) {
  if (cases.length >= 200) throw new Error('手动测试最多 200 组，请先删除一些测试点。');
  rememberCase(); cases.push({input,expected}); activeCase = cases.length-1; renderCase(); switchMode('manual'); $('caseExpected').focus();
}
function setRunning(value) { running = value; $('runButton').disabled = value; $('cancelButton').hidden = !value; $('runLabel').textContent = value ? '运行中' : modeInfo[mode].run; $('connectionState').textContent = value ? '引擎运行中' : '本地引擎就绪'; $('resultsTitle').closest('section').setAttribute('aria-busy',String(value)); }
async function run() {
  if (running) return;
  notice(); const request = payload(); await saveDraft();
  await api('/api/run',request); selectedDetail = null; $('caseDetail').hidden = true; $('compileDetails').open = false; $('resultRows').replaceChildren(); currentResult = null;
  setRunning(true); await poll();
}
function renderResult(state) {
  $('emptyResults').hidden = true; $('resultContent').hidden = false;
  const v = state.verdict; $('overallBadge').textContent = v; $('overallBadge').dataset.verdict = v;
  $('resultPhase').textContent = state.done ? ({AC:'全部测试通过',WA:'发现答案差异',CE:'编译失败',TLE:'超过时间限制',MLE:'超过内存限制',RE:'程序运行异常',OLE:'超过输出限制',JE:'判题流程出错',RUN:'运行完成 · 部分测试点未比较答案',CANCELLED:'任务已停止',READY:'就绪'}[v] || v) : state.phase;
  $('resultMessage').textContent = state.message || '';
  $('progressText').textContent = `${state.completed} / ${state.total}`; $('progress').max = state.total || 1; $('progress').value = state.completed;
  $('resultMeta').textContent = `${state.completed} / ${state.total} 组${state.seed !== undefined ? ` · 种子 ${state.seed}` : ''}`;
  $('compileLog').textContent = state.compileLog || '';
  $('compileDetails').hidden = !state.compileLog;
  if (v === 'CE' || (v === 'JE' && !state.cases.length)) $('compileDetails').open = true;
  if (!currentResult || currentResult.cases.length !== state.cases.length || currentResult.directory !== state.directory) {
    const rows = $('resultRows'); rows.replaceChildren();
    state.cases.forEach(row => {
      const tr = make('tr'); if (selectedDetail?.index === row.index) tr.classList.add('selected');
      tr.append(make('td',`#${String(row.index+1).padStart(2,'0')}`)); const td = make('td'); td.append(badge(row.verdict)); tr.append(td);
      tr.append(make('td',`${row.timeMs} ms`),make('td',`${(row.memoryBytes/1048576).toFixed(2)} MiB`));
      const desc = make('td',row.message); desc.title = row.message; tr.append(desc);
      const action = make('td'),b = make('button','查看','text-button'); b.setAttribute('aria-label',`查看测试点 ${row.index+1}`); b.onclick = handle(() => showDetail(row.index)); action.append(b); tr.append(action); rows.append(tr);
    });
  }
  currentResult = state;
}
async function poll() {
  clearTimeout(pollTimer);
  try {
    const state = await api('/api/status'); renderResult(state); setRunning(!state.done);
    if (!state.done) pollTimer = setTimeout(poll,250);
    else if (state.cases.length && !selectedDetail) { const failed = state.cases.find(c => !['AC','RUN'].includes(c.verdict)); await showDetail((failed || state.cases[0]).index); }
  } catch(e) { notice(e.message); if (running) pollTimer = setTimeout(poll,1000); }
}
function clip(text) { if (text === null || text === undefined) return '（未提供预期输出）'; if (!text.length) return '（空输出）'; return text.length > 80000 ? text.slice(0,80000)+'\n\n…界面仅展示前 80000 字符，下载可获取完整内容。' : text; }
async function showDetail(index) {
  const detail = await api(`/api/case?index=${index}`); selectedDetail = detail; $('caseDetail').hidden = false;
  $('detailTitle').textContent = `测试点 #${String(index+1).padStart(2,'0')} · ${detail.verdict}`;
  $('detailMessage').textContent = detail.message + (detail.exitCode !== undefined ? ` · 退出码 ${detail.exitCode}` : '') + (detail.referenceTimeMs !== undefined ? ` · 参考程序耗时 ${detail.referenceTimeMs} ms` : '');
  $('detailInput').textContent = clip(detail.input); $('detailExpected').textContent = clip(detail.expected); $('detailOutput').textContent = clip(detail.stdout);
  const stderr = [detail.stderr,detail.referenceStderr ? '[参考程序 stderr]\n'+detail.referenceStderr : '',detail.referenceStdout ? '[参考程序 stdout]\n'+detail.referenceStdout : ''].filter(Boolean).join('\n');
  $('stderrDetails').hidden = !stderr; $('detailStderr').textContent = clip(stderr);
  document.querySelector('[data-download="expected"]').disabled = detail.expected === null;
  Array.from($('resultRows').children).forEach((tr,i) => tr.classList.toggle('selected',currentResult?.cases[i]?.index === index));
}
function renderTools() {
  const labels = {cpp:'C++ · g++.exe',python:'Python · python.exe',javac:'Java 编译器 · javac.exe',java:'Java 运行时 · java.exe',cangjie:'仓颉 · cjc.exe'};
  $('toolFields').replaceChildren(); Object.entries(labels).forEach(([key,name]) => {
    const label = make('label',name,'tool-field'); const input = make('input'); input.dataset.tool = key; input.value = tools[key] || ''; input.placeholder = '未检测到，可填写完整可执行文件路径'; input.spellcheck = false; label.append(input); $('toolFields').append(label);
  });
}
function editCode(event) {
  if (event.key !== 'Tab') return;
  event.preventDefault(); const t = event.target, start = t.selectionStart, end = t.selectionEnd;
  t.setRangeText('    ',start,end,'end'); t.dispatchEvent(new Event('input',{bubbles:true}));
}
document.querySelectorAll('.mode-btn').forEach(b => { b.setAttribute('aria-label',modeInfo[b.dataset.mode].name); b.onclick = () => switchMode(b.dataset.mode); });
$('mobileMode').onchange = () => switchMode($('mobileMode').value);
$('goGenerate').onclick = () => switchMode('generated');
$('addCase').onclick = () => { rememberCase(); cases.push({input:'',expected:''}); activeCase = cases.length-1; renderCase(); queueSave(); $('caseInput').focus(); };
$('removeCase').onclick = () => { if (cases.length <= 1) return; cases.splice(activeCase,1); activeCase = Math.min(activeCase,cases.length-1); renderCase(); queueSave(); };
$('hasExpected').onchange = () => { expectedState(); rememberCase(); queueSave(); };
$('source').addEventListener('input',syncSource); $('language').onchange = syncSource;
$('source').onscroll = () => { $('sourceLines').scrollTop = $('source').scrollTop; };
['source','reference','rule','generatorSource'].forEach(id => $(id).addEventListener('keydown',editCode));
$('sampleButton').onclick = () => { $('source').value = samples[$('language').value]; syncSource(); queueSave(); };
$('checker').onchange = () => { $('floatField').hidden = $('checker').value !== 'float'; };
$('template').onchange = handle(() => { templateState(); preset(); });
['sizeMin','sizeMax','valueMin','valueMax','alphabet','weighted'].forEach(id => $(id).addEventListener('change',handle(() => { preset(); queueSave(); })));
$('rule').addEventListener('input',() => { $('template').value = 'custom'; templateState(); resetPreview(); });
$('generatorMode').onchange = generatorState; ['seed','strategy','generatorSource'].forEach(id => $(id).addEventListener('input',resetPreview));
$('previewButton').onclick = handle(async () => {
  notice(); const b = $('previewButton'); b.disabled = true;
  try { const p = generatorPayload(); const r = await api('/api/generate',{...p,index:previewIndex}); previewInput = r.input; $('preview').textContent = clip(r.input); $('previewIndex').textContent = `种子 ${r.seed} · 第 ${r.index+1} 组`; ++previewIndex; if (previewIndex > 999) previewIndex = 0; $('usePreviewButton').disabled = false; }
  finally { b.disabled = false; }
});
$('usePreviewButton').onclick = handle(() => { if (previewInput !== null) addManual(previewInput); });
$('runButton').onclick = handle(run);
$('cancelButton').onclick = handle(async () => { await api('/api/cancel',{}); $('resultMessage').textContent = '正在终止进程并清理资源…'; });
document.addEventListener('keydown',handle(async event => { if ((event.ctrlKey || event.metaKey) && event.key === 'Enter' && !document.querySelector('dialog[open]')) { event.preventDefault(); await run(); } }));
document.addEventListener('input',queueSave); document.addEventListener('change',queueSave);
$('sourceFileButton').onclick = () => $('sourceFile').click();
$('sourceFile').onchange = handle(async () => { const file = $('sourceFile').files[0]; if (!file) return; if (file.size > 1024*1024) throw new Error('源码文件超过 1 MiB。'); $('source').value = await file.text(); const ext = file.name.split('.').pop().toLowerCase(); const lang = {cpp:'cpp',cc:'cpp',cxx:'cpp',py:'python',java:'java',cj:'cangjie'}[ext]; if (lang) $('language').value = lang; syncSource(); queueSave(); $('sourceFile').value = ''; });
$('exportButton').onclick = () => download('judgebox-workspace.json',JSON.stringify(draft(),null,2),'application/json');
$('importButton').onclick = () => $('workspaceFile').click();
$('workspaceFile').onchange = handle(async () => { const file = $('workspaceFile').files[0]; if (!file) return; if (file.size > 20*1024*1024) throw new Error('工作区文件超过 20 MiB。'); const data = JSON.parse(await file.text()); if (data.version !== 1 || !data.fields) throw new Error('不是有效的 JudgeBox 工作区文件。'); applyDraft(data); queueSave(); $('workspaceFile').value = ''; notice(); });
$('counterexampleButton').onclick = () => { if (selectedDetail) download(`judgebox-case-${selectedDetail.index+1}.json`,JSON.stringify(selectedDetail,null,2),'application/json'); };
$('retestButton').onclick = handle(() => { if (selectedDetail) addManual(selectedDetail.input,selectedDetail.expected); });
document.querySelectorAll('[data-download]').forEach(b => b.onclick = () => { if (!selectedDetail) return; const key = b.dataset.download; const ext = {input:'in',expected:'ans',stdout:'out'}[key]; download(`case-${selectedDetail.index+1}.${ext}`,selectedDetail[key] ?? ''); });
$('settingsButton').onclick = () => $('settingsDialog').showModal(); $('helpButton').onclick = () => $('helpDialog').showModal();
document.querySelectorAll('.close-dialog').forEach(b => b.onclick = () => b.closest('dialog').close());
$('saveSettings').onclick = handle(async () => { number('outputKb',1,4096); tools = readTools(); await saveDraft(); $('settingsDialog').close(); });
$('quitButton').onclick = handle(async () => { if (!confirm(running ? '停止当前任务并退出 JudgeBox？' : '退出 JudgeBox 本地引擎？')) return; await saveDraft(); await api('/api/shutdown',{}); clearTimeout(pollTimer); setRunning(false); $('runButton').disabled = true; $('connectionState').textContent = '引擎已退出'; notice('JudgeBox 已退出，草稿保存在本机。可以关闭这个页面。'); });
async function init() {
  $('source').value = samples.cpp; $('reference').value = samples.cpp; $('generatorSource').value = pythonExample; preset(); renderCase(); syncSource();
  try {
    const config = await api('/api/config'); tools = config.tools; renderTools(); $('dataDirectory').textContent = '数据目录：'+config.dataDirectory;
    const saved = await api('/api/draft'); applyDraft(saved); loaded = true; $('connectionState').textContent = '本地引擎就绪';
    const status = await api('/api/status'); if (status.verdict !== 'READY') { renderResult(status); setRunning(!status.done); if (!status.done) await poll(); else if (status.cases.length) await showDetail(status.cases[0].index); }
  } catch(e) { $('connectionState').textContent = '连接失败'; notice(e.message); }
}
init();
