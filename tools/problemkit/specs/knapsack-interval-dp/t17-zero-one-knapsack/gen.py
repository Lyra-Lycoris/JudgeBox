import random


def _join(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261114)
    out = []

    # 01 样例
    out.append({"id": "01", "input": "3 10\n5 4 6\n10 40 30\n"})

    # 02 只有一件物品
    out.append({"id": "02", "input": "1 1\n1\n5\n"})

    # 03 所有物品都超重
    out.append({"id": "03", "input": "4 10\n11 12 13 14\n5 6 7 8\n"})

    # 04 大数据：随机重量与价值
    n, cap = 1000, 2000
    w = [rng.randint(1, 2000) for _ in range(n)]
    v = [rng.randint(0, 10 ** 9) for _ in range(n)]
    out.append({"id": "04", "input": "%d %d\n%s\n%s\n" % (n, cap, _join(w), _join(v))})

    # 05 重量全相同：最多只能放 n 件
    n, cap = 1000, 2000
    out.append({"id": "05", "input": "%d %d\n%s\n%s\n" % (
        n, cap, _join([1] * n), _join([7] * n))})

    # 06 价值全为 0
    n, cap = 500, 1000
    w = [rng.randint(1, cap) for _ in range(n)]
    out.append({"id": "06", "input": "%d %d\n%s\n%s\n" % (n, cap, _join(w), _join([0] * n))})

    # 07 容量只有 1
    n, cap = 200, 1
    v = [rng.randint(0, 10 ** 9) for _ in range(n)]
    out.append({"id": "07", "input": "%d %d\n%s\n%s\n" % (n, cap, _join([1] * n), _join(v))})

    # 08 随机中等
    n, cap = 60, 300
    w = [rng.randint(1, 50) for _ in range(n)]
    v = [rng.randint(0, 1000) for _ in range(n)]
    out.append({"id": "08", "input": "%d %d\n%s\n%s\n" % (n, cap, _join(w), _join(v))})

    # 09 每件物品正好占满背包
    n, cap = 1000, 2000
    v = [rng.randint(0, 10 ** 9) for _ in range(n)]
    out.append({"id": "09", "input": "%d %d\n%s\n%s\n" % (n, cap, _join([2000] * n), _join(v))})

    # 10 大量轻物品
    n, cap = 1000, 2000
    w = [rng.randint(1, 3) for _ in range(n)]
    v = [rng.randint(0, 10) for _ in range(n)]
    out.append({"id": "10", "input": "%d %d\n%s\n%s\n" % (n, cap, _join(w), _join(v))})

    return out
