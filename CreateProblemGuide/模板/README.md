# 模板说明

这个目录是一份**能直接导入**的最小题包（A+B，四种语言 × 两种提交方式），把 `模板/` 里的文件压成 zip 就是交付物。

## 文件清单

| 文件 | 何时需要 | 说明 |
|---|---|---|
| `problem.json` | 必有 | 只放元数据（`schemaVersion: 2`）；不要写 checker / solution / main 的内容，也不要写 `tests` |
| `<caseId>.in` / `<caseId>.ans` | 必有 | 所有测试数据，平铺在 zip 根目录；`.ans` 不能是空文件 |
| `checker.cpp` | SPJ 时 | 自己读 `inf` 判定；删掉它则平台用「逐行 token 比较」判 |
| `main.cpp` / `main.cj` / `main.py` / `main.java` | 函数式 | driver，只做 I/O 胶水；四种语言的 driver 读写同一份 stdin/stdout |
| `starter.cpp` / `starter.cj` / `starter.py` / `starter.java` | 函数式 | 给选手的骨架，必须能和同语言的 driver 一起编译 |
| `solution.cpp` / `solution.cj` / `solution.py` / `solution.java` | 必有 | 函数实现（平台会拼成完整参考程序）；只开完整式的语言这里写完整程序 |
| `说明.md` 等其它文件 | 可选 | 平台忽略，不会当成用例 |

## 改成本题

1. 改 `problem.json` 的 `id`（小写字母/数字/连字符，2–48 字符）、`title`、`difficulty`、`tags`、`statement`。
2. 改 `groups`：第一组必须是 `sample` 且 `points` 为 1，所有组 `points` 加起来必须正好 100。
3. 改 `samples`（只是展示，不参与判分）。
4. 改四种语言 `main.*` 的输入输出协议（必须一致），改 `solution.*` 为真正的参考解。
5. 换掉 `01.in/.ans`、`02.in/.ans`，按 `groups[].cases` 的 id 补数据。
6. 改 `function.package`（仓颉包名）与 `function.signature`（按语言写精确签名）。

## 提交方式的增删

- **默认：四种语言 × 两种方式全开**（`modes` 里每种语言都写 `["function", "full"]`）。
- **只想开完整式**：把该语言的 `modes` 改成 `["full"]`，删掉它的 `main.*` / `starter.*`，`solution.*` 改成完整程序（自带入口）。
- **普通题（不用 SPJ）**：删掉 `checker.cpp`，平台按 token 比较。

## 检查

导入后必须拿到 200，且 `verification.solutions.<语言>.score` 四种语言全为 100、`verification.full.<语言>` 全为 true。
