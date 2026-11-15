import random


def _line(values):
    return " ".join(str(x) for x in values)


def _input(n, a, ops):
    parts = ["%d\n" % n, _line(a) + "\n", "%d\n" % len(ops)]
    for op in ops:
        parts.append(_line(op) + "\n")
    return "".join(parts)


def _random_ops(rng, q, n, limit, update_p=0.5):
    ops = []
    for _ in range(q):
        l = rng.randint(1, n)
        r = rng.randint(l, n)
        if rng.random() < update_p:
            ops.append((1, l, r, rng.randint(-limit, limit)))
        else:
            ops.append((2, l, r, 0))
    return ops


def cases():
    rng = random.Random(20261143)
    big = 1000000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(5, [1, 3, -2, 4, 5],
                                            [(2, 1, 5, 0), (1, 2, 4, 10), (2, 1, 5, 0),
                                             (2, 2, 3, 0), (1, 1, 5, -20), (2, 1, 5, 0)])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": _input(1, [-3],
                                            [(2, 1, 1, 0), (1, 1, 1, 8), (2, 1, 1, 0),
                                             (1, 1, 1, -big), (2, 1, 1, 0)])})

    # 03 边界：全负数
    out.append({"id": "03", "input": _input(6, [-5, -9, -2, -7, -3, -8],
                                            [(2, 1, 6, 0), (2, 2, 3, 0), (1, 1, 6, 4),
                                             (2, 1, 6, 0), (1, 3, 4, -100), (2, 1, 6, 0)])})

    # 04 极值：正负 1e6 交替
    out.append({"id": "04", "input": _input(7, [big, -big, big, -big, big, -big, big],
                                            [(2, 1, 7, 0), (2, 2, 6, 0), (1, 2, 6, big),
                                             (2, 1, 7, 0), (2, 2, 2, 0), (1, 1, 7, -big),
                                             (2, 1, 7, 0)])})

    # 05 边界：全 0，只有加法
    out.append({"id": "05", "input": _input(4, [0, 0, 0, 0],
                                            [(2, 1, 4, 0), (1, 1, 4, 5), (2, 1, 2, 0),
                                             (1, 2, 3, -9), (2, 2, 3, 0), (2, 1, 4, 0)])})

    # 06 中等随机：n = q = 1000
    n, q = 1000, 1000
    out.append({"id": "06", "input": _input(n, [rng.randint(-big, big) for _ in range(n)],
                                            _random_ops(rng, q, n, 1000))})

    # 07 大数据随机：n = 200000，q = 20000
    n, q = 200000, 20000
    out.append({"id": "07", "input": _input(n, [rng.randint(-big, big) for _ in range(n)],
                                            _random_ops(rng, q, n, 1000))})

    # 08 大数据：全部操作整段，n = 200000
    n = 200000
    ops = []
    for _ in range(20000):
        if rng.random() < 0.5:
            ops.append((1, 1, n, rng.randint(-1000, 1000)))
        else:
            ops.append((2, 1, n, 0))
    out.append({"id": "08", "input": _input(n, [rng.randint(-1000, 1000) for _ in range(n)], ops)})

    # 09 大数据：极短区间，n = 200000
    n = 200000
    ops = []
    for _ in range(20000):
        l = rng.randint(1, n)
        r = min(n, l + rng.randint(0, 6))
        if rng.random() < 0.5:
            ops.append((1, l, r, rng.randint(-big, big)))
        else:
            ops.append((2, l, r, 0))
    ops.append((2, 1, n, 0))
    out.append({"id": "09", "input": _input(n, [rng.randint(-big, big) for _ in range(n)], ops)})

    # 10 大数据：所有数相同，长区间加
    n = 200000
    ops = []
    for _ in range(20000):
        l = rng.randint(1, n // 2)
        r = rng.randint(n // 2, n)
        if rng.random() < 0.5:
            ops.append((1, l, r, rng.randint(-1000, 1000)))
        else:
            ops.append((2, l, r, 0))
    ops.append((2, 1, n, 0))
    out.append({"id": "10", "input": _input(n, [7] * n, ops)})

    return out
