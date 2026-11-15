import random


def _join(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261117)
    out = []

    # 01 样例
    out.append({"id": "01", "input": "3 15\n1 1 2\n5 6 7\n10 11 20\n"})

    # 02 只有一件物品
    out.append({"id": "02", "input": "1 5\n1\n5\n7\n"})

    # 03 只有一个组，只能选一件
    out.append({"id": "03", "input": "4 10\n1 1 1 1\n3 4 5 6\n5 7 8 9\n"})

    # 04 大数据：50 个组、300 件物品
    n, cap = 300, 2000
    g = [rng.randint(1, 50) for _ in range(n)]
    w = [rng.randint(1, 100) for _ in range(n)]
    v = [rng.randint(0, 10 ** 9) for _ in range(n)]
    out.append({"id": "04", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join(g), _join(w), _join(v))})

    # 05 所有物品都超重
    n, cap = 100, 10
    g = [rng.randint(1, 10) for _ in range(n)]
    w = [rng.randint(11, 110) for _ in range(n)]
    v = [rng.randint(0, 10 ** 9) for _ in range(n)]
    out.append({"id": "05", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join(g), _join(w), _join(v))})

    # 06 价值全为 0
    n, cap = 60, 500
    g = [rng.randint(1, 20) for _ in range(n)]
    w = [rng.randint(1, 500) for _ in range(n)]
    out.append({"id": "06", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join(g), _join(w), _join([0] * n), )})

    # 07 每组只有一件物品，退化为 0/1 背包
    n, cap = 200, 1000
    g = [i for i in range(1, n + 1)]
    w = [rng.randint(1, 100) for _ in range(n)]
    v = [rng.randint(0, 10 ** 9) for _ in range(n)]
    out.append({"id": "07", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join(g), _join(w), _join(v))})

    # 08 随机中等
    n, cap = 40, 200
    g = [rng.randint(1, 10) for _ in range(n)]
    w = [rng.randint(1, 50) for _ in range(n)]
    v = [rng.randint(0, 1000) for _ in range(n)]
    out.append({"id": "08", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join(g), _join(w), _join(v))})

    # 09 容量为 1，所有物品重量为 2
    n, cap = 50, 1
    g = [rng.randint(1, 5) for _ in range(n)]
    out.append({"id": "09", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join(g), _join([2] * n), _join([1] * n))})

    # 10 只有 3 个组，组内物品很多
    n, cap = 300, 2000
    g = [rng.randint(1, 3) for _ in range(n)]
    w = [rng.randint(1, 1000) for _ in range(n)]
    v = [rng.randint(0, 10 ** 9) for _ in range(n)]
    out.append({"id": "10", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join(g), _join(w), _join(v))})

    # 11 一个组里全是重量 1 的物品，只能拿一件
    n, cap = 300, 2000
    v = [rng.randint(0, 10 ** 9) for _ in range(n)]
    out.append({"id": "11", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join([1] * n), _join([1] * n), _join(v))})

    return out
