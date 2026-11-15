'use strict';
// 题面渲染：Markdown（标题 / 段落 / 列表 / 引用 / 表格 / 代码块 / 行内样式）+ TeX 公式。
// 规格 §4.6。只用 createElement / textContent 构造 DOM，题面文本永远不进 innerHTML，
// 因此不需要也不会出现 HTML 注入。
//
// 分工：本文件负责把 $…$ / $$…$$ 配对成 \(…\) / \[…\] 并生成占位节点，MathJax 只认这两种定界符，
// 正文里孤立的 $ 不会被误判。行内公式与正文同字号，块级公式单独成行、超宽时横向滚动而不是被压缩。

// MathJax 配置必须在 /vendor/tex-svg.js 之前生效（两者都是 defer，按文档顺序执行）。
window.MathJax = {
  startup: {typeset: false},
  tex: {inlineMath: [['\\(', '\\)']], displayMath: [['\\[', '\\]']], processEscapes: false},
  svg: {fontCache: 'global'},
  options: {enableMenu: false}
};

(() => {
const PB = window.PB = window.PB || {};
const el = (tag, className, text) => {
  const e = document.createElement(tag);
  if (className) e.className = className;
  if (text !== undefined) e.textContent = text;
  return e;
};

// ---------- 文本辅助 ----------
// 汉字 / 全角标点：换行拼接时不补空格，中文句子才不会多出缝隙。
const CJK_TAIL = /[\u2010-\u201F\u2026\u2E80-\u9FFF\u3000-\u303F\uFF00-\uFFEF]$/;
const CJK_HEAD = /^[\u2010-\u201F\u2026\u2E80-\u9FFF\u3000-\u303F\uFF00-\uFFEF]/;
const ESCAPABLE = /[\\`*_{}\[\]()#+\-.!|$>~<"':/]/;

// 寻找转义之外的下标；找不到返回 -1。
function findClose(s, marker, from) {
  for (let i = from; i <= s.length - marker.length; i++) {
    if (s[i] === '\\') { i++; continue; }
    if (s.startsWith(marker, i)) return i;
  }
  return -1;
}

// $ 的收尾位置：前面不能是空白（`$ a $` 不是公式），后面不能紧跟数字（避免把 "$5 和 $10" 当成公式）。
function findDollarClose(s, from, display) {
  for (let i = from; i < s.length; i++) {
    if (s[i] === '\\') { i++; continue; }
    if (s[i] !== '$') continue;
    if (display) { if (s[i + 1] === '$') return i; continue; }
    if (/\s/.test(s[i - 1] || '')) continue;
    if (/\d/.test(s[i + 1] || '')) continue;
    return i;
  }
  return -1;
}

// ---------- 行内 ----------
function mathNode(tex, display) {
  const m = el('span', display ? 'math math-display' : 'math', display ? `\\[${tex}\\]` : `\\(${tex}\\)`);
  m.dataset.tex = display ? `$$${tex}$$` : `$${tex}$`;
  return m;
}

function inline(text, parent) {
  const s = String(text ?? '');
  let buffer = '';
  const flush = () => { if (buffer) { parent.append(document.createTextNode(buffer)); buffer = ''; } };

  for (let i = 0; i < s.length;) {
    const c = s[i];

    if (c === '\n') { flush(); parent.append(el('br')); i++; continue; }

    // 反斜杠：行尾是硬换行；\( \) \[ \] 是 TeX；其余标点按转义字符处理。
    if (c === '\\') {
      const n = s[i + 1];
      if (n === '\n') { flush(); parent.append(el('br')); i += 2; continue; }
      if (n === '(' || n === '[') {
        const close = n === '(' ? '\\)' : '\\]';
        const end = s.indexOf(close, i + 2);
        if (end > i + 1) {
          flush();
          parent.append(mathNode(s.slice(i + 2, end).trim(), n === '['));
          i = end + 2; continue;
        }
      }
      if (n && ESCAPABLE.test(n)) { buffer += n; i += 2; continue; }
      buffer += c; i++; continue;
    }

    // 行内代码
    if (c === '`') {
      let ticks = 1; while (s[i + ticks] === '`') ticks++;
      const fence = '`'.repeat(ticks), end = s.indexOf(fence, i + ticks);
      if (end > i) {
        flush();
        const body = s.slice(i + ticks, end).replace(/\n/g, ' ');
        parent.append(el('code', '', body.length > 1 && /^ .* $/.test(body) ? body.slice(1, -1) : body));
        i = end + ticks; continue;
      }
    }

    // 公式
    if (c === '$') {
      const display = s[i + 1] === '$';
      const marker = display ? '$$' : '$';
      const start = i + marker.length;
      const opens = display || (start < s.length && !/\s/.test(s[start]));
      if (opens) {
        const end = findDollarClose(s, start, display);
        const body = end > start ? s.slice(start, end) : '';
        if (body.trim()) {
          flush();
          parent.append(mathNode(body.trim(), display));
          i = end + marker.length; continue;
        }
      }
    }

    // 加粗 / 斜体 / 删除线
    if (c === '*' || c === '_') {
      const triple = s.startsWith(c.repeat(3), i);
      const strong = s.startsWith(c.repeat(2), i);
      if (triple) {
        const end = findClose(s, c.repeat(3), i + 3);
        if (end > i + 3) {
          flush();
          const wrapper = el('strong');
          const em = el('em');
          inline(s.slice(i + 3, end), em);
          wrapper.append(em);
          parent.append(wrapper); i = end + 3; continue;
        }
      }
      if (strong) {
        const end = findClose(s, c.repeat(2), i + 2);
        if (end > i + 2) {
          flush();
          const node = el('strong');
          inline(s.slice(i + 2, end), node);
          parent.append(node); i = end + 2; continue;
        }
      }
      const wordBoundary = c === '_'
        ? !(/[\w\u4e00-\u9fff]/.test(s[i - 1] || '') || /[\w\u4e00-\u9fff]/.test(s[i + 1] || ''))
        : true;
      if (wordBoundary && s[i + 1] && !/\s/.test(s[i + 1])) {
        const end = findClose(s, c, i + 1);
        if (end > i + 1 && !/\s/.test(s[end - 1] || '')) {
          flush();
          const node = el('em');
          inline(s.slice(i + 1, end), node);
          parent.append(node); i = end + 1; continue;
        }
      }
    }
    if (c === '~' && s[i + 1] === '~') {
      const end = s.indexOf('~~', i + 2);
      if (end > i + 2) {
        flush();
        const node = el('del');
        inline(s.slice(i + 2, end), node);
        parent.append(node); i = end + 2; continue;
      }
    }

    // 自动链接 <https://…>
    if (c === '<') {
      const end = s.indexOf('>', i + 1);
      const url = end > i ? s.slice(i + 1, end) : '';
      if (/^https?:\/\/[^\s<>]+$/i.test(url)) {
        flush();
        const a = el('a', '', url);
        a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer';
        parent.append(a); i = end + 1; continue;
      }
    }

    // 链接 / 图片
    if (c === '[' || (c === '!' && s[i + 1] === '[')) {
      const image = c === '!', open = image ? i + 1 : i;
      const close = findClose(s, ']', open + 1);
      if (close > open && s[close + 1] === '(') {
        const end = s.indexOf(')', close + 2);
        if (end > close) {
          flush();
          const label = s.slice(open + 1, close);
          const target = s.slice(close + 2, end).trim().split(/\s+/)[0];
          if (image) {
            parent.append(el('span', 'pb-md-noimage', label ? `［图片：${label}］` : '［图片］'));
          } else if (/^https?:\/\/[^\s]+$/i.test(target)) {
            const a = el('a');
            a.href = target; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.title = target;
            inline(label || target, a);
            parent.append(a);
          } else {
            const span = el('span');
            inline(label, span);
            parent.append(span);
          }
          i = end + 1; continue;
        }
      }
    }

    buffer += c; i++;
  }
  flush();
  return parent;
}

// 段落换行拼接：中文之间不加空格，西文之间加一个，行尾两个空格或反斜杠表示硬换行。
function joinLines(rawLines) {
  let out = '', hardBreak = false;
  for (const raw of rawLines) {
    let line = raw.trim();
    if (!line) continue;
    const hard = / {2,}$/.test(raw) || /\\$/.test(raw);
    if (/\\$/.test(line)) line = line.slice(0, -1).trimEnd();
    if (!out) out = line;
    else if (hardBreak) out += '\n' + line;
    else out += (CJK_TAIL.test(out) || CJK_HEAD.test(line)) ? line : ' ' + line;
    hardBreak = hard;
  }
  return out;
}

// ---------- 块级 ----------
const reFence = /^(\s{0,3})(`{3,}|~{3,})\s*([^`\s]*)\s*$/;
const reAtx = /^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$/;
const reHr = /^\s{0,3}([-*_])(?:\s*\1){2,}\s*$/;
const reQuote = /^\s{0,3}>\s?/;
const reBullet = /^(\s*)([-*+])\s+(.*)$/;
const reOrdered = /^(\s*)(\d{1,9})[.)]\s+(.*)$/;
const reTableSep = /^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$/;

const listItem = line => {
  let m = reBullet.exec(line);
  if (m) return {indent: m[1].length, ordered: false, number: 1, content: m[3], column: line.length - m[3].length};
  m = reOrdered.exec(line);
  if (m) return {indent: m[1].length, ordered: true, number: parseInt(m[2], 10), content: m[3], column: line.length - m[3].length};
  return null;
};

const isTableRow = line => line.includes('|');
function splitRow(line) {
  let s = line.trim();
  if (s.startsWith('|')) s = s.slice(1);
  if (s.endsWith('|') && !s.endsWith('\\|')) s = s.slice(0, -1);
  const cells = []; let cur = '';
  for (let i = 0; i < s.length; i++) {
    if (s[i] === '\\' && s[i + 1] === '|') { cur += '|'; i++; }
    else if (s[i] === '|') { cells.push(cur.trim()); cur = ''; }
    else cur += s[i];
  }
  cells.push(cur.trim());
  return cells;
}

// 能否打断段落 / 懒续行
function startsBlock(line, next) {
  if (reFence.test(line) || reAtx.test(line) || reHr.test(line) || reQuote.test(line)) return true;
  if (/^\s*\$\$/.test(line) || /^\s*\\\[/.test(line)) return true;
  if (listItem(line)) return true;
  if (next !== undefined && isTableRow(line) && reTableSep.test(next) && next.includes('-')) return true;
  return false;
}

function heading(parent, level, text) {
  const size = Math.min(Math.max(level, 1), 4);
  const h = el(`h${size}`, `pb-md-h${size}`);
  inline(text, h);
  parent.append(h);
}

function codeFence(lines, i, m, parent) {
  const indent = m[1].length, fence = m[2], info = m[3] || '';
  const body = [];
  const close = new RegExp(`^\\s{0,3}${fence[0] === '`' ? '`' : '~'}{${fence.length},}\\s*$`);
  i++;
  while (i < lines.length && !close.test(lines[i])) {
    body.push(lines[i].replace(new RegExp(`^\\s{0,${indent}}`), ''));
    i++;
  }
  if (i < lines.length) i++;
  const pre = el('pre', 'pb-md-code');
  const code = el('code', '', body.join('\n'));
  if (info) { code.dataset.lang = info; pre.dataset.lang = info; }
  pre.append(code);
  parent.append(pre);
  return i;
}

// $$ … $$ / \[ … \]，可以跨行；找不到收尾时按普通段落处理，避免吞掉后文。
function displayMath(lines, i, open, close, parent) {
  const first = lines[i].trim().slice(open.length);
  let body = [], end = -1;
  if (first.includes(close)) {
    body.push(first.slice(0, first.lastIndexOf(close)));
    end = i + 1;
  } else {
    if (first.trim()) body.push(first);
    let k = i + 1;
    while (k < lines.length) {
      const line = lines[k];
      if (line.trim().endsWith(close)) {
        const head = line.trim().slice(0, -close.length);
        if (head.trim()) body.push(head);
        end = k + 1; break;
      }
      body.push(line);
      k++;
    }
  }
  if (end < 0) return -1;
  const tex = body.join('\n').trim();
  const node = el('div', 'math-block', `\\[${tex}\\]`);
  node.dataset.tex = `$$${tex}$$`;
  parent.append(node);
  return end;
}

function quote(lines, i, parent) {
  const body = [];
  while (i < lines.length) {
    const line = lines[i];
    if (reQuote.test(line)) { body.push(line.replace(reQuote, '')); i++; continue; }
    if (!line.trim()) {
      if (reQuote.test(lines[i + 1] || '')) { body.push(''); i++; continue; }
      break;
    }
    if (startsBlock(line, lines[i + 1])) break;
    body.push(line); i++;   // 懒续行
  }
  const q = el('blockquote', 'pb-md-quote');
  blocks(body, q);
  parent.append(q);
  return i;
}

function table(lines, i, parent) {
  const head = splitRow(lines[i]);
  const aligns = splitRow(lines[i + 1]).map(cell => {
    const left = cell.startsWith(':'), right = cell.endsWith(':');
    return left && right ? 'center' : right ? 'right' : left ? 'left' : '';
  });
  i += 2;
  const rows = [];
  while (i < lines.length && lines[i].trim() && isTableRow(lines[i])) rows.push(splitRow(lines[i++]));

  const wrap = el('div', 'pb-md-table-wrap');
  const tableEl = el('table', 'pb-md-table');
  const thead = el('thead'), htr = el('tr');
  head.forEach((cell, k) => {
    const th = el('th');
    if (aligns[k]) th.style.textAlign = aligns[k];
    inline(cell, th);
    htr.append(th);
  });
  thead.append(htr);
  tableEl.append(thead);
  const tbody = el('tbody');
  rows.forEach(cells => {
    const tr = el('tr');
    for (let k = 0; k < head.length; k++) {
      const td = el('td');
      if (aligns[k]) td.style.textAlign = aligns[k];
      inline(cells[k] || '', td);
      tr.append(td);
    }
    tbody.append(tr);
  });
  tableEl.append(tbody);
  wrap.append(tableEl);
  parent.append(wrap);
  return i;
}

function list(lines, i, parent) {
  const first = listItem(lines[i]);
  const ordered = first.ordered, indent = first.indent;
  const node = el(ordered ? 'ol' : 'ul', 'pb-md-list');
  if (ordered && first.number !== 1) node.start = first.number;
  let loose = false;

  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) {
      let k = i + 1;
      while (k < lines.length && !lines[k].trim()) k++;
      const next = k < lines.length ? listItem(lines[k]) : null;
      if (next && next.ordered === ordered && Math.abs(next.indent - indent) <= 1) { loose = true; i = k; continue; }
      break;
    }
    const item = listItem(line);
    if (!item || item.ordered !== ordered || Math.abs(item.indent - indent) > 1) break;

    const body = [item.content];
    const column = item.column;
    i++;
    while (i < lines.length) {
      const cur = lines[i];
      if (!cur.trim()) {
        // 空行之后：只有缩进够深（属于本项）或紧跟嵌套列表时才算同一项，
        // 否则列表结束，后面的段落不应被吞进 <li>。
        let k = i + 1;
        while (k < lines.length && !lines[k].trim()) k++;
        if (k >= lines.length) { i = k; break; }
        const ahead = lines[k];
        const aheadItem = listItem(ahead);
        const aheadLead = ahead.length - ahead.trimStart().length;
        const continues = aheadItem ? aheadItem.indent > indent + 1 : aheadLead >= column && !startsBlock(ahead, lines[k + 1]);
        if (!continues) break;
        body.push('');
        i = k;
        continue;
      }
      const nested = listItem(cur);
      if (nested && nested.indent <= indent + 1) break;
      const lead = cur.length - cur.trimStart().length;
      if (nested || lead > indent) { body.push(cur.slice(Math.min(column, lead))); i++; continue; }
      if (startsBlock(cur, lines[i + 1])) break;
      body.push(cur.trim()); i++;   // 懒续行
    }

    const li = el('li');
    blocks(body, li);
    node.append(li);
  }

  if (loose) node.classList.add('pb-md-loose');
  parent.append(node);
  return i;
}

function blocks(lines, parent) {
  for (let i = 0; i < lines.length;) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }
    let m;

    if ((m = reFence.exec(line))) { i = codeFence(lines, i, m, parent); continue; }
    if (/^\s*\$\$/.test(line)) {
      // 同一行的 $$…$$ 后面还有正文时留给段落（行内公式自己会显示成块级），避免吞掉后半句。
      const trimmed = line.trim(), closeAt = trimmed.indexOf('$$', 2);
      if (closeAt < 2 || !trimmed.slice(closeAt + 2).trim()) {
        const next = displayMath(lines, i, '$$', '$$', parent);
        if (next > 0) { i = next; continue; }
      }
    }
    if (/^\s*\\\[/.test(line)) { const next = displayMath(lines, i, '\\[', '\\]', parent); if (next > 0) { i = next; continue; } }
    if ((m = reAtx.exec(line))) { heading(parent, m[1].length, m[2]); i++; continue; }

    // setext 标题：文字下一行是 === 或 ---
    if (i + 1 < lines.length && !listItem(line) && !isTableRow(line)) {
      const under = lines[i + 1].trim();
      if (/^={2,}$/.test(under)) { heading(parent, 1, line.trim()); i += 2; continue; }
      if (/^-{2,}$/.test(under)) { heading(parent, 2, line.trim()); i += 2; continue; }
    }

    if (reHr.test(line)) { parent.append(el('hr', 'pb-md-hr')); i++; continue; }
    if (reQuote.test(line)) { i = quote(lines, i, parent); continue; }
    if (listItem(line)) { i = list(lines, i, parent); continue; }
    if (i + 1 < lines.length && isTableRow(line) && reTableSep.test(lines[i + 1]) && lines[i + 1].includes('-')) {
      i = table(lines, i, parent); continue;
    }

    const para = [];
    while (i < lines.length && lines[i].trim() && !(para.length && startsBlock(lines[i], lines[i + 1]))) para.push(lines[i++]);
    const p = el('p', 'pb-md-p');
    inline(joinLines(para), p);
    parent.append(p);
  }
  return parent;
}

function renderStatement(markdownText) {
  const fragment = document.createDocumentFragment();
  blocks(String(markdownText ?? '').replace(/\r\n?/g, '\n').split('\n'), fragment);
  return fragment;
}
window.renderStatement = renderStatement;

// ---------- 数学 ----------
function fallbackMath(root) {
  root.querySelectorAll('.math, .math-block').forEach(m => {
    if (m.querySelector('mjx-container')) return;
    m.textContent = m.dataset.tex;
    m.classList.add('math-fallback');
    m.title = '公式渲染器不可用，显示原文';
  });
}

// MathJax 是 defer 加载的，题面可能比它先到；最多等 15 秒再降级显示原文。
function waitForMathJax(timeout = 15000) {
  const start = Date.now();
  return new Promise(resolve => {
    const check = () => {
      const MJ = window.MathJax;
      if (MJ && MJ.startup && MJ.startup.promise) return resolve(MJ);
      if (Date.now() - start >= timeout) return resolve(null);
      setTimeout(check, 50);
    };
    check();
  });
}

function typeset(root) {
  if (!root.querySelector('.math, .math-block')) return Promise.resolve();
  return waitForMathJax()
    .then(MJ => (MJ && MJ.typesetPromise ? MJ.typesetPromise([root]) : null))
    .catch(() => null)
    .then(() => fallbackMath(root));
}
PB.typesetMath = typeset;

// 函数式提交的仓颉包名：API 直接返回 problem.package，旧接口回退到 driver 里的 package 声明。
PB.cangjiePackage = problem => {
  if (!problem || !(problem.modes?.cangjie || []).includes('function')) return '';
  if (problem.package) return problem.package;
  const m = /^\s*package\s+([A-Za-z_][\w.]*)/m.exec(problem.drivers?.cangjie || '');
  return m ? m[1] : '';
};

// ---------- 整张题面 ----------
const cache = new Map();

function samplePane(label, text) {
  const pane = el('div', 'pb-sample-pane');
  const head = el('div', 'pb-sample-head');
  head.append(el('span', '', label));
  const copy = el('button', 'pb-copy', '复制');
  copy.type = 'button';
  copy.setAttribute('aria-label', `复制${label}`);
  copy.onclick = () => PB.copy(text, copy);
  head.append(copy);
  pane.append(head, el('pre', 'pb-sample-pre', text));
  return pane;
}

function buildStatement(problem, lang) {
  const zh = lang === 'zh';
  const other = zh ? 'en' : 'zh';
  const pick = (obj, fallback = '') => {
    if (!obj) return fallback;
    if (typeof obj === 'string') return obj;
    return obj[lang] || obj[other] || fallback;
  };
  const root = el('article', 'pb-statement-doc');
  root.lang = zh ? 'zh-CN' : 'en';

  const markdown = String(problem.statement?.[lang] || problem.statement?.[other] || '').trim();
  const body = renderStatement(markdown);

  const header = el('header', 'pb-statement-header');
  const firstHeading = body.firstElementChild?.tagName === 'H1' ? body.firstElementChild : null;
  const title = firstHeading || el('h1', 'pb-md-h1', pick(problem.title, problem.id));
  header.append(title);
  root.append(header);

  if (markdown) root.append(body);
  else root.append(el('p', 'pb-md-p pb-statement-empty', zh ? '本题暂无题面。' : 'No statement available.'));

  if ((problem.samples || []).length) {
    root.append(sectionLabel(zh ? '样例（标准输入 / 输出）' : 'Samples (stdin / stdout)'));
    problem.samples.forEach((sample, k) => {
      const card = el('section', 'pb-sample');
      card.setAttribute('aria-label', `${zh ? '样例' : 'Sample'} ${k + 1}`);
      card.append(el('div', 'pb-sample-title', `${zh ? '样例' : 'Sample'} ${k + 1}`));
      const grid = el('div', 'pb-sample-grid');
      grid.append(samplePane(zh ? '输入' : 'Input', sample.input || ''), samplePane(zh ? '输出' : 'Output', sample.output || ''));
      card.append(grid);
      const explain = pick(sample.explain);
      if (String(explain).trim()) {
        const note = el('div', 'pb-sample-explain');
        note.append(renderStatement(explain));
        card.append(note);
      }
      root.append(card);
    });
  }

  const hints = (problem.hints && (problem.hints[lang]?.length ? problem.hints[lang] : problem.hints[other])) || [];
  if (hints.length) {
    const details = el('details', 'pb-hints');
    details.append(el('summary', '', zh ? `提示（${hints.length}）` : `Hints (${hints.length})`));
    const ol = el('ol', 'pb-md-list');
    hints.forEach(hint => {
      const li = el('li');
      li.append(renderStatement(hint));
      ol.append(li);
    });
    details.append(ol);
    root.append(details);
  }

  const note = String(pick(problem.notes) || '').trim();
  if (note) root.append(el('p', 'pb-statement-note', note));
  return root;
}

function sectionLabel(text) {
  const h = el('h3', 'pb-section-label');
  if (!/[㐀-鿿]/.test(text)) h.classList.add('pb-latin');
  inline(text, h);
  return h;
}

// 把题面挂进 container；同一题同一语言只解析一次，切换语言保持滚动位置，换题回到顶部。
PB.showStatement = (container, scroller, problem, lang) => {
  const key = `${problem.id}\u0000${problem.storedAt || ''}\u0000${lang}`;
  let doc = cache.get(key), fresh = false;
  if (!doc) { doc = buildStatement(problem, lang); cache.set(key, doc); fresh = true; }
  const top = fresh ? 0 : scroller.scrollTop;
  container.replaceChildren(doc);
  scroller.scrollTop = top;
  if (fresh) typeset(doc);
  return doc;
};
PB.forgetStatement = id => { for (const k of cache.keys()) if (k.startsWith(id + '\u0000')) cache.delete(k); };
})();
