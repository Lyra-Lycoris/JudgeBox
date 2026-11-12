# 手把手：把 JudgeBox v1.3.0 发布到 GitHub Release

这篇文档按“从当前仓库到 Release 页面可下载”的顺序写。命令都在仓库根目录 `E:\JudgeBox` 下执行，使用 PowerShell。

---

## 0. 先理解 Release 是什么

GitHub 仓库里的代码由 Git 管理；**安装包不进 Git**，而是作为 Release 的附件上传。

这次发布需要三样东西：

| 内容 | 位置 | 作用 |
| --- | --- | --- |
| 源代码提交 | Git `main` 分支 | 让别人能看到 1.3.0 的代码 |
| Tag `v1.3.0` | Git 标签 | 把 Release 固定到某个提交 |
| 安装包和 SHA-256 | Release 附件 | 用户实际下载的文件 |

⚠️ 本项目 `.gitignore` 忽略了 `dist/`，所以安装包不会出现在 `git status` 里，这是正常的，不要用 `git add -f dist` 强行提交。

---

## 1. 发布前检查

### 1.1 确认版本号一致

```powershell
Select-String -Path package.json,packaging\JudgeBox.iss,src\resources.rc,src\server.cpp,README.md -Pattern '1\.3\.0'
```

应至少看到：

- `package.json` 的 `"version": "1.3.0"`
- `packaging/JudgeBox.iss` 的 `AppVersion=1.3.0`
- `src/resources.rc` 的 `FILEVERSION 1,3,0,0`
- `src/server.cpp` 的 `"version","1.3.0"`
- `README.md` 里的 `v1.3.0` 下载链接

### 1.2 确认安装包和校验值

```powershell
Get-Item dist\JudgeBox-Setup-1.3.0-x64.exe
Get-Content dist\JudgeBox-Setup-1.3.0-x64.exe.sha256

$expected = (Get-Content dist\JudgeBox-Setup-1.3.0-x64.exe.sha256).Split()[0]
$actual   = (Get-FileHash dist\JudgeBox-Setup-1.3.0-x64.exe -Algorithm SHA256).Hash.ToLower()
$expected -eq $actual
```

最后一行必须是 `True`。

当前正确值：

```text
75e64d99d28b93fb46c867a26fcac777071bc7cf2639ec635cf2e0816356f069
```

安装包大小约 427 MB（427,318,459 字节），如果只有一百多 MB，说明上次编译被中断，需要重新编译：

```powershell
powershell -ExecutionPolicy Bypass -File .\package.ps1 -SkipBuild -SkipLocalMatrix -SkipBundledMatrix
```

### 1.3 确认工作区

```powershell
git status --short
git branch --show-current
```

当前分支应为 `main`。`git status` 会显示本次修改的源码、文档和新增的 `third_party/webview2`、图标等文件；`dist/` 和 `build/` 不应出现。

---

## 2. 提交并推送源代码

先把 1.3.0 的代码提交到 `main`，否则后面打的 Tag 还指向旧代码。

```powershell
cd E:\JudgeBox
git add -A
git status --short
git commit -m "Release JudgeBox v1.3.0"
git push origin main
```

提交前建议再看一眼 `git status`，确认没有把临时日志、测试数据加进去。`.runtime/`、`build/`、`dist/` 都已被忽略。

如果 `git push` 被拒绝（远端 `main` 有新提交），先同步再推送：

```powershell
git pull --rebase origin main
# 如有冲突，解决后：
git add -A
git rebase --continue
git push origin main
```

如果第一次提交提示没有身份，先配置：

```powershell
git config user.name "你的名字"
git config user.email "你的邮箱"
```

如果 `git push` 要求登录，使用 GitHub 的 HTTPS 凭据或 Personal Access Token；也可以先配置 SSH。

---

## 3. 创建并推送 Tag

Tag 名必须是 **`v1.3.0`**，带 `v`。README 里的下载地址是：

```text
https://github.com/Lyra-Lycoris/JudgeBox/releases/download/v1.3.0/JudgeBox-Setup-1.3.0-x64.exe
```

如果 Tag 写成 `1.3.0`，这个链接会 404。

```powershell
git tag -a v1.3.0 -m "JudgeBox v1.3.0"
git push origin v1.3.0
```

检查：

```powershell
git tag --list "v1.3.0"
git show v1.3.0 --stat
```

> 如果你已经在 GitHub 网页上创建过同名 Tag，先不要重复创建。用 `git ls-remote --tags origin` 确认远端是否已有 `v1.3.0`。

---

## 4. 方式 A：用 `gh` 命令行发布（推荐）

仓库里已经安装 `gh`（GitHub CLI）。用命令行上传 427 MB 比网页上传更稳，也更容易重试。

### 4.1 登录

```powershell
gh auth status
```

如果显示未登录：

```powershell
gh auth login
```

选择：

1. `GitHub.com`
2. `HTTPS`
3. `Login with a web browser`
4. 浏览器里输入终端显示的一次性代码，授权

登录后再次执行：

```powershell
gh auth status
```

应显示 `Logged in to github.com account ...`。

### 4.2 推荐：先建草稿 Release，再上传，最后发布

先创建草稿，只写标题和说明：

```powershell
gh release create v1.3.0 `
  --title "JudgeBox v1.3.0" `
  --notes-file "docs/release-notes-v1.3.0.md" `
  --verify-tag `
  --draft
```

`--verify-tag` 表示“确认本地/远端已经有 `v1.3.0` 这个 Tag”，避免 gh 自动新建一个指向错误提交的 Tag。

上传两个附件：

```powershell
gh release upload v1.3.0 `
  "dist/JudgeBox-Setup-1.3.0-x64.exe" `
  "dist/JudgeBox-Setup-1.3.0-x64.exe.sha256"
```

如果中途失败或文件传错，用 `--clobber` 覆盖重传：

```powershell
gh release upload v1.3.0 `
  "dist/JudgeBox-Setup-1.3.0-x64.exe" `
  "dist/JudgeBox-Setup-1.3.0-x64.exe.sha256" `
  --clobber
```

打开网页检查：

```powershell
gh release view v1.3.0 --web
```

确认：

- 标题正确；
- 说明文字完整；
- 两个附件都在；
- 附件大小约 427 MB。

确认无误后发布：

```powershell
gh release edit v1.3.0 --draft=false
```

### 4.3 也可以一步完成

如果你不想先建草稿，可以直接创建正式 Release 并上传：

```powershell
gh release create v1.3.0 `
  "dist/JudgeBox-Setup-1.3.0-x64.exe" `
  "dist/JudgeBox-Setup-1.3.0-x64.exe.sha256" `
  --title "JudgeBox v1.3.0" `
  --notes-file "docs/release-notes-v1.3.0.md" `
  --verify-tag
```

上传过程中断时，同样用 `gh release upload ... --clobber` 补传。

### 4.4 用到的 `gh` 命令速查

```powershell
gh release list                     # 列出已有 Release
gh release view v1.3.0              # 查看详情
gh release view v1.3.0 --web        # 浏览器打开
gh release upload v1.3.0 <文件> --clobber
gh release edit v1.3.0 --draft=false
gh release delete v1.3.0 --yes       # 删除 Release（谨慎）
```

---

## 5. 方式 B：完全在 GitHub 网页上发布

如果你不想用命令行：

1. 浏览器打开仓库：
   `https://github.com/Lyra-Lycoris/JudgeBox`
2. 右侧点击 **Releases**，再点 **Draft a new release**。
3. **Choose a tag**：
   - 如果已经推送过 `v1.3.0`，下拉选择它；
   - 如果没有，输入 `v1.3.0`，点击 “Create new tag on publish”。
4. **Target** 选择 `main`。
5. **Release title** 填：
   `JudgeBox v1.3.0`
6. **Describe this release**：把 `docs/release-notes-v1.3.0.md` 的内容整段粘贴进去。
7. 在附件区域上传：
   - `dist/JudgeBox-Setup-1.3.0-x64.exe`
   - `dist/JudgeBox-Setup-1.3.0-x64.exe.sha256`
8. 勾选 **Set as the latest release**。
9. 点击 **Publish release**。

网页上传 427 MB 可能很慢，浏览器超时的话换 `gh` 命令行方式。

---

## 6. 发布后验证

### 6.1 检查 Release 页面

```powershell
gh release view v1.3.0
```

或直接打开：

```text
https://github.com/Lyra-Lycoris/JudgeBox/releases/tag/v1.3.0
```

### 6.2 检查下载链接

README 里的两个链接应该能直接下载：

```text
https://github.com/Lyra-Lycoris/JudgeBox/releases/download/v1.3.0/JudgeBox-Setup-1.3.0-x64.exe
https://github.com/Lyra-Lycoris/JudgeBox/releases/download/v1.3.0/JudgeBox-Setup-1.3.0-x64.exe.sha256
```

在 PowerShell 里实测：

```powershell
$url = "https://github.com/Lyra-Lycoris/JudgeBox/releases/download/v1.3.0/JudgeBox-Setup-1.3.0-x64.exe"
Invoke-WebRequest $url -OutFile "$env:TEMP\JudgeBox-1.3.0-check.exe"
Get-FileHash "$env:TEMP\JudgeBox-1.3.0-check.exe" -Algorithm SHA256
```

哈希应与 `75e64d99d28b93fb46c867a26fcac777071bc7cf2639ec635cf2e0816356f069` 一致。

### 6.3 最后做一次真实安装

在干净环境或虚拟机里：

1. 下载 Release 里的安装包；
2. 校验 SHA-256；
3. 安装；
4. 从桌面图标启动，确认没有命令行窗口；
5. 打开「设置 → 工具链设置」，确认五项都是「内置」；
6. 跑一个 C++ 或 Python 判题。

---

## 7. 发布错了怎么回滚

如果只是说明文字写错、附件漏传，不用删 Release：

```powershell
gh release edit v1.3.0 --notes-file "docs/release-notes-v1.3.0.md"
gh release upload v1.3.0 "dist/JudgeBox-Setup-1.3.0-x64.exe" "dist/JudgeBox-Setup-1.3.0-x64.exe.sha256" --clobber
```

如果 Tag 指错了提交或想整个重来：

```powershell
# 1. 删除 Release
gh release delete v1.3.0 --yes

# 2. 删除远端 Tag
git push origin :refs/tags/v1.3.0

# 3. 删除本地 Tag
git tag -d v1.3.0

# 4. 重新打 Tag 并推送
git tag -a v1.3.0 -m "JudgeBox v1.3.0"
git push origin v1.3.0
```

⚠️ 如果已经有人下载过，尽量不要“静默替换”同一个版本；正确做法是发布 `v1.3.1`，并在说明里写清楚修复内容。

---

## 8. 常见错误

| 现象 | 原因 | 解决 |
| --- | --- | --- |
| `gh: command not found` | 没装 GitHub CLI | `winget install --id GitHub.cli -e`，重开终端 |
| `gh auth status` 显示未登录 | 没授权 | `gh auth login` |
| `HTTP 403` | 没有仓库写权限，或组织开了 SSO | 找仓库管理员加权限；SSO 需在 GitHub 设置里授权 |
| `HTTP 404` | 仓库名/用户名写错，或私有仓库未登录 | `gh repo view Lyra-Lycoris/JudgeBox` 确认 |
| `tag already exists` | Tag 已存在 | 直接用它；或按第 7 节删除后重建 |
| 附件上传到一半失败 | 网络/代理/大文件 | `gh release upload v1.3.0 <文件> --clobber` 重试 |
| 下载链接 404 | Tag 不是 `v1.3.0`，或附件名不一致 | 检查 Tag 和文件名，必须完全一致 |
| Release 页面没有安装包 | 只创建了 Release，没上传附件 | `gh release upload ...` |
| `dist` 不在 `git status` | `.gitignore` 忽略了 `dist/` | 正常现象，安装包走 Release 附件 |
| 安装包只有 100 多 MB | 编译被中断，ISCC 只写了一部分 | 重新运行 `package.ps1` 或 ISCC，确认大小约 427 MB |

---

## 9. 本次发布的最终清单

发布前：

- [ ] `git status` 中没有 `dist/`、`build/`、`.runtime/`
- [ ] 版本号统一为 1.3.0
- [ ] `dist/JudgeBox-Setup-1.3.0-x64.exe` 约 427 MB
- [ ] `.sha256` 与安装包匹配
- [ ] 已提交并推送 `main`
- [ ] 已创建并推送 `v1.3.0` Tag
- [ ] `gh auth status` 正常

发布时：

- [ ] Release 标题：`JudgeBox v1.3.0`
- [ ] Target：`main`
- [ ] 说明：使用 `docs/release-notes-v1.3.0.md`
- [ ] 附件：安装包 + `.sha256`
- [ ] 勾选 latest release

发布后：

- [ ] Release 页面两个附件都能下载
- [ ] README 的 v1.3.0 两个链接返回 200
- [ ] 下载后 SHA-256 一致
- [ ] 干净环境安装、启动、判题通过

---

## 10. 一句话流程

```text
改代码 → 跑测试/打包 → git add/commit/push main → 打 v1.3.0 Tag 并 push
→ gh release create --draft + 上传两个附件 → 网页检查 → 取消草稿发布
→ 下载校验 → 干净环境安装验证
```
