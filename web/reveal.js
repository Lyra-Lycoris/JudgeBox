'use strict';
// 揭榜动画：一个真人 + 一条「上次」幽灵行。时间轴见任务书 §7，全部相对完成时刻 t0。
// 只动 transform / opacity（我的行升起时按规格带一次 blur）；用 Web Animations API 排时间轴，跳过时统一 finish。
(() => {
const PB = window.PB = window.PB || {};
const el = (tag, className, text) => { const e = document.createElement(tag); if (className) e.className = className; if (text !== undefined) e.textContent = String(text); return e; };
const EASE = 'cubic-bezier(.2,.8,.2,1)', RISE = 'cubic-bezier(.16,1,.3,1)';
const T = {head: 180, ghost: 260, me: 420, cells: 760, reorder: 1600, settle: 2200, dwell: 800, fade: 220, stagger: 70};

function conclusion(score, prev) {
  if (prev === null || prev === undefined) return {text: `首次提交 · 得分 ${score}`, tone: 'first'};
  if (score > prev) return {text: `本次 ${score} · 历史 ${prev} · 提升 ${score - prev}`, tone: 'up'};
  if (score === prev) return {text: `本次 ${score} · 历史 ${prev} · 持平`, tone: 'flat'};
  return {text: `本次 ${score} · 历史 ${prev} · 还差 ${prev - score}`, tone: 'down'};
}
PB.conclusion = conclusion;

function row(kind, {rank, name, score, groups, cells}) {
  const r = el('div', `pb-row pb-row-${kind}`); r.setAttribute('role', 'row');
  const rankCell = el('span', 'pb-row-rank', rank); rankCell.setAttribute('role', 'cell');
  const who = el('span', 'pb-row-who'); who.setAttribute('role', 'cell');
  const nameEl = el('span', 'pb-row-name', name); who.append(nameEl);
  if (kind === 'ghost') who.append(el('span', 'pb-row-tag', '上次'));
  const scoreCell = el('span', 'pb-row-score'); scoreCell.setAttribute('role', 'cell');
  const num = el('span', 'pb-row-num', score === null ? '—' : score);
  const bar = el('span', 'pb-row-bar'); const fill = el('span'); bar.append(fill);
  fill.style.transform = `scaleX(${Math.max(0, Math.min(1, (score || 0) / 100))})`;
  scoreCell.append(num, bar);
  const cellWrap = el('span', 'pb-row-cells'); cellWrap.setAttribute('role', 'cell');
  groups.forEach((g, k) => {
    const c = el('span', 'pb-cell');
    const info = cells ? cells[k] : null;
    if (info) { c.dataset.state = info.state; c.textContent = info.state === 'passed' ? `+${info.earned}` : info.state === 'failed' ? '0' : '·'; c.setAttribute('aria-label', `${g.name}：${info.state === 'passed' ? '通过，得 ' + info.earned + ' 分' : info.state === 'failed' ? '未通过' : '未评测'}`); }
    else { c.dataset.state = 'ghost'; c.textContent = ''; }
    cellWrap.append(c);
  });
  r.append(rankCell, who, scoreCell, cellWrap);
  r._parts = {rankCell, nameEl, num, fill, cells: [...cellWrap.children]};
  return r;
}

// status：/api/submit/status 完成态；opts.title、opts.returnFocus。返回 Promise，关闭后 resolve。
PB.reveal = (status, opts = {}) => new Promise(resolve => {
  const score = Number(status.score) || 0;
  const prev = status.previousBest === undefined ? null : status.previousBest;
  const groups = (status.groups || []).map(g => ({name: g.name, points: g.points, earned: g.earned || 0, state: g.state || 'pending'}));
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const result = conclusion(score, prev);

  const overlay = el('div', 'pb-reveal'); overlay.setAttribute('role', 'dialog'); overlay.setAttribute('aria-modal', 'true'); overlay.setAttribute('aria-labelledby', 'pbRevealTitle');
  const board = el('div', 'pb-board');
  const head = el('div', 'pb-board-head');
  const eyebrow = el('span', 'pb-board-eyebrow', 'SCOREBOARD');
  const title = el('h2', 'pb-board-title', opts.title || ''); title.id = 'pbRevealTitle';
  const verdict = PB.verdictBadge(status.verdict);
  head.append(eyebrow, title, verdict);
  const cols = el('div', 'pb-row pb-row-cols'); cols.setAttribute('role', 'row');
  const colCells = el('span', 'pb-row-cells');
  groups.forEach(g => { const c = el('span', 'pb-cell-head'); c.append(el('span', 'pb-cell-name', g.name), el('span', 'pb-cell-points', g.points)); colCells.append(c); });
  cols.append(el('span', 'pb-row-rank', '#'), el('span', 'pb-row-who', '我'), el('span', 'pb-row-score', '得分'), colCells);
  [...cols.children].forEach(c => c.setAttribute('role', 'columnheader'));
  const rows = el('div', 'pb-board-rows'); rows.setAttribute('role', 'rowgroup');
  const meFirst = prev === null || score > prev;
  const ghost = prev === null ? null : row('ghost', {rank: 1, name: '历史最佳', score: prev, groups});
  const me = row('me', {rank: ghost ? 2 : 1, name: '我', score: reduced ? score : (prev ?? 0), groups, cells: groups});
  const first = prev === null ? el('div', 'pb-row-first', '首次提交 · 没有历史记录') : null;
  if (ghost) rows.append(ghost); else rows.append(first);
  rows.append(me);
  const grid = el('div', 'pb-board-grid'); grid.setAttribute('role', 'table'); grid.setAttribute('aria-label', '本题榜单');
  grid.append(cols, rows);
  const foot = el('div', 'pb-board-foot'); foot.setAttribute('aria-live', 'polite');
  const line = el('p', 'pb-conclusion', result.text); line.dataset.tone = result.tone;
  const message = el('p', 'pb-board-message', status.message || '');
  foot.append(line, message);
  const skip = el('button', 'pb-reveal-skip', '跳过动画 · Esc 关闭'); skip.type = 'button';
  board.append(head, grid, foot);
  overlay.append(board, skip);
  document.body.append(overlay);

  const animations = [], timers = [];
  let closed = false, rafId = 0;
  const anim = (node, frames, options) => { const a = node.animate(frames, {fill: 'both', easing: EASE, ...options}); animations.push(a); return a; };
  const later = (ms, fn) => timers.push(setTimeout(fn, ms));
  const animated = [overlay, board, head, cols, ghost, me, me._parts.nameEl, foot, ...me._parts.cells].filter(Boolean);

  function finalState() {
    me._parts.num.textContent = score;
    me._parts.fill.style.transform = `scaleX(${score / 100})`;
    if (ghost && meFirst && rows.firstElementChild !== me) rows.insertBefore(me, ghost);
    me._parts.rankCell.textContent = ghost ? (meFirst ? 1 : 2) : 1;
    if (ghost) ghost._parts.rankCell.textContent = meFirst ? 2 : 1;
    me.classList.add('pb-row-settled');
  }
  function close() {
    if (closed) return; closed = true;
    timers.forEach(clearTimeout); cancelAnimationFrame(rafId);
    animations.forEach(a => { try { a.finish(); } catch {} });
    finalState();
    document.removeEventListener('keydown', onKey, true);
    const out = reduced ? null : overlay.animate([{opacity: 1}, {opacity: 0}], {duration: T.fade, easing: EASE, fill: 'forwards'});
    const done = () => { animated.forEach(n => { n.style.willChange = ''; }); overlay.remove(); opts.returnFocus?.focus?.(); resolve(); };
    if (out) out.finished.then(done, done); else done();
  }
  let settled = false;
  function settle() {
    if (settled || closed) return; settled = true;
    timers.forEach(clearTimeout); cancelAnimationFrame(rafId);
    animations.forEach(a => { try { a.finish(); } catch {} });
    finalState();
    animated.forEach(n => { n.style.willChange = ''; });
    overlay.classList.add('pb-reveal-settled');
    skip.textContent = '点击任意处关闭';
    skip.setAttribute('aria-label', '关闭榜单');
  }
  function onKey(e) {
    if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); close(); return; }
    if ((e.key === 'Enter' || e.key === ' ') && document.activeElement === skip) { e.preventDefault(); e.stopPropagation(); settled ? close() : settle(); return; }
    if (e.key === 'Tab') { e.preventDefault(); skip.focus(); }   // 浮层里只有一个可聚焦元素，Tab 原地循环
  }
  document.addEventListener('keydown', onKey, true);
  overlay.addEventListener('click', () => { if (settled) close(); else settle(); });
  skip.focus({preventScroll: true});

  if (reduced) {
    settle();
    return;
  }
  animated.forEach(n => { n.style.willChange = 'transform, opacity'; });
  // t0：浮层与榜单
  anim(overlay, [{opacity: 0}, {opacity: 1}], {duration: 220});
  anim(board, [{transform: 'scale(.96) translateY(12px)'}, {transform: 'none'}], {duration: 220});
  // +180：榜头与列头
  [head, cols].forEach(n => anim(n, [{opacity: 0}, {opacity: 1}], {duration: 200, delay: T.head}));
  // +260：幽灵行 / 首次提交提示
  const ghostNode = ghost || first;
  anim(ghostNode, [{opacity: 0, transform: 'translateY(-10px)'}, {opacity: 1, transform: 'none'}], {duration: 180, delay: T.ghost});
  // +420：我的行升起；名字 26→30（用 scale 表现），外发光 pulse 一次
  anim(me, [{opacity: 0, transform: 'translateY(56px)', filter: 'blur(6px)'}, {opacity: 1, transform: 'none', filter: 'blur(0)'}], {duration: 520, delay: T.me, easing: RISE});
  anim(me._parts.nameEl, [{transform: `scale(${26 / 30})`}, {transform: 'none'}], {duration: 520, delay: T.me, easing: RISE});
  later(T.me + 520, () => me.classList.add('pb-row-settled'));
  const glow = el('span', 'pb-row-glow'); glow.setAttribute('aria-hidden', 'true'); me.append(glow);
  anim(glow, [{opacity: 0}, {opacity: 1, offset: .35}, {opacity: 0}], {duration: 600, delay: T.me + 260, easing: 'ease-out'});
  // +760：组格子逐格翻转
  me._parts.cells.forEach((c, k) => anim(c, [{transform: 'rotateX(-90deg)', opacity: 0}, {transform: 'none', opacity: 1}], {duration: 300, delay: T.cells + k * T.stagger}));
  // +760：分数滚动（rAF，600 ms，easeOutCubic）与进度条同步
  later(T.cells, () => {
    const from = prev ?? 0, start = performance.now();
    const step = now => {
      const t = Math.min(1, (now - start) / 600), k = 1 - Math.pow(1 - t, 3), v = from + (score - from) * k;
      me._parts.num.textContent = Math.round(v);
      me._parts.fill.style.transform = `scaleX(${Math.max(0, Math.min(1, v / 100))})`;
      if (t < 1 && !closed) rafId = requestAnimationFrame(step);
    };
    rafId = requestAnimationFrame(step);
  });
  // +1.6 s：FLIP 重排（读→写→读在同一帧里完成，然后只做 transform 过渡）
  later(T.reorder, () => {
    if (!ghost || !meFirst) return;
    rafId = requestAnimationFrame(() => {
      const before = new Map([[ghost, ghost.getBoundingClientRect().top], [me, me.getBoundingClientRect().top]]);
      rows.insertBefore(me, ghost);
      me._parts.rankCell.textContent = 1; ghost._parts.rankCell.textContent = 2;
      for (const [node, top] of before) {
        const dy = top - node.getBoundingClientRect().top;
        if (dy) anim(node, [{transform: `translateY(${dy}px)`}, {transform: 'none'}], {duration: 380, easing: RISE, fill: 'none'});
      }
    });
  });
  // +2.2 s：结论行；驻留后自动关闭
  anim(foot, [{opacity: 0, transform: 'translateY(6px)'}, {opacity: 1, transform: 'none'}], {duration: 240, delay: T.settle});
  later(T.settle + 240, settle);
});
})();
