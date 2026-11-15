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
            ops.append((1, rng.randint(1, n), rng.randint(low, high)))
        else:
            l = rng.randint(1, n)
            r = rng.randint(l, n)
            ops.append((2, l, r))
    return ops


def cases():
    rng = random.Random(20261121)
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(5, [1, 2, 3, 4, 5],
                                            [(1, 3, 10), (2, 1, 3), (2, 2, 5)])})

    # 02 边界：n = 1，反复修改单点
    out.append({"id": "02", "input": _input(1, [5],
                                            [(2, 1, 1), (1, 1, -5), (2, 1, 1),
                                             (1, 1, 1000000000), (2, 1, 1)])})

    # 03 边界：全部相同，只改中间一个
    out.append({"id": "03", "input": _input(6, [7] * 6,
                                            [(2, 1, 6), (1, 3, 3), (2, 3, 3), (2, 1, 6),
                                             (1, 1, -7), (2, 1, 6)])})

    # 04 边界：全是负数
    out.append({"id": "04", "input": _input(4, [-3, -1, -4, -1],
                                            [(2, 1, 4), (2, 2, 2), (1, 2, 5), (2, 1, 4), (2, 1, 2)])})

    # 05 极值：正负 1e9 交替
    big = 1000000000
    out.append({"id": "05", "input": _input(5, [big, -big, big, -big, big],
                                            [(2, 1, 5), (1, 1, big), (2, 1, 1),
                                             (1, 3, -big), (2, 1, 5)])})

    # 06 中等随机：n = q = 1000
    n = 1000
    a = [rng.randint(-100000, 100000) for _ in range(n)]
    out.append({"id": "06", "input": _input(n, a, _random_ops(rng, 1000, n, -100000, 100000))})

    # 07 大数据：n = 200000，q = 50000，数值 ±1e9
    n = 200000
    a = [rng.randint(-big, big) for _ in range(n)]
    out.append({"id": "07", "input": _input(n, a, _random_ops(rng, 50000, n, -big, big))})

    # 08 大数据：全 1 数组 + 100000 次修改/查询
    n = 100000
    out.append({"id": "08", "input": _input(n, [1] * n, _random_ops(rng, 100000, n, -1000000000, 1000000000))})

    # 09 大数据：全 0 数组，只在前缀上做单点累加与整段查询
    n = 200000
    ops = []
    for _ in range(50000):
        if rng.random() < 0.5:
            ops.append((1, rng.randint(1, 1000), rng.randint(1, 1000)))
        else:
            ops.append((2, 1, n))
    out.append({"id": "09", "input": _input(n, [0] * n, ops)})

    return out
