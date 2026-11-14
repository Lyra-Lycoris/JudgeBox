'use strict';
// 做题页底部面板：「自测」（自己给输入 / 期望输出，走与提交相同的 driver 组装与 checker）+「提交结果」。
(() => {
const PB = window.PB = window.PB || {};
const byId = id => document.getElementById(id);
const el = (...a) => PB.el(...a);
const MAX_TESTS = 10;
let problem = null, tests = [], running = false, lastCompile = null;

const storeKey = id => `judgebox-selftest-${id}`;
const norm = text => String(text || '').replace(/\r\n?/g, '\n');
function save() { if (problem) PB.store.set(storeKey(problem.id), JSON.stringify(tests.map(t => ({input: t.input, expected: t.expected})))); }
function fromSamples() { return (problem?.samples || []).map(s => ({input: norm(s.input), expected: norm(s.output), result: null})); }

// ---- 底部面板（标签切换、收起、拖动高度） ----
PB.dock = {
  show(tab, open = true) {
    const dock = byId('pbDock');
    dock.dataset.tab = tab;
    document.querySelectorAll('#pbDock [role=tab]').forEach(b => { const on = b.dataset.tab === tab; b.setAttribute('aria-selected', String(on)); b.tabIndex = on ? 0 : -1; });
    byId('pbSelfTest').hidden = tab !== 'test';
    byId('pbResult').hidden = tab !== 'result';
    if (open) setOpen(true);
    PB.problemView?.relayout();
  },
  setResultBadge(verdict) {
    const badge = byId('pbDockResultBadge');
    badge.hidden = !verdict; badge.textContent = verdict || ''; badge.dataset.verdict = verdict || '';
  }
};
function setOpen(open) {
  const dock = byId('pbDock');
  dock.dataset.open = String(open);
  byId('pbDockToggle').setAttribute('aria-expanded', String(open));
  byId('pbDockToggle').setAttribute('aria-label', open ? '收起底部面板' : '展开底部面板');
  PB.store.set('judgebox-problem-dock-open', open ? '1' : '0');
  PB.problemView?.relayout();
}
function setupResize() {
  const handle = byId('pbDockHandle'), pane = document.querySelector('.pb-code-pane'), dock = byId('pbDock'), KEY = 'judgebox-problem-dock';
  let ratio = Math.min(.75, Math.max(.2, Number(PB.store.get(KEY)) || .42));
  const apply = v => { ratio = Math.min(.75, Math.max(.2, v)); pane.style.setProperty('--pb-dock', `${(ratio * 100).toFixed(1)}%`); handle.setAttribute('aria-valuenow', String(Math.round(ratio * 100))); };
  apply(ratio);
  handle.addEventListener('pointerdown', e => { if (dock.dataset.open !== 'true') return; handle.setPointerCapture(e.pointerId); handle.classList.add('dragging'); e.preventDefault(); });
  handle.addEventListener('pointermove', e => {
    if (!handle.hasPointerCapture(e.pointerId)) return;
    const r = pane.getBoundingClientRect(); apply((r.bottom - e.clientY) / r.height);
  });
  const end = e => { if (!handle.hasPointerCapture(e.pointerId)) return; handle.releasePointerCapture(e.pointerId); handle.classList.remove('dragging'); PB.store.set(KEY, String(ratio)); PB.problemView?.relayout(); };
  handle.addEventListener('pointerup', end); handle.addEventListener('pointercancel', end);
  handle.addEventListener('keydown', e => {
    if (e.key === 'ArrowUp') apply(ratio + .04); else if (e.key === 'ArrowDown') apply(ratio - .04); else return;
    e.preventDefault(); PB.store.set(KEY, String(ratio)); PB.problemView?.relayout();
  });
  handle.addEventListener('dblclick', () => { apply(.42); PB.store.set(KEY, '0.42'); PB.problemView?.relayout(); });
}

// ---- 自测用例 ----
function verdictLabel(v) { return v === 'OK' ? '已运行' : v; }
function field(label, value, placeholder, onInput) {
  const wrap = el('label', 'pb-st-field');
  const head = el('span', 'pb-st-field-head', label);
  const area = el('textarea', 'pb-st-text'); area.value = value; area.placeholder = placeholder;
  area.spellcheck = false; area.wrap = 'off'; area.setAttribute('autocapitalize', 'off');
  area.addEventListener('input', () => onInput(area.value));
  wrap.append(head, area);
  return wrap;
}
function outputPane(result) {
  const wrap = el('div', 'pb-st-field pb-st-output');
  const head = el('span', 'pb-st-field-head', '实际输出');
  wrap.append(head);
  if (!result) { wrap.append(el('div', 'pb-st-placeholder', '运行后显示程序输出')); return wrap; }
  const text = norm(result.stdout);
  const copy = el('button', 'pb-copy', '复制'); copy.type = 'button'; copy.setAttribute('aria-label', '复制实际输出'); copy.onclick = () => PB.copy(text, copy);
  head.append(copy);
  const pre = el('pre', 'pb-st-pre', text || '（无输出）'); pre.tabIndex = 0; if (!text) pre.classList.add('pb-st-empty');
  wrap.append(pre);
  if (result.stdoutTruncated) wrap.append(el('p', 'pb-st-note', '输出超过 64 KB，只显示前一部分。'));
  if (result.stderr) { const d = el('details', 'pb-st-stderr'); d.append(el('summary', '', 'stderr'), el('pre', 'pb-st-pre', norm(result.stderr))); wrap.append(d); }
  return wrap;
}
function card(test, i) {
  const c = el('section', 'pb-st-case'); c.setAttribute('aria-label', `自测用例 ${i + 1}`);
  if (test.result) c.dataset.verdict = test.result.verdict;
  const head = el('div', 'pb-st-case-head');
  head.append(el('span', 'pb-st-index', `#${i + 1}`));
  if (test.result) {
    const b = PB.verdictBadge(test.result.verdict); b.textContent = verdictLabel(test.result.verdict);
    if (test.result.verdict === 'OK') b.dataset.verdict = 'RUN';
    head.append(b, el('span', 'pb-st-metric', `${Math.round(test.result.timeMs)} ms`), el('span', 'pb-st-metric', `${(test.result.memoryBytes / 1048576).toFixed(1)} MiB`));
  } else head.append(el('span', 'pb-st-metric pb-muted', test.expected.trim() ? '将按本题 checker 比较' : '只看输出'));
  const remove = el('button', 'pb-st-remove', '✕'); remove.type = 'button'; remove.setAttribute('aria-label', `删除自测用例 ${i + 1}`);
  remove.onclick = () => { tests.splice(i, 1); save(); render(); };
  head.append(remove);
  const grid = el('div', 'pb-st-grid');
  grid.append(
    field('输入', test.input, problem?.judgeMode === 'function' ? '完整 stdin，首行是用例数（通常写 1）' : '程序的 stdin', v => { test.input = v; save(); }),
    field('期望输出（可选）', test.expected, '留空则只运行不比较；填写后用本题 checker 判定', v => { test.expected = v; save(); }),
    outputPane(test.result));
  c.append(head, grid);
  if (test.result?.message) c.append(el('p', 'pb-st-message', test.result.message));
  return c;
}
function render() {
  const panel = byId('pbSelfTestBody');
  const parts = [];
  if (lastCompile && !lastCompile.ok) {
    const box = el('div', 'pb-st-compile');
    const top = el('div', 'pb-st-compile-head');
    const b = PB.verdictBadge(lastCompile.verdict || 'CE'); top.append(b, el('strong', '', '编译失败'), el('span', 'pb-muted', lastCompile.message || ''));
    const copy = el('button', 'pb-copy', '复制'); copy.type = 'button'; copy.onclick = () => PB.copy(lastCompile.log || '', copy); top.append(copy);
    box.append(top);
    const pkg = PB.cangjiePackage?.(problem);
    if (pkg && /package/i.test(lastCompile.log || '')) box.append(el('p', 'pb-result-hint', `提示：本题仓颉代码的包名必须是 package ${pkg}。`));
    const pre = el('pre', 'pb-log', lastCompile.log || '（编译器没有输出）'); pre.tabIndex = 0; box.append(pre);
    parts.push(box);
  }
  if (!tests.length) {
    const empty = el('div', 'pb-st-blank');
    empty.append(el('p', '', '还没有自测用例。'), el('p', 'pb-muted', '点「新建」自己写输入，或「导入样例」从题面样例开始。'));
    parts.push(empty);
  }
  tests.forEach((t, i) => parts.push(card(t, i)));
  panel.replaceChildren(...parts);
  byId('pbSelfTestCount').textContent = tests.length ? String(tests.length) : '';
  byId('pbSelfAdd').disabled = tests.length >= MAX_TESTS;
  byId('pbSelfRun').disabled = running || !tests.length || !problem;
}
function setStatus(text, tone) { const s = byId('pbSelfStatus'); s.textContent = text || ''; s.dataset.tone = tone || ''; }

async function run() {
  if (running || !problem) return;
  const ctx = PB.problemView?.context();
  if (!ctx) return;
  if (ctx.judging) { setStatus('正在判题，提交结束后再自测', 'warn'); return; }
  if (!ctx.source.trim()) { setStatus('代码为空', 'warn'); return; }
  if (!tests.length) { tests.push({input: '', expected: '', result: null}); render(); }
  PB.dock.show('test');
  running = true; byId('pbSelfRun').disabled = true; byId('pbSelfRunLabel').textContent = '运行中…';
  byId('pbSelfTest').setAttribute('aria-busy', 'true');
  setStatus(`编译并运行 ${tests.length} 组…`, 'busy');
  const started = performance.now();
  try {
    const r = await PB.api(`/api/problems/${encodeURIComponent(problem.id)}/run`, {body: {language: ctx.language, source: ctx.source, tests: tests.map(t => ({input: t.input, expected: t.expected}))}});
    lastCompile = r.compile;
    const results = r.results || [];
    tests.forEach((t, i) => { t.result = results[i] || null; });
    const secs = ((performance.now() - started) / 1000).toFixed(1);
    if (!r.compile.ok) setStatus(`编译失败 · ${secs} s`, 'bad');
    else {
      const judged = results.filter(x => x.verdict !== 'OK'), passed = results.filter(x => x.verdict === 'AC').length;
      const bad = results.filter(x => !['AC', 'OK'].includes(x.verdict)).length;
      const compile = r.compile.cached ? '复用上次编译' : `编译 ${(r.compile.ms / 1000).toFixed(1)} s`;
      setStatus(`${judged.length ? `通过 ${passed} / ${judged.length}` : `运行 ${results.length} 组`} · ${compile} · 共 ${secs} s`, bad ? 'bad' : 'good');
    }
  } catch (e) {
    setStatus(e.message, 'bad');
  } finally {
    running = false; byId('pbSelfRunLabel').textContent = '运行自测';
    byId('pbSelfTest').setAttribute('aria-busy', 'false');
    render();
  }
}

PB.selfTest = {
  load(p) {
    problem = p; lastCompile = null; setStatus('');
    let saved = null; try { saved = JSON.parse(PB.store.get(storeKey(p.id)) || 'null'); } catch {}
    tests = Array.isArray(saved) ? saved.slice(0, MAX_TESTS).map(t => ({input: String(t.input || ''), expected: String(t.expected || ''), result: null})) : fromSamples().slice(0, MAX_TESTS);
    const hint = byId('pbSelfHint');
    const pkg = PB.cangjiePackage?.(p);
    hint.textContent = p.judgeMode === 'function'
      ? `与提交相同：你的 solve 会和题目自带的 driver 一起编译。输入写 driver 读的完整 stdin（首行是用例数）。${pkg ? `仓颉包名 package ${pkg}。` : ''}`
      : '输入就是程序的 stdin。';
    render();
  },
  run,
  isRunning: () => running
};

document.addEventListener('DOMContentLoaded', () => {
  setupResize();
  setOpen(PB.store.get('judgebox-problem-dock-open') !== '0');
  document.querySelectorAll('#pbDock [role=tab]').forEach(b => {
    b.onclick = () => { if (byId('pbDock').dataset.tab === b.dataset.tab && byId('pbDock').dataset.open === 'true') setOpen(false); else PB.dock.show(b.dataset.tab); };
    b.onkeydown = e => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      const tabs = [...document.querySelectorAll('#pbDock [role=tab]')], next = tabs[(tabs.indexOf(b) + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      PB.dock.show(next.dataset.tab); next.focus(); e.preventDefault();
    };
  });
  byId('pbDockToggle').onclick = () => setOpen(byId('pbDock').dataset.open !== 'true');
  byId('pbSelfRun').onclick = run;
  byId('pbSelfAdd').onclick = () => {
    if (tests.length >= MAX_TESTS) return;
    tests.push({input: problem?.judgeMode === 'function' ? '1\n' : '', expected: '', result: null}); save(); render();
    PB.dock.show('test');
    const areas = byId('pbSelfTestBody').querySelectorAll('.pb-st-case:last-child textarea');
    areas[0]?.focus(); areas[0]?.setSelectionRange(areas[0].value.length, areas[0].value.length);
  };
  byId('pbSelfSamples').onclick = () => {
    const have = new Set(tests.map(t => norm(t.input).trim()));
    const add = fromSamples().filter(s => !have.has(s.input.trim()));
    tests.push(...add.slice(0, MAX_TESTS - tests.length)); save(); render();
    setStatus(add.length ? `已导入 ${Math.min(add.length, MAX_TESTS)} 个样例` : '样例都已经在列表里了', '');
  };
  byId('pbSelfClear').onclick = () => { if (!tests.length || !confirm('清空全部自测用例？')) return; tests = []; lastCompile = null; save(); render(); setStatus(''); };
});
})();
