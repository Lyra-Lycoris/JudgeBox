import random


def _line(values):
    return " ".join(str(x) for x in values)


def _input(n, a, ops):
    parts = ["%d\n" % n, _line(a) + "\n", "%d\n" % len(ops)]
    for op in ops:
        parts.append(_line(op) + "\n")
    return "".join(parts)


def _random_ops(rng, q, n):
    ops = []
    for _ in range(q):
        l = rng.randint(1, n)
        r = rng.randint(l, n)
        ops.append((l, r))
    return ops


def cases():
    rng = random.Random(20261144)
    big = 1000000000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(7, [2, -3, 4, -1, 2, -5, 3],
                                            [(1, 7), (3, 5), (1, 2), (2, 6), (4, 4)])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": _input(1, [-7], [(1, 1), (1, 1)])})

    # 03 边界：全负数，答案是区间内最大值
    out.append({"id": "03", "input": _input(6, [-4, -1, -7, -3, -9, -2],
                                            [(1, 6), (2, 4), (5, 6), (1, 1), (3, 3)])})

    # 04 边界：全正数，答案是区间和
    out.append({"id": "04", "input": _input(6, [3, 1, 4, 1, 5, 9],
                                            [(1, 6), (2, 5), (1, 3), (4, 4), (3, 6)])})

    # 05 小数据：0 与交替符号
    out.append({"id": "05", "input": _input(8, [0, 5, -3, 0, -2, 7, -1, 0],
                                            [(1, 8), (1, 4), (5, 8), (2, 7), (3, 5), (4, 4)])})

    # 06 极值：正负 1e9 交替
    out.append({"id": "06", "input": _input(7, [big, -big, big, -big, big, -big, big],
                                            [(1, 7), (1, 2), (2, 6), (4, 7), (3, 3)])})

    # 07 中等随机：n = 1000, q = 2000
    n = 1000
    out.append({"id": "07", "input": _input(n, [rng.randint(-100000, 100000) for _ in range(n)],
                                            _random_ops(rng, 2000, n))})

    # 08 大数据随机：n = 200000, q = 20000
    n = 200000
    out.append({"id": "08", "input": _input(n, [rng.randint(-big, big) for _ in range(n)],
                                            _random_ops(rng, 20000, n))})

    # 09 大数据：全部询问整段，n = 200000
    n = 200000
    out.append({"id": "09", "input": _input(n, [rng.randint(-big, big) for _ in range(n)],
                                            [(1, n)] * 20000)})

    # 10 大数据：全部询问单点，n = 200000
    n = 200000
    single = [(p, p) for p in [rng.randint(1, n) for _ in range(20000)]]
    out.append({"id": "10", "input": _input(n, [rng.randint(-big, big) for _ in range(n)], single)})

    return out
