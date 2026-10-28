import {EditorSelection} from "@codemirror/state";
import {EditorView, keymap} from "@codemirror/view";
import {indentMore, indentLess, moveLineUp, moveLineDown, copyLineUp, copyLineDown, toggleComment, undo} from "@codemirror/commands";

function selectNextOccurrence(view) {
  const {state} = view, main = state.selection.main;
  if (main.empty) {
    const word = state.wordAt(main.head);
    if (word) view.dispatch({selection: EditorSelection.single(word.from, word.to)});
    return true;
  }
  const query = state.sliceDoc(main.from, main.to);
  if (!query) return true;
  const ranges = state.selection.ranges.slice();
  const from = Math.max(...ranges.map(range => range.to));
  const doc = state.doc.toString();
  let index = doc.indexOf(query, from);
  if (index < 0) index = doc.indexOf(query);
  if (index >= 0 && !ranges.some(range => range.from === index && range.to === index + query.length)) ranges.push(EditorSelection.range(index, index + query.length));
  view.dispatch({selection: EditorSelection.create(ranges, ranges.length - 1), scrollIntoView: true});
  return true;
}

function selectAllOccurrences(view) {
  const {state} = view, main = state.selection.main;
  const range = main.empty ? state.wordAt(main.head) : main;
  if (!range) return true;
  const query = state.sliceDoc(range.from, range.to), doc = state.doc.toString(), ranges = [];
  let index = 0;
  while (query && (index = doc.indexOf(query, index)) >= 0) {
    ranges.push(EditorSelection.range(index, index + query.length)); index += query.length;
  }
  if (ranges.length) view.dispatch({selection: EditorSelection.create(ranges)});
  return true;
}

export const vscodeKeymap = keymap.of([
  {key: "Mod-d", run: selectNextOccurrence, preventDefault: true},
  {key: "Mod-Shift-l", run: selectAllOccurrences, preventDefault: true},
  {key: "Mod-/", run: toggleComment},
  {key: "Mod-[", run: indentLess},
  {key: "Mod-]", run: indentMore},
  {key: "Alt-ArrowUp", run: moveLineUp},
  {key: "Alt-ArrowDown", run: moveLineDown},
  {key: "Shift-Alt-ArrowUp", run: copyLineUp},
  {key: "Shift-Alt-ArrowDown", run: copyLineDown}
]);

function vimExtension(onMode) {
  let mode = "normal", pending = "", count = "", visualAnchor = null, register = "";
  const setMode = (view, next) => {
    mode = next; pending = ""; count = ""; onMode?.(next.toUpperCase());
    view.contentDOM.dataset.vimMode = next;
    if (next !== "visual") visualAnchor = null;
    view.contentDOM.style.caretColor = "";
  };
  const selection = (view, pos, anchor = pos) => view.dispatch({selection: EditorSelection.single(anchor, pos), scrollIntoView: true});
  const position = view => view.state.selection.main.head;
  const clamp = (view, pos) => Math.max(0, Math.min(view.state.doc.length, pos));
  const move = (view, key, amount) => {
    const state = view.state, pos = position(view), line = state.doc.lineAt(pos);
    let next = pos;
    if (key === "h") next = Math.max(line.from, pos - amount);
    if (key === "l") next = Math.min(line.to, pos + amount);
    if (key === "j" || key === "k") {
      const target = state.doc.line(Math.max(1, Math.min(state.doc.lines, line.number + (key === "j" ? amount : -amount))));
      next = Math.min(target.to, target.from + (pos - line.from));
    }
    if (key === "0") next = line.from;
    if (key === "$") next = line.to;
    if (key === "G") next = state.doc.line(Math.min(state.doc.lines, amount || state.doc.lines)).from;
    if (key === "w") {
      const text = state.doc.toString(); let cursor = pos;
      for (let n = 0; n < amount; n++) { const match = /\w+|[^\w\s]/g; match.lastIndex = cursor + 1; const found = match.exec(text); cursor = found ? found.index : text.length; }
      next = cursor;
    }
    if (key === "b") {
      const text = state.doc.sliceString(0, pos); let cursor = 0;
      for (let n = 0; n < amount; n++) { const matches = [...text.slice(0, cursor || pos).matchAll(/\w+|[^\w\s]/g)]; cursor = matches.length ? matches[matches.length - 1].index : 0; }
      next = cursor;
    }
    if (visualAnchor !== null) selection(view, next, visualAnchor); else selection(view, next);
    return next;
  };
  const remove = (view, from, to, change = false) => {
    from = clamp(view, from); to = clamp(view, to);
    if (to <= from) return;
    register = view.state.sliceDoc(from, to);
    view.dispatch({changes: {from, to}, selection: EditorSelection.cursor(from)});
    setMode(view, change ? "insert" : "normal");
  };
  const openLine = (view, below) => {
    const line = view.state.doc.lineAt(position(view)), at = below ? line.to : line.from;
    const indent = line.text.match(/^\s*/)[0];
    view.dispatch({changes: {from: at, insert: below ? `\n${indent}` : `${indent}\n`}, selection: EditorSelection.cursor(below ? at + 1 + indent.length : at + indent.length)});
    setMode(view, "insert");
  };
  const normalKey = (view, event) => {
    const key = event.key;
    if (/^[1-9]$/.test(key) || (/^[0-9]$/.test(key) && count)) { count += key; return true; }
    const amount = Math.max(1, Number(count) || 1);
    if (pending) {
      const action = pending; pending = ""; count = "";
      const pos = position(view), line = view.state.doc.lineAt(pos);
      if (action === "g" && key === "g") { selection(view, view.state.doc.line(Math.min(view.state.doc.lines, amount)).from); return true; }
      if (["d","y","c"].includes(action) && ["d","w","b","$","0"].includes(key)) {
        let from = pos, to = pos;
        if (key === "d") { from = line.from; to = line.number + amount - 1 < view.state.doc.lines ? view.state.doc.line(line.number + amount).from : line.to; }
        else if (key === "$") to = line.to;
        else if (key === "0") from = line.from;
        else {
          const saved = visualAnchor; visualAnchor = null; to = move(view, key, amount); visualAnchor = saved;
          if (to < from) [from,to] = [to,from];
        }
        if (action === "y") { register = view.state.sliceDoc(from,to); selection(view,pos); setMode(view,"normal"); }
        else remove(view,from,to,action === "c");
        return true;
      }
      return true;
    }
    if (["h","j","k","l","w","b","0","$","G"].includes(key)) { move(view,key,amount); count = ""; return true; }
    if (key === "g" || key === "d" || key === "y" || key === "c") { pending = key; return true; }
    count = "";
    if (key === "i") { setMode(view,"insert"); return true; }
    if (key === "a") { selection(view,Math.min(view.state.doc.lineAt(position(view)).to,position(view)+1)); setMode(view,"insert"); return true; }
    if (key === "I") { selection(view,view.state.doc.lineAt(position(view)).from); setMode(view,"insert"); return true; }
    if (key === "A") { selection(view,view.state.doc.lineAt(position(view)).to); setMode(view,"insert"); return true; }
    if (key === "o" || key === "O") { openLine(view,key === "o"); return true; }
    if (key === "x") { remove(view,position(view),Math.min(view.state.doc.lineAt(position(view)).to,position(view)+amount)); return true; }
    if (key === "v" || key === "V") {
      const pos = position(view), line = view.state.doc.lineAt(pos); visualAnchor = key === "V" ? line.from : pos;
      setMode(view,"visual"); visualAnchor = key === "V" ? line.from : pos; selection(view,key === "V" ? line.to : pos,visualAnchor); return true;
    }
    if (key === "u") { undo(view); return true; }
    if (key === "p" || key === "P") {
      const at = position(view), insert = key === "p" ? Math.min(view.state.doc.length,at+1) : at;
      view.dispatch({changes:{from:insert,insert:register.repeat(amount)},selection:EditorSelection.cursor(insert+register.length*amount)}); return true;
    }
    return true;
  };
  const visualKey = (view, event) => {
    const key = event.key, amount = Math.max(1,Number(count)||1); count = "";
    if (["h","j","k","l","w","b","0","$","G"].includes(key)) { move(view,key,amount); return true; }
    if (["d","x","y","c"].includes(key)) {
      const range = view.state.selection.main, from = range.from, to = range.to || range.from + 1;
      if (key === "y") { register = view.state.sliceDoc(from,to); selection(view,from); setMode(view,"normal"); }
      else remove(view,from,to,key === "c");
      return true;
    }
    if (key === "Escape" || key === "v") { selection(view,position(view)); setMode(view,"normal"); return true; }
    return true;
  };
  return EditorView.domEventHandlers({
    keydown(event, view) {
      if (event.ctrlKey || event.metaKey || event.altKey || event.isComposing) return false;
      if (mode === "insert") {
        if (event.key === "Escape") { const pos = position(view); selection(view,Math.max(0,pos-1)); setMode(view,"normal"); return true; }
        return false;
      }
      const handled = mode === "visual" ? visualKey(view,event) : normalKey(view,event);
      if (handled) { event.preventDefault(); event.stopPropagation(); }
      return handled;
    },
    focus(_event,view) { onMode?.(mode.toUpperCase()); view.contentDOM.dataset.vimMode = mode; },
    blur() { onMode?.(mode.toUpperCase()); }
  }, {eventHandlers: {keydown: {capture: true}}});
}

export function keybindingExtension(name, onMode) {
  return name === "vim" ? vimExtension(onMode) : vscodeKeymap;
}
