'use strict';
// 提交历史抽屉：列表（倒序）→ 点开看只读代码与结果摘要 → 清空本题记录。
(() => {
const PB = window.PB = window.PB || {};
const byId = id => document.getElementById(id);
const el = (...a) => PB.el(...a);
let currentId = null, returnFocus = null, expanded = null;

function relative(iso) {
  const t = Date.parse(iso); if (!Number.isFinite(t)) return '—';
  const s = Math.round((Date.now() - t) / 1000);
  if (s < 45) return '刚刚';
  if (s < 3600) return `${Math.round(s / 60)} 分钟前`;
  if (s < 86400) return `${Math.round(s / 3600)} 小时前`;
  if (s < 86400 * 30) return `${Math.round(s / 86400)} 天前`;
  return new Date(t).toLocaleDateString('zh-CN');
}
PB.relativeTime = relative;
PB.absoluteTime = iso => { const t = Date.parse(iso); return Number.isFinite(t) ? new Date(t).toLocaleString('zh-CN', {hour12: false}) : ''; };

function codeView(source) {
  const lines = String(source || '').replace(/\r\n?/g, '\n').split('\n');
  if (lines.length > 1 && lines[lines.length - 1] === '') lines.pop();
  const wrap = el('div', 'pb-code-view');
  const pre = el('pre', 'pb-code-lines'); pre.setAttribute('aria-label', '提交的源码（只读）'); pre.tabIndex = 0;
  const render = limit => {
    pre.replaceChildren(...lines.slice(0, limit).map((l, i) => { const row = el('span', 'pb-code-line'); row.append(el('span', 'pb-ln', i + 1), el('span', 'pb-lc', l || ' ')); return row; }));
  };
  render(400);
  wrap.append(pre);
  if (lines.length > 400) {
    const more = el('button', 'text-button pb-code-more', `显示全部 ${lines.length} 行`); more.type = 'button';
    more.onclick = () => { render(lines.length); more.remove(); };
    wrap.append(more);
  }
  const copy = el('button', 'pb-copy pb-code-copy', '复制'); copy.type = 'button'; copy.setAttribute('aria-label', '复制源码');
  copy.onclick = () => PB.copy(source, copy);
  wrap.append(copy);
  return wrap;
}
function summary(detail) {
  const box = el('div', 'pb-history-detail');
  const head = el('div', 'pb-history-detail-head');
  head.append(PB.verdictBadge(detail.verdict), el('strong', 'pb-mono', `${detail.score}/100`));
  if (Number.isFinite(detail.durationMs)) head.append(el('span', 'pb-muted', `用时 ${(detail.durationMs / 1000).toFixed(1)} s`));
  if (detail.sourceTruncated) head.append(el('span', 'pb-warn', '源码过大，已截断保存'));
  box.append(head);
  if (detail.message) box.append(el('p', 'pb-muted', detail.message));
  if ((detail.groups || []).length) {
    const g = el('div', 'pb-history-groups');
    detail.groups.forEach(x => { const c = el('span', 'pb-mini-group', `${x.name} ${x.earned ?? 0}/${x.points}`); c.dataset.state = x.state; g.append(c); });
    box.append(g);
  }
  if (detail.compileLog) { const d = el('details', 'pb-compile'); d.open = detail.verdict === 'CE'; d.append(el('summary', '', '编译日志'), el('pre', 'pb-log', detail.compileLog)); box.append(d); }
  box.append(codeView(detail.source));
  return box;
}
async function toggle(item, sub) {
  if (expanded && expanded.item === item) { expanded.panel.remove(); item.setAttribute('aria-expanded', 'false'); expanded = null; return; }
  if (expanded) { expanded.panel.remove(); expanded.item.setAttribute('aria-expanded', 'false'); }
  const panel = el('div', 'pb-history-panel', '加载中…');
  item.after(panel); item.setAttribute('aria-expanded', 'true'); expanded = {item, panel};
  try { const detail = await PB.api('/api/submissions/' + encodeURIComponent(sub.id)); panel.replaceChildren(summary(detail)); }
  catch (e) { panel.textContent = e.message; }
}
async function load() {
  const list = byId('pbHistoryList'); expanded = null;
  list.replaceChildren(el('p', 'pb-muted pb-history-empty', '加载中…'));
  try {
    const data = await PB.api('/api/submissions?problemId=' + encodeURIComponent(currentId));
    const subs = data.submissions || [];
    byId('pbHistoryClear').disabled = !subs.length;
    if (!subs.length) { list.replaceChildren(el('p', 'pb-muted pb-history-empty', '还没有提交记录。')); return; }
    list.replaceChildren(...subs.map(sub => {
      const item = el('button', 'pb-history-item'); item.type = 'button'; item.setAttribute('aria-expanded', 'false');
      const time = el('span', 'pb-history-time', relative(sub.at)); time.title = PB.absoluteTime(sub.at);
      item.append(time, el('span', 'pb-history-lang', PB.languageNames[sub.language] || sub.language),
        el('span', 'pb-history-score', `${sub.score}`), PB.verdictBadge(sub.verdict),
        el('span', 'pb-history-cases', `${sub.passed ?? 0}/${sub.cases ?? 0} 点`));
      item.setAttribute('aria-label', `${PB.absoluteTime(sub.at)}，${PB.languageNames[sub.language] || sub.language}，${sub.score} 分，${sub.verdict}`);
      item.onclick = () => toggle(item, sub);
      return item;
    }));
  } catch (e) { list.replaceChildren(el('p', 'pb-muted pb-history-empty', e.message)); }
}
PB.history = {
  isOpen: () => !byId('pbHistory').hidden,
  open(problemId, focusBack) {
    currentId = problemId; returnFocus = focusBack || document.activeElement;
    byId('pbHistory').hidden = false; document.body.classList.add('pb-drawer-open');
    byId('pbHistoryClose').focus();
    return load();
  },
  refresh() { if (!byId('pbHistory').hidden && currentId) return load(); },
  close() {
    if (byId('pbHistory').hidden) return;
    byId('pbHistory').hidden = true; document.body.classList.remove('pb-drawer-open');
    returnFocus?.focus?.();
  }
};
document.addEventListener('DOMContentLoaded', () => {
  byId('pbHistoryClose').onclick = () => PB.history.close();
  byId('pbHistory').addEventListener('keydown', e => { if (e.key === 'Escape') { e.stopPropagation(); PB.history.close(); } });
  byId('pbHistoryClear').onclick = async () => {
    if (!currentId || !confirm('清空本题的全部提交记录？此操作不可撤销，题目本身不受影响。')) return;
    try { const r = await PB.api('/api/submissions/clear', {body: {problemId: currentId}}); PB.toast(`已清空 ${r.removed} 条记录`); await load(); PB.problemView?.refreshBest(); }
    catch (e) { PB.toast(e.message); }
  };
});
})();
