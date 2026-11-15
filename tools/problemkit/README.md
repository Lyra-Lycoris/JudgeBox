# problemkit：题包批量生成工具

一道题一个 spec 目录；`build.py` 把它变成能直接导入 JudgeBox 的题包 zip，并在本地用
**C++ / 仓颉 / Python / Java × 函数式 / 完整式** 共 8 种组合跑一遍验证。

```powershell
python tools/problemkit/build.py <spec-dir> [更多 spec-dir ...]
python tools/problemkit/build.py tools/problemkit/specs/prefix-sums/* --out build/problemkit
```

产物在 `build/problemkit/<id>.zip`，报告里每个 `[语言 方式] ok` 都必须通过。

## 1. 目录结构

```
specs/<专题 slug>/<题目 id>/
  meta.json            元数据 + signature（见 §2）
  statement.zh.md      中文题面（Markdown + LaTeX）
  statement.en.md      英文题面
  gen.py               生成测试数据：def cases(): 返回 [{"id": "01", "input": "..."}, ...]
  solution.cpp         参考解（只写 solve，不要 main）
  solution.py          参考解（只写 solve）
  solution.java        参考解（只写静态方法，不要 import / class / 外层大括号）
  solution.cj          参考解（首行 package <signature.package>，只写 func solve）
  checker.cpp          可选：SPJ（#include "testlib.h"）
```

## 2. meta.json

```json
{
  "id": "prefix-sum-range",
  "title": {"zh": "区间求和", "en": "Range Sum Queries"},
  "difficulty": 1200,
  "topic": "前缀和与差分",
  "tags": ["前缀和"],
  "limits": {"timeMs": 2000, "memoryMb": 256},
  "judgeType": "function",
  "source": {"platform": "luogu", "id": "P1001", "url": "https://www.luogu.com.cn/problem/P1001"},
  "samples": [{"input": "3 1\n1 2 3\n1 3\n", "output": "6\n"}],
  "signature": {
    "package": "prefix_sum_range",
    "params": [{"name": "n", "type": "int"}, {"name": "a", "type": "ints", "count": "n"}],
    "returns": "int",
    "hint": {"zh": "返回区间和"}
  }
}
```

- `id`：`^[a-z0-9][a-z0-9-]{1,47}$`，全局唯一。本批次用 `t<两位专题号>-` 前缀。
- `difficulty`：800–3500 且是 100 的整数倍。
- `topic`：必须与本批次的专题名完全一致（中文）。
- `tags`：1–3 个，只能取词表：模拟、枚举、排序、二分、贪心、构造、前缀和、差分、双指针、滑动窗口、
  哈希、栈、队列、单调栈、堆、并查集、树状数组、线段树、字符串、Trie、KMP、图论、最短路、最小生成树、
  拓扑排序、二分图、网络流、树、最近公共祖先、动态规划、背包、区间DP、状压DP、数位DP、树形DP、数学、
  数论、组合数学、概率期望、计算几何、位运算、分治、记忆化搜索、高精度、交互。
- `judgeType`：`function`（本批默认）或 `special`（有 checker.cpp 时）。
- `source.platform`：`luogu` / `leetcode` / `codeforces` / `other`；`url` 必须 `https://` 开头，可省略。
- `samples`：1–5 条，只展示不判分；`input`/`output` 必填。
- `limits.timeMs` 100–60000、`limits.memoryMb` 16–4096。

## 3. signature：driver 自动生成

`params` 按顺序就是 driver 从 stdin 读取的顺序，`returns` 决定怎么输出。

| type | 含义 | 读取方式 |
|---|---|---|
| `int` | 一个整数 | C++/Java 用 64 位整数，仓颉 `Int64`，Python `int` |
| `ints` | 一组整数 | 带 `"count": "n"` 表示个数由前面的参数给出；不带则 driver 先读一个 k |
| `string` | 一个不含空白的字符串 | 读一个 token |
| `strings` | 一组字符串 | 同 `ints`，带 `count` 或不带 |
| `matrix` | 整数矩阵 | 需 `"rows": "n", "cols": "m"` 引用前面的参数 |

| returns | 输出 |
|---|---|
| `int` | 一行一个整数 |
| `bool` | 一行 `YES` / `NO` |
| `string` | 一行字符串 |
| `ints_space` | 一行，空格分隔 |
| `ints_k` / `ints_lines` | 先输出个数，再每个一行 |

- `"repeat": true`：driver 先读一个 `T`，然后每组调用一次 `solve`，每次输出一行。题面里要写清楚多组。
- 生成的函数签名（写进 `function.signature`，做题页的 starter 与签名展示都用它）：
  - C++：`long long solve(long long n, const vector<long long>& a)`
  - 仓颉：`func solve(n: Int64, a: Array<Int64>): Int64`
  - Python：`def solve(n: int, a: list[int]) -> int`
  - Java：`static long solve(long n, long[] a)`
- `signature.hint.zh`：写进 starter 的 TODO 注释。
- `signature.package`：仓颉包名，小写下划线标识符，`solution.cj` 首行必须一致。

**不要**在 `params` 里放只用于读取、不参与计算的参数（例如多组的 T）——`repeat` 已经处理了。

## 4. gen.py

```python
import random

def cases():
    rng = random.Random(20261114)
    out = [{"id": "01", "input": "3 1\n1 2 3\n1 3\n"}]
    n = 200000
    a = [rng.randint(-10**9, 10**9) for _ in range(n)]
    out.append({"id": "02", "input": "..."})
    return out
```

- 返回 6–12 条用例；`id` 用 `01`、`02`…（不写也行，会按顺序补）。
- 第一条通常当样例组（真实判分，1 分），所以要与 `samples[0]` 一致。
- 至少要有：小数据、边界（n=1、全相同、负数、最大值）、随机中等、大数据。
- 单条输入 ≤ 4 MiB，所有 .in/.ans 合计 ≤ 64 MiB；答案 ≤ 4 MiB。
- 用固定随机种子，保证可复现。

## 5. 参考解写法（最容易 CE 的地方）

- C++：只写 `#include <bits/stdc++.h>` 与函数，**不要 `int main`**；参数类型必须与生成的 driver 声明完全一致。
- Python：只写 `def solve`；可以 `import sys`，不要写 `main()`。
- Java：只写静态方法（`static long solve(...)`），**不要** `import`、`class`、外层大括号。
- 仓颉：
  - 首行 `package <signature.package>`。
  - 只写 `func solve`，不要 `main`。
  - `ArrayList` 用 `add`（没有 `append`）；`for (i in 0..n)` 左闭右开；`Int64.parse(...)` 需 `import std.convert.Parsable`。
  - 数组参数是固定长度 `Array<Int64>`，不能 `append`；需要动态数组时自己用 `ArrayList` 再转 `Array`。
  - 可以用 `import std.sort.*` 的 `sort(arr)`、`sort(arr, descending: true)`。

## 6. 题面要求

- 中英各一份，`#` 标题开头，写清：题意、输入格式、输出格式、数据范围、样例说明。
- 不要写「两种提交方式」「函数签名」小节：平台界面已经展示提交方式与签名，题面只讲题目本身。
- 允许 Markdown 子集 + `$...$` / `$$...$$` LaTeX；不要写原始 HTML、图片、相对链接。
- 数据范围与 `gen.py` 实际生成的数据必须一致。

## 7. 验收标准

```
python tools/problemkit/build.py <spec-dir>
```
输出里 8 行都必须 `ok`（`cpp/cangjie/python/java` × `function/full`），最后一行 `完成 ...zip（语言 cpp,cangjie,python,java）` 没有「降级」。
任何语言失败都会打印编译错误或用例差异，按提示修 `solution.*` / `signature` / `gen.py` 后重跑。
