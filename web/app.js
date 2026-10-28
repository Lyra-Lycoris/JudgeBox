'use strict';
const $ = id => document.getElementById(id);
const token = location.hash.slice(1) || sessionStorage.getItem('judgebox-token') || '';
if (token) sessionStorage.setItem('judgebox-token', token);
let mode = 'manual', cases = [], dataset = null, runCaseLabel = null;
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
  manual: {name:'手动测试', data:'测试数据', description:'填写输入与答案，快速验证程序', run:'运行判题'},
  generated: {name:'生成测试', data:'输入生成器', description:'选择模板，批量构造边界与随机数据', run:'运行判题'},
  stress: {name:'随机对拍', data:'参考程序与输入', description:'用正确程序自动发现答案差异', run:'开始对拍'}
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
function formatTime(value) {
  const ms = Number(value);
  if (!Number.isFinite(ms)) return '—';
  if (ms < 1) return '<1 ms';
  return `${ms.toFixed(ms < 10 ? 2 : ms < 100 ? 1 : 0)} ms`;
}
function formatMemory(value) {
  const bytes = Number(value);
  if (!Number.isFinite(bytes)) return '—';
  return bytes < 1048576 ? `${(bytes/1024).toFixed(2)} KB` : `${(bytes/1048576).toFixed(2)} MB`;
}
let editorLanguage = '';
function showDiagnostics(result, source) {
  const state = $('diagnosticState');
  const items = Array.isArray(result.diagnostics) ? result.diagnostics : [];
  state.classList.remove('diagnostic-bad', 'diagnostic-warn');
  if (!source.trim()) { state.textContent = ''; return []; }
  const errors = items.filter(item => item.severity !== 'warning');
  const warnings = items.filter(item => item.severity === 'warning');
  if (!items.length) { state.textContent = result.status || '无错误'; state.classList.toggle('diagnostic-bad', Boolean(result.status)); return []; }
  const parts = [];
  if (errors.length) parts.push(`${errors.length} 个错误`);
  if (warnings.length) parts.push(`${warnings.length} 个警告`);
  const first = errors[0] || warnings[0];
  state.textContent = `${parts.join('，')} · 第 ${first.line} 行：${first.message}`;
  state.classList.toggle('diagnostic-bad', errors.length > 0);
  state.classList.toggle('diagnostic-warn', errors.length === 0);
  return items;
}
function syncSource() {
  if (window.JudgeEditor) {
    JudgeEditor.pull();
    const language = $('language').value;
    if (language !== editorLanguage) { editorLanguage = language; JudgeEditor.setLanguage(language); }
  }
  const lines = $('sourceLines');
  if (lines) lines.textContent = Array.from({length:Math.min($('source').value.split('\n').length,10000)},(_,i) => i+1).join('\n');
  $('sourceFileName').textContent = {cpp:'Main.cpp',python:'main.py',java:'Main.java',cangjie:'main.cj'}[$('language').value];
}
function mountEditor() {
  if (!window.JudgeEditor || $('source').dataset.editor) return;
  $('source').dataset.editor = '1';
  JudgeEditor.mount($('source'), {
    getLanguage: () => $('language').value,
    lint: async (source, language) => {
      if (!source.trim()) return showDiagnostics({diagnostics:[]}, '');
      try {
        const result = await api('/api/diagnostics', {source, language});
        return showDiagnostics(result, source);
      } catch (e) { return showDiagnostics({diagnostics:[], status:e.message || String(e)}, source); }
    }
  });
  editorLanguage = $('language').value;
}
function rememberCases() {
  if (dataset) return;
  document.querySelectorAll('.case-card').forEach(card => {
    const index = Number(card.dataset.index);
    if (!cases[index]) return;
    const compare = card.querySelector('.compare-answer').checked;
    cases[index] = {input:card.querySelector('.case-input').value, expected:compare ? card.querySelector('.case-expected').value : null};
  });
}
function caseCard(item, index) {
  const card = make('article', undefined, 'case-card');
  card.dataset.index = String(index);
  const head = make('div', undefined, 'case-card-head');
  head.append(make('h3', `样例 ${index + 1}`, 'case-card-title'));
  const actions = make('div', undefined, 'case-card-actions');
  const runOne = make('button', '运行这组', 'text-button run-one');
  runOne.type = 'button';
  runOne.setAttribute('aria-label', `只运行样例 ${index + 1}`);
  runOne.disabled = running;
  runOne.onclick = handle(() => submitRun(index));
  const remove = make('button', '删除', 'text-button muted');
  remove.type = 'button';
  remove.setAttribute('aria-label', `删除样例 ${index + 1}`);
  remove.onclick = () => { rememberCases(); cases.splice(index, 1); renderCases(); queueSave(); };
  actions.append(runOne, remove);
  head.append(actions);
  const body = make('div', undefined, 'manual-fields');
  const inputTitle = make('div', undefined, 'field-title');
  const inputLabel = make('label', '输入');
  const input = make('textarea', undefined, 'data-code case-input');
  input.id = index === 0 ? 'caseInput' : `caseInput-${index}`;
  inputLabel.htmlFor = input.id;
  input.spellcheck = false;
  input.placeholder = '输入';
  input.value = item.input;
  input.addEventListener('input', () => { cases[index].input = input.value; });
  const copyInput = make('button', '复制', 'text-button muted');
  copyInput.type = 'button';
  copyInput.onclick = () => navigator.clipboard?.writeText(input.value);
  inputTitle.append(inputLabel, copyInput);
  const expectedTitle = make('div', undefined, 'field-title');
  const expectedLabel = make('label', '预期输出');
  const expected = make('textarea', undefined, 'data-code case-expected');
  expected.id = index === 0 ? 'caseExpected' : `caseExpected-${index}`;
  expectedLabel.htmlFor = expected.id;
  expected.spellcheck = false;
  expected.placeholder = '预期输出';
  expected.value = item.expected ?? '';
  expected.disabled = item.expected === null;
  const compareLabel = make('label', undefined, 'checkbox');
  const compare = make('input');
  compare.type = 'checkbox';
  compare.className = 'compare-answer';
  if (index === 0) compare.id = 'hasExpected';
  compare.checked = item.expected !== null;
  compare.addEventListener('change', () => {
    expected.disabled = !compare.checked;
    cases[index].expected = compare.checked ? expected.value : null;
  });
  expected.addEventListener('input', () => { if (compare.checked) cases[index].expected = expected.value; });
  compareLabel.append(compare, document.createTextNode('比较答案'));
  const copyExpected = make('button', '复制', 'text-button muted');
  copyExpected.type = 'button';
  copyExpected.onclick = () => navigator.clipboard?.writeText(expected.value);
  const expectedTools = make('div', undefined, 'case-card-actions');
  expectedTools.append(compareLabel, copyExpected);
  expectedTitle.append(expectedLabel, expectedTools);
  body.append(inputTitle, input, expectedTitle, expected);
  card.append(head, body);
  return card;
}
function datasetCard(item) {
  const card = make('article',undefined,'case-card');
  const head = make('div',undefined,'case-card-head');
  head.append(make('h3',item.name,'case-card-title'));
  const body = make('div',undefined,'manual-fields');
  body.append(make('p',`输入 ${formatMemory(item.inputBytes)} · 答案 ${item.expectedBytes === null ? '未提供' : formatMemory(item.expectedBytes)}`,'field-help'));
  card.append(head,body); return card;
}
function renderCases() {
  const list = $('caseList');
  list.replaceChildren();
  if (dataset) {
    dataset.cases.slice(0,200).forEach(item => list.append(datasetCard(item)));
    if (dataset.cases.length > 200) list.append(make('p',`其余 ${dataset.cases.length-200} 组不在界面展开，判题时仍会全部运行。`,'field-help'));
  } else cases.forEach((item, index) => list.append(caseCard(item, index)));
  $('caseEmpty').hidden = cases.length > 0 || Boolean(dataset);
  $('addCase').disabled = !dataset && cases.length >= 200;
}
function focusCase(index, field) {
  const card = document.querySelector(`.case-card[data-index="${index}"]`);
  if (!card) return;
  card.scrollIntoView({block:'nearest'});
  card.querySelector(field).focus();
}
function datasetLabel() {
  if (!dataset) return '';
  return dataset.label || dataset.directory.split(/[\\/]/).filter(Boolean).at(-1) || '数据集';
}
function switchMode(next, save = true) {
  if (!modeInfo[next]) return;
  rememberCases(); mode = next;
  $('mobileMode').value = next;
  document.querySelectorAll('.mode-btn').forEach(b => { const active = b.dataset.mode === mode; b.classList.toggle('active',active); b.setAttribute('aria-pressed',String(active)); });
  const info = modeInfo[mode], label = mode === 'manual' ? datasetLabel() : '';
  $('dataTitle').textContent = label ? `${info.data} · ${label}` : info.data;
  document.title = label ? `${label} · JudgeBox` : 'JudgeBox · 本地判题工作台';
  $('modeDescription').textContent = info.description;
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
  rememberCases();
  const p = {source:$('source').value,language:$('language').value,mode,timeMs:number('timeMs',10,60000),memoryMb:number('memoryMb',16,4096),outputKb:number('outputKb',1,16*1024*1024),checker:$('checker').value,tolerance:Number($('tolerance').value),stopOnFailure:$('stopOnFailure').checked,tools:readTools()};
  if (!p.source.trim()) { $('source').focus(); throw new Error('请先粘贴待测程序。'); }
  if (p.checker === 'float' && (!Number.isFinite(p.tolerance) || p.tolerance < 0 || p.tolerance > 1)) throw new Error('浮点容差须在 0 到 1 之间。');
  if (mode === 'manual') {
    if (dataset) p.dataset = {directory:dataset.directory};
    else {
      if (!cases.length) throw new Error('请先新建测试用例或导入数据目录。');
      p.cases = cases.map(c => ({...c}));
    }
  }
  else Object.assign(p,generatorPayload(),{count:number('count',1,1000)});
  if (mode === 'stress') { p.reference = $('reference').value; p.referenceLanguage = $('referenceLanguage').value; p.referenceTimeMs = number('referenceTimeMs',10,60000); if (!p.reference.trim()) { $('reference').focus(); throw new Error('请填写参考程序。'); } }
  return p;
}
function draft() {
  rememberCases(); const fields = {}; inputIds.forEach(id => { fields[id] = $(id).type === 'checkbox' ? $(id).checked : $(id).value; });
  return {version:1,mode,fields,cases:cases.map(c => ({...c})),dataset,tools:readTools()};
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
  dataset = data.dataset && typeof data.dataset.directory === 'string' && Array.isArray(data.dataset.cases) ? data.dataset : null;
  if (dataset) cases = [];
  else if (Array.isArray(data.cases) && data.cases.length <= 200) {
    cases = data.cases.map(c => { if (typeof c.input !== 'string' || !(c.expected === null || typeof c.expected === 'string')) throw new Error('工作区测试点格式不正确。'); return {input:c.input,expected:c.expected}; }).filter(c => c.input !== '' || (c.expected !== null && c.expected !== ''));
  }
  inputIds.forEach(id => { if (data.fields[id] !== undefined) { if ($(id).type === 'checkbox') $(id).checked = Boolean(data.fields[id]); else $(id).value = String(data.fields[id]); } });
  if (data.tools) { tools = {...tools,...data.tools}; renderTools(); }
  renderCases(); templateState(); generatorState(); syncSource(); switchMode(data.mode || 'manual',false); $('floatField').hidden = $('checker').value !== 'float';
}
function download(name, text, type = 'text/plain;charset=utf-8') { const url = URL.createObjectURL(new Blob([text],{type})); const a = make('a'); a.href = url; a.download = name; document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url),1000); }
function addManual(input, expected = null) {
  if (cases.length >= 200) throw new Error('手动测试最多 200 组，请先删除一些测试点。');
  dataset = null; rememberCases(); cases.push({input,expected}); renderCases(); switchMode('manual'); focusCase(cases.length - 1, '.case-expected');
}
function setRunning(value) { running = value; $('runButton').disabled = value; $('cancelButton').hidden = !value; document.querySelectorAll('.run-one').forEach(button => { button.disabled = value; }); $('runLabel').textContent = value ? '运行中' : modeInfo[mode].run; $('connectionState').textContent = value ? '引擎运行中' : '本地引擎就绪'; $('resultsTitle').closest('section').setAttribute('aria-busy',String(value)); }
async function submitRun(onlyIndex) {
  if (running) return;
  notice(); const request = payload();
  runCaseLabel = Number.isInteger(onlyIndex) ? onlyIndex : null;
  if (runCaseLabel !== null) request.cases = [cases[runCaseLabel]];
  await saveDraft();
  await api('/api/run',request); selectedDetail = null; $('caseDetail').hidden = true; $('compileDetails').open = false; $('resultRows').replaceChildren(); currentResult = null;
  setRunning(true); await poll();
}
function renderResult(state) {
  document.querySelector('.side').classList.toggle('showing-results',state.done);
  $('editCasesButton').hidden = !state.done;
  $('emptyResults').hidden = true; $('resultContent').hidden = false;
  const v = state.verdict; $('overallBadge').textContent = v; $('overallBadge').dataset.verdict = v;
  $('resultPhase').textContent = state.done ? ({AC:'全部测试通过',WA:'发现答案差异',CE:'编译失败',TLE:'超过时间限制',MLE:'超过内存限制',RE:'程序运行异常',OLE:'超过输出限制',JE:'判题流程出错',RUN:'运行完成 · 部分测试点未比较答案',CANCELLED:'任务已停止',READY:'就绪'}[v] || v) : state.phase;
  $('resultMessage').textContent = state.message || '';
  $('progressText').textContent = `${state.completed} / ${state.total}`; $('progress').max = state.total || 1; $('progress').value = state.completed;
  const hasFinalTime = state.done && state.cases.length > 0;
  $('overallTime').hidden = !hasFinalTime; $('progressArea').hidden = hasFinalTime;
  if (hasFinalTime) {
    const average = state.cases.reduce((sum, row) => sum + Number(row.timeMs || 0), 0) / state.cases.length;
    $('overallTimeValue').textContent = formatTime(average);
    $('overallTimeBasis').textContent = state.cases.length > 1 ? `${state.cases.length} 组算术平均` : '单组 CPU 耗时';
    $('overallTime').title = state.cases.length < state.total ? '仅统计停止前实际运行的测试点' : '全部测试点的用户态 CPU 耗时算术平均值';
  }
  $('resultMeta').textContent = `${state.completed} / ${state.total} 组${state.seed !== undefined ? ` · 种子 ${state.seed}` : ''}`;
  $('compileLog').textContent = state.compileLog || '';
  $('compileDetails').hidden = !state.compileLog;
  if (v === 'CE' || (v === 'JE' && !state.cases.length)) $('compileDetails').open = true;
  if (!currentResult || currentResult.cases.length !== state.cases.length || currentResult.directory !== state.directory) {
    const rows = $('resultRows'); rows.replaceChildren();
    state.cases.forEach(row => {
      const card = make('button',undefined,'result-card'); card.type = 'button'; card.dataset.verdict = row.verdict;
      if (selectedDetail?.index === row.index) card.classList.add('selected');
      const shown = runCaseLabel !== null && state.cases.length === 1 ? runCaseLabel : row.index;
      card.setAttribute('aria-label',`测试点 ${shown+1}，${row.verdict}，${formatTime(row.timeMs)}，${formatMemory(row.memoryBytes)}。查看详情`);
      card.title = row.message || '点击查看测试点详情';
      card.append(make('span',`#${shown+1}`,'result-card-index'),make('strong',row.verdict,'result-card-verdict'),make('span',`${formatTime(row.timeMs)} / ${formatMemory(row.memoryBytes)}`,'result-card-metrics'));
      card.onclick = handle(() => showDetail(row.index)); rows.append(card);
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
function clip(text) { if (text === null || text === undefined) return '（未提供预期输出）'; if (!text.length) return '（空输出）'; return text.length > 1145 ? text.slice(0,1145)+'...' : text; }
function visibleText(parent, text, changed = false) {
  const fragment = document.createDocumentFragment();
  for (const char of text) {
    if (char === ' ' || char === '\t' || char === '\u00a0' || char === '\u200b') {
      const symbol = make('span', char === ' ' ? '·' : char === '\t' ? '→\t' : char === '\u00a0' ? '⍽' : 'ZWSP', 'ws');
      symbol.title = char === ' ' ? '空格' : char === '\t' ? '制表符' : char === '\u00a0' ? '不换行空格' : '零宽空格';
      fragment.append(symbol);
    } else fragment.append(document.createTextNode(char));
  }
  if (changed) { const mark = make('span', undefined, 'diff-changed'); mark.append(fragment); parent.append(mark); }
  else parent.append(fragment);
}
function characterDiff(expected, actual) {
  const operations = [];
  const push = (kind,text) => { if (!text) return; if (operations.at(-1)?.kind === kind) operations.at(-1).text += text; else operations.push({kind,text}); };
  if (expected.length * actual.length > 160000) {
    let prefix = 0, suffix = 0;
    while (prefix < expected.length && prefix < actual.length && expected[prefix] === actual[prefix]) prefix++;
    while (suffix < expected.length - prefix && suffix < actual.length - prefix && expected[expected.length-1-suffix] === actual[actual.length-1-suffix]) suffix++;
    push('same',expected.slice(0,prefix)); push('removed',expected.slice(prefix,expected.length-suffix)); push('added',actual.slice(prefix,actual.length-suffix)); push('same',suffix ? expected.slice(-suffix) : '');
    return operations;
  }
  const table = Array.from({length:expected.length+1},() => new Uint16Array(actual.length+1));
  for (let i=expected.length-1;i>=0;i--) for (let j=actual.length-1;j>=0;j--) table[i][j] = expected[i] === actual[j] ? table[i+1][j+1]+1 : Math.max(table[i+1][j],table[i][j+1]);
  let i=0,j=0;
  while (i<expected.length || j<actual.length) {
    if (i<expected.length && j<actual.length && expected[i]===actual[j]) push('same',expected[i]),i++,j++;
    else if (j<actual.length && (i===expected.length || table[i][j+1]>=table[i+1][j])) push('added',actual[j++]);
    else push('removed',expected[i++]);
  }
  return operations;
}
function diffRow(target,line,number,kind,operations,side) {
  const row = make('div',undefined,`diff-line ${kind === 'removed' ? 'diff-removed' : kind === 'added' ? 'diff-added' : ''}`);
  row.append(make('span',number === null ? '' : String(number+1),'diff-number'));
  const content = make('span',undefined,'diff-text');
  if (line !== null) {
    if (kind === 'changed') for (const operation of operations) {
      if (operation.kind === 'same') visibleText(content,operation.text);
      else if ((side === 'expected' && operation.kind === 'removed') || (side === 'actual' && operation.kind === 'added')) visibleText(content,operation.text,true);
    }
    else visibleText(content,line);
    const end = make('span','¶','ws ws-newline'); end.title = '行尾'; content.append(end);
  }
  row.append(content); target.append(row);
}
function lineDiff(expected, actual) {
  const a = expected.replace(/\r\n/g, '\n').replace(/\n$/, '').split('\n');
  const b = actual.replace(/\r\n/g, '\n').replace(/\n$/, '').split('\n');
  if (a.length * b.length > 250000) return a.map((line, i) => ({a:line,b:b[i] ?? null,ai:i,bi:b[i] === undefined ? null : i,kind:line === b[i] ? 'same' : 'changed'})).concat(b.slice(a.length).map((line,j) => ({a:null,b:line,ai:null,bi:a.length+j,kind:'added'})));
  const table = Array.from({length:a.length + 1}, () => new Uint16Array(b.length + 1));
  for (let i = a.length - 1; i >= 0; i--) for (let j = b.length - 1; j >= 0; j--) table[i][j] = a[i] === b[j] ? table[i+1][j+1] + 1 : Math.max(table[i+1][j],table[i][j+1]);
  const raw = []; let i = 0, j = 0;
  while (i < a.length || j < b.length) {
    if (i < a.length && j < b.length && a[i] === b[j]) raw.push({a:a[i],b:b[j],ai:i,bi:j,kind:'same'}),i++,j++;
    else if (j < b.length && (i === a.length || table[i][j+1] >= table[i+1][j])) raw.push({a:null,b:b[j],ai:null,bi:j,kind:'added'}),j++;
    else raw.push({a:a[i],b:null,ai:i,bi:null,kind:'removed'}),i++;
  }
  const rows = [];
  for (let k = 0; k < raw.length;) {
    if (raw[k].kind === 'same') { rows.push(raw[k++]); continue; }
    const removed = [], added = [];
    while (k < raw.length && raw[k].kind !== 'same') (raw[k].kind === 'removed' ? removed : added).push(raw[k++]);
    const length = Math.max(removed.length,added.length);
    for (let n = 0; n < length; n++) {
      const left = removed[n], right = added[n];
      rows.push(left && right ? {...left,b:right.b,bi:right.bi,kind:'changed'} : left || right);
    }
  }
  return rows;
}
function renderOutputDiff(expected, actual) {
  const left = $('detailExpected'), right = $('detailOutput');
  left.replaceChildren(); right.replaceChildren(); left.classList.add('diff-output'); right.classList.add('diff-output');
  for (const row of lineDiff(expected, actual)) {
    const operations = row.kind === 'changed' ? characterDiff(row.a,row.b) : null;
    diffRow(left,row.a,row.ai,row.kind === 'added' ? 'empty' : row.kind,operations,'expected');
    diffRow(right,row.b,row.bi,row.kind === 'removed' ? 'empty' : row.kind,operations,'actual');
  }
}
async function showDetail(index) {
  const detail = await api(`/api/case?index=${index}`); selectedDetail = detail; $('caseDetail').hidden = false;
  const shown = runCaseLabel !== null && currentResult?.cases.length === 1 ? runCaseLabel : index;
  $('detailTitle').textContent = `${detail.name || `样例 #${String(shown+1).padStart(2,'0')}`} · ${detail.verdict}`;
  $('detailMessage').textContent = detail.message + (detail.exitCode !== undefined ? ` · 退出码 ${detail.exitCode}` : '') + (detail.referenceTimeMs !== undefined ? ` · 参考程序耗时 ${formatTime(detail.referenceTimeMs)}` : '') + (detail.fileBacked ? ' · 大数据模式仅显示前 1145 个字符' : '');
  $('detailInput').textContent = clip(detail.input);
  document.querySelector('.output-grid').classList.toggle('diff-grid',detail.verdict === 'WA' && detail.expected !== null && !detail.fileBacked);
  $('detailExpected').classList.remove('diff-output'); $('detailOutput').classList.remove('diff-output');
  if (detail.verdict === 'WA' && detail.expected !== null && !detail.fileBacked) {
    renderOutputDiff(clip(detail.expected),clip(detail.stdout));
    requestAnimationFrame(() => {
      const firstDifference = $('detailOutput').querySelector('.diff-changed') || $('detailExpected').querySelector('.diff-changed');
      firstDifference?.scrollIntoView({block:'center',inline:'center',behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
    });
  }
  else { $('detailExpected').textContent = clip(detail.expected); $('detailOutput').textContent = clip(detail.stdout); }
  const stderr = [detail.stderr,detail.referenceStderr ? '[参考程序 stderr]\n'+detail.referenceStderr : '',detail.referenceStdout ? '[参考程序 stdout]\n'+detail.referenceStdout : ''].filter(Boolean).join('\n');
  $('stderrDetails').hidden = !stderr; $('detailStderr').textContent = clip(stderr);
  document.querySelector('[data-download="expected"]').disabled = detail.expected === null || detail.fileBacked;
  document.querySelector('[data-download="input"]').disabled = Boolean(detail.fileBacked);
  document.querySelector('[data-download="stdout"]').disabled = Boolean(detail.fileBacked);
  $('counterexampleButton').disabled = Boolean(detail.fileBacked); $('retestButton').disabled = Boolean(detail.fileBacked);
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
$('addCase').onclick = () => {
  if (!dataset && cases.length >= 200) return;
  dataset = null; rememberCases(); cases.push({input:'',expected:''}); renderCases(); focusCase(cases.length - 1, '.case-input'); queueSave();
};
$('source').addEventListener('input',syncSource); $('language').onchange = syncSource;
if ($('sourceLines')) $('source').onscroll = () => { $('sourceLines').scrollTop = $('source').scrollTop; };
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
$('runButton').onclick = handle(() => submitRun());
$('editCasesButton').onclick = () => { document.querySelector('.side').classList.remove('showing-results'); $('editCasesButton').hidden = true; };
$('judgeSummary').addEventListener('click', event => {
  if (!window.matchMedia('(max-width: 800px)').matches) return;
  if (event.target.closest('.judge-scroll, button, a, input, select, textarea')) return;
  $('judgeDock').classList.toggle('expanded');
});
$('cancelButton').onclick = handle(async () => { await api('/api/cancel',{}); $('resultMessage').textContent = '正在终止进程并清理资源…'; });
document.addEventListener('keydown',handle(async event => { if ((event.ctrlKey || event.metaKey) && event.key === 'Enter' && !document.querySelector('dialog[open]')) { event.preventDefault(); await submitRun(); } }));
document.addEventListener('input',queueSave); document.addEventListener('change',queueSave);
$('sourceFileButton').onclick = () => $('sourceFile').click();
$('sourceFile').onchange = handle(async () => { const file = $('sourceFile').files[0]; if (!file) return; if (file.size > 1024*1024) throw new Error('源码文件超过 1 MiB。'); $('source').value = await file.text(); const ext = file.name.split('.').pop().toLowerCase(); const lang = {cpp:'cpp',cc:'cpp',cxx:'cpp',py:'python',java:'java',cj:'cangjie'}[ext]; if (lang) $('language').value = lang; syncSource(); queueSave(); $('sourceFile').value = ''; });
$('exportButton').onclick = () => download('judgebox-workspace.json',JSON.stringify(draft(),null,2),'application/json');
$('importButton').onclick = () => $('workspaceFile').click();
$('datasetButton').onclick = handle(async () => {
  const directory = prompt('请输入包含 .in / .ans（或 .out）文件的数据目录完整路径：',dataset?.directory || '');
  if (!directory?.trim()) return;
  dataset = await api('/api/dataset/import',{directory:directory.trim()}); cases = [];
  switchMode('manual'); renderCases(); queueSave();
  notice(`已快速导入 ${dataset.cases.length} 组，共 ${formatMemory(dataset.totalBytes)}；文件内容不会载入浏览器。`);
});
$('workspaceFile').onchange = handle(async () => { const file = $('workspaceFile').files[0]; if (!file) return; if (file.size > 20*1024*1024) throw new Error('工作区文件超过 20 MiB。'); const data = JSON.parse(await file.text()); if (data.version !== 1 || !data.fields) throw new Error('不是有效的 JudgeBox 工作区文件。'); applyDraft(data); queueSave(); $('workspaceFile').value = ''; notice(); });
$('counterexampleButton').onclick = () => { if (selectedDetail) download(`judgebox-case-${selectedDetail.index+1}.json`,JSON.stringify(selectedDetail,null,2),'application/json'); };
$('retestButton').onclick = handle(() => { if (selectedDetail) addManual(selectedDetail.input,selectedDetail.expected); });
document.querySelectorAll('[data-download]').forEach(b => b.onclick = () => { if (!selectedDetail) return; const key = b.dataset.download; const ext = {input:'in',expected:'ans',stdout:'out'}[key]; download(`case-${selectedDetail.index+1}.${ext}`,selectedDetail[key] ?? ''); });
$('settingsButton').onclick = () => $('settingsDialog').showModal(); $('helpButton').onclick = () => $('helpDialog').showModal();
document.querySelectorAll('.close-dialog').forEach(b => b.onclick = () => b.closest('dialog').close());
$('saveSettings').onclick = handle(async () => { number('outputKb',1,16*1024*1024); tools = readTools(); await saveDraft(); $('settingsDialog').close(); });
$('quitButton').onclick = handle(async () => { if (!confirm(running ? '停止当前任务并退出 JudgeBox？' : '退出 JudgeBox 本地引擎？')) return; await saveDraft(); await api('/api/shutdown',{}); clearTimeout(pollTimer); setRunning(false); $('runButton').disabled = true; $('connectionState').textContent = '引擎已退出'; notice('JudgeBox 已退出，草稿保存在本机。可以关闭这个页面。'); });
function setupSplitter() {
  const splitter = $('splitter'), workbench = document.querySelector('.workbench');
  let percent = 40;
  try { percent = Math.min(72,Math.max(28,Number(localStorage.getItem('judgebox-pane-width')) || 40)); } catch {}
  const apply = value => { percent = Math.min(72,Math.max(28,value)); workbench.style.setProperty('--left-pane',`${percent}%`); splitter.setAttribute('aria-valuenow',String(Math.round(percent))); };
  apply(percent);
  splitter.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    splitter.setPointerCapture(event.pointerId); splitter.classList.add('dragging'); event.preventDefault();
  });
  splitter.addEventListener('pointermove', event => {
    if (!splitter.hasPointerCapture(event.pointerId)) return;
    const bounds = workbench.getBoundingClientRect(); apply((event.clientX - bounds.left) / bounds.width * 100);
  });
  const finish = event => {
    if (!splitter.hasPointerCapture(event.pointerId)) return;
    splitter.releasePointerCapture(event.pointerId); splitter.classList.remove('dragging');
    try { localStorage.setItem('judgebox-pane-width',String(percent)); } catch {}
  };
  splitter.addEventListener('pointerup',finish); splitter.addEventListener('pointercancel',finish);
  splitter.addEventListener('keydown', event => {
    if (!['ArrowLeft','ArrowRight','Home'].includes(event.key)) return;
    event.preventDefault(); apply(event.key === 'Home' ? 40 : percent + (event.key === 'ArrowLeft' ? -2 : 2));
    try { localStorage.setItem('judgebox-pane-width',String(percent)); } catch {}
  });
  splitter.addEventListener('dblclick',() => { apply(40); try { localStorage.setItem('judgebox-pane-width','40'); } catch {} });
}
function setupKeybinding() {
  let saved = 'vscode'; try { saved = localStorage.getItem('judgebox-keybinding') || 'vscode'; } catch {}
  $('keybinding').value = saved === 'vim' ? 'vim' : 'vscode'; $('vimMode').hidden = saved !== 'vim';
  $('keybinding').onchange = () => {
    const value = $('keybinding').value; window.JudgeEditor?.setKeybinding(value); $('vimMode').hidden = value !== 'vim';
    try { localStorage.setItem('judgebox-keybinding',value); } catch {}
  };
  document.addEventListener('judgebox-save',() => saveDraft().catch(e => notice(e.message)));
}
async function init() {
  setupSplitter(); setupKeybinding();
  $('source').value = ''; $('reference').value = ''; $('generatorSource').value = pythonExample; preset(); renderCases(); mountEditor(); syncSource();
  try {
    const config = await api('/api/config'); tools = config.tools; renderTools(); $('dataDirectory').textContent = '数据目录：'+config.dataDirectory;
    const saved = await api('/api/draft'); applyDraft(saved); loaded = true; $('connectionState').textContent = '本地引擎就绪';
    const status = await api('/api/status'); if (status.verdict !== 'READY') { renderResult(status); setRunning(!status.done); if (!status.done) await poll(); else if (status.cases.length) await showDetail(status.cases[0].index); }
  } catch(e) { $('connectionState').textContent = '连接失败'; notice(e.message); }
}
init();
