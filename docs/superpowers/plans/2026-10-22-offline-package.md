# Offline Toolchain Package Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for inline execution; request one independent final review.

**Goal:** 验证四种语言并交付内置工具链的 Windows 11 x64 离线安装包。
**Architecture:** 固定版本 runtimes 目录，exe 相对寻址；每用户可写记录目录；工具链自检与单文件 Inno Setup 安装包。
**Tech Stack:** C++20 / Win32 / Python 构建脚本 / Inno Setup。
**Spec:** docs/superpowers/specs/2026-10-22-offline-package-design.md

## Global Constraints

不改用户 PATH/现有 SDK；不动用户运行记录；不发布至外部；不得用 skip 掩盖缺失工具；保留第三方 notices；仅承诺实际测试过的 x64 组合。

## Review Focus

- 目标机没有开发软件：所有工具都必须从发布包找到，清理 PATH 后测试。
- 发布目录包含中文/空格、记录目录只读：相对工具路径、可写用户目录和路径兼容验证。
- Python 嵌入式运行库：py_compile、标准库动态扩展、CYaRon 和依赖离线验证。
- SDK 的间接 DLL 与子编译器：完整包依赖提取、PE 扫描和干净环境运行矩阵。
- 安装升级/卸载：不删除用户记录，不自动启动未知旧版本，验证静默安装和已安装目录。

## Tasks

- [x] 1. 创建 tests/toolchain_matrix.py 并先对本机工具执行四语言矩阵，修复真实失败。
- [x] 2. 创建 scripts/stage_toolchains.py 与固定依赖清单，准备 runtimes；测试 bundled-first 检测失败后实现工具链检测（src/compiler.cpp），并调整默认用户数据目录。
- [x] 3. 在搬迁后的包上清空开发环境变量执行语言矩阵；补充自检入口与依赖扫描，记录报告。
- [x] 4. packaging/JudgeBox.iss 与打包脚本生成离线 exe，静默安装到测试目录再次验证。
- [x] 5. 独立只读审查、修复、运行适当回归，更新使用说明、版本与验证边界，交付实际产物。

## Ledger

- 本机为 Windows 11 Home 中文版 x64，未发现 Windows Sandbox 或现成 VM；清 PATH 的本机验证不能等同于干净 VM 验证。
- 2026-10-22：本机四语言矩阵、清空环境变量的内置工具链矩阵、PE 直接依赖扫描均通过。安装包静默安装到带中文和空格的目录后，内置 Python 的 `--self-test` 通过 30 项；升级和卸载保留了用户数据。产物为 `dist/JudgeBox-Setup-1.1.0-x64.exe`。修复了目录联接重复打开时被 libstdc++ `equivalent` 误判，以及安装参数含空格时被拆开的问题。
