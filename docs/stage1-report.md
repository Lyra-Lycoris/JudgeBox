# 阶段一交接报告（题目系统后端）

2026-11-13 · 本地 commit，未 push。
验收命令：`powershell -ExecutionPolicy Bypass -File .\build.ps1` → ctest **5/5 通过**（process / core / toolchain_paths / api / problem，总 85.2 s）。
`tests/problem_api_test.py` 11 条断言全绿（§10.1 的 8 条 + 重复导入/删除、外部 data.zip、判题中途取消各一条）。

## 1. 实现的接口（是否与规格一致）

| 接口 | 说明 | 规格 |
|---|---|---|
| GET `/api/problems` | 扫 `problems/`，合并提交统计，按 bestScore→difficulty→id 排序 | §6.1 一致 |
| GET `/api/problems/{id}` | 增加 statement/hints/samples/signature/starter/drivers/groups(含 caseCount)/judgedLanguages | §6.2 一致 |
| POST `/api/problems/import` | `json` / `path` / `zipPath`；结构段 + 编译段；幂等覆盖返回 `replaced`；body 上限 64 MiB | §6.3 一致 |
| DELETE `/api/problems/{id}` | 删题包 + 该题提交缓存 | §6.4 一致 |
| POST `/api/submit` | 校验题目/语言/源码，忙时 409「已有提交正在判题」 | §6.5 一致 |
| GET `/api/submit/status` | phase/completed/total/verdict/score/best/groups[].state/cases[]；done 后补 improved/previousBest/finishedAt/message | §6.6 一致（另带 compileLog） |
| GET `/api/submissions?problemId=` | 时间倒序，最多 200 条 | §6.7 一致 |
| GET `/api/submissions/{id}` | 6.7 + source/groups/cases（另带 compileLog/message/durationMs） | §6.8 一致 |
| POST `/api/submissions/clear` | `{problemId}` 或 `{}`，返回 `removed` | §6.9 一致 |
| 静态资源表 | `web/*.js|css|html` + `web/vendor/**/*.js` 编译期嵌入，先查表再走旧分支 | §6.10 一致 |

新增：`src/problems.*`、`src/problemjudge.*`、`src/submitstore.*`、`src/ziputil.*`、`src/apierror.hpp`、
`third_party/testlib/{testlib.h,LICENSE}`（官方 0.9.51）、`tests/problem_api_test.py`、
`tests/fixtures/ict-renjian-cihua/{problem.json,ac-solution.cj}`。
改动：`src/server.cpp`（新分支 / 资源表 / 64 MiB）、`CMakeLists.txt`、`.gitignore`（`/.cache/`）、`README.md`。

## 2. 与规格的偏差（Claude 需要知道）

1. **题目目录** `dataDir.parent_path()/problems`（与 `runs` 同级），不是 §5 目录图里的 `<dataDir>/problems`；任务书 T2 与 §5 正文一致，已与项目所有者确认。
2. **仓颉多文件的 `package` 行**：§7.3 要求“只有第一个文件保留，其余剥掉”。cjc 1.2.0 实测会报 `found more than one package declaration`（无 package 的文件落进 default 包）。改成**每个文件都补齐同一个 package**，与 §11.2「package 名必须一致」相符。
3. **driver 自检**用 `drivers.<lang> + starter.<lang>` 编译，顺带证明 starter 与 driver 签名自洽（§6.3-7 只要求“编译 driver”）。
4. **testlib.h 内置进 exe**（CMake 生成 `testlib_asset.hpp`），编译 checker 时写进工作目录用 `-I.`，安装包不依赖源码树。checker 由内置 g++ 编译，运行时把编译器 bin 目录加进 PATH（否则 libstdc++ DLL 缺失，退出码 0xC0000135）。
5. **落盘 problem.json** 抽走 `tests`，保留 `testsZipPath`（读取时忽略，`data.zip` 才是权威），追加 `storedAt`。
6. **无历史时字段是 null**：bestScore / lastVerdict / lastSubmittedAt / best / previousBest，不是 0。
7. **未提交过时** `/api/submit/status` 返回 `{done:true, verdict:"READY"}`，不是 404，前端不用特判。
8. **提交与调试互斥**：`/api/run` 在跑时提交 409（§11.9「不能并发」）；反向不拦，`/api/run` 行为保持原样。
9. **hints / samples[].explain** 子键宽松（缺一侧按空处理），顶层字段仍是严格白名单。
10. **提交记录 ≤256 KB**：超了先丢 compileLog、再截断 source（`sourceTruncated:true`）；提交源码上限 1 MiB。

## 3. 实测耗时（本机，内置 g++ 16.1.0 / cangjie 1.2.0）

- 导入 fixture（8 用例）：**10.9 s** = checker 6.8 + cpp driver 1.5 + cangjie driver 0.9 + 参考解编译 0.9 + 8 点 0.7。
- 一次仓颉 AC 提交：**8.4 s** = checker 6.8 + 仓颉编译 0.9 + 8 点 0.67（单点 0–63 ms）。
- 判题中途 `/api/cancel`：0.5 s 内回到 `CANCELLED`，记录照常落盘，之后仍能继续判题。
- `ctest -R problem`：71.1 s；全套 ctest：85.2 s。
- 大头是每次提交都重编 testlib 版 checker（`-O2`）。嫌慢的话，下一步可按 checker 源码哈希缓存 `checker.exe`。

## 4. 已知 bug / 未覆盖

- **没有 C++ 标准答案**（按项目所有者选择只写仓颉）：C++ 函数式只覆盖到「driver+solve 拼接能编译、能跑、被 checker 判 WA」，C++ AC 没有 fixture 级覆盖。
- 提交记录剪枝（每题 ≤50）没被测试触发；多题排序也只测了单题。
- `io` 模式没有端到端测试（fixture 是 function 模式）；代码复用 `compileProgram()`。
- 导入同步跑在服务器单线程 accept 循环里：约 11 s 内其他请求排队；前端只能“停止等待”，不能真取消（与 §6.3 说明一致）。
- 判题进行中 DELETE 掉该题没有加保护：已解压的题包会继续跑完，结束后会重建提交目录。
- CANCELLED / CE / JE 也会落一条 score=0 的记录，于是 `bestScore` 变 0、`attempts` +1（规格没写要不要排除，按保守做法保留）。
- 组内首错即跳组，所以 WA 时 `completed < total` 是预期行为。

## 5. 前端可以直接依赖的行为

- `done=false` 时 `groups` 已带 `state`（pending/running/passed/failed）与 `earned`；`cases[]` 每跑完一点追加一条，`completed` 同步；`phase` 取值为「准备题包 / 编译 checker / 编译提交 / 运行测试点 i / N / 已完成」。
- `done=true` 一定有 `verdict`、`score`、`message`、`improved`、`previousBest`、`finishedAt`；`best` 已含本次。
- CE：`verdict="CE"`、`score=0`、`compileLog` ≤64 KB、`groups` 全 pending、`cases` 为空。
- WA：`score` 只累计“组内全 AC”的组，`groups[].earned`/`state` 可直接渲染。
- `/api/problems` 的 `bestScore` 为 null 表示没做过；排序是「未做 → 分数低 → 难度低 → id」。
- 题面/样例/签名保证 `{zh,en}` 两侧齐全（校验强制）；`samples[].input` 就是喂给 driver 的完整 stdin（首行 1），`output` 是应输出内容。
- 调 `/api/problems/import` 请把 HTTP 超时放到 ≥120 s；判题轮询 250 ms 足够。
