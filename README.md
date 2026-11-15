# JudgeBox

[JudgeBox-Setup-1.5.0-x64.exe](https://github.com/Lyra-Lycoris/JudgeBox/releases/download/v1.5.0/JudgeBox-Setup-1.5.0-x64.exe) · [SHA-256](https://github.com/Lyra-Lycoris/JudgeBox/releases/download/v1.5.0/JudgeBox-Setup-1.5.0-x64.exe.sha256)

上面是 Windows 11 x64 离线安装包，自带 C++、Python、Java、仓颉工具链。安装后从桌面或开始菜单打开，会直接显示 JudgeBox 窗口，不再弹出命令行窗口，也不需要手动选择工具链。界面使用系统自带的 WebView2 运行库；Windows 11 已内置该组件。

还有关于数据生成的功能 我在下面写了，请你们看完好不好

## 开发版

```powershell
git clone https://github.com/Lyra-Lycoris/JudgeBox.git
cd JudgeBox
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

需要 Windows 10/11、CMake 3.20+ 和 MSYS2 UCRT64。完成后双击根目录的 `JudgeBox.exe`，或运行 `启动JudgeBox.cmd`。窗口界面使用系统自带的 Microsoft Edge WebView2 运行库；Windows 11 已内置，Windows 10 若提示缺失请安装 WebView2 Runtime。自动化测试可以运行 `JudgeBox.exe --no-browser`，它只启动本地引擎并打印地址。

以及别告诉我你不会用git，不会用git的请先自己找点教程，实在不愿意，用安装包也可以

## 题目系统（开发中）

后端题包层已经可用：一个题包 **zip** → `POST /api/problems/import` → 题单 / 提交 / 判题 / 历史。出题规范见 [CreateProblemGuide](CreateProblemGuide/CreateProblemGuide.md)，同目录下有可直接导入的 `完整示例.zip` 和 `模板/`。
zip 根目录放 `problem.json`（`schemaVersion: 2`）、`<caseId>.in/.ans`、`checker.cpp`（SPJ，可选），以及 C++/仓颉/Python/Java 各一套 `main.*`（函数式 driver）/`starter.*`/`solution.*`；没有 `checker.cpp` 时按内置 token 比较判。
每道题都同时支持四种语言 × 两种提交方式：**完整程序**（选手自己写 `main`）与**函数式**（选手只实现 `solve`，平台和题包自带的 driver 拼接）。题包自检会把四种语言的函数参考解都跑满 100 分，并验证完整式参考程序。
验收：`ctest --test-dir build -R problem --output-on-failure`，会导入夹具题包，用参考解跑满 100 分，再提交错误代码校验 0 分，并覆盖四种语言两种方式的提交。
题目统一放在 exe 同级的 `ProblemDatabase/`（开发时就是 `E:\JudgeBox\ProblemDatabase`），文件名 `<id>_<题目名>_.zip`；直接把 zip 拷进去刷新即可。
判题缓存写在 exe 同级的 `.cache/`（`submissions/` 历史、`judge/` 逐点产物、`checkers/` 编译缓存）。
手工试：`JudgeBox.exe --no-browser --data-dir %TEMP%\jb`，用启动窗口地址里的 token 调接口即可。

### 题目元数据（题单与做题页的卡片）

`problem.json` 在 v2 的基础上多了四个可选字段，题单筛选、做题页卡片和 `solveRecord` 分层都靠它们：

| 字段 | 作用 |
|---|---|
| `topic` | 专题（如「动态规划」「图论与搜索」）。题单页按专题筛选，`solveRecord/<专题>/…` 也按它分目录 |
| `judgeType` | 裁判方式：`standard`（普通，逐 token 比较）、`special`（特殊，题包带 `checker.cpp`）、`interactive`（交互）、`function`（函数，只实现 `solve`） |
| `source` | 题目来源：`{"platform": "luogu" \| "leetcode" \| "codeforces" \| "other", "id": "P1001", "url": "https://…"}` |
| `selfJudge` | 自判题：题包里只有测试数据，没有参考解与 driver，判题直接拿 `.ans` 比。保存时不跑自检 |

做题页顶部是四张独立卡片：**时间限制**、**内存限制**、**评判方式**、**题目来源**（洛谷 / 力扣 / Codeforces 会显示平台名与编号，带链接）。

### 新建 / 编辑题目

题单页右上角「新建题目」，或题目卡片的「⋯ → 编辑题目」：

- 新建时默认是**自判题**：填好专题、标签、题面、样例与测试数据即可保存，判题直接对比 `.ans`。也可以把四种语言的完整参考程序填进「参考解」区域，保存成正式题（会跑自检）。
- 测试数据可以一条条手填，也可以点「从目录导入测试数据」，选一个装着成对 `<名字>.in` / `<名字>.ans` 的文件夹，一次读进来。
- 编辑已有题目只改元数据 / 题面 / 测试数据，题包里的参考解与 driver 原样保留；如果测试数据太大没被完整载入，保存时不会改动数据。
- 接口：`POST /api/problems/save`，`GET /api/problems/<id>/raw`（编辑用），`GET /api/problems/<id>/cases`（自测用），`POST /api/problems/scan-cases`（从目录导入测试数据），`DELETE /api/problems/<id>` 删除。

做题页「自测」面板里的「导入题目数据」会把题包的 `.in/.ans` 拉进来，像调试一样看输入与输出；自判题打开时会自动导入。

### solveRecord：自己的做题代码

做题页的草稿除了存 `localStorage`，还会自动写到 exe 同级的 `solveRecord/`：

```
solveRecord/<专题>/<id>_<题目名>/
  cpp/{full/main.cpp, function/solve.cpp}
  python/{full/main.py, function/solve.py}
  cangjie/{full/src/main.cj, function/src/solution.cj}   外加 cjpm.toml + build.cmd
  java/{full/src/main/java/Main.java, function/src/main/java/Solution.java}  外加 pom.xml + build.cmd
```

仓颉与 Java 的每个叶子目录都是一个能单独打开的小工程。接口：`POST /api/record/save`、`POST /api/record/scaffold`（一次建好一道题的八个目录）、`GET /api/records?problemId=…`。

`ProblemDatabase/` 与 `solveRecord/` 已写进 JudgeBox 的 `.gitignore`，各自是独立仓库：

- 题库：[JudgeBox-ProblemDatabase](https://github.com/Lyra-Lycoris/JudgeBox-ProblemDatabase)（公开，235 个题包随仓库分发）
- 做题记录：[JudgeBox-SolveRecord](https://github.com/Lyra-Lycoris/JudgeBox-SolveRecord)（只提交目录骨架，自己的代码按需提交）

### 题库自动同步（启动时静默增量更新）

每次启动，程序都会在**后台线程**里同时探测两个源（GitHub 与 Gitee 镜像），挑**延迟最低**的那个拉清单，再按「文件名 + 大小」跟本地 `ProblemDatabase/` 比对，只下载缺失或变化的题包；下载是**并发 8 路**的，全部处理完前端再刷新题单并提示「已同步 N 道题」。整个过程不阻塞窗口、不影响做题，离线时静默失败。

- 默认两个源：`Lyra-Lycoris/JudgeBox-ProblemDatabase`（GitHub）与 `night-ling114/JudgeBox-ProblemDatabase`（Gitee 镜像）。
- **所有题包优先从 Gitee 下载**（地址按 Gitee 排前，同一个包 Gitee 优先），Gitee 上还没有的题才回退 GitHub；清单取并集，所以镜像暂时落后也不会漏题。实测本机 Gitee 5.1 MB/s、GitHub 1.3 MB/s，235 道题 320 MB 首次拉取 **63 秒**。
- 下载走系统自带的 `curl.exe`：`raw.githubusercontent.com` 在部分网络下会让 WinHTTP 卡在 IPv6 上超时，curl 更稳；没有 curl 时自动退回 WinHTTP。一个地址失败会换下一个源的地址重试。
- 每次启动只发两次目录请求（各几十 KB），题包没变化就一个字节都不下；单次失败会重试 3 次，下次启动继续补。
- 关掉：在 `ProblemDatabase/.sync.json` 里写 `{"enabled": false}`，或设环境变量 `JUDGEBOX_SYNC_OFF=1`。
- 换成自己的仓库 / 固定某个源：`.sync.json` 写
  ```json
  {"sources": [
    {"kind": "gitee",  "repo": "owner/name", "ref": "main"},
    {"kind": "github", "repo": "owner/name", "ref": "main"}
  ]}
  ```
  （`kind` 可选 `github` / `gitee`；`path` 留空表示仓库根目录就是题库；Gitee 的 API 默认 `https://gitee.com/api/v5`、默认分支 `master`，导入来的仓库通常是 `main`，要显式写 `ref`）
- 状态：`GET /api/sync/status`，返回 `running / kind / repo / sourceMs / sources / added / updated / skipped / failed / error`。

### 批量出题工具

`tools/problemkit/` 把「一道题一个 spec 目录」编译成题包：生成四种语言的 driver 与 starter、用参考解算出 `.ans`、本地跑满 8 种组合的验证、再打包成 zip。约定见 [tools/problemkit/README.md](tools/problemkit/README.md)。

```powershell
python tools/problemkit/build.py tools/problemkit/specs/<专题>/<题目id>
python tools/problemkit/install.py          # 装进 ProblemDatabase
python tools/problemkit/smoke.py            # 起引擎，检查每道题能不能正常加载
```


## 数据生成 JSON

对拍方式和数据生成模式需要对格式进行规范，我们规定了一些预设，当然，不可能把所有方式的预设全部写了，我们只能用手写 json 去定制每一个题目的生成规则

因为作者在json相关的知识储备也没有那么充足，所以以下文案由grok4.7生成，作者二次校订

在「生成测试」中把数据模板改为「自定义 JSON 规则」。
注意很多地方都要带引号

一份规则按 `steps` 从上到下执行。某一步用 `name` 记下的整数，后面用字符串引用，例如 `"count": "n"`。表达式可写变量、整数、`+ - * /` 和括号，除法向零取整。

### 先写 n，再写一行整数

```json
{
  "steps": [
    {"type": "int", "name": "n", "min": 1, "max": 8},
    {"type": "array", "count": "n", "min": -10, "max": 10}
  ]
}
```

```text
5
3 -1 8 0 4
```

`int` 在 `min` 到 `max` 之间取一个整数，换行输出，并记入 `name`。`array` 在同一行输出 `count` 个整数。只保存数值、不写入输入时，加上 `"emit": false`。

### 同一行多个数

```json
{
  "steps": [
    {"type": "line", "items": [
      {"name": "n", "min": 2, "max": 8},
      {"name": "m", "min": "n-1", "max": "n*(n-1)/2"},
      1
    ]}
  ]
}
```

得到一行 `n m 1`。`items` 中的对象会随机取值；数字和 `"n"` 这样的表达式直接输出。

### 一次输入里包含多组

```json
{
  "steps": [
    {"type": "int", "name": "T", "min": 1, "max": 3},
    {"type": "repeat", "count": "T", "steps": [
      {"type": "int", "name": "n", "min": 1, "max": 8},
      {"type": "array", "count": "n", "min": 0, "max": 100}
    ]}
  ]
}
```

`repeat` 将内部步骤重复 `count` 次，变量 `i` 从 1 开始。界面上的「测试组数」是程序启动几次；这里的 `T` 是这一次输入中有几组。

### 每组一个长度随机的 01 串

```json
{
  "steps": [
    {"type": "int", "name": "n", "min": 1, "max": 5},
    {"type": "repeat", "count": "n", "steps": [
      {"type": "int", "name": "len", "min": 1, "max": 8, "emit": false},
      {"type": "string", "length": "len", "alphabet": "01"}
    ]}
  ]
}
```

```text
3
0110
1
001
```

这个在codeforces上常见，`string` 输出一行字符串。`length` 填写一个数，或填写前面生成的变量名；长度要随机时，先用 `"emit": false` 生成这个变量。`alphabet` 是允许出现的字符，默认 `abc`。

### 矩阵、树、图、固定文本

矩阵输出 `rows` 行，每行 `cols` 个整数：

```json
{"type": "matrix", "rows": "n", "cols": "m", "min": 0, "max": 9}
```

树输出 `n-1` 行 `u v`。点从 1 编号，结果连通且无环。点数由前面的步骤输出，`tree` 只输出边。`"weighted": true` 时，`min` 和 `max` 是边权范围。

```json
{"type": "int", "name": "n", "min": 2, "max": 8}
{"type": "tree", "nodes": "n"}
```

图输出 `m` 条无自环、无重边的边，点数和边数由前面的步骤输出。`"directed": true` 为有向图。需要连通图时使用 Python 脚本。

```json
{"type": "graph", "nodes": "n", "edges": "m", "directed": false, "weighted": false, "min": 1, "max": 20}
```

`literal` 按 `text` 原样写入，换行写成 `\n`：

```json
{"type": "literal", "text": "0\n"}
```

### 界限

整数和表达式的中间结果在 ±10^12 以内。一组输入最多 1 MiB。`count`、`rows`、`cols` 和 `repeat` 的次数最大 10000；字符串长度最大 100000；数组与矩阵合计最多 100000 个数。树最多 10000 个点，简单图最多 1000 个点、100000 条边。嵌套最多 12 层。

「最小」「最大」「边界与随机交替」只改变整数取到下界还是上界。字符串的内容，以及树和图的连边，仍然随机。同一套规则、种子和测试序号会生成同一份输入。

更复杂的约束改用界面中的 Python / CYaRon 脚本，见 [输入生成规则](docs/输入生成规则.md)。
