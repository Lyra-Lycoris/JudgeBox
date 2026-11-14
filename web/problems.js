'use strict';
// 题目系统公共层：API、错误条、路由，以及题单页（筛选 / 导入 / 删除）。
(() => {
const PB = window.PB = window.PB || {};
const byId = id => document.getElementById(id);

PB.el = (tag, className, text) => {
  const e = document.createElement(tag);
  if (className) e.className = className;
  if (text !== undefined && text !== null) e.textContent = String(text);
  return e;
};
PB.store = {
  get(key) { try { return localStorage.getItem(key); } catch { return null; } },
  set(key, value) { try { localStorage.setItem(key, value); } catch {} },
  remove(key) { try { localStorage.removeItem(key); } catch {} }
};
PB.languageNames = {cpp: 'C++ 20', cangjie: '仓颉'};
PB.diffColor = d => d < 1200 ? '#9ca3af' : d < 1400 ? '#4ccb7f' : d < 1600 ? '#22d3ee' : d < 1900 ? '#52a8ff'
  : d < 2200 ? '#a855f7' : d < 2500 ? '#f59e0b' : d < 3000 ? '#ef4444' : '#b91c1c';
PB.diffBadge = d => { const b = PB.el('span', 'pb-diff', d); b.style.setProperty('--pb-diff', PB.diffColor(Number(d))); b.title = `难度 ${d}`; return b; };
PB.verdictBadge = v => { const b = PB.el('span', 'verdict pb-verdict', v || '—'); b.dataset.verdict = v === 'RUNNING' ? 'RUN' : (v || ''); return b; };
PB.status = p => p.bestScore === null || p.bestScore === undefined ? 'todo' : p.bestScore >= (p.totalPoints || 100) ? 'solved' : 'tried';
PB.statusName = {todo: '未做', tried: '尝试过', solved: '已满分'};
PB.copy = async (text, button) => {
  try { await navigator.clipboard.writeText(text); }
  catch { const t = PB.el('textarea'); t.value = text; document.body.append(t); t.select(); document.execCommand('copy'); t.remove(); }
  if (!button) return;
  const label = button.dataset.label || button.textContent; button.dataset.label = label;
  button.textContent = '✓'; button.classList.add('pb-copied');
  clearTimeout(button._pbTimer); button._pbTimer = setTimeout(() => { button.textContent = label; button.classList.remove('pb-copied'); }, 1200);
};

// ---- 错误条：403 常驻；断线每 2 s 重试，恢复后自动消失 ----
let authFailed = false, retryTimer = null;
function banner(text) { const b = byId('pbBanner'); b.textContent = text || ''; b.hidden = !text; }
PB.authFailed = () => { authFailed = true; clearInterval(retryTimer); retryTimer = null; banner('会话已失效，请用启动窗口里的地址重新打开。'); };
function connectionLost() {
  if (authFailed || retryTimer) return;
  banner('与本地引擎的连接已断开，正在每 2 秒重试…');
  retryTimer = setInterval(async () => {
    try {
      const r = await fetch('/api/submit/status', {headers: {'X-JudgeBox-Token': PB.token()}});
      if (r.status === 403) return PB.authFailed();
      clearInterval(retryTimer); retryTimer = null; banner('');
      window.dispatchEvent(new CustomEvent('pb-reconnected'));
    } catch {}
  }, 2000);
}
window.addEventListener('judgebox-auth-failed', PB.authFailed);

class ApiError extends Error { constructor(message, status, data) { super(message); this.status = status; this.data = data; } }
PB.token = () => sessionStorage.getItem('judgebox-token') || '';
PB.api = async (path, {method, body, signal} = {}) => {
  const token = PB.token();
  if (!token) { PB.authFailed(); throw new ApiError('会话已失效，请用启动窗口里的地址重新打开。', 403); }
  const options = {method: method || (body === undefined ? 'GET' : 'POST'), headers: {'X-JudgeBox-Token': token}, signal};
  if (body !== undefined) { options.headers['Content-Type'] = 'application/json'; options.body = JSON.stringify(body); }
  let response;
  try { response = await fetch(path, options); }
  catch (e) { if (e.name === 'AbortError') throw e; connectionLost(); throw new ApiError('无法连接本地引擎。', 0); }
  let data = null; try { data = await response.json(); } catch {}
  if (response.status === 403) { PB.authFailed(); throw new ApiError('会话已失效，请用启动窗口里的地址重新打开。', 403, data); }
  if (!response.ok) throw new ApiError((data && data.error) || `请求失败：${response.status}`, response.status, data);
  if (!data) throw new ApiError('本地引擎没有返回有效响应。', response.status);
  return data;
};
PB.toast = message => { if (!authFailed && message) { banner(message); clearTimeout(PB._toast); PB._toast = setTimeout(() => { if (!authFailed && !retryTimer) banner(''); }, 5000); } };

// ---- 题单页 ----
const ranges = [
  {label: '≤1200', test: d => d <= 1200}, {label: '1200–1600', test: d => d > 1200 && d <= 1600},
  {label: '1600–2000', test: d => d > 1600 && d <= 2000}, {label: '2000–2500', test: d => d > 2000 && d < 2500},
  {label: '≥2500', test: d => d >= 2500}
];
const filters = {range: -1, tags: new Set(), status: 'all', query: ''};
let problems = [], loadedOnce = false, importAbort = null, openMenu = null;

function chip(label, pressed, onClick, extra) {
  const b = PB.el('button', 'pb-chip' + (extra ? ' ' + extra : ''), label);
  b.type = 'button'; b.setAttribute('aria-pressed', String(pressed)); b.onclick = onClick; return b;
}
function renderFilters() {
  const root = byId('pbFilters'); const focusedKey = document.activeElement?.dataset?.key;
  const group = (name, nodes) => { const g = PB.el('div', 'pb-filter-group'); g.setAttribute('role', 'group'); g.setAttribute('aria-label', name); g.append(PB.el('span', 'pb-filter-label', name), ...nodes); return g; };
  const diff = [chip('全部', filters.range < 0, () => { filters.range = -1; update(); })];
  ranges.forEach((r, i) => diff.push(chip(r.label, filters.range === i, () => { filters.range = filters.range === i ? -1 : i; update(); })));
  const counts = new Map();
  problems.forEach(p => (p.tags || []).forEach(t => counts.set(t, (counts.get(t) || 0) + 1)));
  const tags = [...counts].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'zh')).map(([t]) => t);
  const tagChip = t => { const c = chip(t, filters.tags.has(t), () => { filters.tags.has(t) ? filters.tags.delete(t) : filters.tags.add(t); update(); }); c.dataset.key = 'tag-' + t; return c; };
  const tagNodes = tags.slice(0, 15).map(tagChip);
  if (tags.length > 15) {
    const more = PB.el('details', 'pb-more'); const s = PB.el('summary', 'pb-chip', `更多（${tags.length - 15}）`);
    const pop = PB.el('div', 'pb-more-pop'); pop.append(...tags.slice(15).map(tagChip));
    if (tags.slice(15).some(t => filters.tags.has(t))) more.open = true;
    more.append(s, pop); tagNodes.push(more);
  }
  const status = ['all', 'todo', 'tried', 'solved'].map(k => chip(k === 'all' ? '全部' : PB.statusName[k], filters.status === k, () => { filters.status = k; update(); }));
  const searchWrap = PB.el('label', 'pb-search');
  const search = PB.el('input'); search.type = 'search'; search.id = 'pbSearch'; search.placeholder = '搜索标题或 id'; search.value = filters.query;
  search.setAttribute('aria-label', '搜索标题或 id（按 / 聚焦）');
  search.oninput = () => { filters.query = search.value; renderGrid(); };
  searchWrap.append(search, PB.el('kbd', '', '/'));
  root.replaceChildren(group('难度', diff), ...(tags.length ? [group('标签', tagNodes)] : []), group('状态', status), searchWrap);
  if (focusedKey) root.querySelector(`[data-key="${CSS.escape(focusedKey)}"]`)?.focus();
}
function update() {
  const active = document.activeElement, inFilters = byId('pbFilters').contains(active);
  const label = inFilters ? active.textContent : null, groupLabel = inFilters ? active.closest('[role=group]')?.getAttribute('aria-label') : null;
  renderFilters(); renderGrid();
  if (label && groupLabel) [...byId('pbFilters').querySelectorAll(`[role=group][aria-label="${groupLabel}"] .pb-chip`)].find(c => c.textContent === label)?.focus();
}
function matches(p) {
  if (filters.range >= 0 && !ranges[filters.range].test(p.difficulty)) return false;
  for (const t of filters.tags) if (!(p.tags || []).includes(t)) return false;
  if (filters.status !== 'all' && PB.status(p) !== filters.status) return false;
  const q = filters.query.trim().toLowerCase();
  if (q && ![p.id, p.title?.zh, p.title?.en].some(s => String(s || '').toLowerCase().includes(q))) return false;
  return true;
}
function closeMenu() { if (openMenu) { openMenu.menu.hidden = true; openMenu.button.setAttribute('aria-expanded', 'false'); openMenu = null; } }
function card(p) {
  const status = PB.status(p), best = p.bestScore ?? 0, total = p.totalPoints || 100;
  const c = PB.el('article', 'pb-card'); c.dataset.status = status; c.dataset.id = p.id; c.tabIndex = 0;
  c.setAttribute('aria-label', `${p.title?.zh || p.id}，难度 ${p.difficulty}，${PB.statusName[status]}${p.bestScore == null ? '' : `，最佳 ${best}/${total}`}`);
  const top = PB.el('div', 'pb-card-top');
  const dot = PB.el('span', 'pb-status-dot'); dot.dataset.status = status; dot.title = PB.statusName[status];
  const statusText = PB.el('span', 'pb-status-text', PB.statusName[status]);
  const menuButton = PB.el('button', 'pb-card-menu-btn', '⋯'); menuButton.type = 'button';
  menuButton.setAttribute('aria-label', `${p.title?.zh || p.id} 的更多操作`); menuButton.setAttribute('aria-haspopup', 'menu'); menuButton.setAttribute('aria-expanded', 'false');
  const menu = PB.el('div', 'pb-card-menu'); menu.setAttribute('role', 'menu'); menu.hidden = true;
  const openItem = PB.el('button', '', '打开'); openItem.type = 'button'; openItem.setAttribute('role', 'menuitem');
  const deleteItem = PB.el('button', 'pb-danger', '删除'); deleteItem.type = 'button'; deleteItem.setAttribute('role', 'menuitem');
  openItem.onclick = e => { e.stopPropagation(); closeMenu(); location.hash = '#/problem/' + encodeURIComponent(p.id); };
  deleteItem.onclick = async e => {
    e.stopPropagation(); closeMenu();
    if (!confirm(`删除题目「${p.title?.zh || p.id}」？题包与该题的全部提交记录都会被删除。`)) return;
    try { await PB.api('/api/problems/' + encodeURIComponent(p.id), {method: 'DELETE'}); PB.forgetProblem?.(p.id); await PB.list.refresh(); }
    catch (err) { PB.toast(err.message); }
  };
  menu.append(openItem, deleteItem);
  menuButton.onclick = e => {
    e.stopPropagation(); const wasOpen = openMenu?.menu === menu; closeMenu();
    if (!wasOpen) { menu.hidden = false; menuButton.setAttribute('aria-expanded', 'true'); openMenu = {menu, button: menuButton}; openItem.focus(); }
  };
  top.append(PB.diffBadge(p.difficulty), dot, statusText, menuButton, menu);
  const title = PB.el('h3', 'pb-card-title', p.title?.zh || p.id);
  const sub = PB.el('p', 'pb-card-sub', p.title?.en || '');
  const tags = PB.el('div', 'pb-card-tags'); (p.tags || []).forEach(t => tags.append(PB.el('span', 'pb-tag', t)));
  const score = PB.el('div', 'pb-card-score');
  const bar = PB.el('div', 'pb-bar'); bar.setAttribute('role', 'progressbar'); bar.setAttribute('aria-valuemin', '0'); bar.setAttribute('aria-valuemax', String(total)); bar.setAttribute('aria-valuenow', String(best)); bar.setAttribute('aria-label', '最佳得分');
  const fill = PB.el('span'); fill.style.width = `${Math.max(0, Math.min(100, best / total * 100))}%`; bar.append(fill);
  score.append(bar, PB.el('span', 'pb-card-points', p.bestScore == null ? `—/${total}` : `${best}/${total}`));
  const foot = PB.el('div', 'pb-card-foot');
  foot.append(PB.el('span', 'pb-card-id', p.id), PB.el('span', 'pb-card-meta', p.attempts ? `${p.attempts} 次提交` : (p.judgeMode === 'io' ? '完整程序' : '函数式')));
  c.append(top, title, sub, tags, score, foot);
  const open = () => { location.hash = '#/problem/' + encodeURIComponent(p.id); };
  c.onclick = e => { if (!e.target.closest('.pb-card-menu, .pb-card-menu-btn')) open(); };
  c.onkeydown = e => { if (e.target === c && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); open(); } };
  return c;
}
function renderGrid() {
  const shown = problems.filter(matches);
  byId('pbGrid').replaceChildren(...shown.map(card));
  byId('pbEmpty').hidden = !loadedOnce || problems.length > 0;
  byId('pbFilters').hidden = problems.length === 0;
  byId('pbNoMatch').hidden = problems.length === 0 || shown.length > 0;
  const solved = problems.filter(p => PB.status(p) === 'solved').length;
  byId('pbListStats').textContent = problems.length ? `已满分 ${solved} / 共 ${problems.length}` : '';
}
PB.list = {
  async refresh() {
    try { const data = await PB.api('/api/problems'); problems = data.problems || []; loadedOnce = true; }
    catch (e) { if (e.status !== 403 && e.status !== 0) PB.toast(e.message); if (!loadedOnce) return; }
    renderFilters(); renderGrid();
  }
};

// ---- 导入 ----
function showImportError(error) {
  const details = error?.data?.details;
  const lines = Array.isArray(details) && details.length
    ? details.map((d, i) => `${String(i + 1).padStart(2, ' ')}. [${d.level || 'error'}] ${d.message}`)
    : [error?.message || String(error)];
  byId('pbErrorTitle').textContent = error?.data?.error || '导入失败';
  byId('pbErrorDetails').textContent = lines.join('\n');
  byId('pbErrorDialog').showModal();
}
async function importPackage(body, name) {
  if (importAbort) return;
  importAbort = new AbortController();
  const buttons = [byId('pbImportButton'), byId('pbEmptyImport')];
  buttons.forEach(b => { b.disabled = true; });
  byId('pbImportText').textContent = `正在导入并自检 ${name || '题包'}（编译 checker、driver 并跑参考答案，约 5–30 秒）…`;
  byId('pbImportProgress').hidden = false;
  try {
    const result = await PB.api('/api/problems/import', {body, signal: importAbort.signal});
    const sol = Object.entries(result.verification?.solutions || {}).map(([l, r]) => `${PB.languageNames[l] || l} ${r.score}`).join('，');
    PB.toast(`${result.replaced ? '已覆盖' : '已导入'} ${result.id}${sol ? `（参考答案 ${sol}）` : ''}`);
    await PB.list.refresh();
  } catch (e) {
    if (e.name === 'AbortError') PB.toast('已停止等待；服务端仍会把这次导入跑完，稍后刷新题单即可看到结果。');
    else showImportError(e);
  } finally {
    importAbort = null; buttons.forEach(b => { b.disabled = false; }); byId('pbImportProgress').hidden = true;
  }
}
function toBase64(bytes) {
  let binary = '';
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
  return btoa(binary);
}
async function importFile(file) {
  if (!file) return;
  if (!/\.zip$/i.test(file.name)) return showImportError(new Error('请选择题包 zip（.zip 文件）。'));
  if (file.size > 44 * 1024 * 1024) return showImportError(new Error('题包超过 44 MiB（base64 传输会再涨约三分之一）；更大的题包请用接口的 zipPath 导入。'));
  await importPackage({zip: toBase64(new Uint8Array(await file.arrayBuffer()))}, file.name);
}

// ---- 路由 ----
const views = {problems: 'pbProblemsView', problem: 'pbProblemView'};
function setView(name) {
  document.body.dataset.view = name;
  const main = byId('main'); main.hidden = name !== 'debug'; main.setAttribute('aria-hidden', String(name !== 'debug'));
  for (const [key, id] of Object.entries(views)) { const v = byId(id); v.hidden = key !== name; v.setAttribute('aria-hidden', String(key !== name)); }
  document.querySelectorAll('.pb-nav-link').forEach(a => { const on = a.dataset.route === name || (name === 'problem' && a.dataset.route === 'problems'); a.classList.toggle('active', on); if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
}
function route() {
  closeMenu();
  const hash = location.hash;
  if (hash.startsWith('#/problem/')) {
    setView('problem'); PB.problemView?.open(decodeURIComponent(hash.slice('#/problem/'.length)));
  } else if (hash === '#/debug') {
    setView('debug'); PB.problemView?.leave();
  } else {
    if (hash !== '#/problems') history.replaceState(null, '', '#/problems');
    setView('problems'); PB.problemView?.leave(); PB.list.refresh();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // 题目视图里的输入不应触发调试台的草稿自动保存（app.js 在 document 上监听 input/change）。
  ['pbProblemsView', 'pbProblemView', 'pbHistory', 'pbErrorDialog'].forEach(id => ['input', 'change'].forEach(t => byId(id).addEventListener(t, e => e.stopPropagation())));
  byId('pbImportButton').onclick = byId('pbEmptyImport').onclick = () => byId('pbImportFile').click();
  byId('pbImportFile').onchange = async () => { const f = byId('pbImportFile').files[0]; byId('pbImportFile').value = ''; await importFile(f); };
  byId('pbImportCancel').onclick = () => importAbort?.abort();
  byId('pbErrorCopy').onclick = () => PB.copy(byId('pbErrorDetails').textContent, byId('pbErrorCopy'));
  byId('pbClearCache').onclick = async () => {
    if (!confirm('清空全部题目的提交记录？题目本身不会被删除。')) return;
    try { const r = await PB.api('/api/submissions/clear', {body: {}}); PB.toast(`已清空 ${r.removed} 条提交记录`); await PB.list.refresh(); }
    catch (e) { PB.toast(e.message); }
  };
  const list = byId('pbProblemsView');
  list.addEventListener('dragover', e => { if ([...(e.dataTransfer?.types || [])].includes('Files')) { e.preventDefault(); list.classList.add('pb-dropping'); } });
  list.addEventListener('dragleave', e => { if (!list.contains(e.relatedTarget)) list.classList.remove('pb-dropping'); });
  list.addEventListener('drop', e => { e.preventDefault(); list.classList.remove('pb-dropping'); importFile(e.dataTransfer.files[0]); });
  document.addEventListener('click', e => { if (openMenu && !openMenu.menu.contains(e.target)) closeMenu(); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && openMenu) { const b = openMenu.button; closeMenu(); b.focus(); }
    const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) || e.target.isContentEditable;
    if (e.key === '/' && !typing && document.body.dataset.view === 'problems' && !document.querySelector('dialog[open]')) { e.preventDefault(); byId('pbSearch')?.focus(); }
  });
  window.addEventListener('hashchange', route);
  window.addEventListener('pb-reconnected', () => { if (document.body.dataset.view === 'problems') PB.list.refresh(); });
  if (!PB.token()) PB.authFailed();
  route();
});
})();
