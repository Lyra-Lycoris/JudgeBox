import random


def _line(values):
    return " ".join(str(x) for x in values)


def _input(n, a, ops):
    parts = ["%d\n" % n, _line(a) + "\n", "%d\n" % len(ops)]
    for op in ops:
        parts.append(_line(op) + "\n")
    return "".join(parts)


def _random_ops(rng, q, n, low, high):
    ops = []
    for _ in range(q):
        if rng.random() < 0.5:
            l = rng.randint(1, n)
            r = rng.randint(l, n)
            ops.append((1, l, r, rng.randint(low, high)))
        else:
            ops.append((2, rng.randint(1, n), 0, 0))
    return ops


def cases():
    rng = random.Random(20261122)
    big = 1000000000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(5, [1, 2, 3, 4, 5],
                                            [(1, 1, 3, 10), (2, 2, 0, 0),
                                             (1, 2, 5, -4), (2, 3, 0, 0)])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": _input(1, [5],
                                            [(2, 1, 0, 0), (1, 1, 1, -5), (2, 1, 0, 0),
                                             (1, 1, 1, big), (2, 1, 0, 0)])})

    # 03 边界：全部相同，反复整段加
    out.append({"id": "03", "input": _input(6, [5] * 6,
                                            [(1, 1, 6, 5), (2, 1, 0, 0), (2, 6, 0, 0),
                                             (1, 3, 4, -10), (2, 3, 0, 0), (2, 2, 0, 0)])})

    # 04 边界：全是负数
    out.append({"id": "04", "input": _input(4, [-3, -1, -4, -1],
                                            [(2, 1, 0, 0), (2, 4, 0, 0), (1, 1, 4, -7),
                                             (2, 2, 0, 0), (1, 2, 3, 4), (2, 3, 0, 0)])})

    # 05 极值：正负 1e9 交替，整段与单点交替
    out.append({"id": "05", "input": _input(5, [big, -big, big, -big, big],
                                            [(1, 1, 5, big), (2, 1, 0, 0), (1, 3, 3, -big),
                                             (2, 3, 0, 0), (2, 5, 0, 0)])})

    # 06 中等随机
    n = 1000
    a = [rng.randint(-100000, 100000) for _ in range(n)]
    out.append({"id": "06", "input": _input(n, a, _random_ops(rng, 1000, n, -100000, 100000))})

    # 07 大数据：n = 100000，q = 100000
    n = 100000
    a = [rng.randint(-big, big) for _ in range(n)]
    out.append({"id": "07", "input": _input(n, a, _random_ops(rng, 100000, n, -big, big))})

    # 08 大数据：n = 200000，q = 30000
    n = 200000
    a = [rng.randint(-big, big) for _ in range(n)]
    out.append({"id": "08", "input": _input(n, a, _random_ops(rng, 30000, n, -big, big))})

    # 09 大数据：全 0，区间加后逐个查询整段
    n = 200000
    ops = []
    for _ in range(10000):
        ops.append((1, 1, n, big))
        ops.append((2, rng.randint(1, n), 0, 0))
        ops.append((2, 1, 0, 0))
    out.append({"id": "09", "input": _input(n, [0] * n, ops)})

    return out
