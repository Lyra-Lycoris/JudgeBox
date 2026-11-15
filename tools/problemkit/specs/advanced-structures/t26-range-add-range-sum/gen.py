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
    rng = random.Random(20261141)
    big = 1000000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(5, [1, 2, 3, 4, 5],
                                            [(1, 1, 3, 10), (2, 1, 5, 0),
                                             (1, 2, 2, -5), (2, 2, 4, 0)])})

    # 02 边界：n = 1，正负抵消
    out.append({"id": "02", "input": _input(1, [-7],
                                            [(1, 1, 1, 5), (2, 1, 1, 0),
                                             (1, 1, 1, -big), (2, 1, 1, 0)])})

    # 03 边界：全是极小数，先整体加正数再变小范围
    out.append({"id": "03", "input": _input(8, [-big] * 8,
                                            [(2, 1, 8, 0), (1, 1, 8, big), (2, 1, 8, 0),
                                             (1, 3, 5, -1), (2, 1, 8, 0), (2, 3, 5, 0)])})

    # 04 极值：正负交替的 1e6，整体加 1e6
    out.append({"id": "04", "input": _input(6, [big, -big, big, -big, big, -big],
                                            [(2, 1, 6, 0), (1, 1, 6, big), (2, 1, 6, 0),
                                             (2, 2, 5, 0), (1, 2, 2, -big), (2, 1, 6, 0)])})

    # 05 边界：初始全 0，单点反复加减
    out.append({"id": "05", "input": _input(3, [0, 0, 0],
                                            [(2, 1, 3, 0), (1, 1, 1, big), (2, 1, 3, 0),
                                             (1, 2, 3, -big), (2, 1, 3, 0), (2, 2, 2, 0)])})

    # 06 中等随机：n = q = 1000
    n, q = 1000, 1000
    out.append({"id": "06", "input": _input(n, [rng.randint(-big, big) for _ in range(n)],
                                            _random_ops(rng, q, n, 1000))})

    # 07 大数据随机：n = 200000，q = 80000
    n, q = 200000, 80000
    out.append({"id": "07", "input": _input(n, [rng.randint(-big, big) for _ in range(n)],
                                            _random_ops(rng, q, n, 1000))})

    # 08 大数据：全部操作整段，n = 200000
    n = 200000
    ops = []
    for _ in range(80000):
        if rng.random() < 0.5:
            ops.append((1, 1, n, rng.randint(-1000, 1000)))
        else:
            ops.append((2, 1, n, 0))
    ops.append((2, 1, n, 0))
    out.append({"id": "08", "input": _input(n, [0] * n, ops)})

    # 09 大数据：只有单点修改与单点询问，n = 200000
    n = 200000
    ops = []
    for _ in range(60000):
        p = rng.randint(1, n)
        if rng.random() < 0.5:
            ops.append((1, p, p, rng.randint(-big, big)))
        else:
            ops.append((2, p, p, 0))
    ops.append((1, 1, n, 0))
    ops.append((2, 1, n, 0))
    out.append({"id": "09", "input": _input(n, [rng.randint(-big, big) for _ in range(n)], ops)})

    # 10 大数据：前缀与后缀交替，n = 200000
    n = 200000
    ops = []
    for _ in range(80000):
        r = rng.randint(1, n)
        if rng.random() < 0.5:
            ops.append((1, 1, r, rng.randint(-1000, 1000)))
        else:
            ops.append((2, n - r + 1, n, 0))
    ops.append((2, 1, n, 0))
    out.append({"id": "10", "input": _input(n, [rng.randint(-1000, 1000) for _ in range(n)], ops)})

    return out
