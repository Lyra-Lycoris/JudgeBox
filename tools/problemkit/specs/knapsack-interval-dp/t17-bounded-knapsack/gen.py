import random


def _join(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261116)
    out = []

    # 01 样例
    out.append({"id": "01", "input": "2 10\n3 5\n4 7\n3 2\n"})

    # 02 只有一件物品
    out.append({"id": "02", "input": "1 1000\n1\n1\n1\n"})

    # 03 一件物品、数量极大 => 可以拿满容量
    out.append({"id": "03", "input": "1 1000\n1\n1\n1000000000\n"})

    # 04 价值全为 0
    n, cap = 100, 1000
    w = [rng.randint(1, cap) for _ in range(n)]
    c = [rng.randint(1, 10 ** 9) for _ in range(n)]
    out.append({"id": "04", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join(w), _join([0] * n), _join(c))})

    # 05 大数据：随机
    n, cap = 100, 1000
    w = [rng.randint(1, 50) for _ in range(n)]
    v = [rng.randint(0, 10 ** 9) for _ in range(n)]
    c = [rng.randint(1, 10 ** 9) for _ in range(n)]
    out.append({"id": "05", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join(w), _join(v), _join(c))})

    # 06 每种物品数量都是 1，退化为 0/1 背包
    n, cap = 100, 1000
    w = [rng.randint(1, cap) for _ in range(n)]
    v = [rng.randint(0, 10 ** 9) for _ in range(n)]
    out.append({"id": "06", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join(w), _join(v), _join([1] * n))})

    # 07 容量为 1
    out.append({"id": "07", "input": "1 1\n1\n1000000000\n1000000000\n"})

    # 08 随机中等，数量都很小
    n, cap = 20, 200
    w = [rng.randint(1, 20) for _ in range(n)]
    v = [rng.randint(0, 1000) for _ in range(n)]
    c = [rng.randint(1, 5) for _ in range(n)]
    out.append({"id": "08", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join(w), _join(v), _join(c))})

    # 09 总数量 700 件，容量 1000，答案应为 700
    n, cap = 100, 1000
    out.append({"id": "09", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join([1] * n), _join([1] * n), _join([7] * n))})

    # 10 每件物品正好占满背包，只能选一件
    n, cap = 50, 1000
    v = [rng.randint(0, 10 ** 9) for _ in range(n)]
    out.append({"id": "10", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join([1000] * n), _join(v), _join([10 ** 9] * n))})

    # 11 数量全为极大值
    n, cap = 100, 1000
    w = [rng.randint(1, cap) for _ in range(n)]
    v = [rng.randint(0, 10 ** 9) for _ in range(n)]
    out.append({"id": "11", "input": "%d %d\n%s\n%s\n%s\n" % (
        n, cap, _join(w), _join(v), _join([10 ** 9] * n))})

    return out
