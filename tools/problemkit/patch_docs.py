"""更新文档措辞：题面不再包含「两种提交方式 / 函数签名」小节。"""
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
GUIDE = ROOT / 'CreateProblemGuide' / 'CreateProblemGuide.md'
KIT = ROOT / 'tools' / 'problemkit' / 'README.md'
README = ROOT / 'README.md'
CHANGELOG = ROOT / 'CHANGELOG.md'

EDITS = [
    (GUIDE,
     '- 题面里请把签名和"完整式 / 函数式"两种提交方式都讲清楚；四种语言的签名不一致（Python 的 `list[int]`、Java 的 `long[]`），不要只写仓颉那一份。',
     '- 题面里**不要**再写「两种提交方式」「函数签名」小节：做题页会按当前选择的提交方式自动显示裁判方式，编辑器的 starter 也已经带上精确签名。'),
    (GUIDE,
     '- 题面要说明**两种提交方式**：完整式交完整程序，函数式只实现 `signature` 里的 `solve`；四种语言的签名都要给（或直接引用 starter）。',
     '- 题面只讲题目本身；提交方式与函数签名由平台界面展示（做题页的提交方式下拉框、裁判方式卡片、编辑器 starter），不要写进题面。'),
    (GUIDE,
     '- [ ] `id` 合法；`difficulty` 是整百；`tags` 来自词表；题面中英齐全，并说明两种提交方式。',
     '- [ ] `id` 合法；`difficulty` 是整百；`tags` 来自词表；题面中英齐全（不写提交方式与函数签名）。'),
    (KIT,
     '- 必须说明两种提交方式（完整程序 / 函数式），并给出四种语言的签名（可以照抄 driver 生成的签名）。',
     '- 不要写「两种提交方式」「函数签名」小节：平台界面已经展示提交方式与签名，题面只讲题目本身。'),
    (README,
     '- 生成的函数签名（会自动写进题面签名段）：',
     '- 生成的函数签名（写进 `function.signature`，做题页的 starter 与签名展示都用它）：'),
    (CHANGELOG,
     '- 题库扩充：新增 28 个专题共 224 道原创题',
     '- 题面只保留题目本身：删掉「两种提交方式 / 函数签名」小节，做题页也不再在标题下重复 time limit 文案（顶部已有卡片）；裁判方式卡片跟随「提交方式」变化（完整程序 → 普通裁判，函数式 → 函数裁判，SPJ 题保持特殊裁判）。\n- 题库扩充：新增 28 个专题共 224 道原创题'),
]


def main():
    for path, old, new in EDITS:
        text = path.read_text(encoding='utf-8')
        if old not in text:
            print('MISS', path.name, old[:36])
            continue
        path.write_text(text.replace(old, new, 1), encoding='utf-8')
        print('patched', path.name)


if __name__ == '__main__':
    main()
