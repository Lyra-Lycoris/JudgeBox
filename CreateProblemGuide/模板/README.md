# 模板说明

这个目录是一份**能直接导入**的最小题包（A+B），把 `模板/` 里的文件压成 zip 就是交付物。

## 文件清单

| 文件 | 何时需要 | 说明 |
|---|---|---|
| `problem.json` | 必有 | 只放元数据；不要写 checker / solution / main 的内容，也不要写 `tests` |
| `<caseId>.in` / `<caseId>.ans` | 必有 | 所有测试数据，平铺在 zip 根目录；`.ans` 不能是空文件 |
| `checker.cpp` | SPJ 时 | 自己读 `inf` 判定；删掉它则平台用「逐行 token 比较」判 |
| `main.cj` / `main.cpp` | function 模式 | driver，只做 I/O 胶水；语言由文件是否存在决定 |
| `starter.cj` / `starter.cpp` | function 模式 | 有 `main.*` 就必须有同语言的 `starter.*` |
| `solution.cj` / `solution.cpp` | 必有（至少一种） | 参考解；多文件用 `solution_1.cj`、`solution_2.cj`… |
| `说明.md` 等其它文件 | 可选 | 平台忽略，不会当成用例 |

## 改成本题

1. 改 `problem.json` 的 `id`（小写字母/数字/连字符，2–48 字符）、`title`、`difficulty`、`tags`、`statement`。
2. 改 `groups`：第一组必须是 `sample` 且 `points` 为 1，所有组 `points` 加起来必须正好 100。
3. 改 `samples`（只是展示，不参与判分）。
4. 改 `main.*` 的输入输出协议，改 `solution.*` 为真正的参考解。
5. 换掉 `01.in/.ans`、`02.in/.ans`，按 `groups[].cases` 的 id 补数据。

## 两种模式的删改

- **io 模式**：`problem.json` 里 `judgeMode` 改成 `"io"`，删掉整个 `function` 段，删掉 `main.*` 和 `starter.*`，把 `solution.*` 改成完整程序（自带 `main`）。
- **只有一种语言**：删掉另一种语言的 `main/starter/solution`；`function` 段的 `signature` 保留双语。
- **普通题（不用 SPJ）**：删掉 `checker.cpp`，平台按 token 比较。

## 检查

导入后必须拿到 200，且 `verification.solutions.<语言>.score` 全为 100。
