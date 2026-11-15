import random


def line(values):
    return " ".join(str(x) for x in values)


def pack(n, cost, a):
    return "%d %d\n%s\n" % (n, cost, line(a))


def cases():
    rng = random.Random(20261116)
    out = []

    # 01 样例
    out.append({"id": "01", "input": pack(3, 10, [1, 2, 3])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": pack(1, 0, [1000])})

    # 03 边界：两个 1，C = 0（分开更优）
    out.append({"id": "03", "input": pack(2, 0, [1, 1])})

    # 04 小数据：C 很大
    out.append({"id": "04", "input": pack(5, 1000, [1, 1, 1, 1, 1])})

    # 05 中等随机
    n = 1000
    out.append({"id": "05", "input": pack(n, 50, [rng.randint(1, 1000) for _ in range(n)])})

    # 06 大数据：全是 1000，C 最大，答案接近 (2e8)^2
    n = 200000
    out.append({"id": "06", "input": pack(n, 1000000, [1000] * n)})

    # 07 大数据：全是 1，C = 0
    n = 200000
    out.append({"id": "07", "input": pack(n, 0, [1] * n)})

    # 08 大数据：随机
    n = 200000
    out.append({"id": "08", "input": pack(n, 12345, [rng.randint(1, 1000) for _ in range(n)])})

    # 09 大数据：1 与 1000 交替
    n = 200000
    out.append({"id": "09", "input": pack(n, 0, [1 if i % 2 == 0 else 1000 for i in range(n)])})

    # 10 中等：随机 + 大 C
    n = 2000
    out.append({"id": "10", "input": pack(n, 999999, [rng.randint(1, 1000) for _ in range(n)])})

    return out
