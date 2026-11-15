"""题包 driver / starter 生成：把题目声明的参数与返回类型翻译成四种语言的 I/O 胶水。

约定（meta.json 的 signature 段）：
  params: [{"name": "n", "type": "int"}, {"name": "a", "type": "ints", "count": "n"}]
  returns: int | bool | string | ints_space | ints_k | ints_lines | none
  repeat: true 时 driver 先读一个 T，然后每组调用一次 solve
类型：
  int    一个整数（C++/Java long long/long，仓颉 Int64，Python int）
  ints   一组整数；带 count 表示个数由前面的参数给出，否则 driver 自己先读 k
  string 一个不含空白的字符串
  strings 一组字符串；同上，带 count 或自己读 k
  matrix  rows × cols 的整数矩阵；rows / cols 引用前面的参数
"""

CPP_TYPES = {"int": "long long", "ints": "vector<long long>", "string": "string",
             "strings": "vector<string>", "matrix": "vector<vector<long long>>"}
CJ_TYPES = {"int": "Int64", "ints": "Array<Int64>", "string": "String",
            "strings": "Array<String>", "matrix": "Array<Array<Int64>>"}
PY_TYPES = {"int": "int", "ints": "list[int]", "string": "str", "strings": "list[str]",
            "matrix": "list[list[int]]"}
JAVA_TYPES = {"int": "long", "ints": "long[]", "string": "String", "strings": "String[]",
              "matrix": "long[][]"}
RETURN_TYPES = {"int": "int", "bool": "bool", "string": "string", "ints_space": "ints",
                "ints_k": "ints", "ints_lines": "ints", "none": "none"}


def _param_type(param, table):
    return table[param["type"]]


def signature_cpp(params, returns):
    args = []
    for p in params:
        if p["type"] in ("ints", "strings"):
            args.append("const %s& %s" % (CPP_TYPES[p["type"]], p["name"]))
        elif p["type"] == "matrix":
            args.append("const %s& %s" % (CPP_TYPES[p["type"]], p["name"]))
        else:
            args.append("%s %s" % (CPP_TYPES[p["type"]], p["name"]))
    ret = {"int": "long long", "bool": "bool", "string": "string"}.get(returns, "vector<long long>")
    return "%s solve(%s)" % (ret, ", ".join(args))


def signature_cangjie(params, returns):
    args = ["%s: %s" % (p["name"], CJ_TYPES[p["type"]]) for p in params]
    ret = {"int": "Int64", "bool": "Bool", "string": "String"}.get(returns, "Array<Int64>")
    return "func solve(%s): %s" % (", ".join(args), ret)


def signature_python(params, returns):
    args = ["%s: %s" % (p["name"], PY_TYPES[p["type"]]) for p in params]
    ret = {"int": "int", "bool": "bool", "string": "str"}.get(returns, "list[int]")
    return "def solve(%s) -> %s" % (", ".join(args), ret)


def signature_java(params, returns):
    args = ["%s %s" % (JAVA_TYPES[p["type"]], p["name"]) for p in params]
    ret = {"int": "long", "bool": "boolean", "string": "String"}.get(returns, "long[]")
    return "static %s solve(%s)" % (ret, ", ".join(args))


def signature_text(params, returns):
    return {"cpp": signature_cpp(params, returns), "cangjie": signature_cangjie(params, returns),
            "python": signature_python(params, returns), "java": signature_java(params, returns)}


def _cpp_reads(params, indent="    "):
    """返回 (声明代码, 实参名列表)，按参数顺序读取 stdin。"""
    lines, names = [], []
    for p in params:
        n, t = p["name"], p["type"]
        if t == "int":
            lines.append("%s%s = %s;" % (indent, "long long " + n, ""))  # 占位，下面重写
            lines[-1] = "%slong long %s; cin >> %s;" % (indent, n, n)
        elif t == "ints":
            if "count" in p:
                lines.append("%svector<long long> %s(%s); for (auto& x : %s) cin >> x;" % (indent, n, p["count"], n))
            else:
                lines.append("%sint %s_n; cin >> %s_n; vector<long long> %s(%s_n); for (auto& x : %s) cin >> x;"
                             % (indent, n, n, n, n, n))
        elif t == "strings":
            if "count" in p:
                lines.append("%svector<string> %s(%s); for (auto& x : %s) cin >> x;" % (indent, n, p["count"], n))
            else:
                lines.append("%sint %s_n; cin >> %s_n; vector<string> %s(%s_n); for (auto& x : %s) cin >> x;"
                             % (indent, n, n, n, n, n))
        elif t == "string":
            lines.append("%sstring %s; cin >> %s;" % (indent, n, n))
        elif t == "matrix":
            lines.append("%svector<vector<long long>> %s(%s, vector<long long>(%s)); for (auto& row : %s) for (auto& x : row) cin >> x;"
                         % (indent, n, p["rows"], p["cols"], n))
        else:
            raise ValueError("不支持的类型 " + t)
        names.append(n)
    return lines, names


def driver_cpp(params, returns, repeat):
    body = []
    arg_names = [p["name"] for p in params]
    call = "solve(%s)" % ", ".join(arg_names)
    if repeat:
        body.append("    int T; cin >> T;")
        body.append("    while (T--) {")
        reads, _ = _cpp_reads(params, "        ")
        body.extend(reads)
        body.extend(_cpp_emit(returns, call, "        "))
        body.append("    }")
    else:
        reads, _ = _cpp_reads(params)
        body.extend(reads)
        body.extend(_cpp_emit(returns, call, "    "))
    return ("#include <bits/stdc++.h>\nusing namespace std;\n\n"
            "%s;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n%s\n    return 0;\n}\n"
            % (signature_cpp(params, returns), "\n".join(body)))


def _cpp_emit(returns, call, indent):
    if returns == "int":
        return ["%slong long answer = %s;" % (indent, call), "%scout << answer << '\\n';" % indent]
    if returns == "bool":
        return ["%sbool answer = %s;" % (indent, call), "%scout << (answer ? \"YES\" : \"NO\") << '\\n';" % indent]
    if returns == "string":
        return ["%sstring answer = %s;" % (indent, call), "%scout << answer << '\\n';" % indent]
    if returns == "ints_space":
        return ["%svector<long long> answer = %s;" % (indent, call),
                "%sfor (size_t i = 0; i < answer.size(); ++i) cout << answer[i] << (i + 1 == answer.size() ? '\\n' : ' ');" % indent,
                "%sif (answer.empty()) cout << '\\n';" % indent]
    if returns in ("ints_k", "ints_lines"):
        return ["%svector<long long> answer = %s;" % (indent, call),
                "%scout << answer.size() << '\\n';" % indent,
                "%sfor (auto x : answer) cout << x << '\\n';" % indent]
    return ["%s%s;" % (indent, call)]


CJ_HELPER = """import std.convert.Parsable
import std.collection.*

var __tokens = ArrayList<String>()
var __cursor = 0

func __nextToken(): String {
    while (__cursor >= __tokens.size) {
        __tokens = ArrayList<String>()
        let parts = readln().trimAscii().split(" ")
        for (part in parts) {
            if (!part.isEmpty()) {
                __tokens.add(part)
            }
        }
        __cursor = 0
    }
    let value = __tokens[__cursor]
    __cursor += 1
    return value
}

func __nextInt(): Int64 {
    return Int64.parse(__nextToken())
}

func __nextInts(count: Int64): Array<Int64> {
    let values = Array<Int64>(count, repeat: 0)
    for (i in 0..count) {
        values[i] = __nextInt()
    }
    return values
}

func __nextStrings(count: Int64): Array<String> {
    let values = Array<String>(count, repeat: "")
    for (i in 0..count) {
        values[i] = __nextToken()
    }
    return values
}
"""


def _cj_reads(params, indent="    "):
    lines, names = [], []
    for p in params:
        n, t = p["name"], p["type"]
        if t == "int":
            lines.append("%slet %s = __nextInt()" % (indent, n))
        elif t == "ints":
            if "count" in p:
                lines.append("%slet %s = __nextInts(%s)" % (indent, n, p["count"]))
            else:
                lines.append("%slet %s_count = __nextInt()" % (indent, n))
                lines.append("%slet %s = __nextInts(%s_count)" % (indent, n, n))
        elif t == "strings":
            if "count" in p:
                lines.append("%slet %s = __nextStrings(%s)" % (indent, n, p["count"]))
            else:
                lines.append("%slet %s_count = __nextInt()" % (indent, n))
                lines.append("%slet %s = __nextStrings(%s_count)" % (indent, n, n))
        elif t == "string":
            lines.append("%slet %s = __nextToken()" % (indent, n))
        elif t == "matrix":
            lines.append("%slet %s = Array<Array<Int64>>(%s, { _ => __nextInts(%s) })" % (indent, n, p["rows"], p["cols"]))
        else:
            raise ValueError("不支持的类型 " + t)
        names.append(n)
    return lines, names


def _cj_emit(returns, call, indent):
    if returns == "int":
        return ["%sprintln(%s)" % (indent, call)]
    if returns == "bool":
        return ["%sif (%s) {" % (indent, call), "%s    println(\"YES\")" % indent, "%s} else {" % indent,
                "%s    println(\"NO\")" % indent, "%s}" % indent]
    if returns == "string":
        return ["%sprintln(%s)" % (indent, call)]
    if returns == "ints_space":
        return ["%slet __answer = %s" % (indent, call),
                "%sfor (i in 0..__answer.size) {" % indent,
                "%s    if (i > 0) { print(\" \") }" % indent,
                "%s    print(__answer[i].toString())" % indent,
                "%s}" % indent,
                "%sprintln(\"\")" % indent]
    if returns in ("ints_k", "ints_lines"):
        return ["%slet __answer = %s" % (indent, call),
                "%sprintln(__answer.size)" % indent,
                "%sfor (x in __answer) {" % indent,
                "%s    println(x)" % indent,
                "%s}" % indent]
    return ["%s%s" % (indent, call)]


def driver_cangjie(params, returns, repeat, package):
    body = []
    call = "solve(%s)" % ", ".join(p["name"] for p in params)
    if repeat:
        body.append("    let T = __nextInt()")
        body.append("    for (_ in 0..T) {")
        reads, _ = _cj_reads(params, "        ")
        body.extend(reads)
        body.extend(_cj_emit(returns, call, "        "))
        body.append("    }")
    else:
        reads, _ = _cj_reads(params)
        body.extend(reads)
        body.extend(_cj_emit(returns, call, "    "))
    # 仓颉同包函数不需要前置声明（模板 main.cj 也是直接调用 solve）。
    return ("package %s\n\n%s\nmain(): Unit {\n%s\n}\n"
            % (package, CJ_HELPER, "\n".join(body)))


def _py_reads(params, indent="    "):
    lines, names = [], []
    for p in params:
        n, t = p["name"], p["type"]
        if t == "int":
            lines.append("%s%s = int(data[pos]); pos += 1" % (indent, n))
        elif t == "ints":
            if "count" in p:
                lines.append("%s%s = [int(x) for x in data[pos:pos + %s]]; pos += %s" % (indent, n, p["count"], p["count"]))
            else:
                lines.append("%s%s_n = int(data[pos]); pos += 1" % (indent, n))
                lines.append("%s%s = [int(x) for x in data[pos:pos + %s_n]]; pos += %s_n" % (indent, n, n, n))
        elif t == "strings":
            if "count" in p:
                lines.append("%s%s = [x.decode() for x in data[pos:pos + %s]]; pos += %s" % (indent, n, p["count"], p["count"]))
            else:
                lines.append("%s%s_n = int(data[pos]); pos += 1" % (indent, n))
                lines.append("%s%s = [x.decode() for x in data[pos:pos + %s_n]]; pos += %s_n" % (indent, n, n, n))
        elif t == "string":
            lines.append("%s%s = data[pos].decode(); pos += 1" % (indent, n))
        elif t == "matrix":
            lines.append("%s%s = [[int(x) for x in data[pos + r * %s: pos + (r + 1) * %s]] for r in range(%s)]"
                         % (indent, n, p["cols"], p["cols"], p["rows"]))
            lines.append("%spos += %s * %s" % (indent, p["rows"], p["cols"]))
        else:
            raise ValueError("不支持的类型 " + t)
        names.append(n)
    return lines, names


def _py_emit(returns, call, indent):
    if returns == "int":
        return ["%sprint(%s)" % (indent, call)]
    if returns == "bool":
        return ["%sprint('YES' if %s else 'NO')" % (indent, call)]
    if returns == "string":
        return ["%sprint(%s)" % (indent, call)]
    if returns == "ints_space":
        return ["%sprint(' '.join(str(x) for x in %s))" % (indent, call)]
    if returns in ("ints_k", "ints_lines"):
        return ["__answer = %s" % call, "%sprint(len(__answer))" % indent,
                "%sprint('\\n'.join(str(x) for x in __answer))" % indent]
    return ["%s%s" % (indent, call)]


def driver_python(params, returns, repeat):
    # 选手代码在前、driver 追加在后：driver 自带 import 与 main()。
    body = ["def main():", "    data = sys.stdin.buffer.read().split()", "    pos = 0"]
    call = "solve(%s)" % ", ".join(p["name"] for p in params)
    if repeat:
        body.append("    t = int(data[pos]); pos += 1")
        body.append("    for _ in range(t):")
        reads, _ = _py_reads(params, "        ")
        body.extend(reads)
        body.extend(_py_emit(returns, call, "        "))
    else:
        reads, _ = _py_reads(params)
        body.extend(reads)
        body.extend(_py_emit(returns, call, "    "))
    body.append("")
    body.append("")
    body.append("main()")
    return "import sys\n\n\n" + "\n".join(body) + "\n"


def _java_reads(params, indent="        "):
    lines, names = [], []
    for p in params:
        n, t = p["name"], p["type"]
        if t == "int":
            lines.append("%slong %s = Long.parseLong(st.nextToken());" % (indent, n))
        elif t == "ints":
            if "count" in p:
                lines.append("%slong[] %s = new long[(int) (%s)];" % (indent, n, p["count"]))
                lines.append("%sfor (int i = 0; i < %s.length; ++i) %s[i] = Long.parseLong(st.nextToken());" % (indent, n, n))
            else:
                lines.append("%sint %s_n = Integer.parseInt(st.nextToken());" % (indent, n))
                lines.append("%slong[] %s = new long[%s_n];" % (indent, n, n))
                lines.append("%sfor (int i = 0; i < %s_n; ++i) %s[i] = Long.parseLong(st.nextToken());" % (indent, n, n))
        elif t == "strings":
            if "count" in p:
                lines.append("%sString[] %s = new String[(int) (%s)];" % (indent, n, p["count"]))
                lines.append("%sfor (int i = 0; i < %s.length; ++i) %s[i] = st.nextToken();" % (indent, n, n))
            else:
                lines.append("%sint %s_n = Integer.parseInt(st.nextToken());" % (indent, n))
                lines.append("%sString[] %s = new String[%s_n];" % (indent, n, n))
                lines.append("%sfor (int i = 0; i < %s_n; ++i) %s[i] = st.nextToken();" % (indent, n, n))
        elif t == "string":
            lines.append("%sString %s = st.nextToken();" % (indent, n))
        elif t == "matrix":
            lines.append("%slong[][] %s = new long[(int) (%s)][(int) (%s)];" % (indent, n, p["rows"], p["cols"]))
            lines.append("%sfor (int i = 0; i < %s.length; ++i) for (int j = 0; j < %s[i].length; ++j) %s[i][j] = Long.parseLong(st.nextToken());"
                         % (indent, n, n, n))
        else:
            raise ValueError("不支持的类型 " + t)
        names.append(n)
    return lines, names


def _java_emit(returns, call, indent):
    if returns == "int":
        return ["%sSystem.out.println(%s);" % (indent, call)]
    if returns == "bool":
        return ["%sSystem.out.println(%s ? \"YES\" : \"NO\");" % (indent, call)]
    if returns == "string":
        return ["%sSystem.out.println(%s);" % (indent, call)]
    if returns == "ints_space":
        return ["%slong[] __answer = %s;" % (indent, call),
                "%sStringBuilder __sb = new StringBuilder();" % indent,
                "%sfor (int i = 0; i < __answer.length; ++i) { if (i > 0) __sb.append(' '); __sb.append(__answer[i]); }" % indent,
                "%sSystem.out.println(__sb);" % indent]
    if returns in ("ints_k", "ints_lines"):
        return ["%slong[] __answer = %s;" % (indent, call),
                "%sSystem.out.println(__answer.length);" % indent,
                "%sStringBuilder __sb = new StringBuilder();" % indent,
                "%sfor (long x : __answer) __sb.append(x).append('\\n');" % indent,
                "%sSystem.out.print(__sb);" % indent]
    return ["%s%s;" % (indent, call)]


def driver_java(params, returns, repeat):
    body = ["        BufferedReader br = new BufferedReader(new InputStreamReader(System.in), 1 << 16);",
            "        StringBuilder buffer = new StringBuilder();",
            "        char[] chunk = new char[1 << 16];",
            "        int read;",
            "        while ((read = br.read(chunk)) > 0) buffer.append(chunk, 0, read);",
            "        StringTokenizer st = new StringTokenizer(buffer.toString());"]
    call = "solve(%s)" % ", ".join(p["name"] for p in params)
    if repeat:
        body.append("        int T = Integer.parseInt(st.nextToken());")
        body.append("        for (int __case = 0; __case < T; ++__case) {")
        reads, _ = _java_reads(params, "            ")
        body.extend(reads)
        body.extend(_java_emit(returns, call, "            "))
        body.append("        }")
    else:
        reads, _ = _java_reads(params)
        body.extend(reads)
        body.extend(_java_emit(returns, call, "        "))
    return ("    public static void main(String[] args) throws Exception {\n" + "\n".join(body) + "\n    }\n")


STARTER_DEFAULT = {
    "int": {"cpp": "return 0;", "cangjie": "return 0", "python": "return 0", "java": "return 0;"},
    "bool": {"cpp": "return false;", "cangjie": "return false", "python": "return False", "java": "return false;"},
    "string": {"cpp": "return \"\";", "cangjie": "return \"\"", "python": "return \"\"", "java": "return \"\";"},
    "ints_space": {"cpp": "return {};", "cangjie": "return Array<Int64>()", "python": "return []", "java": "return new long[0];"},
    "ints_k": {"cpp": "return {};", "cangjie": "return Array<Int64>()", "python": "return []", "java": "return new long[0];"},
    "ints_lines": {"cpp": "return {};", "cangjie": "return Array<Int64>()", "python": "return []", "java": "return new long[0];"},
    "none": {"cpp": "", "cangjie": "", "python": "", "java": ""},
}


def starter(language, params, returns, package, hint):
    comment = "    // TODO: %s\n" % hint.replace("\n", " ") if hint else "    // TODO\n"
    if language == "cpp":
        return "#include <bits/stdc++.h>\nusing namespace std;\n\n%s {\n%s%s\n}\n" % (
            signature_cpp(params, returns), comment, STARTER_DEFAULT[returns]["cpp"])
    if language == "cangjie":
        return "package %s\n\n%s {\n%s%s\n}\n" % (package, signature_cangjie(params, returns), comment,
                                                  STARTER_DEFAULT[returns]["cangjie"])
    if language == "python":
        return "import sys\n\n\n%s:\n    # TODO: %s\n    %s\n" % (
            signature_python(params, returns), hint.replace("\n", " ") if hint else "",
            STARTER_DEFAULT[returns]["python"])
    if language == "java":
        return "    %s {\n        // TODO: %s\n        %s\n    }\n" % (
            signature_java(params, returns), hint.replace("\n", " ") if hint else "",
            STARTER_DEFAULT[returns]["java"])
    raise ValueError(language)


def generate(meta):
    """返回 {文件名: 内容}，包含 main.* 与 starter.*。"""
    sig = meta["signature"]
    params = sig["params"]
    returns = sig["returns"]
    repeat = bool(sig.get("repeat"))
    package = sig.get("package") or meta["id"].replace("-", "_")
    hint = (sig.get("hint") or {}).get("zh", "")
    return {
        "main.cpp": driver_cpp(params, returns, repeat),
        "main.cj": driver_cangjie(params, returns, repeat, package),
        "main.py": driver_python(params, returns, repeat),
        "main.java": driver_java(params, returns, repeat),
        "starter.cpp": starter("cpp", params, returns, package, hint),
        "starter.cj": starter("cangjie", params, returns, package, hint),
        "starter.py": starter("python", params, returns, package, hint),
        "starter.java": starter("java", params, returns, package, hint),
    }
