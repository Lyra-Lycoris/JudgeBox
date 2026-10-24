# JudgeBox

Windows 本地判题与随机对拍工具。C++20 执行引擎，双击启动，在浏览器里粘贴代码即可使用；页面资源全部随 exe 内置，使用时无需联网

声明：纯手写部分大约占据30% 主要负责了src的工程目录初始化部分与时间判定逻辑，VibeCoding完成了剩余部分与前端工作

完整离线发行版为 `dist/JudgeBox-Setup-1.1.0-x64.exe`。安装包内置 GCC 16.1.0、CPython 3.14.9、Temurin JDK 21.0.11+10、仓颉 SDK 1.2.0、CYaRon 0.7.0 及其依赖，目标机器不需要预装这些工具。此版本面向 Windows 11 x64，安装到当前用户目录，不改系统 PATH。安装目录约需 1.7 GiB 空间，安装时还需额外临时空间。
仓库根目录仅含 `JudgeBox.exe` 的开发版仍依赖本机工具链
不能只复制那个exe 就获得四种语言的离线工具

离线版安装后可运行开始菜单的 `Check Toolchains` 或安装目录的 `Check-Toolchains.cmd`；它调用 `JudgeBox.exe --self-test`，使用内置 Python 验证全部四语言及 CYaRon，不依赖系统 Python。报告保存在当前数据目录的 `toolchain-self-test.json`。安装包的 SHA-256 在同目录 `.sha256` 文件中。打包脚本还会把安装包静默装到带中文和空格的目录，复测后把 `toolchain-installed-unicode-report.json` 放在安装包旁边。

## 启动

双击项目根目录的 **JudgeBox.exe**，或 **启动JudgeBox.cmd**。程序自动打开本机浏览器；保持终端窗口运行。右上角“退出”或终端 `Ctrl+C` 可停止引擎。关闭浏览器页面不会停止引擎。

根目录开发版 exe 由 `build.ps1` 构建复制，源码仓库不追踪生成的 exe。首次从源码使用：

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

需要 Windows 10/11、CMake 3.20+、MSYS2 UCRT64 GCC（C++20）和 MinGW Makefiles。脚本会使用本机 `C:\msys64\ucrt64\bin`（若存在）；其他位置需先把工具链放入 PATH。

也可以手动构建：

```powershell
cmake -S . -B build -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
cmake --build build -j 4
ctest --test-dir build --output-on-failure
.\build\JudgeBox.exe
```

构建后的 JudgeBox.exe 静态链接自身 GCC 运行库。被测程序的编译器、解释器仍需安装；界面“工具链设置”会自动检测，并允许填写 exe 的完整路径。执行时自动为编译器及待测程序补入相应工具链的 DLL 路径。

## 三种流程

- **手动测试**：粘贴源码，添加多组标准输入与预期输出，运行后查看每点的状态、时间、内存、退出码和 stderr。勾选“参与答案比较”时，空字符串也是有效的空答案；取消勾选后只运行，成功显示 RUN。
- **生成测试**：选择数组、整数对、矩阵、字符串、树、简单图、多组数组模板，设置规模、范围、种子与边界策略，预览后批量运行。可把数据加入手动测试，填写肉眼算出的正确答案。
- **随机对拍**：另贴已 AC 程序或暴力程序，选择其语言与独立时间上限。两个程序接收同一输入，发现第一个不一致或待测程序异常时停止，展示并下载反例。参考程序错误会明确显示 JE，编译日志或测试详情包含原因。

固定种子、规则、取值策略、测试序号可复现内置生成器的数据。复杂格式可编辑 JSON 规则，或使用 Python/CYaRon 生成器，详见 [输入生成规则](docs/输入生成规则.md)。完整离线包已带 CYaRon；仅运行开发版时，它仍是可选依赖。

支持 C++20、Python 3、Java、仓颉。Java 源码入口须为无 package 的 `Main` 类。Java 最大堆按内存上限计算，给 JVM 原生开销预留空间；较低内存可能无法启动 JVM，可提高到 512 或 1024 MiB。仓颉编译命令与运行时路径已在本机 cjc 1.2.0 验证；中文工具/编译目录优先使用 Windows 短文件名，必要时创建每用户英文目录联接，访问原有 SDK 而不复制整套工具。GCC 同时禁用路径前缀规范化，防止把英文入口还原成无法识别的中文路径。

## 判题规则与资源

| 状态 | 含义 |
| --- | --- |
| AC | 所有参与比较的测试点均通过 |
| WA | 正常退出，但输出不符合比较规则 |
| TLE | 超过墙钟时间，终止进程树 |
| MLE | Windows Job Object 内存限制通知确认超限 |
| RE | 程序以非零或异常退出码结束 |
| CE | 源码编译失败，显示编译日志 |
| OLE | stdout 和 stderr 合计超过输出上限 |
| JE | 编译器/解释器无法启动、参考程序错误、生成器错误或内部异常 |
| RUN | 正常运行结束，但有测试点未提供预期答案 |
| CANCELLED | 用户停止任务 |

默认 Token 比较按空白切分后逐项比较；严格模式逐字节比较（包含 CRLF/LF、尾随空白）；浮点模式对有限数值使用 `|actual - expected| <= ε * max(1, |expected|)`，非数值 token 仍按原字符串比较。诊断显示首个不同 token 或字节位置。stderr 不参与答案比较。

单点默认 1000 ms / 256 MiB / 1024 KiB 总输出。时间为墙钟时间，不是 CPU 时间，会包含解释器/JVM 启动成本；显示时间不含等待内存通知的收尾。内存指标为整个 Windows Job 的峰值提交字节，不是工作集，也不保证与在线平台一致。Windows 以 Job 提交量执行硬上限，MLE 通过完成端口资源通知识别；极端情况下若 OS 未送达通知，程序自行处理分配失败后退出可能表现为 RE、WA 或正常退出。编译限制为 60 秒 / 2 GiB / 2 MiB 输出，编译器资源失败显示 JE。

挂起创建进程、加入 Job 后恢复；限制句柄继承，stdin/stdout/stderr 并发传递；超时、超输出、取消和正常退出时均回收整个进程树。每次提交、参考程序及每个测试点使用独立工作目录。

**仅运行可信的个人代码。** Job Object 提供资源和进程树管理，未提供文件系统、网络隔离，不构成安全沙箱。

## 草稿、记录与导出

草稿自动存到 `runs/draft.json`，跨启动恢复；使用“导出工作区”保存源码、用例、生成规则、种子和工具链设置，另一台机器可导入并调整工具路径。每次任务在独立子目录保存 `request.json`、`result.json`、每点 `case-N.json`、编译源码与产物。界面显示本次引擎最近一次任务；旧记录可从磁盘查看。反例可分别下载 `.in`、`.ans`、`.out` 或完整测试点 JSON。

直接启动 exe 时，数据目录默认为 `%LOCALAPPDATA%\JudgeBox\runs`，安装目录只读也能使用；开发用启动脚本固定使用项目根目录 `runs`。升级只替换带有 JudgeBox 归属标记的运行库等目录，卸载保留用户数据。命令行可改路径与端口：

```powershell
.\JudgeBox.exe --data-dir E:\JudgeBox\runs --port 18080
.\JudgeBox.exe --no-browser
```

默认随机端口，只绑定 `127.0.0.1`。启动窗口第一行给出含会话凭据的本机地址；页面 API 校验会话凭据与 Host/Origin。自动草稿不依赖浏览器随机端口的 localStorage。

## 验证

`ctest` 包含执行器、生成器/比较器、实际 HTTP API 三组测试（API 测试需要 Python）。覆盖真实 AC、WA、TLE、MLE、RE、CE、OLE、取消、无答案、大输入、双流输出、进程树回收、中文空格路径、多语言、工具链不在 PATH、参考程序和生成器错误、跨域校验及 Java 大堆。

可选浏览器测试使用本机 Chrome：

```powershell
python -m pip install --target .runtime/playwright playwright
python tests/browser_test.py
```

验证源码粘贴、手动判题、自动生成、对拍、反例导出、工作区导入、草稿恢复、弹窗和小屏布局，截图保存于 `build/judgebox-*.png`。

项目附带 [nlohmann/json 3.12.0](https://github.com/nlohmann/json/releases/tag/v3.12.0)，许可见 `third_party/json.LICENSE.MIT`。数据生成流程参考 [CYaRon](https://github.com/luogu-dev/cyaron) 的使用思路，内置规则生成器独立实现，未复制其代码。用户原有未提交的进程实现备份在 `docs/process_win32.before.cpp.txt`。

## 离线包构建与验证边界

开发机具有上述固定版本的 MSYS2 UCRT64、Temurin JDK 和仓颉 SDK 后，执行 `powershell -ExecutionPolicy Bypass -File .\package.ps1`。可用 `-Msys`、`-Jdk`、`-Cangjie`、`-Python` 指定开发工具路径。脚本先构建并跑本机四语言矩阵；若已有版本匹配的暂存工具链，就只刷新程序文件，否则从本机 SDK 重新汇集并安装固定 Python 包。随后在清理开发环境变量后验证内置工具、扫描直接 DLL 依赖、生成离线安装包，再静默安装到中文加空格路径，用内置 Python 执行 `--self-test`，并确认升级和卸载都不删除用户数据。首次构建需要下载 Python 嵌入式包、Python 包和 Inno Setup；下载发生在开发机，已生成安装包在目标机使用时不需要下载。

发布文件的逐文件哈希、工具版本和来源分别在安装目录 `runtimes/file-sha256.json`、`runtimes/manifest.json`，测试报告在 `validation`，原始许可在各运行库和 `notices`。开发包版本及输入目录必须一致才能复现对应工具链；这些本机 SDK 的完整文件哈希作为发布清单记录，不宣称与任何未经核对的上游压缩包逐字节一致。公开再分发第三方二进制时，还需按各自许可提供对应源码；来源链接与许可文本不能替代该义务。

验证针对本机 Windows 11 Home 中文版 x64（10.0.26200）：四语言的 UTF-8 输入输出、常用库、CE、RE、TLE、OLE；清理 PATH/Java/Python/编译器环境变量；内置 CYaRon；直接 PE 依赖扫描；中文、空格安装路径及未启用短文件名磁盘的路径兼容。没有干净 Windows VM 的实测，也没有 ARM64 原生运行的实测，所以不承诺所有 Windows 11 配置均能运行。若系统策略同时禁止短文件名和目录联接，可改用英文安装/数据路径。未签名安装包可能显示 Windows 发布者确认；该包没有代码签名证书。

仅支持列出的语言版本与随包组件。Python 嵌入式包不包含所有桌面开发组件或任意第三方库，未内置 NumPy 等额外算法库；自检也不等于对所有合法程序的编译器正确性证明。
