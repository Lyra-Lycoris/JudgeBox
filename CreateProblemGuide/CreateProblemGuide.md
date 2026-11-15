# 出题指南（题包 v2：四种语言 × 两种提交方式）

> **读者**：出题者（人或模型）。读完应当能独立产出一个能被 JudgeBox 导入、且参考答案在 **C++ / 仓颉 / Python / Java × 完整式 / 函数式** 共 8 种组合下都跑满 100 分的题包。
> **唯一判据**：`POST /api/problems/import` 返回 200，且 `verification.solutions.<语言>.score == 100`、`verification.full.<语言> == true`（四种语言都要有）。
> **交付物是一个 zip**。同目录下有一份可直接导入的 [完整示例.zip](完整示例.zip) 和一个 [模板/](模板/) 目录（A+B，四种语言两种方式全开，能直接跑通）。
> 本文按 2026-11-14 的实现写；报错原文都取自习校验器，可以按字面搜索。

## 0. 交付物：一个 zip

```
<id>.zip
  problem.json               # 只能放元数据（见 §2）
  <caseId>.in                # 全部测试数据，平铺在根目录
  <caseId>.ans
  checker.cpp                # 可选：SPJ / 自定义判定；没有就按内置 token 比较
  main.cpp    starter.cpp    solution.cpp      # C++     （完整式参考程序由平台自动拼出）
  main.cj     starter.cj     solution.cj       # 仓颉
  main.py     starter.py     solution.py       # Python
  main.java   starter.java   solution.java     # Java
```

硬性约束：

- **不能有子目录**（`题包 zip 不能有子目录：xxx`）；所有文件平铺在根目录。
- **文件名一律用 ASCII**（`a-z A-Z 0-9 _ - .`）。平台用系统 `tar.exe` 解压，包里出现中文文件名会解压失败。`problem.json` 里的中文内容没问题，只有**文件名**受限。
- 导入时允许 zip 里套一层同名目录（Windows 右键"压缩到 zip"很常见），平台会自动下钻；但不要套两层。
- 除上表以外的文件（`README.md` 之类）会被忽略，不会当成用例。
- 导入接口只收 zip：`{"zipPath": "绝对路径"}` 或 `{"zip": "<base64>"}`（§9）；也可以直接把 zip 拷进 `ProblemDatabase`，刷新题单就会出现。
- zip 体积：base64 上传建议 ≤ 44 MiB（请求体上限 64 MiB）；更大的用 `zipPath`。

## 1. 概念

| 词 | 含义 |
|---|---|
| 题包 | 上面那个 zip；最终放在 exe 同级的 `ProblemDatabase/<id>_<题目名>_.zip` |
| 用例 case | 一份 `.in` + 一份同名 `.ans`；判题时一个用例起一个进程 |
| 组 group | 若干用例 + 一个分值；组内全 AC 才拿这组的全部分数 |
| 提交方式 | `function`（函数式：选手只写函数）或 `full`（完整式：选手交完整程序） |
| driver（`main.*`） | 只做 I/O 胶水：读 stdin → 调选手的 `solve` → 写 stdout。**函数式**必填 |
| starter（`starter.*`） | 给选手的初始骨架：签名 + `// TODO` + 返回空值，必须能和 driver 一起编译 |
| solution（`solution.*`） | 标准答案。**函数式**里是函数实现（平台会拼成完整程序）；**只开完整式**的语言里是完整程序 |
| checker（`checker.cpp`） | 可选。给了就是 SPJ/自定义判定；不给就按 token 比较 |

**两种提交方式对选手的区别**

- 完整式：选手拿到的是"自己写 `main` 的完整程序"模板，判题时直接编译他交的源码。
- 函数式：选手只实现 `solve`（签名见题面），平台把题包里的 driver 和他的代码拼起来编译。

**题包必须同时提供**：每种语言的 driver + starter + 函数参考解；完整式不需要额外文件（平台用 `main.* + solution.*` 自动拼出完整参考程序并自检）。

## 2. `problem.json`（只放元数据）

**白名单**：只允许下表 16 个键，多一个就报 `未知字段 xxx`。

| 字段 | 类型 | 必填 | 约束 |
|---|---|---|---|
| `schemaVersion` | int | 是 | 新题必须写 `2`；`1` 是旧格式（只支持 C++/仓颉、单一 `judgeMode`），仅用于兼容老题包 |
| `id` | string | 是 | `^[a-z0-9][a-z0-9-]{1,47}$`（2–48 字符）；同时是目录名与 API 路径；不要用 `import` 当 id |
| `title` | `{zh,en}` | 是 | 只允许这两个键；两侧非空，各 ≤ 80 字符（按 Unicode 码点） |
| `difficulty` | int | 是 | 800–3500 且是 100 的整数倍，决定题单排序 |
| `tags` | string[] | 是 | 1–3 个，必须来自 §8.3 词表；重复不会报错，但别写 |
| `limits` | `{timeMs,memoryMb}` | 是 | 只允许这两个键；`timeMs` 100–60000，`memoryMb` 16–4096 |
| `modes` | object | 是（v2） | 语言 → 提交方式数组。语言只能是 `cpp`、`cangjie`、`python`、`java`；方式只能是 `function`、`full`；每种语言至少一种、不能重复 |
| `statement` | `{zh,en}` | 是 | 只允许这两个键；两侧非空，各 ≤ 64 KB（UTF-8 字节）；Markdown 子集见 §7.1 |
| `samples` | array | 是 | 1–5 项，见 §7.2。**只展示，不参与判分** |
| `groups` | array | 是 | 至少 2 组，第一组必须是 `sample`，见 §5 |
| `function` | object | 有 `function` 方式时必填 | 只允许 `package` 与 `signature`；driver/starter 不写在这里（来自文件） |
| `notes` | `{zh,en}` | 否 | 出题人备注，只给导入者看 |
| `topic` | string | 否 | 专题（≤ 24 字符），题单按它筛选，`solveRecord/<专题>/…` 也按它分目录 |
| `judgeType` | string | 否 | `standard`（普通，默认）/ `special`（特殊，带 checker）/ `interactive`（交互）/ `function`（函数）。不写就按内容推断：有 checker → special，有函数式 → function，否则 standard |
| `source` | object | 否 | 只允许 `platform`（`luogu`/`leetcode`/`codeforces`/`other`）、`id`、`url`（`https://` 开头） |
| `selfJudge` | bool | 否 | `true` = 自判题：只有测试数据，没有参考解与 driver，判题直接比对 `.ans`。导入/保存时不跑自检；此时 `modes` 可省略（默认四种语言都只开完整式），且不允许声明 `function` |

**不要写** `tests`、`testsZipPath`、`checker`、`solution`、`driver`、`starter`、`judgeMode`（v2）、`signature`（题包里的 `signature` 在 `function.signature` 下面）：这些现在都由文件提供或不属于题包，写进 JSON 会报 `未知字段` 或专门的迁移提示。

```json
{
  "schemaVersion": 2,
  "id": "a-plus-b",
  "title": {"zh": "A+B 问题", "en": "A Plus B"},
  "difficulty": 800,
  "tags": ["模拟"],
  "limits": {"timeMs": 1000, "memoryMb": 128},
  "modes": {
    "cpp":     ["function", "full"],
    "cangjie": ["function", "full"],
    "python":  ["function", "full"],
    "java":    ["function", "full"]
  },
  "statement": {"zh": "# A+B\n…", "en": "# A Plus B\n…"},
  "samples": [{"input": "2\n3\n", "output": "5\n", "explain": {"zh": "2 + 3 = 5。", "en": "2 + 3 = 5."}}],
  "groups": [{"name": "sample", "points": 1, "cases": ["01"]},
             {"name": "main", "points": 99, "cases": ["02"]}],
  "function": {
    "package": "demo",
    "signature": {
      "zh": "func solve(a: Int64, b: Int64): Int64",
      "en": "solve(a, b) -> a + b",
      "cpp":     "long long solve(long long a, long long b)",
      "cangjie": "func solve(a: Int64, b: Int64): Int64",
      "python":  "def solve(a: int, b: int) -> int",
      "java":    "static long solve(long a, long b)"
    }
  }
}
```

### 2.1 `modes`（本题支持哪些语言、哪些方式）

- **新题的标准是四种语言 × 两种方式全开**（上面那份 JSON）。题库里的题也都按这个标准交付。
- 校验器只要求"声明了就必须有对应文件"，所以过渡期可以少开几种语言/方式；但不要在一道正式题里只开 C++——选手会以为题目坏了。
- 某个语言声明了 `function`，就必须有 `main.<ext>`、`starter.<ext>`、`solution.<ext>`，并且 `function` 段要有 `package` 和 `signature`。
- 某个语言只声明 `full`，则 `solution.<ext>` 必须是**完整程序**（自带入口），不能有 `main.<ext>` / `starter.<ext>`。
- 同时声明两种方式时：`solution.<ext>` 是**函数实现**，完整式参考程序由 `main.<ext> + solution.<ext>` 自动拼出（§4.4）。

### 2.2 `function.signature`

- `zh` / `en` 必填，是给人看的签名（题面里会展示）。
- 可选的 `cpp` / `cangjie` / `python` / `java` 是**按语言**的精确签名；题面里按语言展示，选手的 starter 也是这个签名。
- 题面里**不要**再写「两种提交方式」「函数签名」小节：做题页会按当前选择的提交方式自动显示裁判方式，编辑器的 starter 也已经带上精确签名。

## 3. 语言与文件对照

| 语言 | 扩展名 | driver | starter | 参考解（函数式） |
|---|---|---|---|---|
| C++ | `.cpp` | `main.cpp` | `starter.cpp` | `solution.cpp` |
| 仓颉 | `.cj` | `main.cj` | `starter.cj` | `solution.cj` |
| Python | `.py` | `main.py` | `starter.py` | `solution.py` |
| Java | `.java` | `main.java` | `starter.java` | `solution.java` |

- `judgedLanguages`：就是 `modes` 里声明的语言（按 C++、仓颉、Python、Java 的顺序）。
- 每种语言的函数参考解只能有一个文件；`solution_1.cpp` 这类多文件只属于旧格式（v1），v2 会报错。
- 参考解总大小：每种语言 ≤ 512 KB。

## 4. 四种语言怎么写（最容易 CE 的地方）

### 4.1 C++

`main.cpp`：

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

`solution.cpp` / `starter.cpp` 只写函数，**不能有 `main`**，也不能 `#include` 自己额外写的头文件。平台把 `main.cpp + solution.cpp` 拼成一个 `Main.cpp` 编译。

### 4.2 仓颉（包名最常错）

`main.cj` 是完整文件：

```cangjie
package demo

import std.convert.Parsable

main(): Unit {
    let a = Int64.parse(readln().trimAscii())
    let b = Int64.parse(readln().trimAscii())
    println(solve(a, b))
}
```

`solution.cj` / `starter.cj` 首行也必须是 `package demo`。规则：

1. `function.package` 必填，整道题只用这一个名字。
2. `main.cj`、`starter.cj`、`solution.cj` **首行都必须是 `package <function.package>`**。
3. 选手提交没写 `package` → 平台自动补；写了别的包名 → 不改写，按 CE 报错（日志原样返回）。
4. 函数式判题时 driver 与选手代码是两个 `.cj` 文件一起编译；完整式参考程序由平台合并成一个文件（package 只留一个、开头 `import` 去重提前），所以两个文件的 `import` 都必须写在文件最前面。

仓颉速查：

```cangjie
import std.convert.Parsable                 // Int64.parse
import std.collection.{ArrayList, HashMap}
import std.sort.*                           // sort(arr) / sort(arr, descending: true)

let n = Int64.parse(readln().trimAscii())
let a = Array<Int64>(n, repeat: 0)
for (i in 0..n) { a[i] = ... }              // 0..n 左闭右开
let map = HashMap<Int64, Int64>()
let old = map[1] ?? 0
map[1] = old + 1
println(value)
```

### 4.3 Python

选手代码在前、`main.py` 追加在后，合成一个 `main.py`。因此 driver 要**自带 import、定义 `main()`、并在最后调用 `main()`**：

```python
import sys


def main():
    data = sys.stdin.buffer.read().split()
    a = int(data[0])
    b = int(data[1])
    print(solve(a, b))


main()
```

`starter.py` / `solution.py` 只写 `solve`：

```python
import sys


def solve(a: int, b: int) -> int:
    return a + b
```

### 4.4 Java（类体外壳由平台补）

平台生成：

```java
import java.util.*;
import java.io.*;
import java.math.*;

public class Main {
<main.java 的内容>
<选手代码>
}
```

所以 `main.java` 只写类体成员（`public static void main(...)` 等），**不要写 import / class / 外层大括号**：

```java
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        long a = Long.parseLong(st.nextToken());
        long b = Long.parseLong(st.nextToken());
        System.out.println(solve(a, b));
    }
```

`solution.java` / `starter.java` 只写静态方法：

```java
    static long solve(long a, long b) {
        return a + b;
    }
```

- 完整式提交时选手自己写完整程序，**必须**是 `public class Main` 且带 `public static void main`（平台把文件存成 `Main.java` 再 `javac`）。
- 判题时 JVM 的 `-Xmx` 会自动按 `limits.memoryMb` 调小，不用自己写。

### 4.5 完整式参考程序怎么来

- 同时开了 `function` 的语言：平台自动拼
  - C++：`main.cpp + solution.cpp`
  - Python：`solution.py + main.py`
  - Java：和函数式相同的 class Main 外壳
  - 仓颉：把 `main.cj` 与 `solution.cj` 合并（package 去重、开头 import 提前）
- 只开 `full` 的语言：`solution.<ext>` 本身就是完整程序，直接编译。

## 5. 用例数据

### 5.1 文件与 id

- 平铺：`<caseId>.in` + `<caseId>.ans` 放在 zip 根目录。
- `caseId` 匹配 `^[a-z0-9][a-z0-9_-]{0,15}$`（1–16 字符，小写字母/数字/`-`/`_`，以字母或数字开头）。
- 每个 case 必须恰好属于一个组；`groups[].cases` 里的 id 必须都有对应文件（`用例 05 缺少 05.in` / `05.ans`）。
- zip 里不允许有组外的 `.in/.ans`（`用例 07 不在任何组中`）。
- `.ans` 不能是空文件；建议末尾保留换行。
- UTF-8，可带 BOM；单文件 ≤ 4 MiB；用例数 ≤ 200；`Σ(input+ans)` ≤ 64 MiB；zip 内文件数 ≤ 500。

### 5.2 `.ans` 从哪来

先用参考解跑 `.in` 得到输出，再当 `.ans`。注意：

- **普通题（不写 checker）**：`.ans` 必须和选手输出的 token 序列一致，顺序也要一致。
- **SPJ 题**：`.ans` 只是占位（平台要求它存在），判定完全由 `checker.cpp` 读 `inf` 现场完成；`.ans` 里放参考解的输出即可。
- **多解且可枚举的题**：可以写"比较型 checker"（和 `.ans` 的集合/排序结果比），也可以写 SPJ。**真正的多解（任何合法输出都算对）必须用 SPJ**，不能靠把"所有解"塞进 `.ans`。

### 5.3 输入编码

- `.in` 会**原样**喂给进程的 stdin，平台不加、不减任何东西。
- 一个进程只跑一个用例。要带"用例数"就由 **driver 自己**决定：driver 读 `T` 就写 `1`；driver 不读 `T` 就完全不用写。
- 四种语言的 driver 必须读**同一份** `.in`、写**同一种**输出格式（`.ans` 只有一份）。

## 6. 组与分值

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

## 7. checker：默认比较 与 SPJ

### 7.1 不写 `checker.cpp`（默认）

平台用内置 **token 比较**：把选手输出和 `.ans` 按空白切成 token 逐段比，空白/换行的差异不算错，token 顺序算错。适合绝大多数"输出唯一"的题。

### 7.2 写 `checker.cpp`（SPJ / 自定义判定）

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
- checker 与语言无关：四种语言的输出都交给同一个 checker，所以格式必须统一。

### 7.3 两个必踩的坑

**① 行尾**：Windows 上程序 `println` 输出 CRLF，而 `.ans` 可能是 LF。按行读时先去掉行尾 `\r` 和多余空格，否则假 WA。

**② `readInt()` 之后不要直接 `readLine()`**：`readInt` 会把流停在行尾分隔符前，紧接着的 `readLine()` 读到空串，整个文件错位一行。正确做法是先 `readLine()` 读表头再自己 `stoi`：

```cpp
auto header = ouf.readLine();
if (header.empty()) quitf(_wa, "缺少解数");
int n = std::stoi(header);
for (int i = 0; i < n; ++i) { auto line = ouf.readLine(); /* 去掉 \r */ }
```

## 8. 题面、样例、标签

### 8.1 题面 Markdown 子集

允许：`#`~`######` 标题、段落、`**粗体**`、`*斜体*`、`~~删除线~~`、行内代码、围栏代码块（```lang）、有序/无序列表（可多层嵌套，列表后另起一段要空一行）、`>` 引用、表格（含 `:---:` 对齐）、水平线、链接（仅 `https://`，带 `rel="noopener"`）、`<https://…>` 自动链接、行尾两个空格或 `\` 换行、数学 `$…$` 与 `$$…$$`（离线 MathJax 渲染；也接受 `\(…\)` 与 `\[…\]`）。

公式排版：行内公式与正文同字号；`$$…$$` 单独成行居中，公式比题面宽时在块内横向滚动，不会被缩小。`$` 与 `$$` 必须成对且 `$` 内层首尾不空格，否则按普通文本显示。

不允许：原始 HTML、`<script>`、iframe、行内 `style`、脚注、相对链接、图片。

- 中英两侧都必须写，各 ≤ 64 KB。
- 题面只讲题目本身；提交方式与函数签名由平台界面展示（做题页的提交方式下拉框、裁判方式卡片、编辑器 starter），不要写进题面。
- 题面里的仓颉示例代码首行必须是 `package <function.package>`（§4.2）。

### 8.2 `samples`（只展示，不判分）

```json
{"input": "2\n3\n", "output": "5\n", "explain": {"zh": "2 + 3 = 5。", "en": "2 + 3 = 5."}}
```

- 1–5 项；只允许 `input`/`output`/`explain` 三个键；`input`/`output` 非空字符串。
- `input` 是喂给程序的**完整 stdin**，`output` 是它应当输出的完整内容（driver 读 `T` 就在这里写 `1`）。
- `explain` 可选，`{zh,en}` 字符串。
- **`samples` 不参与判分**；判分只看 `groups[].cases` 对应的 `.in/.ans`。样例组（`sample`）是另一回事：它是真实判分组，用例来自文件。

### 8.3 标签词表（只能用这些）

模拟、枚举、排序、二分、贪心、构造、前缀和、差分、双指针、滑动窗口、哈希、栈、队列、单调栈、堆、并查集、树状数组、线段树、字符串、Trie、KMP、图论、最短路、最小生成树、拓扑排序、二分图、网络流、树、最近公共祖先、动态规划、背包、区间DP、状压DP、数位DP、树形DP、数学、数论、组合数学、概率期望、计算几何、位运算、分治、记忆化搜索、高精度、交互

## 9. 判题语义与限制

- 一个用例一个进程；stdin 是 `.in`，stdout 落盘后交给 checker（或内置比较）。
- 时间上限 = `limits.timeMs`（墙钟，语言系数 1.0，四种语言一样）。**Python/Java 的启动开销也算在内**，出数据时给足余量。
- 内存 = `limits.memoryMb`（Job Object 硬上限）；Java 的 `-Xmx` 会自动调到 `memoryMb` 以内。
- 输出上限 = `max(1 MiB, .ans 大小 + 1 MiB)`。
- 编译上限：60 秒 / 2 GiB / 2 MiB 输出；编译日志超过 64 KB 会截断。
- 函数式提交的额外开销：C++/Python/Java 拼成一个源文件；仓颉是两个 `.cj` 一起编译，编译时间略长。
- `verdict` 取值：`AC WA TLE MLE RE OLE CE JE CANCELLED`；得分只累计"组内全 AC"的组，`verdict` 取第一个非 AC。
- 判题是单任务：已有提交在判时再提交返回 409；调试任务（`/api/run`）在跑时提交也返回 409。
- 提交源码 ≤ 1 MiB；单条提交记录 ≤ 256 KB（超了先丢 `compileLog`、再截断源码并标 `sourceTruncated`）；每题最多保留 50 条提交。
- 提交记录会保存 `language` 与 `mode`（`function`/`full`）。

## 10. 导入与自检

### 10.1 接口

```json
{"zipPath": "E:\\problems\\a-plus-b.zip"}
{"zip": "<zip 的 base64>"}
```

- 只收 zip；`zipPath` 必须是绝对路径。前端网页走 base64（选文件 → 自动编码）。
- 请求体上限 64 MiB；base64 会膨胀约 1/3，所以网页导入建议 ≤ 44 MiB。
- 导入是同步的：首次要编译 checker 与四种语言的 driver/starter/参考解，约 10–60 秒；成功会覆盖同 `id` 的旧版本并返回 `"replaced": true`。
- **题库目录**：exe 同级的 `ProblemDatabase/`，里面只放题包 zip，命名 `<id>_<题目名>_.zip`（题目名取 `title.zh`，去掉了文件名非法字符）。导入就是把上传的 zip 按这个名字写进去；也可以直接把 zip 拷进去，刷新题单即出现。
- 首页题单和题目详情都从 zip 里的 `problem.json` 读，卡片标题是其中的 `title.zh`，**不是压缩包文件名**。
- 导入失败**不会写盘**，旧版本原样保留，可以反复试。

### 10.2 自检三项（任何一项失败即 400）

1. 有 `checker.cpp` 就编译它（`checker 编译失败（前 20 行）：…`）。
2. 对每个声明了 `function` 的语言，用 `main + starter` 编译一次（`drivers.cpp 编译失败（前 20 行）：…`）。
3. 对每道题：

   - **函数式**：用 `main + solution` 跑全部用例，必须 100 分；
   - **完整式**：`solution` 本身就是完整程序的（只开 `full` 的语言）直接跑；两种方式都开的语言由平台拼出完整程序后跑，必须 100 分（C++/Python/Java 与函数式是同一份程序，成绩沿用；仓颉合并后单独跑）。
   - 失败报 `参考答案未满分（语言）：…` 或 `完整式参考答案未满分（语言）：…`。

成功响应：

```json
{"ok": true, "id": "a-plus-b", "replaced": true,
 "verification": {"cases": 2,
   "groups": [{"name": "sample", "points": 1, "passed": true}],
   "checker": "custom", "checkerCompiled": true,
   "drivers": {"cpp": true, "cangjie": true, "python": true, "java": true},
   "solutions": {"cpp": {"score": 100, "verdict": "AC"},
                 "cangjie": {"score": 100, "verdict": "AC"},
                 "python": {"score": 100, "verdict": "AC"},
                 "java": {"score": 100, "verdict": "AC"}},
   "full": {"cpp": true, "cangjie": true, "python": true, "java": true}}}
```

`checker` 是 `"custom"`（有 checker.cpp）或 `"builtin"`（走内置比较，此时 `checkerCompiled` 为 false）。

### 10.3 报错对照表

| `details[].message` | 原因 | 怎么改 |
|---|---|---|
| `未知字段 xxx` | `problem.json` 多写了键 / 拼错 | 对照 §2 的 12 个键 |
| `schemaVersion 只能是 1（旧格式）或 2（四语言 × 两提交方式）` | 版本号写错 | 新题写 2 |
| `schemaVersion 2 不再使用 judgeMode，请改用 modes` | 旧字段没删 | 删 `judgeMode`，加 `modes` |
| `schemaVersion 2 必须提供 modes（语言 → 提交方式数组）` | 少了 modes | 补 §2.1 |
| `modes 里的语言 xxx 不支持` | 语言拼错/用了别的语言 | 只能是 cpp、cangjie、python、java |
| `modes.cpp 里的 xxx 只能是 function 或 full` | 方式拼错 | 改成 `function` / `full` |
| `请提供题包 zip：…` | 没给 zipPath / zip | 按 §10.1 |
| `zipPath 必须是绝对路径` / `找不到题包 zip` | 路径错 | 用绝对路径并确认存在 |
| `题包 zip 根目录没有 problem.json` | 少了题面文件，或套了两层目录 | 平铺到根目录 |
| `题包 zip 不能有子目录：xxx` | 包里有文件夹 | 全部平铺 |
| `题包 zip 解压失败（文件名请全部用 ASCII）` | 包内有中文文件名 | 改成 ASCII 文件名 |
| `id 格式不合法` | 大写 / 下划线 / 长度不对 | `^[a-z0-9][a-z0-9-]{1,47}$` |
| `title.zh 不能为空` / `title.en` | 少写一侧 | 双语都要写 |
| `difficulty 必须是 800–3500 之间 100 的整数倍` | 档位写错 | 改整百 |
| `未知标签 xxx` | 不在词表 | 从 §8.3 选 |
| `groups 至少需要 2 组（含 sample）` | 只有一组 | 至少 sample + 一个判分组 |
| `第一组必须是 sample 组` / `样例组 points 必须为 1` | 首组写错 | 见 §6 |
| `groups 分值之和为 98，应为 100` | 分不完 | 调到总和 100 |
| `用例 02 出现在多个组中` | 一个 case 挂两组 | 每个 case 只留一组 |
| `用例 05 缺少 05.in` / `05.ans` | 数据文件不齐 | 补齐 |
| `用例 05 的 .ans 是空文件` | 答案为空 | 写真实答案 |
| `用例 07 不在任何组中` | 有组外用例 | 删掉或加进组 |
| `函数式提交必须提供 function 段（package 与 signature）` | 声明了 function 但没 function 段 | 补 §2 |
| `function.package 含有非法字符` | 包名带空格 / `/` | 用单个标识符 |
| `缺少 main.cpp（C++ 函数式 driver）` | 声明了 function 但没 driver | 补 `main.*` |
| `缺少 starter.cpp（C++ 函数式 starter）` | 声明了 function 但没 starter | 补 `starter.*` |
| `缺少 solution.py（Python 函数式参考解）` | 声明了 function 但没参考解 | 补 `solution.*` |
| `modes 没有声明 Python 的函数式提交，但题包里有 main.py` | 多给了文件 | 在 `modes` 里声明 function，或删掉文件 |
| `缺少 solution.java（Java 只声明完整式提交时必须提供完整参考程序）` | 只开 full 却没有完整程序 | 补完整程序，或改成两种方式都开 |
| `schemaVersion 2 每种语言只能有一个 solution.cpp（不支持 solution_1 多文件）` | v2 用了旧多文件写法 | 合并成一个文件 |
| `有 solution.cpp，但没有对应的 main.cpp（参考答案的语言必须有 driver）` | 旧格式（v1）没配 driver | 补 `main.*`，或把 schemaVersion 改成 2 |
| `checker 编译失败（前 20 行）` | checker 编译错误 | 按日志修 |
| `drivers.cpp 编译失败（前 20 行）` | driver/starter 错 / 包名不一致 | 看日志 |
| `参考答案（仓颉）编译失败（前 20 行）` | 参考解编译错误 | 看日志 |
| `参考答案未满分（C++）：组 boundary 未通过（用例 05 WA）：…` | 参考解错 / checker 判错 | 先看 message |
| `完整式参考答案未满分（Python）` | 完整式路径有问题 | 看函数式是否满分、driver/参考解有没有写错 |

## 11. 模板与完整示例

- [模板/](模板/)：一份能直接导入的 A+B（四种语言 × 两种提交方式、SPJ、两个用例）。改 `problem.json` 和 `solution.*` 就能变成你的题。
- [完整示例.zip](完整示例.zip)：`人间词话`（四种语言 × 两种提交方式、仓颉参考解、自定义 checker、8 个用例、4 个组），可直接导入。
- 本地批量自检（可选）：仓库里的 `tests/problem_api_test.py` 会用真实 exe 导入并提交；创建题包时也可以先用四种语言的编译器手工跑一遍。

## 12. 交付检查清单

- [ ] 交付物是一个 zip，根目录平铺，没有子目录，文件名全 ASCII；最终以 `<id>_<题目名>_.zip` 放进 `ProblemDatabase/`。
- [ ] `problem.json` 是 `schemaVersion: 2`；只有 §2 的 12 个键；没有 `tests` / `checker` / `solution` / `driver` / `starter` / `judgeMode`。
- [ ] `modes` 四种语言 × 两种方式全开（`cpp`/`cangjie`/`python`/`java` 各 `["function","full"]`）。
- [ ] 四种语言都有 `main.<ext>`、`starter.<ext>`、`solution.<ext>`；starter 与 driver 能一起编译。
- [ ] `function.package` 与四个仓颉文件首行一致；`signature` 有 zh/en，最好也有四种语言的精确签名。
- [ ] 四种语言的 driver 读同一份 stdin、写同一种输出；输出与 `.ans` 逐 token 一致。
- [ ] 参考解不写 `main`（函数式），C++ 不额外 include 本地头文件，Java 不写 class 外壳/import。
- [ ] `id` 合法；`difficulty` 是整百；`tags` 来自词表；题面中英齐全（不写提交方式与函数签名）。
- [ ] `groups` 至少 2 组，第一组 `sample` 且 1 分，`Σpoints == 100`。
- [ ] 每个 case 只属于一个组，`.in`/`.ans` 成对、`.ans` 非空、没有组外用例。
- [ ] `samples` 的 `input`/`output` 是完整 stdin/stdout（只展示，不判分）。
- [ ] 有 `checker.cpp` 时它能处理多解/乱序/0 解、读完选手输出、容忍 `\r`；没有时输出与 `.ans` token 一致。
- [ ] 导入返回 200，`verification.solutions.*.score` 全 100，`verification.full.*` 全 true。
- [ ] 另外手动交一次明显错误的代码，确认判 WA 而不是 AC；再分别用四种语言各交一次正确的完整式/函数式代码，确认都能 AC。
