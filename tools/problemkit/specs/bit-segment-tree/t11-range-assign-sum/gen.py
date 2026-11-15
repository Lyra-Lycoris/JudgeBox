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
        l = rng.randint(1, n)
        r = rng.randint(l, n)
        ops.append((l, r, rng.randint(low, high)))
    return ops


def cases():
    rng = random.Random(20261125)
    big = 1000000000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(5, [1, 2, 3, 4, 5],
                                            [(1, 3, 7), (2, 5, 0), (1, 5, 2)])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": _input(1, [5],
                                            [(1, 1, -7), (1, 1, big), (1, 1, 0)])})

    # 03 边界：全部相同，单点赋值
    out.append({"id": "03", "input": _input(6, [4] * 6,
                                            [(3, 3, 9), (2, 2, -1), (1, 6, 4), (2, 5, 0)])})

    # 04 边界：全是负数
    out.append({"id": "04", "input": _input(5, [-3, -1, -4, -1, -5],
                                            [(1, 5, -1), (2, 4, -100), (1, 2, 7), (5, 5, -big)])})

    # 05 极值：整段赋值 ±1e9
    out.append({"id": "05", "input": _input(7, [big, -big, big, -big, big, -big, big],
                                            [(1, 7, big), (1, 7, -big), (2, 2, big), (1, 7, 0)])})

    # 06 中等随机
    n = 1000
    out.append({"id": "06", "input": _input(n, [rng.randint(-100000, 100000) for _ in range(n)],
                                            _random_ops(rng, 1000, n, -100000, 100000))})

    # 07 大数据：n = 100000，q = 50000
    n = 100000
    out.append({"id": "07", "input": _input(n, [rng.randint(-big, big) for _ in range(n)],
                                            _random_ops(rng, 50000, n, -big, big))})

    # 08 大数据：n = 200000，q = 30000
    n = 200000
    out.append({"id": "08", "input": _input(n, [rng.randint(-big, big) for _ in range(n)],
                                            _random_ops(rng, 30000, n, -big, big))})

    # 09 大数据：全部是整段赋值，检验懒标记是否被正确覆盖
    n = 100000
    out.append({"id": "09", "input": _input(n, [1] * n,
                                            [(1, n, i % 1000 - 500) for i in range(100000)])})

    # 10 大数据：很短的区间赋值，频繁打散标记
    n = 100000
    out.append({"id": "10", "input": _input(n, [0] * n,
                                            _random_ops(rng, 30000, 3, -big, big))})

    return out
