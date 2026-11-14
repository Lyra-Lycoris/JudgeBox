'use strict';
// 题面 Markdown 子集渲染（规格 §4.6）+ MathJax 调用 + 双语缓存。
// 只用 createElement / textContent 构造 DOM，用户文本永远不进 innerHTML，因此不需要也不会出现 HTML 注入。

// MathJax 配置必须在 /vendor/tex-svg.js 之前生效（两者都是 defer，按文档顺序执行）。
// 我们自己把 $…$ 包成 \( \)，因此只识别这两种定界符；正文里的单个 $ 不会被误判。
window.MathJax = {
  startup: {typeset: false},
  tex: {inlineMath: [['\\(', '\\)']], displayMath: [['\\[', '\\]']], processEscapes: false},
  svg: {fontCache: 'global'},
  options: {enableMenu: false}
};

(() => {
const PB = window.PB = window.PB || {};
const el = (tag, className, text) => { const e = document.createElement(tag); if (className) e.className = className; if (text !== undefined) e.textContent = text; return e; };

// ---------- 行内 ----------
function findClosing(s, marker, from) {
  for (let i = from; i <= s.length - marker.length; i++) {
    if (s[i] === '\\') { i++; continue; }
    if (s.startsWith(marker, i)) return i;
  }
  return -1;
}
function inline(text, parent) {
  let buffer = '';
  const flush = () => { if (buffer) { parent.append(document.createTextNode(buffer)); buffer = ''; } };
  for (let i = 0; i < text.length;) {
    const c = text[i];
    if (c === '\\' && i + 1 < text.length && /[\\`*_{}\[\]()#+\-.!|$>~]/.test(text[i + 1])) { buffer += text[i + 1]; i += 2; continue; }
    if (c === '`') {
      let ticks = 1; while (text[i + ticks] === '`') ticks++;
      const fence = '`'.repeat(ticks), end = text.indexOf(fence, i + ticks);
      if (end > i) { flush(); parent.append(el('code', '', text.slice(i + ticks, end).replace(/^ (.*) $/, '$1'))); i = end + ticks; continue; }
    }
    if (c === '$') {
      const display = text[i + 1] === '$', marker = display ? '$$' : '$', start = i + marker.length;
      const end = findClosing(text, marker, start);
      const body = end > start ? text.slice(start, end) : '';
      if (body.trim() && (display || (!/^\s/.test(body) && !/\s$/.test(body)))) {
        flush();
        const m = el('span', display ? 'math math-display' : 'math', display ? `\\[${body}\\]` : `\\(${body}\\)`);
        m.dataset.tex = text.slice(i, end + marker.length);
        parent.append(m); i = end + marker.length; continue;
      }
    }
    if (c === '*' && text[i + 1] === '*') {
      const end = findClosing(text, '**', i + 2);
      if (end > i + 2) { flush(); const s = el('strong'); inline(text.slice(i + 2, end), s); parent.append(s); i = end + 2; continue; }
    }
    if (c === '*' && text[i + 1] !== ' ' && text[i + 1] !== '*') {
      const end = findClosing(text, '*', i + 1);
      if (end > i + 1 && text[end - 1] !== ' ') { flush(); const s = el('em'); inline(text.slice(i + 1, end), s); parent.append(s); i = end + 1; continue; }
    }
    if ((c === '[') || (c === '!' && text[i + 1] === '[')) {
      const image = c === '!', open = image ? i + 1 : i;
      const close = findClosing(text, ']', open + 1);
      if (close > open && text[close + 1] === '(') {
        const end = text.indexOf(')', close + 2);
        if (end > close) {
          flush();
          const label = text.slice(open + 1, close), url = text.slice(close + 2, end).trim().split(/\s+/)[0];
          if (image) parent.append(el('span', 'pb-md-noimage', label ? `［图片：${label}］` : '［图片］'));
          else if (/^https:\/\/[^\s]+$/i.test(url)) {
            const a = el('a'); a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.title = url; inline(label || url, a); parent.append(a);
          } else inline(label, parent);
          i = end + 1; continue;
        }
      }
    }
    buffer += c; i++;
  }
  flush();
  return parent;
}

// ---------- 块级 ----------
const reFence = /^\s{0,3}(`{3,}|~{3,})\s*([\w+#-]*)\s*$/;
const reHeading = /^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$/;
const reHr = /^\s{0,3}([-*_])(\s*\1){2,}\s*$/;
const reQuote = /^\s{0,3}>\s?/;
const reList = /^(\s*)([-*+]|\d{1,9}[.)])\s+(.*)$/;
const reTableSep = /^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$/;
const splitRow = line => { let s = line.trim(); if (s.startsWith('|')) s = s.slice(1); if (s.endsWith('|') && !s.endsWith('\\|')) s = s.slice(0, -1); const cells = []; let cur = ''; for (let i = 0; i < s.length; i++) { if (s[i] === '\\' && s[i + 1] === '|') { cur += '|'; i++; } else if (s[i] === '|') { cells.push(cur.trim()); cur = ''; } else cur += s[i]; } cells.push(cur.trim()); return cells; };
const isBlockStart = (line, next) => reFence.test(line) || reHeading.test(line) || reHr.test(line) || reQuote.test(line) || reList.test(line) || /^\s*\$\$/.test(line) || (line.includes('|') && next !== undefined && reTableSep.test(next) && next.includes('-'));

function sectionLabel(text) {
  const h = el('h3', 'pb-section-label');
  if (!/[㐀-鿿]/.test(text)) h.classList.add('pb-latin');
  inline(text, h); return h;
}
function blocks(lines, parent) {
  for (let i = 0; i < lines.length;) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }
    let m;
    if ((m = reFence.exec(line))) {
      const fence = m[1], body = []; i++;
      while (i < lines.length && !(lines[i].trim().startsWith(fence[0].repeat(fence.length)) && !lines[i].trim().slice(fence.length).trim())) body.push(lines[i++]);
      i++;
      const pre = el('pre', 'pb-md-code'), code = el('code', '', body.join('\n'));
      if (m[2]) { code.dataset.lang = m[2]; pre.dataset.lang = m[2]; }
      pre.append(code); parent.append(pre); continue;
    }
    if (/^\s*\$\$/.test(line)) {
      const first = line.trim().slice(2); let tex = [];
      if (first.endsWith('$$') && first.length >= 2) { tex.push(first.slice(0, -2)); i++; }
      else {
        if (first) tex.push(first); i++;
        while (i < lines.length && !lines[i].trim().endsWith('$$')) tex.push(lines[i++]);
        if (i < lines.length) { const last = lines[i].trim().slice(0, -2); if (last) tex.push(last); i++; }
      }
      const body = tex.join('\n');
      const d = el('div', 'math-block', `\\[${body}\\]`); d.dataset.tex = `$$${body}$$`; parent.append(d); continue;
    }
    if ((m = reHeading.exec(line))) {
      const level = Math.min(m[1].length, 3);
      if (level === 3 || m[1].length > 3) parent.append(sectionLabel(m[2]));
      else { const h = el(level === 1 ? 'h1' : 'h2', level === 1 ? 'pb-md-h1' : 'pb-md-h2'); inline(m[2], h); parent.append(h); }
      i++; continue;
    }
    if (reHr.test(line)) { parent.append(el('hr', 'pb-md-hr')); i++; continue; }
    if (reQuote.test(line)) {
      const body = []; while (i < lines.length && (reQuote.test(lines[i]) || (lines[i].trim() && !isBlockStart(lines[i], lines[i + 1]) && body.length))) body.push(lines[i++].replace(reQuote, ''));
      const q = el('blockquote', 'pb-md-quote'); blocks(body, q); parent.append(q); continue;
    }
    if (line.includes('|') && i + 1 < lines.length && reTableSep.test(lines[i + 1]) && lines[i + 1].includes('-')) {
      const head = splitRow(line), aligns = splitRow(lines[i + 1]).map(s => s.startsWith(':') && s.endsWith(':') ? 'center' : s.endsWith(':') ? 'right' : '');
      i += 2;
      const wrap = el('div', 'pb-md-table-wrap'), table = el('table', 'pb-md-table'), thead = el('thead'), tr = el('tr');
      head.forEach((h, k) => { const th = el('th'); if (aligns[k]) th.style.textAlign = aligns[k]; inline(h, th); tr.append(th); });
      thead.append(tr); table.append(thead);
      const tbody = el('tbody');
      while (i < lines.length && lines[i].includes('|') && lines[i].trim()) {
        const row = el('tr'); splitRow(lines[i]).slice(0, head.length).forEach((c, k) => { const td = el('td'); if (aligns[k]) td.style.textAlign = aligns[k]; inline(c, td); row.append(td); });
        tbody.append(row); i++;
      }
      table.append(tbody); wrap.append(table); parent.append(wrap); continue;
    }
    if (reList.test(line)) { i = list(lines, i, parent); continue; }
    const para = [];
    while (i < lines.length && lines[i].trim() && !(para.length && isBlockStart(lines[i], lines[i + 1]))) para.push(lines[i++].trim());
    const p = el('p', 'pb-md-p'); inline(joinLines(para), p); parent.append(p);
  }
  return parent;
}
// 中文行与行之间不该多出空格；拉丁文字之间保留一个空格。
function joinLines(parts) {
  return parts.reduce((acc, cur) => !acc ? cur : (/[　-鿿＀-￯]$/.test(acc) || /^[　-鿿＀-￯]/.test(cur)) ? acc + cur : acc + ' ' + cur, '');
}
function list(lines, i, parent, depth = 0) {
  const first = reList.exec(lines[i]), base = first[1].length, ordered = /\d/.test(first[2]);
  const node = el(ordered ? 'ol' : 'ul', 'pb-md-list');
  if (ordered && parseInt(first[2], 10) !== 1) node.start = parseInt(first[2], 10);
  let li = null, text = [];
  const close = () => { if (li) { const span = el('span'); inline(joinLines(text), span); li.prepend(span); } li = null; text = []; };
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { const next = lines[i + 1] !== undefined && reList.exec(lines[i + 1]); if (next && next[1].length >= base) { i++; continue; } break; }
    const m = reList.exec(line);
    if (m) {
      const indent = m[1].length;
      if (indent < base) break;
      if (indent <= base + 1) { if (/\d/.test(m[2]) !== ordered) break; close(); li = el('li'); node.append(li); text = [m[3]]; i++; continue; }
      if (li && depth === 0) { i = list(lines, i, li, 1); continue; }   // 只支持嵌套一层
      if (li) { text.push(m[3]); i++; continue; }
      break;
    }
    if (!li || isBlockStart(line, lines[i + 1])) break;
    text.push(line.trim()); i++;
  }
  close(); parent.append(node);
  return i;
}

function renderStatement(markdownText) {
  const fragment = document.createDocumentFragment();
  blocks(String(markdownText || '').replace(/\r\n?/g, '\n').split('\n'), fragment);
  return fragment;
}
window.renderStatement = renderStatement;

// ---------- 数学 ----------
function fallbackMath(root) {
  root.querySelectorAll('.math, .math-block').forEach(m => {
    if (m.querySelector('mjx-container')) return;
    m.textContent = m.dataset.tex; m.classList.add('math-fallback'); m.title = '公式渲染器不可用，显示原文';
  });
}
function typeset(root) {
  if (!root.querySelector('.math, .math-block')) return Promise.resolve();
  const MJ = window.MathJax;
  const timer = new Promise(resolve => setTimeout(resolve, 3000));
  if (!MJ || !MJ.startup || !MJ.startup.promise) { fallbackMath(root); return Promise.resolve(); }
  const run = MJ.startup.promise.then(() => MJ.typesetPromise ? MJ.typesetPromise([root]) : null).catch(() => {});
  return Promise.race([run, timer]).then(() => fallbackMath(root));
}
PB.typesetMath = typeset;
// function 模式仓颉 driver 的 package 名（API 不单独返回，取 driver 首个 package 声明）。
PB.cangjiePackage = problem => {
  if (problem?.judgeMode !== 'function') return '';
  const m = /^\s*package\s+([A-Za-z_][\w.]*)/m.exec(problem.drivers?.cangjie || '');
  return m ? m[1] : '';
};

// ---------- 整张题面 ----------
const cache = new Map();
function samplePane(label, text) {
  const pane = el('div', 'pb-sample-pane');
  const head = el('div', 'pb-sample-head'); head.append(el('span', '', label));
  const copy = el('button', 'pb-copy', '复制'); copy.type = 'button'; copy.setAttribute('aria-label', `复制${label}`);
  copy.onclick = () => PB.copy(text, copy);
  head.append(copy);
  pane.append(head, el('pre', 'pb-sample-pre', text));
  return pane;
}
function buildStatement(problem, lang) {
  const L = (obj, fallback = '') => (obj && (obj[lang] || obj[lang === 'zh' ? 'en' : 'zh'])) || fallback;
  const zh = lang === 'zh';
  const root = el('article', 'pb-statement-doc'); root.lang = zh ? 'zh-CN' : 'en';
  const body = renderStatement(L(problem.statement));
  const header = el('header', 'pb-statement-header');
  const firstHeading = body.firstElementChild?.classList.contains('pb-md-h1') ? body.firstElementChild : null;
  const title = firstHeading || el('h1', 'pb-md-h1', L(problem.title, problem.id));
  const sec = v => (v / 1000).toString();
  const limits = el('p', 'pb-statement-limits', `time limit per test ${sec(problem.limits.timeMs)} second${problem.limits.timeMs === 1000 ? '' : 's'} · memory limit per test ${problem.limits.memoryMb} megabytes`);
  header.append(title, limits);
  root.append(header, body);
  if (problem.judgeMode === 'function' && L(problem.signature)) {
    root.append(sectionLabel(zh ? '函数签名' : 'Signature'));
    const pre = el('pre', 'pb-md-code pb-signature'); pre.append(el('code', '', L(problem.signature))); root.append(pre);
    const pkg = PB.cangjiePackage(problem);
    if (pkg) {
      const note = el('div', 'pb-package-note');
      note.append(el('span', 'pb-package-label', zh ? '仓颉包名' : 'Cangjie package'));
      const code = el('code', '', `package ${pkg}`); note.append(code);
      note.append(el('span', '', zh ? '仓颉提交的第一行必须是这一行（不写会自动补上；写成别的包名会编译失败）。C++ 不需要包名。'
        : 'Your Cangjie file must start with this line (added automatically if missing; any other package name fails to compile). C++ needs none.'));
      root.append(note);
    }
  }
  if ((problem.samples || []).length) {
    root.append(sectionLabel(zh ? '样例（标准输入 / 输出）' : 'Samples (stdin / stdout)'));
    problem.samples.forEach((s, k) => {
      const card = el('section', 'pb-sample'); card.setAttribute('aria-label', `${zh ? '样例' : 'Sample'} ${k + 1}`);
      card.append(el('div', 'pb-sample-title', `${zh ? '样例' : 'Sample'} ${k + 1}`));
      const grid = el('div', 'pb-sample-grid');
      grid.append(samplePane(zh ? '输入' : 'Input', s.input || ''), samplePane(zh ? '输出' : 'Output', s.output || ''));
      card.append(grid);
      const explain = L(s.explain);
      if (explain) { const p = el('div', 'pb-sample-explain'); p.append(renderStatement(explain)); card.append(p); }
      root.append(card);
    });
  }
  const hints = (problem.hints && (problem.hints[lang]?.length ? problem.hints[lang] : problem.hints[zh ? 'en' : 'zh'])) || [];
  if (hints.length) {
    const d = el('details', 'pb-hints');
    d.append(el('summary', '', zh ? `提示（${hints.length}）` : `Hints (${hints.length})`));
    const ol = el('ol', 'pb-md-list');
    hints.forEach(h => { const li = el('li'); li.append(renderStatement(h)); ol.append(li); });
    d.append(ol); root.append(d);
  }
  return root;
}
// 把题面挂进 container；同一题同一语言只解析一次，切换语言保持滚动位置。
PB.showStatement = (container, scroller, problem, lang) => {
  const key = `${problem.id}\u0000${problem.storedAt || ''}\u0000${lang}`;
  let doc = cache.get(key), fresh = false;
  if (!doc) { doc = buildStatement(problem, lang); cache.set(key, doc); fresh = true; }
  const top = scroller.scrollTop;
  container.replaceChildren(doc);
  scroller.scrollTop = top;
  if (fresh) typeset(doc);
  return doc;
};
PB.forgetStatement = id => { for (const k of cache.keys()) if (k.startsWith(id + '\u0000')) cache.delete(k); };
})();
