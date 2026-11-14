# 出题指南（题包 v1）

> **读者**：出题者（人或模型）。读完应当能独立产出一个能被 JudgeBox 导入、且参考答案跑满 100 分的题包。
> **唯一判据**：`POST /api/problems/import` 返回 200，且 `verification.solutions.<语言>.score == 100`。
> **交付物是一个 zip**。同目录下有一份可直接导入的 [完整示例.zip](完整示例.zip) 和一个 [模板/](模板/) 目录（A+B，能直接跑通）。
> 本文按 2026-11-14 的实现写；报错原文都取自习校验器，可以按字面搜索。

## 0. 交付物：一个 zip

```
<id>.zip
  problem.json           # 只能放元数据（见 §2）
  <caseId>.in            # 全部测试数据，平铺在根目录
  <caseId>.ans
  checker.cpp            # 可选：SPJ / 自定义判定；没有就按内置 token 比较
  main.cj / main.cpp     # function 模式：driver（按语言，至少一种）
  starter.cj / starter.cpp   # function 模式：有 main.* 就必须有同语言的 starter.*
  solution.cj / solution.cpp # 参考解（至少一种语言；多文件用 solution_1.*、solution_2.*…）
```

硬性约束：

- **不能有子目录**（`题包 zip 不能有子目录：xxx`）；所有文件平铺在根目录。
- **文件名一律用 ASCII**（`a-z A-Z 0-9 _ - .`）。平台用系统 `tar.exe` 解压，包里出现中文文件名会解压失败。`problem.json` 里的中文内容没问题，只有**文件名**受限。
- 导入时允许 zip 里套一层同名目录（Windows 右键"压缩到 zip"很常见），平台会自动下钻；但不要套两层。
- 除上表以外的文件（`README.md` 之类）会被忽略，不会当成用例。
- 导入接口只收 zip：`{"zipPath": "绝对路径"}` 或 `{"zip": "<base64>"}`（§9）。
- zip 体积：base64 上传建议 ≤ 44 MiB（请求体上限 64 MiB）；更大的用 `zipPath`。

## 1. 概念

| 词 | 含义 |
|---|---|
| 题包 | 上面那个 zip；导入后落在 `<dataDir>/../problems/<id>/` |
| 用例 case | 一份 `.in` + 一份同名 `.ans`；判题时一个用例起一个进程 |
| 组 group | 若干用例 + 一个分值；组内全 AC 才拿这组的全部分数 |
| driver（`main.*`） | 只做 I/O 胶水：读 stdin → 调选手函数 → 写 stdout。`function` 模式必填 |
| starter（`starter.*`） | 给选手的初始骨架：签名 + `// TODO` + 返回空值，必须能独立编译 |
| solution（`solution.*`） | 标准答案，只在导入自检里跑，用来证明"题出得对" |
| checker（`checker.cpp`） | 可选。给了就是 SPJ/自定义判定；不给就按 token 比较 |

## 2. `problem.json`（只放元数据）

**白名单**：只允许下表 12 个键，多一个就报 `未知字段 xxx`。

| 字段 | 类型 | 必填 | 约束 |
|---|---|---|---|
| `schemaVersion` | int | 是 | 必须为 `1` |
| `id` | string | 是 | `^[a-z0-9][a-z0-9-]{1,47}$`（2–48 字符）；同时是目录名与 API 路径；不要用 `import` 当 id |
| `title` | `{zh,en}` | 是 | 只允许这两个键；两侧非空，各 ≤ 80 字符（按 Unicode 码点） |
| `difficulty` | int | 是 | 800–3500 且是 100 的整数倍，决定题单排序 |
| `tags` | string[] | 是 | 1–3 个，必须来自 §7.3 词表；重复不会报错，但别写 |
| `limits` | `{timeMs,memoryMb}` | 是 | 只允许这两个键；`timeMs` 100–60000，`memoryMb` 16–4096 |
| `judgeMode` | `"io"` \| `"function"` | 是 | 见 §3 |
| `statement` | `{zh,en}` | 是 | 只允许这两个键；两侧非空，各 ≤ 64 KB（UTF-8 字节）；Markdown 子集见 §7.1 |
| `samples` | array | 是 | 1–5 项，见 §7.2。**只展示，不参与判分** |
| `groups` | array | 是 | 至少 2 组，第一组必须是 `sample`，见 §5 |
| `function` | object | `function` 模式必填 | 只允许 `package` 与 `signature:{zh,en}`；driver/starter 不写在这里（来自文件） |
| `notes` | `{zh,en}` | 否 | 出题人备注，只给导入者看 |

**不要写** `tests`、`testsZipPath`、`checker`、`solution`、`driver`、`starter`：这些现在都由文件提供，写进 JSON 会报 `未知字段`。

```json
{
  "schemaVersion": 1,
  "id": "a-plus-b",
  "title": {"zh": "A+B 问题", "en": "A Plus B"},
  "difficulty": 800,
  "tags": ["模拟"],
  "limits": {"timeMs": 1000, "memoryMb": 128},
  "judgeMode": "function",
  "statement": {"zh": "# A+B\n…", "en": "# A Plus B\n…"},
  "samples": [{"input": "2\n3\n", "output": "5\n", "explain": {"zh": "2 + 3 = 5。", "en": "2 + 3 = 5."}}],
  "groups": [{"name": "sample", "points": 1, "cases": ["01"]},
             {"name": "main", "points": 99, "cases": ["02"]}],
  "function": {"package": "demo", "signature": {"zh": "func solve(a: Int64, b: Int64): Int64", "en": "solve(a: int, b: int) -> int"}}
}
```

## 3. 两种判题模式与文件组合

| 文件 | `io` | `function` |
|---|---|---|
| `main.cj` / `main.cpp` | **不要有**（有就报错） | 至少一个；语言由文件是否存在决定 |
| `starter.cj` / `starter.cpp` | 不要有 | 每种有 `main.*` 的语言都必须有 |
| `solution.cj` / `solution.cpp` | 至少一种；是**完整程序**（自带 `main`） | 至少一种；是函数实现，和 `main` 拼接 |
| `checker.cpp` | 可选 | 可选 |
| `function` 段 | 不需要 | 必须有 `package` + `signature` |

- `judgedLanguages`：`function` 模式等于 `main.*` 的语言集合；`io` 模式恒为 `["cpp","cangjie"]`。
- **想让选手交 C++，就必须有 `main.cpp` + `starter.cpp`**（`function` 模式）；只给仓颉，C++ 选手提交不了。
- `solution` 的每种语言都必须有对应 `main.*`（`有 solution.cpp，但没有对应的 main.cpp`）。
- `io` 模式下参考解也可以多文件（`solution_1.cpp`…），C++ 按编号顺序拼接、仓颉按顺序编译。

### 3.1 driver 写什么

driver 就是 `main`，只做三件事：读 stdin → 调用签名里的函数 → 写 stdout。**不要把题解写进 driver。**

```cangjie
package demo

import std.convert.Parsable

main(): Unit {
    let a = Int64.parse(readln().trimAscii())
    let b = Int64.parse(readln().trimAscii())
    println(solve(a, b))
}
```

```cpp
#include <bits/stdc++.h>
using namespace std;
long long solve(long long a, long long b);   // 声明必须与选手实现一致

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long a, b;
    cin >> a >> b;
    cout << solve(a, b) << '\n';
    return 0;
}
```

规则：

1. 必须有 `main`（仓颉 `main(): Unit`），并且和 `starter.*` 一起能编译通过。
2. C++ 的调用必须先在 driver 里声明函数；选手文件只给定义，**不能写 `main`**，也不能 `#include` 自己额外写的头文件（整个编译单元只有 driver + 选手这一份源码）。
3. 输入输出协议完全由 driver 决定；判题只管把 `.in` 塞进 stdin、把 stdout 交给 checker。
4. 赛题常见写法"先读用例数 `T` 再循环"时，`.in` 第一行写 `T=1`（§4.3）。

### 3.2 仓颉包名（最容易 CE 的地方）

仓颉的 driver 和选手代码编译在**同一个 package** 里，包名不一致直接 CE：

1. `function.package` 必填，整道题只用这一个名字。
2. `main.cj`、`starter.cj`、`solution.cj`（以及每个 `solution_N.cj`）**首行都必须是 `package <function.package>`**。
3. 题面里的仓颉示例代码首行也要写同一个 `package`。
4. 选手提交没写 `package` → 平台自动补；写了别的包名 → 不改写，按 CE 报错（日志原样返回）。
5. C++ 不涉及包名。

### 3.3 多文件参考解

- 单文件：`solution.cj` / `solution.cpp`。
- 多文件：`solution_1.cj`、`solution_2.cj`… **编号必须从 1 连续**，按编号顺序编译（C++ 拼接）。
- 每种语言合计 ≤ 512 KB。
- 选手提交永远是**单个源码字符串（单文件）**；如果参考解需要多文件，选手要自己合并成一个文件交。

## 4. 用例数据

### 4.1 文件与 id

- 平铺：`<caseId>.in` + `<caseId>.ans` 放在 zip 根目录。
- `caseId` 匹配 `^[a-z0-9][a-z0-9_-]{0,15}$`（1–16 字符，小写字母/数字/`-`/`_`，以字母或数字开头）。
- 每个 case 必须恰好属于一个组；`groups[].cases` 里的 id 必须都有对应文件（`用例 05 缺少 05.in` / `05.ans`）。
- zip 里不允许有组外的 `.in/.ans`（`用例 07 不在任何组中`）。
- `.ans` 不能是空文件；建议末尾保留换行。
- UTF-8，可带 BOM；单文件 ≤ 4 MiB；用例数 ≤ 200；`Σ(input+ans)` ≤ 64 MiB；zip 内文件数 ≤ 500。

### 4.2 `.ans` 从哪来

先用参考解跑 `.in` 得到输出，再当 `.ans`。注意：

- **普通题（不写 checker）**：`.ans` 必须和选手输出的 token 序列一致，顺序也要一致。
- **SPJ 题**：`.ans` 只是占位（平台要求它存在），判定完全由 `checker.cpp` 读 `inf` 现场完成；`.ans` 里放参考解的输出即可。
- **多解且可枚举的题**：可以写"比较型 checker"（和 `.ans` 的集合/排序结果比），也可以写 SPJ。**真正的多解（任何合法输出都算对）必须用 SPJ**，不能靠把"所有解"塞进 `.ans`。

### 4.3 输入编码

- `.in` 会**原样**喂给进程的 stdin，平台不加、不减任何东西。
- 要带"用例数"就由 **driver 自己**决定：driver 读 `T` 就写 `1`（一个进程只跑一个用例）；driver 不读 `T` 就完全不用写。

## 5. 组与分值

```json
"groups": [
  {"name": "sample", "points": 1,  "cases": ["01"]},
  {"name": "simple", "points": 20, "cases": ["02", "03"]},
  {"name": "boundary", "points": 29, "cases": ["04", "05", "06"]},
  {"name": "long", "points": 50, "cases": ["07", "08"]}
]
```

- 至少 2 组（`groups 至少需要 2 组（含 sample）`）。
- `groups[0]` 必须 `name == "sample"`、`points == 1`、`cases` 非空。它是**真实判分**的一组（题面里的 `samples` 才是纯展示）。
- 其余组名必须匹配 `^[a-z][a-z0-9_-]{0,15}$`，不能重名（`组名 simple 重复`）。
- 每组 `points` 是 ≥ 0 的整数；每组 `cases` 非空；只允许 `name`/`points`/`cases` 三个键。
- **`Σ groups[].points` 必须严格等于 100**（含 sample 的 1 分），否则报 `groups 分值之和为 98，应为 100`。
- 计分：组内全部 AC 才拿该组 `points`；组内第一个非 AC（WA/TLE/MLE/RE/OLE）就跳到下一组，该组记 0 分，后面的用例不跑（`completed < total` 是正常现象）。
- CE/JE/CANCELLED 是整份提交级别的错误：`score = 0`，不按组计分。

## 6. checker：默认比较 与 SPJ

### 6.1 不写 `checker.cpp`（默认）

平台用内置 **token 比较**：把选手输出和 `.ans` 按空白切成 token 逐段比，空白/换行的差异不算错，token 顺序算错。适合绝大多数"输出唯一"的题。

### 6.2 写 `checker.cpp`（SPJ / 自定义判定）

```cpp
#include "testlib.h"

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);      // 参数固定是 <input> <output> <answer>
    long long a = inf.readLong();        // inf = 输入（判多解/合法性时用）
    long long b = inf.readLong();
    long long actual = ouf.readLong();   // ouf = 选手输出
    if (actual != a + b) quitf(_wa, "期望 %lld，实际 %lld", a + b, actual);
    quitf(_ok, "ok");                    // 多余内容由 testlib 在退出时检查
}
```

- 平台内置 testlib 0.9.51，编译时把 `testlib.h` 放在工作目录：直接 `#include "testlib.h"`，**不能 include 其他本地头文件**。
- 编译：`g++ -std=c++20 -O2 -pipe -I. checker.cpp -o checker.exe`，60 秒超时；按源码哈希缓存，改完再导会重新编。
- 运行：`checker.exe <input> <output> <answer>`，工作目录是该用例目录；**10 秒超时**；退出码 `0` = AC，非 0 = WA；stdout+stderr 前 4 KB 作为该点的 `message`；checker 超时/崩溃 = JE。
- 必须自己处理：**多解/顺序无关**（按集合或排序比）、**0 解**、**行尾差异**。
- **必须把选手输出读完**：testlib 在 `quit()` 时检查输出流，没读完会报 `wrong output format Extra information in the output file`（看起来像 WA，其实是 checker 没读完）。比较完 token 后可以调 `ouf.readEof();`。
- 不要用 `quitf(_fail, ...)` 表示"选手错"（那是 checker 自己的前提被破坏），选手错一律 `_wa`。

### 6.3 两个必踩的坑

**① 行尾**：Windows 上程序 `println` 输出 CRLF，而 `.ans` 可能是 LF。按行读时先去掉行尾 `\r` 和多余空格，否则假 WA。

**② `readInt()` 之后不要直接 `readLine()`**：`readInt` 会把流停在行尾分隔符前，紧接着的 `readLine()` 读到空串，整个文件错位一行。正确做法是先 `readLine()` 读表头再自己 `stoi`：

```cpp
auto header = ouf.readLine();
if (header.empty()) quitf(_wa, "缺少解数");
int n = std::stoi(header);
for (int i = 0; i < n; ++i) { auto line = ouf.readLine(); /* 去掉 \r */ }
```

## 7. 题面、样例、标签

### 7.1 题面 Markdown 子集

允许：`#`~`###` 标题、段落、`**粗体**`、`*斜体*`、行内代码、围栏代码块（```lang）、有序/无序列表（可嵌套一层）、`>` 引用、表格、水平线、链接（仅 `https://`，带 `rel="noopener"`）、数学 `$…$` 与 `$$…$$`（离线 MathJax 渲染）。

不允许：原始 HTML、`<script>`、iframe、行内 `style`、脚注、相对链接、图片。

- 中英两侧都必须写，各 ≤ 64 KB。
- 题面里的仓颉示例代码首行必须是 `package <function.package>`（§3.2）。

### 7.2 `samples`（只展示，不判分）

```json
{"input": "2\n3\n", "output": "5\n", "explain": {"zh": "2 + 3 = 5。", "en": "2 + 3 = 5."}}
```

- 1–5 项；只允许 `input`/`output`/`explain` 三个键；`input`/`output` 非空字符串。
- `input` 是喂给程序的**完整 stdin**，`output` 是它应当输出的完整内容（driver 读 `T` 就在这里写 `1`）。
- `explain` 可选，`{zh,en}` 字符串。
- **`samples` 不参与判分**；判分只看 `groups[].cases` 对应的 `.in/.ans`。样例组（`sample`）是另一回事：它是真实判分组，用例来自文件。

### 7.3 标签词表（只能用这些）

模拟、枚举、排序、二分、贪心、构造、前缀和、差分、双指针、滑动窗口、哈希、栈、队列、单调栈、堆、并查集、树状数组、线段树、字符串、Trie、KMP、图论、最短路、最小生成树、拓扑排序、二分图、网络流、树、最近公共祖先、动态规划、背包、区间DP、状压DP、数位DP、树形DP、数学、数论、组合数学、概率期望、计算几何、位运算、分治、记忆化搜索、高精度、交互

## 8. 判题语义与限制

- 一个用例一个进程；stdin 是 `.in`，stdout 落盘后交给 checker（或内置比较）。
- 时间上限 = `limits.timeMs`（墙钟，语言系数 1.0）；内存 = `limits.memoryMb`（Job Object 硬上限）；输出上限 = `max(1 MiB, .ans 大小 + 1 MiB)`。
- 编译上限：60 秒 / 2 GiB / 2 MiB 输出；编译日志超过 64 KB 会截断。
- `verdict` 取值：`AC WA TLE MLE RE OLE CE JE CANCELLED`；得分只累计"组内全 AC"的组，`verdict` 取第一个非 AC。
- 判题是单任务：已有提交在判时再提交返回 409；调试任务（`/api/run`）在跑时提交也返回 409。
- 提交源码 ≤ 1 MiB；单条提交记录 ≤ 256 KB（超了先丢 `compileLog`、再截断源码并标 `sourceTruncated`）；每题最多保留 50 条提交。

## 9. 导入与自检

### 9.1 接口

```json
{"zipPath": "E:\\problems\\a-plus-b.zip"}
{"zip": "<zip 的 base64>"}
```

- 只收 zip；`zipPath` 必须是绝对路径。前端网页走 base64（选文件 → 自动编码）。
- 请求体上限 64 MiB；base64 会膨胀约 1/3，所以网页导入建议 ≤ 44 MiB。
- 导入是同步的：首次要编译 checker 与 driver，约 5–20 秒；成功会覆盖同 `id` 的旧版本并返回 `"replaced": true`。
- 导入失败**不会写盘**，旧版本原样保留，可以反复试。

### 9.2 自检三项（任何一项失败即 400）

1. 有 `checker.cpp` 就编译它（`checker 编译失败（前 20 行）：…`）。
2. 对每种 driver 语言用 `main + starter` 编译一次（`drivers.cpp 编译失败（前 20 行）：…`）。
3. 对每种 `solution` 语言跑全部用例，必须 100 分（`参考答案未满分：…`）。

成功响应：

```json
{"ok": true, "id": "a-plus-b", "replaced": true,
 "verification": {"cases": 2,
   "groups": [{"name": "sample", "points": 1, "passed": true}],
   "checker": "custom", "checkerCompiled": true,
   "drivers": {"cpp": true, "cangjie": true},
   "solutions": {"cpp": {"score": 100, "verdict": "AC"}}}}
```

`checker` 是 `"custom"`（有 checker.cpp）或 `"builtin"`（走内置比较，此时 `checkerCompiled` 为 false）。

### 9.3 报错对照表

| `details[].message` | 原因 | 怎么改 |
|---|---|---|
| `未知字段 xxx` | `problem.json` 多写了键 / 拼错 | 对照 §2 的 12 个键 |
| `请提供题包 zip：…` | 没给 zipPath / zip | 按 §9.1 |
| `zipPath 必须是绝对路径` / `找不到题包 zip` | 路径错 | 用绝对路径并确认存在 |
| `题包 zip 根目录没有 problem.json` | 少了题面文件，或套了两层目录 | 平铺到根目录 |
| `题包 zip 不能有子目录：xxx` | 包里有文件夹 | 全部平铺 |
| `题包 zip 解压失败（文件名请全部用 ASCII）` | 包内有中文文件名 | 改成 ASCII 文件名 |
| `id 格式不合法` | 大写 / 下划线 / 长度不对 | `^[a-z0-9][a-z0-9-]{1,47}$` |
| `title.zh 不能为空` / `title.en` | 少写一侧 | 双语都要写 |
| `difficulty 必须是 800–3500 之间 100 的整数倍` | 档位写错 | 改整百 |
| `未知标签 xxx` | 不在词表 | 从 §7.3 选 |
| `groups 至少需要 2 组（含 sample）` | 只有一组 | 至少 sample + 一个判分组 |
| `第一组必须是 sample 组` / `样例组 points 必须为 1` | 首组写错 | 见 §5 |
| `groups 分值之和为 98，应为 100` | 分不完 | 调到总和 100 |
| `用例 02 出现在多个组中` | 一个 case 挂两组 | 每个 case 只留一组 |
| `用例 05 缺少 05.in` / `05.ans` | 数据文件不齐 | 补齐 |
| `用例 05 的 .ans 是空文件` | 答案为空 | 写真实答案 |
| `用例 07 不在任何组中` | 有组外用例 | 删掉或加进组 |
| `function 模式必须提供 function 段（package 与 signature）` | 少了 function | 补 §2 |
| `function.package 含有非法字符` | 包名带空格 / `/` | 用单个标识符 |
| `缺少 starter.cpp（function 模式每个 driver 都要配 starter）` | 只有 main | 补 starter |
| `io 模式不需要 main.cpp（选手自己写 main）` | io 题带了 driver | 删掉 main/starter |
| `缺少参考解：solution.cj 或 solution.cpp` | 没有参考解 | 补一个 |
| `有 solution.cpp，但没有对应的 main.cpp` | 参考解语言没 driver | 补 main+starter，或删该 solution |
| `solution_ 编号必须从 1 连续` | 多文件编号跳号 | 改成 1、2、3… |
| `checker 编译失败（前 20 行）` | checker 编译错误 | 按日志修 |
| `drivers.cpp 编译失败（前 20 行）` | driver 错 / 包名不一致 | 看日志 |
| `参考答案（cangjie）编译失败（前 20 行）` | 参考解编译错误 | 看日志 |
| `参考答案未满分：组 boundary 未通过（用例 05 WA）：…` | 参考解错 / checker 判错 | 先看 message |

## 10. 模板与完整示例

- [模板/](模板/)：一份能直接导入的 A+B（function 模式 + SPJ + 双语言 + 两个用例）。改 `problem.json` 和 `solution.*` 就能变成你的题；`模板/README.md` 写了每种模式下该删哪些文件。
- [完整示例.zip](完整示例.zip)：`人间词话`（function 模式、仓颉多文件参考解、自定义 checker、8 个用例、4 个组），可直接导入。

## 11. 交付检查清单

- [ ] 交付物是一个 zip，根目录平铺，没有子目录，文件名全 ASCII。
- [ ] `problem.json` 只有 §2 的 12 个键；没有 `tests` / `checker` / `solution` / `driver` / `starter`。
- [ ] `id` 合法；`difficulty` 是整百；`tags` 来自词表；题面中英齐全。
- [ ] `groups` 至少 2 组，第一组 `sample` 且 1 分，`Σpoints == 100`。
- [ ] 每个 case 只属于一个组，`.in`/`.ans` 成对、`.ans` 非空、没有组外用例。
- [ ] `samples` 的 `input`/`output` 是完整 stdin/stdout（只展示，不判分）。
- [ ] 模式与文件匹配：function 有 main+starter（语言成对），io 没有 main/starter。
- [ ] 每种 `solution` 语言都有 `main.*`；多文件编号连续、每个 `.cj` 首行 `package` 一致。
- [ ] 有 `checker.cpp` 时它能处理多解/乱序/0 解、读完选手输出、容忍 `\r`；没有时输出与 `.ans` token 一致。
- [ ] 导入返回 200，`verification.solutions.*.score` 全 100。
- [ ] 另外手动交一次明显错误的代码，确认判 WA 而不是 AC。
