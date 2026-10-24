# JudgeBox

[JudgeBox-Setup-1.1.0-x64.exe](https://github.com/Lyra-Lycoris/JudgeBox/releases/download/v1.1.0/JudgeBox-Setup-1.1.0-x64.exe) · [SHA-256](https://github.com/Lyra-Lycoris/JudgeBox/releases/download/v1.1.0/JudgeBox-Setup-1.1.0-x64.exe.sha256)

上面是 Windows 11 x64 离线安装包，自带 C++、Python、Java、仓颉。安装后从开始菜单打开。

还有关于数据生成的功能 我在下面写了，请你们看完好不好

## 开发版

```powershell
git clone https://github.com/Lyra-Lycoris/JudgeBox.git
cd JudgeBox
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

需要 Windows 10/11、CMake 3.20+ 和 MSYS2 UCRT64。完成后双击根目录的 `JudgeBox.exe`，或运行 `启动JudgeBox.cmd`。

以及别告诉我你不会用git，不会用git的请先自己找点教程，实在不愿意，用安装包也可以

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
