# JudgeBox 更新说明

## v1.5.0（2026-11-15）

这一版把「题库」做成了能直接分发的东西：**装完就有 235 道题**，四种语言 × 两种提交方式，题单按 28 个专题组织，代码自动存进 `solveRecord/`。

### 题库：235 道题，28 个专题

- 新增 224 道原创题（加上原有 11 道共 **235 题**），难度 1000–2300 全覆盖，28 个专题：模拟与实现、枚举与暴力、排序与贪心、二分与二分答案、前缀和与差分、双指针与滑动窗口、哈希与计数、栈与队列、堆与优先队列、并查集、树状数组与线段树、字符串与匹配、图论与搜索、最短路与最小生成树、树与最近公共祖先、线性动态规划、背包与区间DP、状压DP与树形DP、数位DP与计数DP、数学与数论、组合数学与概率期望、位运算与构造、分治与递归、计算几何与高精度、综合思维与特殊裁判、高级数据结构与分块、复杂DP与最优化、思维难题与构造。
- 每道题都是 **C++ / 仓颉 / Python / Java × 完整程序式 / 函数评判式** 8 种组合，全部在本地真编译、真跑数据验证过，并抽样用真实提交校验 AC。
- 题包元数据新增 `topic`（专题）、`judgeType`（普通/特殊/交互/函数裁判）、`source`（洛谷/力扣/Codeforces）、`selfJudge`（只有测试数据的自判题）。

### 装完自动拉题库（静默、增量、双源）

- 全新安装第一次启动，后台自动从 GitHub / Gitee 拉取题库：**235 题 320 MB 约 63 秒**，不阻塞窗口，拉完题单自动刷新。
- 每次启动只比对一次清单（按「文件名 + 大小」），没变化就一个字节都不下。
- 双源：默认 GitHub + Gitee 镜像（`night-ling114/JudgeBox-ProblemDatabase`），清单取并集防漏题，**每个题包优先走 Gitee**，失败自动换源；下载 8 路并发，走系统 `curl.exe`（规避 WinHTTP 在 `raw.githubusercontent.com` 上的 IPv6 超时），代理环境变量失效时自动退回 WinHTTP。
- 题单加载提速：题包元数据落盘索引，235 道题从「每次启动 6.0 s」降到「首次 1.5–2.5 s、之后 0.1 s 内」。
- 可用 `ProblemDatabase/.sync.json` 或 `JUDGEBOX_SYNC_OFF=1` 关闭，也能改成自己的仓库。

### 做题界面

- 顶部把**时间限制 / 内存限制 / 评判方式 / 题目来源**做成四张独立小卡片。
- 评判方式跟随提交方式：完整程序 → 普通裁判，函数式 → 函数裁判；SPJ 题保持特殊裁判。
- 题面只保留题目本身：删掉「两种提交方式 / 函数签名」小节，也不再在标题下重复 time limit 文案。
- 题单页新增专题筛选；卡片只保留难度/状态、中英标题、标签、专题与来源、得分进度。

### 自建题目与自判

- 题库界面支持手动增删：右上角「新建题目」、卡片菜单「编辑题目 / 删除」。
- 新建默认是**自判题**：只填题面 + 测试数据即可，判题直接拿 `.ans` 比；测试数据可以手填、用样例生成，或「从目录导入」一批 `.in/.ans`。
- 也可以给自建题补四种语言的完整参考程序，保存时自动跑自检，变成正式题。
- 做题页「自测 → 导入题目数据」把题包的测试数据拉进面板，像调试一样看输入输出。
- 新接口：`/api/problems/save`、`/api/problems/<id>/raw`、`/api/problems/<id>/cases`、`/api/problems/scan-cases`、`/api/record/save`、`/api/record/scaffold`、`/api/sync/status`。

### solveRecord：自己的代码按专题归档

- 做题草稿自动写到 `solveRecord/<专题>/<题目>/<语言>/<完整式|函数式>/`。
- 仓颉与 Java 的每个叶子目录都是能单独打开的小工程（`cjpm.toml` / `pom.xml` + `build.cmd`）。

### 出题工具链

- 新增 `tools/problemkit/`：从「一题一个 spec 目录」生成四语言 driver/starter、用参考解算 `.ans`、本地验证 8 种组合、打包成题包 zip，配套 `install.py` / `smoke.py` / `scaffold_records.py` / `report.py`。

### 仓库拆分

- `ProblemDatabase/` 与 `solveRecord/` 移出主仓库，各自独立：[题库](https://github.com/Lyra-Lycoris/JudgeBox-ProblemDatabase)、[做题记录](https://github.com/Lyra-Lycoris/JudgeBox-SolveRecord)；Gitee 镜像：[JudgeBox-ProblemDatabase](https://gitee.com/night-ling114/JudgeBox-ProblemDatabase)。

详细说明见 [v1.5.0 更新报告](docs/Update-v1.5.0.md)。

<!-- 以下是 v1.4.0 的四语言题包升级，已并入 1.5.0 -->

## v1.4.x 开发记录：四语言 × 两种提交方式

- 题目系统升级为题包 v2：每道题都支持 **C++ / 仓颉 / Python / Java** 四种语言的 **完整式** 与 **函数式** 两种提交方式，共 8 种组合。
  - 完整式：选手交完整程序（自己写 `main`）；函数式：选手只实现 `solve`，平台与题包自带的 driver 拼接。
  - 做题页新增「提交方式」下拉框；语言、提交方式、草稿、自测、提交历史、题单卡片都会显示对应组合。
  - 导入自检会编译并跑通四种语言的函数参考解（`verification.solutions.*.score == 100`），并验证四种语言的完整式参考程序（`verification.full.* == true`）。
  - Java 判题自动按题目内存上限调整 `-Xmx`；仓颉完整式参考程序由平台把 driver 与参考解合并后自检。
- 题包格式：`problem.json` 用 `schemaVersion: 2` + `modes`（语言 → `function`/`full`）+ `function.signature`（zh/en + 四种语言的精确签名）；每种语言提供 `main.*` / `starter.*` / `solution.*`。旧格式 `schemaVersion: 1` 仍可导入。
- 出题规范重写：[CreateProblemGuide.md](CreateProblemGuide/CreateProblemGuide.md)、`模板/` 与 `完整示例.zip` 全部升级为四语言 × 两方式。
- 题库内全部题目迁移为四语言 × 两方式，四种语言都提供函数式参考解与 starter。
- 提交记录保存 `mode`（`function` / `full`），历史列表可区分。
- 新增题包元数据：`topic`（专题）、`judgeType`（普通 / 特殊 / 交互 / 函数裁判）、`source`（洛谷 / 力扣 / Codeforces）、`selfJudge`（只有测试数据的自判题）。
- 题单页新增专题筛选，卡片显示专题 / 裁判方式 / 来源；做题页顶部把时间限制、内存限制、评判方式、题目来源做成四张独立卡片。
- 题库界面支持手动增删：新增「新建题目」对话框与卡片菜单里的「编辑题目」，可改元数据、题面、样例、测试数据；`POST /api/problems/save`、`GET /api/problems/<id>/raw`、`GET /api/problems/<id>/cases`。
- 自判题：只导入 `.in/.ans`，判题直接比对答案；做题页「自测 → 导入题目数据」把题包数据拉进来，像调试一样看输入输出。
- 新增 `solveRecord/`：做题草稿自动按「专题 / 题目 / 语言 / 完整式·函数式」落盘，仓颉与 Java 的每个叶子目录都是可单独打开的小工程（`cjpm.toml` / `pom.xml`），另有 `POST /api/record/save`、`/api/record/scaffold` 接口。
- `ProblemDatabase/` 与 `solveRecord/` 移出 JudgeBox 仓库（`.gitignore`），各自作为独立仓库维护。
- 新增 `tools/problemkit/`：从「一题一个 spec 目录」生成四语言 driver/starter、用参考解算 `.ans`、本地验证 8 种组合并打包成题包 zip；配套 `install.py` / `smoke.py` / `scaffold_records.py`。
- 题面只保留题目本身：删掉「两种提交方式 / 函数签名」小节，做题页也不再在标题下重复 time limit 文案（顶部已有卡片）；裁判方式卡片跟随「提交方式」变化（完整程序 → 普通裁判，函数式 → 函数裁判，SPJ 题保持特殊裁判）。
- 题库扩充：新增 28 个专题共 224 道原创题（难度 1000–2300 全覆盖，题库合计 235 题），四种语言两种提交方式全部通过本地验证，并抽样用真实提交校验 AC。
- 题单加载提速：题包元数据落盘索引（`.cache/problemdb/index-<题库哈希>.json`，按 `大小@修改时间` 失效），冷读改成多线程并行；235 道题从「每次启动 6.0 s」降到「首次 1.5–2.5 s、之后 0.1 s 内」，浏览器到第一张卡片约 0.6 s。
- 新增 GitHub 题库静默同步：每次启动在后台线程拉一次仓库目录清单，按「文件名 + 大小」增量下载缺失/变化的题包到 `ProblemDatabase/`，不阻塞界面；同步完成后前端自动刷新题单并提示「已从 GitHub 同步 N 道题」。下载优先用系统 `curl.exe`（规避 WinHTTP 在 raw.githubusercontent.com 上的 IPv6 超时），失败重试 3 次、下次启动续传；可用 `ProblemDatabase/.sync.json` 或 `JUDGEBOX_SYNC_OFF=1` 关闭；接口 `GET /api/sync/status`。
- 题库改为随仓库分发：[JudgeBox-ProblemDatabase](https://github.com/Lyra-Lycoris/JudgeBox-ProblemDatabase) 已公开并提交 235 个题包，全新安装第一次启动即可自动拉下来。
- 题库同步支持 **Gitee 镜像**（`.sync.json` 里 `kind: "gitee"`，API 走 `gitee.com/api/v5`），可把仓库换成国内镜像；首次装题库改成 **8 路并发下载**。
- 同步改为**双源**：默认同时探测 GitHub 与 Gitee 镜像（`night-ling114/JudgeBox-ProblemDatabase`），清单取并集防漏题；**每个题包的下载地址都按「Gitee 优先」排序**（新题也先走 Gitee，Gitee 上没有才回退 GitHub），单个地址失败自动换源重试。本机实测 Gitee 5.1 MB/s、GitHub 1.3 MB/s，235 题 320 MB 首次拉取 **63 秒**（此前串行约 18–25 分钟）。

## v1.4.0（2026-11-14）

- 新增题目系统：题单页按难度 / 标签 / 状态筛选；做题页左侧双语题面（数学公式离线渲染）、右侧 C++ / 仓颉编辑器，内置 starter 与函数签名。
- 提交后按组判题：完整 IO 式与封装函数式两种模式，逐点起进程，用 checker（SPJ）或内置 token 比较判分，按组计分、满分 100；结果按 ICPC 揭榜动画呈现，并与本题历史最佳对比。
- 题包改为一个 zip 交付：`problem.json` + 用例 `.in/.ans` + `checker.cpp`（SPJ，可选）+ `main.*`/`starter.*`（函数题）+ `solution.*`；同一 id 重导即覆盖。
- 出题资料随仓库提供：`CreateProblemGuide/`（出题指南、可直接导入的完整示例 zip、可改的模板）。
- 提交历史落在 exe 同级的 `.cache/`，可在界面清空；每题保留最近 50 条。
- 修：判题中途取消在编译 checker 阶段被误判为 JE；含中文路径的题包 zip 无法解压。
- 修：题面公式被图标样式压成 17×17 方块——行内 `$n$` 撑得比正文大、`$$\sum…$$` 缩成看不清的一条；题面改为按 Markdown 结构渲染（分级标题、多层列表、引用、表格、代码块），列表后的段落不再被并进列表项。

详细说明见 [2026-11-14 更新报告](docs/Update-v1.4.0.md)。

## v1.3.1（2026-11-12）

- 随机对拍的参考程序改用与待测程序相同的编辑器，支持高亮、键位和语法检查。
- 启动脚本每次先做增量编译，再启动较新的那份程序，并行数按本机逻辑处理器和内存计算。

详细说明见 [2026-11-12 更新报告](docs/更新报告-2026-11-12.md)。

## v1.3.0（2026-11-11）

- 桌面/开始菜单图标补齐：程序、安装包、卸载入口和窗口都使用 JudgeBox 图标，桌面快捷方式默认创建。
- 启动方式改为原生窗口：安装后双击图标直接打开 JudgeBox 窗口，不再显示命令行窗口，也不需要手动打开浏览器。界面由系统自带的 WebView2 承载。
- 工具链完全内置：C++、Python、Java、仓颉随安装包分发，启动时自动检测并锁定使用；旧草稿里残留的空路径不会再覆盖内置工具链。
- 工具链设置页改为只读展示，并明确提示“已内置、无需选择”；只有内置文件缺失时才允许填写自定义路径。
- 安装包、卸载程序和程序资源都补齐版本信息与图标。

## v1.2.0（2026-11-11）

本版本重点是前端美观程度，参照了作者之前的博客（acm-lycoris.cn）的已经成熟前端页面，现在变得更好看了。
