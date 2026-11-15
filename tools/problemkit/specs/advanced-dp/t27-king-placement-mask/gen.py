import random


def pack(n, m, masks):
    return "%d %d\n%s\n" % (n, m, " ".join(str(x) for x in masks))


def cases():
    rng = random.Random(20261120)
    out = []

    # 01 样例
    out.append({"id": "01", "input": pack(2, 2, [0, 0])})

    # 02 边界：1x1 空格
    out.append({"id": "02", "input": pack(1, 1, [0])})

    # 03 边界：1x1 坏格
    out.append({"id": "03", "input": pack(1, 1, [1])})

    # 04 边界：单行，宽度 9
    out.append({"id": "04", "input": pack(1, 9, [0])})

    # 05 小数据：3x3 空棋盘
    out.append({"id": "05", "input": pack(3, 3, [0, 0, 0])})

    # 06 边界：整行全坏
    out.append({"id": "06", "input": pack(1, 9, [511])})

    # 07 大数据：200 行 9 列，随机坏格
    n = 200
    out.append({"id": "07", "input": pack(n, 9, [rng.randint(0, 511) for _ in range(n)])})

    # 08 大数据：200 行 8 列，随机坏格
    n = 200
    out.append({"id": "08", "input": pack(n, 8, [rng.randint(0, 255) for _ in range(n)])})

    # 09 大数据：200 行 9 列，没有坏格
    n = 200
    out.append({"id": "09", "input": pack(n, 9, [0] * n)})

    # 10 大数据：200 行 5 列，交错坏格
    n = 200
    out.append({"id": "10", "input": pack(n, 5, [(0b10101 if i % 2 == 0 else 0b01010) for i in range(n)])})

    # 11 小数据：2 行 9 列
    out.append({"id": "11", "input": pack(2, 9, [0, 0])})

    return out
