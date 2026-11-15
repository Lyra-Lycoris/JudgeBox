# JudgeBox v1.5.0 更新报告（2026-11-15）

## 一句话

装完就有 **235 道题**（28 个专题，难度 1000–2300，四语言 × 两种提交方式），启动时后台静默从 GitHub / Gitee 增量同步；题库可以自己新建、编辑、导入测试数据；做题代码自动按「专题 / 题目 / 语言 / 提交方式」存进 `solveRecord/`。

## 题库

- **235 道题**：新增 224 道原创题 + 原有 11 道；28 个专题覆盖模拟、枚举、贪心、二分、前缀和、双指针、哈希、栈队列、堆、并查集、树状数组/线段树、字符串、图论、最短路/最小生成树、树/LCA、线性 DP、背包/区间 DP、状压/树形 DP、数位/计数 DP、数学、组合/期望、位运算/构造、分治、计算几何/高精度、综合思维/SPJ、高级数据结构、复杂 DP、思维难题。
- 每道题 **C++ / 仓颉 / Python / Java × 完整程序式 / 函数评判式**，8 种组合都在本地真编译、跑满数据验证；另抽样用真实提交校验 AC。
- 难度分布：1000×25、1100×25、1200×25、1300×26、1400×30、1500×4、1600×25、1700×4、1800×25、1900×5、2000×6、2100×25、2200×5、2300×5。

## 题库分发与同步

| 项 | 数据 |
|---|---|
| 题包总量 | 235 个 zip / 320 MB |
| 全新安装首次拉取 | **63 秒**（320 MB，8 路并发） |
| 日常启动 | 只比对清单，几十毫秒，0 下载 |
| 源 | GitHub + Gitee 镜像双源，**题包优先走 Gitee**，失败自动换源 |
| 实测吞吐 | Gitee 5.1 MB/s、GitHub 1.3 MB/s |

- 清单按「文件名 + 大小」比对，只下缺失/变化的题包；两份清单取并集，镜像落后也不漏题。
- 下载走系统 `curl.exe`（WinHTTP 在 `raw.githubusercontent.com` 上会 IPv6 超时），代理变量失效时自动退回 WinHTTP。
- 首次 6.0 s 的题单加载也顺手优化了：题包元数据落盘索引 + 并行冷读，降到首次 1.5–2.5 s、之后 0.1 s 内。
- 想关掉：`ProblemDatabase/.sync.json` 写 `{"enabled": false}` 或设 `JUDGEBOX_SYNC_OFF=1`；也能换成自己的仓库（`sources` 数组）。

## 做题界面

- 顶部四张独立卡片：**时间限制 / 内存限制 / 评判方式 / 题目来源**。
- 评判方式跟随提交方式变化：完整程序 → 普通裁判；函数式 → 函数裁判；SPJ 题保持特殊裁判。
- 题面去掉「两种提交方式 / 函数签名」小节与标题下的 time limit 重复文案，只讲题目本身。
- 题单页新增**专题筛选**；卡片只保留难度/状态、中英标题、标签、专题与来源、得分进度。

## 自建题目

- 题库界面手动增删：「新建题目」→ 填题面 + 测试数据即可（默认自判题，判题直接比对 `.ans`）。
- 测试数据支持手填、从样例生成、或**从目录批量导入**一批 `.in` / `.ans`。
- 也能给自建题补四种语言的完整参考程序，保存时自动跑自检变成正式题。
- 做题页「自测 → 导入题目数据」把题包测试数据拉进面板，像调试一样看输入输出。

## solveRecord

```
solveRecord/<专题>/<id>_<题目名>/
  cpp/{full/main.cpp, function/solve.cpp}
  python/{full/main.py, function/solve.py}
  cangjie/{full,function}/  cjpm.toml + build.cmd + src/*.cj
  java/{full,function}/     pom.xml + build.cmd + src/main/java/*.java
```

做题草稿自动落盘；仓颉与 Java 的每个叶子目录都是可单独打开的小工程。

## 仓库拆分

- 主仓库：[Lyra-Lycoris/JudgeBox](https://github.com/Lyra-Lycoris/JudgeBox)（`ProblemDatabase/` 与 `solveRecord/` 已 gitignore）
- 题库：[JudgeBox-ProblemDatabase](https://github.com/Lyra-Lycoris/JudgeBox-ProblemDatabase)（235 个题包随仓库分发）
- Gitee 镜像：[night-ling114/JudgeBox-ProblemDatabase](https://gitee.com/night-ling114/JudgeBox-ProblemDatabase)
- 做题记录：[JudgeBox-SolveRecord](https://github.com/Lyra-Lycoris/JudgeBox-SolveRecord)（只有目录骨架）

## 出题工具链

`tools/problemkit/`：一题一个 spec 目录 → 生成四语言 driver/starter、用参考解算 `.ans`、本地验证 8 种组合、打包成题包 zip，配套 `build_all.py` / `install.py` / `smoke.py` / `report.py` / `scaffold_records.py`。

## 升级说明

- 旧版的题目、草稿、提交记录都还在（`ProblemDatabase/`、`solveRecord/`、`.cache/` 原地不动），覆盖安装即可。
- 第一次启动会自动补题（如果你之前题库是空的），约 1 分钟；不想联网就往 `ProblemDatabase/.sync.json` 写 `{"enabled": false}`。
