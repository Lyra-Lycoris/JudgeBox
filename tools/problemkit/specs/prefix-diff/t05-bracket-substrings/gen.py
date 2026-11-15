import random


def cases():
    rng = random.Random(20261121)
    n = 200000
    half = n // 2
    out = []

    # 01 样例
    out.append({"id": "01", "input": "()()\n"})

    # 02 边界：单个左括号
    out.append({"id": "02", "input": "(\n"})

    # 03 边界：单个右括号
    out.append({"id": "03", "input": ")\n"})

    # 04 边界：最短的合法串
    out.append({"id": "04", "input": "()\n"})

    # 05 嵌套串接一个独立的 ()
    out.append({"id": "05", "input": "(())()\n"})

    # 06 中等规模：1000 个字符，左右括号各一半随机打乱
    medium = ["("] * 500 + [")"] * 500
    rng.shuffle(medium)
    out.append({"id": "06", "input": "".join(medium) + "\n"})

    # 07 大数据：200000 层嵌套，答案是 100000
    out.append({"id": "07", "input": "(" * 100000 + ")" * 100000 + "\n"})

    # 08 大数据：() 重复 100000 次，答案 5000050000
    out.append({"id": "08", "input": "()" * 100000 + "\n"})

    # 09 大数据：全是左括号
    out.append({"id": "09", "input": "(" * n + "\n"})

    # 10 大数据：全是右括号
    out.append({"id": "10", "input": ")" * n + "\n"})

    # 11 大数据：左右括号各一半，随机打乱
    chars = ["("] * half + [")"] * half
    rng.shuffle(chars)
    out.append({"id": "11", "input": "".join(chars) + "\n"})

    # 12 大数据：先全部左括号、后半随机，制造大量不同前缀和
    rest = ["(" if rng.random() < 0.5 else ")" for _ in range(half)]
    out.append({"id": "12", "input": "(" * half + "".join(rest) + "\n"})
    return out
