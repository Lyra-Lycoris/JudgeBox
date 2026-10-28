import {EditorState, Compartment} from "@codemirror/state";
import {EditorView, keymap, lineNumbers, highlightActiveLineGutter, highlightSpecialChars, drawSelection, dropCursor, rectangularSelection, crosshairCursor, highlightActiveLine, placeholder} from "@codemirror/view";
import {indentUnit, syntaxHighlighting, bracketMatching, foldGutter, foldKeymap, indentOnInput, StreamLanguage} from "@codemirror/language";
import {history, defaultKeymap, historyKeymap, indentWithTab} from "@codemirror/commands";
import {highlightSelectionMatches, searchKeymap} from "@codemirror/search";
import {closeBrackets, autocompletion, closeBracketsKeymap, completionKeymap} from "@codemirror/autocomplete";
import {linter, lintGutter, lintKeymap, forceLinting} from "@codemirror/lint";
import {cpp} from "@codemirror/lang-cpp";
import {python} from "@codemirror/lang-python";
import {java} from "@codemirror/lang-java";
import {classHighlighter} from "@lezer/highlight";
import {keybindingExtension} from "./keybindings.js";

const cangjieLanguage = StreamLanguage.define({
  startState: () => ({block: false}),
  token(stream, state) {
    if (state.block) {
      if (stream.match("*/")) state.block = false;
      else stream.next();
      return "comment";
    }
    if (stream.match("//")) { stream.skipToEnd(); return "comment"; }
    if (stream.match("/*")) { state.block = true; return "comment"; }
    if (stream.match(/"(?:[^"\\]|\\.)*"/)) return "string";
    if (stream.match(/'(?:[^'\\]|\\.)*'/)) return "string";
    if (stream.match(/\b\d[\d_]*(?:\.\d+)?\b/)) return "number";
    if (stream.match(/\b(?:let|var|const|func|class|struct|interface|enum|import|package|if|else|for|while|match|case|where|return|public|private|protected|open|override|abstract|init|this|super|in|extend|prop|mut|type|foreign|unsafe|spawn|synchronized|try|catch|finally|throw|as|is|main|true|false|break|continue|from)\b/)) return "keyword";
    if (stream.match(/\b(?:Int8|Int16|Int32|Int64|IntNative|UInt8|UInt16|UInt32|UInt64|UIntNative|Float16|Float32|Float64|Bool|Rune|String|Unit|Array|Option|Nothing|Range)\b/)) return "typeName";
    if (stream.match(/[A-Za-z_][\w]*/)) return "variableName";
    stream.next();
    return null;
  }
});

function languageSupport(language) {
  if (language === "python") return python();
  if (language === "java") return java();
  if (language === "cangjie") return cangjieLanguage;
  return cpp();
}

function toMark(view, item) {
  const doc = view.state.doc;
  const lineNo = Math.min(Math.max(1, Number(item.line) || 1), doc.lines);
  const endLineNo = Math.min(Math.max(lineNo, Number(item.endLine) || lineNo), doc.lines);
  const start = doc.line(lineNo);
  const end = doc.line(endLineNo);
  const from = Math.min(start.to, start.from + Math.max(0, (Number(item.column) || 1) - 1));
  let to = Math.min(end.to, end.from + Math.max(0, (Number(item.endColumn) || (Number(item.column) || 1) + 1) - 1));
  if (to <= from && from < start.to) to = Math.min(start.to, from + 1);
  return {from, to: Math.max(from, to), severity: item.severity === "warning" ? "warning" : "error", message: String(item.message || "错误")};
}

function mount(textarea, options) {
  const languageConf = new Compartment();
  const keybindingConf = new Compartment();
  let applying = false;
  const onVimMode = mode => { const badge = document.getElementById("vimMode"); if (badge) badge.textContent = mode; };
  const view = new EditorView({
    parent: textarea.parentElement,
    state: EditorState.create({
      doc: textarea.value,
      extensions: [
        lineNumbers(), highlightActiveLineGutter(), highlightSpecialChars(), history(), foldGutter(),
        drawSelection(), dropCursor(), EditorState.allowMultipleSelections.of(true), indentOnInput(),
        indentUnit.of("    "), EditorState.tabSize.of(4), bracketMatching(), closeBrackets(), autocompletion(),
        rectangularSelection(), crosshairCursor(), highlightActiveLine(), highlightSelectionMatches(),
        keybindingConf.of(keybindingExtension(document.getElementById("keybinding")?.value || "vscode", onVimMode)),
        keymap.of([indentWithTab, ...closeBracketsKeymap, ...defaultKeymap, ...searchKeymap, ...historyKeymap, ...foldKeymap, ...completionKeymap, ...lintKeymap]),
        syntaxHighlighting(classHighlighter),
        languageConf.of(languageSupport(options.getLanguage())),
        lintGutter(),
        linter(async editorView => {
          const items = await options.lint(editorView.state.doc.toString(), options.getLanguage());
          return (items || []).map(item => toMark(editorView, item)).filter(mark => mark.from < editorView.state.doc.length && mark.to >= mark.from);
        }, {delay: 500}),
        placeholder("源程序"),
        EditorView.updateListener.of(update => {
          if (!update.docChanged || applying) return;
          applying = true;
          textarea.value = update.state.doc.toString();
          textarea.dispatchEvent(new Event("input", {bubbles: true}));
          applying = false;
        }),
        EditorView.contentAttributes.of({"aria-label": "待测程序源码"})
      ]
    })
  });
  textarea.hidden = true;
  textarea.addEventListener("input", () => {
    if (applying) return;
    const next = textarea.value;
    if (next === view.state.doc.toString()) return;
    applying = true;
    view.dispatch({changes: {from: 0, to: view.state.doc.length, insert: next}});
    applying = false;
  });
  return {
    pull() {
      const next = textarea.value;
      if (next === view.state.doc.toString()) return;
      applying = true;
      view.dispatch({changes: {from: 0, to: view.state.doc.length, insert: next}});
      applying = false;
    },
    setLanguage(language) {
      view.dispatch({effects: languageConf.reconfigure(languageSupport(language))});
      forceLinting(view);
    },
    setKeybinding(name) {
      view.dispatch({effects: keybindingConf.reconfigure(keybindingExtension(name, onVimMode))});
      view.focus();
    }
  };
}

let current = null;
window.JudgeEditor = {
  mount(textarea, options) { current = mount(textarea, options); },
  pull() { if (current) current.pull(); },
  setLanguage(language) { if (current) current.setLanguage(language); },
  setKeybinding(name) { if (current) current.setKeybinding(name); }
};
