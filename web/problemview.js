'use strict';
// 做题页：题面 + 独立编辑器实例 + 草稿 + 提交/轮询 + 揭榜 + 结果面板。
(() => {
const PB = window.PB = window.PB || {};
const byId = id => document.getElementById(id);
const el = (...a) => PB.el(...a);
const ACTIVE_KEY = 'judgebox-pb-active';   // sessionStorage：{problemId, submissionId}，刷新后据此恢复判题
// 完整程序模式的初始骨架（函数式模式用题包里的 starter.*）。
const fullTemplates = {
  cpp: '#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n\n    return 0;\n}\n',
  cangjie: 'main(): Int64 {\n    return 0\n}\n',
  python: 'import sys\n\n\ndef main():\n    data = sys.stdin.buffer.read().split()\n\n\nmain()\n',
  java: 'import java.util.*;\nimport java.io.*;\n\npublic class Main {\n    public static void main(String[] args) throws Exception {\n        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n    }\n}\n'
};
const fileNames = {
  function: {cpp: 'solve.cpp', cangjie: 'solve.cj', python: 'solve.py', java: 'solve.java'},
  full: {cpp: 'main.cpp', cangjie: 'main.cj', python: 'main.py', java: 'Main.java'}
};
// 评判方式与题目来源：卡片上的中文名。
const judgeNames = {standard: '普通裁判', special: '特殊裁判', interactive: '交互裁判', function: '函数裁判'};
const sourceNames = {luogu: '洛谷', leetcode: '力扣', codeforces: 'Codeforces', other: '自建'};
let problem = null, language = 'cpp', mode = 'function', editor = null, statementLang = PB.store.get('judgebox-statement-lang') === 'en' ? 'en' : 'zh';
let judging = false, pollTimer = null, saveTimer = null, recordTimer = null, opening = null, lastResult = null;

const draftKey = (id, lang, kind) => `judgebox-draft-${id}-${lang}-${kind}`;
const modesFor = lang => (problem?.modes?.[lang] || []);
const fileName = () => fileNames[mode]?.[language] || 'solve.cpp';
const initialCode = () => {
  if (mode === 'function') return (problem?.starter && problem.starter[language]) || '';
  return fullTemplates[language] || '';
};
const readActive = () => { try { return JSON.parse(sessionStorage.getItem(ACTIVE_KEY) || 'null'); } catch { return null; } };

// ---- 诊断：函数式提交只有函数体，按语言补一个能编译的外壳；行号映射回选手代码 ----
function lintSource(code, lang) {
  const wrap = (prefix, suffix) => {
    const lines = code.split('\n'), offset = prefix.length;
    return {source: [...prefix, ...lines, ...suffix].join('\n'),
      map: line => line > offset && line <= offset + lines.length ? line - offset : null};
  };
  if (mode !== 'function') return {source: code, map: line => line};
  if (lang === 'java') return wrap(['import java.util.*;', 'import java.io.*;', 'import java.math.*;', '', 'public class Main {'], ['}']);
  if (lang === 'cangjie') {
    const pkg = problem?.package || '';
    const hasPackage = /^\s*package\s/m.test(code);
    const prefix = pkg && !hasPackage ? [`package ${pkg}`, ''] : [];
    return wrap(prefix, ['', 'main(): Unit {}']);
  }
  return {source: code, map: line => line};
}
async function lint(code, lang) {
  const state = byId('pbDiagnostic');
  if (!code.trim()) return showDiagnostics({diagnostics: []}, '', state);
  try {
    const {source, map} = lintSource(code, lang);
    const result = await PB.api('/api/diagnostics', {body: {source, language: lang}});
    const items = (result.diagnostics || []).map(d => {
      const line = map(Number(d.line) || 1); if (line === null) return null;
      const endLine = d.endLine ? map(Number(d.endLine)) ?? line : undefined;
      return {...d, line, endLine};
    }).filter(Boolean);
    return showDiagnostics({...result, diagnostics: items}, code, state);
  } catch (e) { return showDiagnostics({diagnostics: [], status: e.message || String(e)}, code, state); }
}
function mountEditor() {
  if (editor || !window.JudgeEditor) return;
  editor = window.JudgeEditor.mount(byId('pbSource'), {
    getLanguage: () => language,
    lint,
    placeholder: '在这里实现 solve',
    label: '题解代码'
  });
}
function setCode(text) { byId('pbSource').value = text; editor?.pull(); updateCounts(); }
function updateCounts() { byId('pbChars').textContent = `${byId('pbSource').value.length} 字符`; }
function saveDraft() {
  if (!problem) return;
  const value = byId('pbSource').value;
  const key = draftKey(problem.id, language, mode);
  if (value === initialCode()) PB.store.remove(key); else PB.store.set(key, value);
  byId('pbSaved').textContent = '已保存'; byId('pbSaved').dataset.state = 'saved';
  scheduleRecordSave(1400, language, mode);
}
// 做题代码同时落到 solveRecord/<专题>/<题目>/<语言>/<方式>/，方便平时整理。
function setRecordState(text, state) {
  const node = byId('pbRecordState');
  if (!node) return;
  node.textContent = text || ''; node.dataset.state = state || '';
}
function scheduleRecordSave(delay = 1400, lang = language, kind = mode) {
  if (!problem) return;
  clearTimeout(recordTimer);
  const target = problem.id, sourceText = () => byId('pbSource').value;
  recordTimer = setTimeout(async () => {
    const source = sourceText();
    if (!source.trim()) return;
    try {
      await PB.api('/api/record/save', {body: {problemId: target, language: lang, mode: kind, source}});
      if (problem?.id === target) setRecordState(`已存入 solveRecord · ${PB.modeNames[kind] || kind}`, 'saved');
    } catch (e) { if (e.status !== 403) setRecordState('solveRecord 保存失败：' + e.message, 'error'); }
  }, delay);
}
// 语言与提交方式两个下拉框联动：切语言时如果当前方式不支持，就落到该语言支持的第一种。
function syncSelectors() {
  const modes = modesFor(language);
  if (!modes.includes(mode)) mode = modes[0] || 'full';
  const modeSelect = byId('pbMode');
  modeSelect.replaceChildren(...modes.map(m => { const o = el('option', '', PB.modeNames[m] || m); o.value = m; return o; }));
  modeSelect.value = mode;
  modeSelect.disabled = judging || modes.length <= 1;
  byId('pbLanguage').value = language;
}
function loadDraft() {
  syncSelectors();
  const draft = PB.store.get(draftKey(problem.id, language, mode));
  setCode(draft ?? initialCode());
  byId('pbFileName').textContent = fileName();
  byId('pbLangLabel').textContent = `${PB.languageNames[language] || language} · ${PB.modeNames[mode] || mode}`;
  if (problem) renderJudgeCard();
  const pkg = language === 'cangjie' && mode === 'function' ? PB.cangjiePackage(problem) : '';
  byId('pbPackage').hidden = !pkg; byId('pbPackage').textContent = pkg ? `package ${pkg}` : '';
  byId('pbPackage').title = pkg ? `仓颉提交首行必须是 package ${pkg}` : '';
  editor?.setLanguage(language);
  if (editor) byId('pbSource').placeholder = mode === 'function' ? '在这里实现 solve' : '完整程序';
  PB.selfTest?.render?.();
}
function switchLanguage(lang) {
  if (lang === language && byId('pbFileName').textContent === fileName()) return;
  clearTimeout(saveTimer); saveDraft();
  language = lang; PB.store.set('judgebox-problem-lang', lang);
  const modes = modesFor(language);
  if (!modes.includes(mode)) mode = modes[0] || 'full';
  PB.store.set('judgebox-problem-mode', mode);
  loadDraft();
}
function switchMode(kind) {
  if (kind === mode) return;
  clearTimeout(saveTimer); saveDraft();
  mode = kind; PB.store.set('judgebox-problem-mode', mode);
  loadDraft();
}

// 裁判方式跟随「提交方式」：完整程序 → 普通裁判，函数式 → 函数裁判；
// 题目本身声明为特殊 / 交互裁判时保持原样。
function judgeKind() {
  const declared = problem?.judgeType || 'standard';
  if (declared === 'special' || declared === 'interactive') return declared;
  return mode === 'function' ? 'function' : 'standard';
}
function renderJudgeCard() {
  const judge = judgeKind();
  const judgeCard = byId('pbJudgeType').closest('.pb-fact');
  judgeCard.dataset.type = judge;
  judgeCard.title = {standard: '逐 token 比较选手输出与标准答案', special: '题目自带 checker（SPJ）判定',
    interactive: '交互裁判：选手程序与交互器通讯', function: '选手只实现函数，平台用题目 driver 拼接'}[judge] || '';
  byId('pbJudgeType').textContent = judgeNames[judge] || judge;
}

// ---- 视图 ----
function renderHeader() {
  byId('pbTitle').textContent = problem.title?.[statementLang] || problem.title?.zh || problem.id;
  byId('pbDiff').replaceWith(Object.assign(PB.diffBadge(problem.difficulty), {id: 'pbDiff'}));
  byId('pbTopic').textContent = problem.topic || '';
  // 时间 / 内存 / 评判方式 / 来源：四张独立卡片
  const limits = problem.limits || {};
  byId('pbTimeLimit').textContent = `${limits.timeMs || '—'} ms`;
  byId('pbMemoryLimit').textContent = `${limits.memoryMb || '—'} MiB`;
  renderJudgeCard();
  const src = problem.source || {};
  const srcCard = byId('pbSourceCard').closest('.pb-fact');
  const link = byId('pbSourceCard');
  if (src.platform) {
    srcCard.dataset.platform = src.platform;
    link.textContent = `${sourceNames[src.platform] || src.platform}${src.id ? ' · ' + src.id : ''}`;
    link.title = src.url || link.textContent;
    if (src.url) { link.href = src.url; link.removeAttribute('aria-disabled'); }
    else { link.removeAttribute('href'); }
  } else {
    delete srcCard.dataset.platform;
    link.textContent = problem.selfJudge ? '自建题目 · 自判' : '自建题目';
    link.removeAttribute('href');
    link.title = problem.selfJudge ? '只有测试数据，由你自己的程序对比输入输出' : '';
  }
  const select = byId('pbLanguage');
  const langs = (problem.judgedLanguages || []).filter(l => PB.languageNames[l]);
  select.replaceChildren(...langs.map(l => { const o = el('option', '', PB.languageNames[l]); o.value = l; return o; }));
  const preferred = PB.store.get('judgebox-problem-lang');
  language = langs.includes(preferred) ? preferred : langs[0] || 'cpp';
  const preferredMode = PB.store.get('judgebox-problem-mode');
  const modes = modesFor(language);
  mode = modes.includes(preferredMode) ? preferredMode : (modes[0] || 'full');
  select.value = language;
  renderJudgeCard();
  renderBest();
}
function renderBest() {
  byId('pbBest').textContent = problem?.bestScore == null ? 'best —' : `best ${problem.bestScore}/${problem.totalPoints || 100}`;
}
function renderStatement() {
  document.querySelectorAll('.pb-segment [data-lang]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.lang === statementLang)));
  const pane = document.querySelector('.pb-statement-pane');
  PB.showStatement(byId('pbStatement'), pane, problem, statementLang);
  byId('pbTitle').textContent = problem.title?.[statementLang] || problem.title?.zh || problem.id;
}
function showPane(name) {
  byId('pbBody').dataset.pane = name;
  document.querySelectorAll('.pb-mobile-tabs [data-pane]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.pane === name)));
  if (name === 'code') editor?.relayout();
}
function notFound(id, message) {
  problem = null;
  byId('pbTitle').textContent = '题目不存在';
  byId('pbTopic').textContent = '';
  byId('pbTimeLimit').textContent = '—'; byId('pbMemoryLimit').textContent = '—';
  byId('pbJudgeType').textContent = '—'; byId('pbSourceCard').textContent = '—';
  byId('pbSourceCard').removeAttribute('href');
  setRecordState('');
  const box = el('div', 'pb-not-found');
  box.append(el('p', '', message || `找不到题目 ${id}。`));
  const back = el('a', 'pb-btn', '← 返回题单'); back.href = '#/problems'; box.append(back);
  byId('pbStatement').replaceChildren(box);
  byId('pbSubmit').disabled = true;
}

async function open(id) {
  mountEditor();
  if (problem && problem.id === id) { editor?.relayout(); return; }
  if (opening === id) return;
  opening = id;
  clearTimeout(saveTimer); clearTimeout(recordTimer); if (problem) saveDraft();
  PB.history.close();
  byId('pbResult').replaceChildren(el('p', 'pb-st-blank pb-muted', '提交后在这里查看分组结果。')); lastResult = null;
  PB.dock.setResultBadge(''); PB.dock.show('test', false);
  byId('pbStatement').replaceChildren(el('p', 'pb-muted pb-loading', '加载题目…'));
  byId('pbTitle').textContent = '…';
  try {
    const detail = await PB.api('/api/problems/' + encodeURIComponent(id));
    if (opening !== id) return;
    problem = detail;
    byId('pbSubmit').disabled = judging;
    renderHeader(); renderStatement(); loadDraft(); PB.selfTest.load(problem); showPane(byId('pbBody').dataset.pane || 'statement');
    editor?.relayout();
    await resume();
  } catch (e) {
    if (opening === id) notFound(id, e.status === 404 ? `找不到题目 ${id}，可能已被删除。` : e.message);
  } finally { if (opening === id) opening = null; }
}
function leave() { clearTimeout(saveTimer); if (problem) saveDraft(); clearTimeout(recordTimer); if (problem) scheduleRecordSave(0); PB.history.close(); }

// ---- 提交与轮询 ----
function lock(on) {
  judging = on;
  byId('pbSubmit').disabled = on || !problem;
  byId('pbSubmitLabel').textContent = on ? '判题中' : '提交';
  byId('pbLanguage').disabled = on;
  byId('pbMode').disabled = on || modesFor(language).length <= 1;
  byId('pbReset').disabled = on;
  byId('pbSelfRun').disabled = on || PB.selfTest.isRunning();
  const box = byId('pbEditor'); box.inert = on; box.classList.toggle('pb-locked', on); box.setAttribute('aria-busy', String(on));
  byId('pbProgress').hidden = !on;
  if (!on) clearTimeout(pollTimer);
}
function renderProgress(s) {
  const total = s.total || 0, done = s.completed || 0;
  byId('pbProgressFill').style.transform = `scaleX(${total ? done / total : 0})`;
  byId('pbProgressText').textContent = s.phase || '判题中';
}
async function submit() {
  if (judging || !problem) return;
  clearTimeout(saveTimer); saveDraft();
  const source = byId('pbSource').value;
  if (!source.trim()) { PB.toast('代码为空。'); return; }
  clearTimeout(recordTimer); scheduleRecordSave(0);
  lock(true); renderProgress({phase: '提交中'});
  try {
    const r = await PB.api('/api/submit', {body: {problemId: problem.id, language, mode, source}});
    sessionStorage.setItem(ACTIVE_KEY, JSON.stringify({problemId: problem.id, submissionId: r.submissionId}));
    poll(r.submissionId, problem.id, true);
  } catch (e) {
    lock(false);
    PB.toast(e.status === 409 ? `${e.message}（调试台或另一次提交正在运行，请稍后再试）` : e.message);
  }
}
function poll(submissionId, problemId, animate) {
  clearTimeout(pollTimer);
  const tick = async () => {
    let s;
    try { s = await PB.api('/api/submit/status'); }
    catch (e) { if (e.status === 403) { lock(false); return; } pollTimer = setTimeout(tick, 1000); return; }
    if (!problem || problem.id !== problemId) { pollTimer = setTimeout(tick, 250); return; }
    if (s.submissionId && s.submissionId !== submissionId) { lock(false); sessionStorage.removeItem(ACTIVE_KEY); return; }
    renderProgress(s);
    if (!s.done) { pollTimer = setTimeout(tick, 250); return; }
    await finish(s, animate);
  };
  tick();
}
async function finish(s, animate) {
  sessionStorage.removeItem(ACTIVE_KEY);
  byId('pbProgress').hidden = true;
  if (animate && document.body.dataset.view === 'problem') {
    await PB.reveal(s, {title: problem.title?.[statementLang] || problem.title?.zh || problem.id, returnFocus: byId('pbSubmit')});
  }
  lock(false);
  renderResult(s);
  if (problem.bestScore == null || s.score > problem.bestScore) problem.bestScore = s.score;
  renderBest();
  PB.history.refresh();
  if (animate) byId('pbSubmit').focus({preventScroll: true});
}
async function resume() {
  const active = readActive();
  if (!active || active.problemId !== problem.id) return;
  let s; try { s = await PB.api('/api/submit/status'); } catch { return; }
  if (s.submissionId !== active.submissionId) { sessionStorage.removeItem(ACTIVE_KEY); return; }
  if (!s.done) { lock(true); renderProgress(s); poll(active.submissionId, problem.id, true); }
  else await finish(s, false);   // 刷新前已判完：直接给结果，不再播动画
}
async function refreshBest() {
  if (!problem) return;
  try { const d = await PB.api('/api/problems/' + encodeURIComponent(problem.id)); problem.bestScore = d.bestScore; renderBest(); } catch {}
}

// ---- 结果面板 ----
function fmtMs(v) { const n = Number(v); return Number.isFinite(n) ? `${Math.round(n)} ms` : '—'; }
function fmtMem(v) { const n = Number(v); return Number.isFinite(n) && n > 0 ? `${(n / 1048576).toFixed(1)} MiB` : '—'; }
function renderResult(s) {
  lastResult = s;
  const box = byId('pbResult');
  PB.dock.show('result'); PB.dock.setResultBadge(s.verdict);
  const score = Number(s.score) || 0, prev = s.previousBest ?? null;
  const head = el('div', 'pb-result-head');
  const big = el('div', 'pb-result-score'); big.setAttribute('aria-live', 'polite');
  const num = el('strong', '', score); num.id = 'pbResultScore';
  big.append(num, el('span', '', '/100'));
  const meta = el('div', 'pb-result-meta');
  const cases = s.cases || [];
  const maxTime = cases.reduce((m, c) => Math.max(m, Number(c.timeMs) || 0), 0);
  meta.append(PB.verdictBadge(s.verdict), el('span', 'pb-muted', Number.isFinite(s.durationMs) ? `用时 ${(s.durationMs / 1000).toFixed(1)} s` : cases.length ? `最慢 ${fmtMs(maxTime)}` : ''));
  head.append(big, meta);
  const delta = prev === null ? null : score - prev;
  const compare = el('p', 'pb-result-compare', prev === null ? `本次 ${score} · 首次提交` : `本次 ${score} · 历史最佳 ${prev} · ${delta > 0 ? '+' + delta : delta < 0 ? '−' + (-delta) : '±0'}`);
  compare.dataset.tone = delta === null ? 'first' : delta > 0 ? 'up' : delta < 0 ? 'down' : 'flat';
  const parts = [head, compare];
  if (s.verdict === 'JE') { const alert = el('div', 'pb-result-alert'); alert.append(el('strong', '', '判题设施错误'), el('pre', 'pb-log', s.message || '未知错误')); parts.push(alert); }
  else if (s.message) parts.push(el('p', 'pb-result-message', s.message));
  const pkg = PB.cangjiePackage(problem);
  if (s.verdict === 'CE' && pkg && /more than one package declaration|package name/i.test(s.compileLog || '')) {
    parts.push(el('p', 'pb-result-hint', `提示：本题仓颉代码的包名必须是 package ${pkg}，请检查第一行。`));
  }
  if (s.compileLog) { const d = el('details', 'pb-compile'); d.open = s.verdict === 'CE'; const pre = el('pre', 'pb-log', s.compileLog); pre.tabIndex = 0; const copy = el('button', 'pb-copy', '复制'); copy.type = 'button'; copy.onclick = () => PB.copy(s.compileLog, copy); d.append(el('summary', '', '编译日志'), copy, pre); parts.push(d); }
  const groupsMeta = new Map((problem?.groups || []).map(g => [g.name, g]));
  const table = el('div', 'pb-group-table'); table.setAttribute('role', 'table'); table.setAttribute('aria-label', '分组结果');
  const hr = el('div', 'pb-group-row pb-group-header'); hr.setAttribute('role', 'row');
  ['组名', '分值', '得分', '用例', '状态'].forEach(t => { const c = el('span', '', t); c.setAttribute('role', 'columnheader'); hr.append(c); });
  table.append(hr);
  (s.groups || []).forEach(g => {
    const gc = cases.filter(c => c.group === g.name), passed = gc.filter(c => c.verdict === 'AC').length;
    const totalCases = groupsMeta.get(g.name)?.caseCount ?? gc.length;
    const r = el('button', 'pb-group-row'); r.type = 'button'; r.setAttribute('aria-expanded', 'false'); r.dataset.state = g.state;
    const stateText = {passed: '通过', failed: '未通过', pending: '未评测', running: '评测中'}[g.state] || g.state;
    r.append(el('span', 'pb-group-name', g.name), el('span', '', g.points), el('span', 'pb-mono', g.earned ?? 0), el('span', 'pb-mono', `${passed}/${totalCases}`));
    const chip = el('span', 'pb-state-chip', stateText); chip.dataset.state = g.state; r.append(chip);
    const list = el('div', 'pb-case-list'); list.hidden = true;
    gc.forEach(c => {
      const row = el('div', 'pb-case-row');
      const msg = el('button', 'pb-case-msg', c.message || ''); msg.type = 'button'; msg.title = c.message || ''; msg.disabled = !c.message;
      msg.onclick = () => msg.classList.toggle('pb-expanded');
      row.append(el('span', 'pb-mono', c.caseId), PB.verdictBadge(c.verdict), el('span', 'pb-mono pb-muted', fmtMs(c.timeMs)), el('span', 'pb-mono pb-muted', fmtMem(c.memoryBytes)), msg);
      list.append(row);
    });
    if (totalCases > gc.length) list.append(el('p', 'pb-muted pb-case-skip', `其余 ${totalCases - gc.length} 个用例未评测（组内首错即跳过）`));
    r.onclick = () => { list.hidden = !list.hidden; r.setAttribute('aria-expanded', String(!list.hidden)); };
    table.append(r, list);
  });
  parts.push(table);
  const actions = el('div', 'pb-result-actions');
  const again = el('button', 'pb-btn pb-btn-primary', '重新提交'); again.type = 'button'; again.onclick = submit;
  const hist = el('button', 'pb-btn', '查看历史'); hist.type = 'button'; hist.onclick = () => PB.history.open(problem.id, hist);
  actions.append(again, hist);
  parts.push(actions);
  box.replaceChildren(...parts);
  editor?.relayout();
}

// ---- 分隔条（独立 key，不影响调试页） ----
function setupSplitter() {
  const splitter = byId('pbSplitter'), body = byId('pbBody'), KEY = 'judgebox-problem-split';
  let percent = Math.min(75, Math.max(25, Number(PB.store.get(KEY)) || 46));
  const apply = v => { percent = Math.min(75, Math.max(25, v)); body.style.setProperty('--split', `${percent}%`); splitter.setAttribute('aria-valuenow', String(Math.round(percent))); };
  const persist = () => PB.store.set(KEY, String(percent));
  apply(percent);
  splitter.addEventListener('pointerdown', e => { splitter.setPointerCapture(e.pointerId); splitter.classList.add('dragging'); e.preventDefault(); });
  splitter.addEventListener('pointermove', e => {
    if (!splitter.hasPointerCapture(e.pointerId)) return;
    const r = body.getBoundingClientRect(); apply((e.clientX - r.left) / r.width * 100);
  });
  const end = e => { if (!splitter.hasPointerCapture(e.pointerId)) return; splitter.releasePointerCapture(e.pointerId); splitter.classList.remove('dragging'); persist(); editor?.relayout(); };
  splitter.addEventListener('pointerup', end); splitter.addEventListener('pointercancel', end);
  splitter.addEventListener('keydown', e => {
    const step = e.shiftKey ? 5 : 2;
    if (e.key === 'ArrowLeft') apply(percent - step); else if (e.key === 'ArrowRight') apply(percent + step);
    else if (e.key === 'Home') apply(25); else if (e.key === 'End') apply(75); else return;
    e.preventDefault(); persist();
  });
  splitter.addEventListener('dblclick', () => { apply(46); persist(); editor?.relayout(); });
}

PB.problemView = {open, leave, refreshBest, submit,
  relayout: () => editor?.relayout(),
  recordSave: () => { clearTimeout(recordTimer); return scheduleRecordSave(0); },
  context: () => problem ? {language, mode, source: byId('pbSource').value, judging, problem} : null};
PB.forgetProblem = id => { PB.forgetStatement?.(id); if (problem?.id === id) problem = null; };

document.addEventListener('DOMContentLoaded', () => {
  setupSplitter();
  byId('pbSource').addEventListener('input', () => {
    updateCounts(); byId('pbSaved').textContent = '保存中…'; byId('pbSaved').dataset.state = 'saving';
    clearTimeout(saveTimer); saveTimer = setTimeout(saveDraft, 400);
  });
  byId('pbLanguage').onchange = () => switchLanguage(byId('pbLanguage').value);
  byId('pbMode').onchange = () => switchMode(byId('pbMode').value);
  byId('pbReset').onclick = () => {
    if (!problem || !confirm('用初始代码覆盖当前草稿？')) return;
    PB.store.remove(draftKey(problem.id, language, mode)); setCode(initialCode()); saveDraft();
  };
  byId('pbSubmit').onclick = submit;
  byId('pbCancel').onclick = async () => { try { await PB.api('/api/cancel', {body: {}}); byId('pbProgressText').textContent = '正在取消…'; } catch (e) { PB.toast(e.message); } };
  byId('pbHistoryButton').onclick = () => { if (!problem) return; PB.history.isOpen() ? PB.history.close() : PB.history.open(problem.id, byId('pbHistoryButton')); };
  document.querySelectorAll('.pb-segment [data-lang]').forEach(b => b.onclick = () => {
    if (statementLang === b.dataset.lang || !problem) return;
    statementLang = b.dataset.lang; PB.store.set('judgebox-statement-lang', statementLang); renderStatement();
  });
  document.querySelectorAll('.pb-mobile-tabs [data-pane]').forEach(b => b.onclick = () => showPane(b.dataset.pane));
  // 捕获阶段拦下 Ctrl+Enter，避免 CodeMirror 插空行，也避免触发调试台的运行。
  window.addEventListener('keydown', e => {
    if (document.body.dataset.view !== 'problem' || document.querySelector('dialog[open], .pb-reveal')) return;
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); e.stopPropagation(); if (e.shiftKey) PB.selfTest.run(); else submit(); }
  }, true);
  window.addEventListener('beforeunload', () => { if (problem) saveDraft(); });
});
})();
