'use strict';
// 题库编辑器：新建题目（只带测试数据，自己程序自判）与编辑已有题目（元数据 / 题面 / 测试数据）。
(() => {
const PB = window.PB = window.PB || {};
const byId = id => document.getElementById(id);
const el = (...a) => PB.el(...a);

// 与后端 problems.cpp 的标签词表保持一致（题包校验会拒绝词表外的标签）。
const TAGS = ['模拟', '枚举', '排序', '二分', '贪心', '构造', '前缀和', '差分', '双指针', '滑动窗口', '哈希', '栈',
  '队列', '单调栈', '堆', '并查集', '树状数组', '线段树', '字符串', 'Trie', 'KMP', '图论', '最短路', '最小生成树',
  '拓扑排序', '二分图', '网络流', '树', '最近公共祖先', '动态规划', '背包', '区间DP', '状压DP', '数位DP', '树形DP',
  '数学', '数论', '组合数学', '概率期望', '计算几何', '位运算', '分治', '记忆化搜索', '高精度', '交互'];
const TOPICS = ['模拟与实现', '枚举与暴力', '排序与贪心', '二分与二分答案', '前缀和与差分', '双指针与滑动窗口',
  '哈希与计数', '栈与队列', '堆与优先队列', '并查集', '树状数组与线段树', '字符串与匹配', '图论与搜索',
  '最短路与最小生成树', '树与最近公共祖先', '线性动态规划', '背包与区间DP', '状压DP与树形DP', '数位DP与计数DP',
  '数学与数论', '组合数学与概率期望', '位运算与构造', '分治与递归', '计算几何与高精度', '综合思维与特殊裁判'];
const LANGS = [['cpp', 'C++'], ['cangjie', '仓颉'], ['python', 'Python'], ['java', 'Java']];

let state = null;   // {isNew, id, meta, cases, files, dirty}

const idPattern = /^[a-z0-9][a-z0-9-]{1,47}$/;
const norm = text => String(text || '').replace(/\r\n?/g, '\n');
const field = (label, node, hint) => {
  const wrap = el('label', 'pb-ed-field');
  wrap.append(el('span', '', label), node);
  if (hint) wrap.append(el('span', 'pb-ed-hint', hint));
  return wrap;
};
const wide = node => { node.dataset.wide = '1'; return node; };
const textarea = (value, placeholder, rows = 6) => {
  const t = el('textarea'); t.value = value || ''; t.spellcheck = false; t.placeholder = placeholder || '';
  t.rows = rows; t.wrap = 'off'; return t;
};
const input = (value, type = 'text', extra = {}) => {
  const i = el('input'); i.type = type; i.value = value ?? '';
  Object.assign(i, extra); return i;
};
const section = (title, hint) => {
  const box = el('section', 'pb-ed-section');
  const head = el('h3', '', title);
  if (hint) head.append(el('span', '', hint));
  box.append(head);
  return box;
};
function setStatus(text, tone) {
  const node = byId('pbEditorStatus');
  node.textContent = text || ''; node.dataset.state = tone || '';
}
function setBusy(busy) {
  byId('pbEditorSave').disabled = busy;
  byId('pbEditorVerifyBox').disabled = busy;
  byId('pbEditorForm').setAttribute('aria-busy', String(busy));
}

// ---- 打开 / 载入 ----
async function open(problemId) {
  const dialog = byId('pbEditorDialog');
  state = {isNew: !problemId, id: problemId || '', meta: null, cases: [], files: {}, loaded: false};
  byId('pbEditorEyebrow').textContent = problemId ? '编辑题目' : '新建题目';
  byId('pbEditorTitle').textContent = problemId ? `编辑 ${problemId}` : '题目编辑器';
  byId('pbEditorBody').replaceChildren(el('p', 'pb-ed-hint', '加载中…'));
  setStatus('');
  if (!dialog.open) dialog.showModal();
  if (problemId) {
    try {
      const raw = await PB.api('/api/problems/' + encodeURIComponent(problemId) + '/raw');
      state.meta = raw.meta || {};
      state.files = raw.files || {};
      state.cases = (raw.cases || []).map(c => ({id: c.id, input: norm(c.input), answer: norm(c.answer)}));
      state.groupCaseCount = (state.meta.groups || []).reduce((n, g) => n + ((g.cases || []).length), 0);
      state.loaded = true;
      render();
    } catch (e) {
      byId('pbEditorBody').replaceChildren(el('p', 'pb-ed-hint', '加载失败：' + e.message));
    }
  } else {
    state.meta = {schemaVersion: 2, title: {zh: '', en: ''}, difficulty: 1200, topic: '', tags: [], limits: {timeMs: 2000, memoryMb: 256},
      judgeType: 'standard', statement: {zh: '', en: ''}, samples: [], modes: {}, selfJudge: true, source: {}};
    state.loaded = true;
    render();
    setTimeout(() => byId('pbEdTitleZh')?.focus(), 30);
  }
}
function close() {
  const dialog = byId('pbEditorDialog');
  if (dialog.open) dialog.close();
  state = null;
}

// ---- 渲染 ----
function render() {
  const body = byId('pbEditorBody');
  const meta = state.meta;
  const parts = [];

  // 1. 基本信息
  const basic = section('基本信息', 'id、标题、难度、专题、限制与来源');
  const grid = el('div', 'pb-ed-grid');
  const idInput = input(state.id);
  idInput.id = 'pbEdId'; idInput.placeholder = '如 lc2270-split-array'; idInput.disabled = !state.isNew;
  idInput.oninput = () => { state.id = idInput.value.trim(); };
  grid.append(field('题目 id', idInput, state.isNew ? '小写字母/数字/短横线，2–48 字符，保存后不可改' : 'id 不可修改'));
  const zh = input(meta.title?.zh || ''); zh.id = 'pbEdTitleZh'; zh.oninput = () => { meta.title.zh = zh.value; };
  const en = input(meta.title?.en || ''); en.id = 'pbEdTitleEn'; en.oninput = () => { meta.title.en = en.value; };
  grid.append(field('中文标题', zh), field('English title', en));
  const difficulty = input(meta.difficulty ?? 1200, 'number', {min: 800, max: 3500, step: 100});
  difficulty.id = 'pbEdDifficulty'; difficulty.oninput = () => { meta.difficulty = Number(difficulty.value) || 0; };
  grid.append(field('难度（100 的倍数）', difficulty));
  const topicInput = input(meta.topic || ''); topicInput.id = 'pbEdTopic'; topicInput.setAttribute('list', 'pbTopicList'); topicInput.placeholder = '选一个专题，或自己写';
  topicInput.oninput = () => { meta.topic = topicInput.value.trim(); };
  grid.append(field('专题', topicInput));
  const timeMs = input(meta.limits?.timeMs ?? 2000, 'number', {min: 100, max: 60000, step: 100});
  timeMs.id = 'pbEdTime'; timeMs.oninput = () => { meta.limits = {...(meta.limits || {}), timeMs: Number(timeMs.value) || 0}; };
  const memoryMb = input(meta.limits?.memoryMb ?? 256, 'number', {min: 16, max: 4096, step: 16});
  memoryMb.id = 'pbEdMemory'; memoryMb.oninput = () => { meta.limits = {...(meta.limits || {}), memoryMb: Number(memoryMb.value) || 0}; };
  grid.append(field('时间限制（ms）', timeMs), field('内存限制（MiB）', memoryMb));
  const judge = el('select'); judge.id = 'pbEdJudge';
  Object.entries(PB.judgeNames).forEach(([value, label]) => { const o = el('option', '', label); o.value = value; judge.append(o); });
  judge.value = meta.judgeType || 'standard';
  judge.onchange = () => { meta.judgeType = judge.value; };
  grid.append(field('评判方式', judge, '普通=逐 token 比较；特殊=checker；函数=只写 solve'));
  const platform = el('select'); platform.id = 'pbEdPlatform';
  [['', '不标注'], ...Object.entries(PB.sourceLabels)].forEach(([value, label]) => { const o = el('option', '', label); o.value = value; platform.append(o); });
  platform.value = meta.source?.platform || '';
  const sourceId = input(meta.source?.id || ''); sourceId.id = 'pbEdSourceId'; sourceId.placeholder = '如 P1001 / 2270 / 1324D';
  const sourceUrl = input(meta.source?.url || ''); sourceUrl.id = 'pbEdSourceUrl'; sourceUrl.placeholder = 'https://…（可选）';
  platform.onchange = () => { meta.source = platform.value ? {...(meta.source || {}), platform: platform.value} : {}; };
  sourceId.oninput = () => { if (!meta.source) meta.source = {}; meta.source.id = sourceId.value.trim(); };
  sourceUrl.oninput = () => { if (!meta.source) meta.source = {}; meta.source.url = sourceUrl.value.trim(); };
  grid.append(field('题目来源', platform), field('来源编号', sourceId), field('来源链接', sourceUrl));
  basic.append(grid);

  // 标签
  const tagWrap = el('div', 'pb-ed-chips');
  const tags = new Set(meta.tags || []);
  TAGS.forEach(t => {
    const b = el('button', 'pb-ed-chip', t); b.type = 'button'; b.setAttribute('aria-pressed', String(tags.has(t)));
    b.onclick = () => {
      if (tags.has(t)) tags.delete(t); else if (tags.size < 3) tags.add(t); else return PB.toast('最多 3 个标签');
      meta.tags = [...tags]; b.setAttribute('aria-pressed', String(tags.has(t)));
    };
    tagWrap.append(b);
  });
  basic.append(field('标签（1–3 个）', tagWrap));
  parts.push(basic);

  // 2. 题面
  const statement = section('题面', 'Markdown + LaTeX，中英各一份');
  const stGrid = el('div', 'pb-ed-grid');
  const zhStatement = textarea(meta.statement?.zh, '# 题目\n\n读入…', 12); zhStatement.oninput = () => { meta.statement.zh = zhStatement.value; };
  const enStatement = textarea(meta.statement?.en, '# Problem\n\nRead…', 12); enStatement.oninput = () => { meta.statement.en = enStatement.value; };
  stGrid.append(wide(field('中文题面', zhStatement)), wide(field('English statement', enStatement)));
  statement.append(stGrid);
  parts.push(statement);

  // 3. 样例
  const samples = section('样例', '只展示，不判分（判分用下面的测试数据）');
  const sampleList = el('div', 'pb-ed-files');
  (meta.samples || []).forEach((sample, index) => sampleList.append(sampleRow(sample, index)));
  const sampleAdd = el('button', 'pb-btn', '+ 添加样例'); sampleAdd.type = 'button';
  sampleAdd.onclick = () => {
    meta.samples = [...(meta.samples || []), {input: '', output: '', explain: {zh: ''}}];
    render();
  };
  const tools = el('div', 'pb-ed-tools'); tools.append(sampleAdd);
  samples.append(tools, sampleList);
  parts.push(samples);

  // 4. 测试数据
  const caseSection = section('测试数据', '每一条是一对 .in / .ans；判题时一个用例一个进程');
  const truncated = !state.isNew && state.groupCaseCount > state.cases.length;
  if (truncated) caseSection.append(el('p', 'pb-ed-hint', `题包里的测试数据较大（共 ${state.groupCaseCount} 组，只载入 ${state.cases.length} 组用于预览）。保存时不会改动测试数据。`));
  const caseList = el('div', 'pb-ed-files');
  if (!truncated) state.cases.forEach((item, index) => caseList.append(caseRow(item, index)));
  const caseTools = el('div', 'pb-ed-tools');
  if (!truncated) {
    const add = el('button', 'pb-btn', '+ 添加测试数据'); add.type = 'button';
    add.onclick = () => {
      state.cases.push({id: nextCaseId(), input: '', answer: ''});
      render();
    };
    const fromSamples = el('button', 'pb-btn', '用样例生成'); fromSamples.type = 'button';
    fromSamples.onclick = () => {
      const have = new Set(state.cases.map(c => norm(c.input).trim()));
      const add = (meta.samples || []).filter(s => norm(s.input).trim() && !have.has(norm(s.input).trim()))
        .map(s => ({id: nextCaseId(), input: norm(s.input), answer: norm(s.output)}));
      if (!add.length) return PB.toast('样例都已在测试数据里了');
      state.cases.push(...add); render();
    };
    caseTools.append(add, fromSamples);
    caseSection.append(caseTools);
    // 从本地目录批量导入 <名字>.in / <名字>.ans —— 自建题最常见的就是「我手上已经有一套数据」。
    const dirRow = el('div', 'pb-ed-tools');
    const dirInput = input('');
    dirInput.id = 'pbEdDir';
    dirInput.placeholder = '数据目录绝对路径，例如 E:\\data\\problem1（里面有成对的 .in 与 .ans）';
    dirInput.style.flex = '1 1 340px';
    const scan = el('button', 'pb-btn', '从目录导入测试数据'); scan.type = 'button';
    scan.onclick = async () => {
      const directory = dirInput.value.trim();
      if (!directory) { setStatus('请先填写数据目录', 'error'); return; }
      if (state.cases.length && !confirm(`当前已有 ${state.cases.length} 组测试数据，用目录里的数据替换掉？`)) return;
      scan.disabled = true; setStatus('正在读取目录…', 'busy');
      try {
        const result = await PB.api('/api/problems/scan-cases', {body: {directory}});
        state.cases = (result.cases || []).map(c => ({id: c.id, input: norm(c.input), answer: norm(c.answer)}));
        render();
        setStatus(`已从 ${result.directory} 导入 ${state.cases.length} 组测试数据`, 'ok');
      } catch (e) { setStatus(e.message, 'error'); }
      finally { scan.disabled = false; }
    };
    dirRow.append(dirInput, scan);
    caseSection.append(dirRow);
  }
  caseSection.append(caseList);
  parts.push(caseSection);

  // 5. 参考解（新建时可选，编辑时只读展示）
  const files = section('参考解与题包文件', state.isNew ? '不填就按「自判题」保存：只存测试数据，判题直接比对 .ans' : '已有题包文件，保存时原样保留');
  if (state.isNew) {
    const note = el('p', 'pb-ed-hint', '要出正式题（函数式 / 特殊裁判），把四种语言的完整参考程序填进来；留空则保存为自判题。');
    files.append(note);
    state.solutions = state.solutions || {};
    const solved = el('div', 'pb-ed-files');
    LANGS.forEach(([lang, name]) => {
      const area = textarea(state.solutions[lang] || '', `${name} 完整参考程序（自带 main）`, 8);
      area.oninput = () => { state.solutions[lang] = area.value; };
      const details = el('details'); details.append(el('summary', '', `${name} 参考解（可选）`), area);
      solved.append(details);
    });
    files.append(solved);
  } else {
    const names = Object.keys(state.files || {}).sort();
    files.append(el('p', 'pb-ed-hint', names.length ? `题包内代码文件：${names.join('、')}` : '题包里没有代码文件（自判题）。'));
    const details = el('details'); details.append(el('summary', '', '查看 / 下载题包文件'));
    names.forEach(name => {
      const pre = el('pre', 'pb-error-details', state.files[name]); pre.tabIndex = 0;
      details.append(el('p', 'pb-ed-hint', name), pre);
    });
    files.append(details);
  }
  parts.push(files);

  // 专题候选
  const dl = el('datalist'); dl.id = 'pbTopicList';
  const known = [...new Set([...TOPICS, ...(PB.list?.topics?.() || [])])];
  known.forEach(t => { const o = el('option'); o.value = t; dl.append(o); });
  parts.push(dl);

  body.replaceChildren(...parts);
  byId('pbEditorVerify').hidden = false;
}
function nextCaseId() {
  const used = new Set(state.cases.map(c => c.id));
  for (let i = 1; i < 100; i++) { const id = String(i).padStart(2, '0'); if (!used.has(id)) return id; }
  return 'c' + Date.now();
}
function sampleRow(sample, index) {
  const row = el('div', 'pb-ed-case'); row.dataset.sample = String(index);
  const head = el('div', 'pb-ed-case-head', `样例 ${index + 1}`);
  const remove = el('button', 'text-button', '删除'); remove.type = 'button'; remove.style.marginLeft = 'auto';
  remove.onclick = () => { state.meta.samples.splice(index, 1); render(); };
  head.append(remove);
  const grid = el('div', 'pb-ed-case-grid');
  const inArea = textarea(sample.input, '样例输入', 5); inArea.dataset.role = 'input'; inArea.oninput = () => { sample.input = inArea.value; };
  const outArea = textarea(sample.output, '样例输出', 5); outArea.dataset.role = 'output'; outArea.oninput = () => { sample.output = outArea.value; };
  grid.append(field('输入', inArea), field('输出', outArea));
  row.append(head, grid);
  return row;
}
function caseRow(item, index) {
  const row = el('div', 'pb-ed-case'); row.dataset.caseId = item.id;
  const head = el('div', 'pb-ed-case-head');
  const idInput = input(item.id); idInput.className = 'pb-ed-case-id'; idInput.setAttribute('aria-label', '用例 id');
  idInput.oninput = () => { item.id = idInput.value.trim(); row.dataset.caseId = item.id; };
  head.append(el('span', '', `#${index + 1}`), idInput);
  const remove = el('button', 'text-button', '删除'); remove.type = 'button'; remove.style.marginLeft = 'auto';
  remove.onclick = () => { state.cases.splice(index, 1); render(); };
  head.append(remove);
  const grid = el('div', 'pb-ed-case-grid');
  const inArea = textarea(item.input, '输入（.in）', 6); inArea.dataset.role = 'input'; inArea.oninput = () => { item.input = inArea.value; };
  const ansArea = textarea(item.answer, '预期输出（.ans）', 6); ansArea.dataset.role = 'answer'; ansArea.oninput = () => { item.answer = ansArea.value; };
  grid.append(field('输入', inArea), field('预期输出', ansArea));
  row.append(head, grid);
  return row;
}

// ---- 保存 ----
function payload() {
  const meta = state.meta;
  const body = {
    id: state.id,
    edit: !state.isNew,
    title: {zh: (meta.title?.zh || '').trim(), en: (meta.title?.en || '').trim()},
    difficulty: Number(meta.difficulty) || 0,
    topic: (meta.topic || '').trim() || '未分类',
    tags: [...(meta.tags || [])],
    limits: {timeMs: Number(meta.limits?.timeMs) || 0, memoryMb: Number(meta.limits?.memoryMb) || 0},
    judgeType: meta.judgeType || 'standard',
    statement: {zh: norm(meta.statement?.zh), en: norm(meta.statement?.en)},
    samples: (meta.samples || []).filter(s => norm(s.input).trim() && norm(s.output).trim())
      .map(s => ({input: norm(s.input), output: norm(s.output)}))
  };
  if (meta.source?.platform) {
    const source = {platform: meta.source.platform};
    if ((meta.source.id || '').trim()) source.id = meta.source.id.trim();
    if ((meta.source.url || '').trim()) source.url = meta.source.url.trim();
    body.source = source;
  }
  const truncated = !state.isNew && state.groupCaseCount > state.cases.length;
  if (!truncated) body.cases = state.cases.map(c => ({id: c.id, input: norm(c.input), answer: norm(c.answer)}));
  if (state.isNew) {
    const provided = LANGS.filter(([lang]) => (state.solutions?.[lang] || '').trim());
    if (provided.length) {
      body.files = {};
      body.modes = {};
      provided.forEach(([lang]) => {
        const ext = {cpp: 'cpp', cangjie: 'cj', python: 'py', java: 'java'}[lang];
        body.files['solution.' + ext] = state.solutions[lang];
        body.modes[lang] = ['full'];
      });
    }
  }
  return body;
}
function validate(body) {
  if (!idPattern.test(body.id)) return '题目 id 不合法：需要 2–48 位小写字母/数字/短横线，且以字母或数字开头。';
  if (!body.title.zh) return '请填写中文标题。';
  if (!body.title.en) return '请填写英文标题。';
  if (!(body.difficulty >= 800 && body.difficulty <= 3500 && body.difficulty % 100 === 0)) return '难度需要是 800–3500 之间 100 的整数倍。';
  if (!body.tags.length || body.tags.length > 3) return '请选择 1–3 个标签。';
  if (!(body.limits.timeMs >= 100 && body.limits.timeMs <= 60000)) return '时间限制需要在 100–60000 ms 之间。';
  if (!(body.limits.memoryMb >= 16 && body.limits.memoryMb <= 4096)) return '内存限制需要在 16–4096 MiB 之间。';
  if (!body.statement.zh.trim()) return '请填写中文题面。';
  if (!body.statement.en.trim()) return '请填写英文题面。';
  if (!body.samples.length) return '至少需要一个样例（题面样例只做展示，但题包要求 1–5 个）。';
  if (body.cases && !body.cases.length) return '至少需要一条测试数据。';
  if (body.cases) for (const c of body.cases) {
    if (!/^[a-z0-9][a-z0-9_-]{0,15}$/.test(c.id)) return `测试数据 id「${c.id}」不合法：小写字母/数字/_/-，最多 16 位。`;
    if (!norm(c.answer).trim()) return `测试数据 ${c.id} 的预期输出为空。`;
  }
  if (body.id === 'import') return 'id 不能是 import。';
  return '';
}
async function save() {
  const body = payload();
  const problem = validate(body);
  if (problem) { setStatus(problem, 'error'); return; }
  const verify = byId('pbEditorVerifyBox').checked;
  setBusy(true);
  setStatus(verify ? '正在保存并自检（编译参考解、跑测试数据，约 10–60 秒）…' : '正在保存…', 'busy');
  try {
    const result = await PB.api('/api/problems/save', {body});
    const solutions = result.verification?.solutions || {};
    const summary = Object.entries(solutions).map(([l, r]) => `${PB.languageNames[l] || l} ${r.score}`).join('，');
    setStatus(`已${result.edit ? '更新' : '保存'} ${result.id}${summary ? `（参考答案 ${summary}）` : result.selfJudge ? '（自判题）' : ''}`, 'ok');
    PB.forgetProblem?.(result.id);
    await PB.list.refresh();
    setTimeout(close, 600);
  } catch (e) {
    const details = e.data?.details;
    const lines = Array.isArray(details) && details.length ? details.map((d, i) => `${i + 1}. ${d.message}`).join('\n') : e.message;
    setStatus('保存失败：' + (e.data?.error || e.message), 'error');
    const box = byId('pbEditorBody');
    let pre = byId('pbEdSaveError');
    if (!pre) {
      pre = el('pre', 'pb-error-details'); pre.id = 'pbEdSaveError'; pre.tabIndex = 0;
      box.append(pre);
    }
    pre.textContent = lines;
    pre.scrollIntoView({block: 'nearest'});
  } finally {
    setBusy(false);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  byId('pbEditorSave').onclick = save;
  document.querySelectorAll('[data-close-editor]').forEach(b => b.onclick = close);
  byId('pbEditorDialog').addEventListener('cancel', e => { e.preventDefault(); close(); });
  byId('pbEditorDialog').addEventListener('click', e => {
    if (e.target === byId('pbEditorDialog')) close();   // 点遮罩关闭
  });
  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    if (byId('pbEditorDialog').open) { e.preventDefault(); close(); }
  });
});
PB.editor = {open, close, isOpen: () => !!byId('pbEditorDialog')?.open};
})();
