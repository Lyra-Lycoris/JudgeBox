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
    rng = random.Random(20261128)
    big = 1000000000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(5, [1, -2, 3, -1, 2],
                                            [(2, 1, 5), (1, 2, 3), (2, 1, 5), (2, 2, 2)])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": _input(1, [-5],
                                            [(2, 1, 1), (1, 1, 3), (2, 1, 1), (1, 1, -big)])})

    # 03 边界：全是负数，答案是区间内最大值
    out.append({"id": "03", "input": _input(6, [-4, -1, -7, -3, -9, -2],
                                            [(2, 1, 6), (2, 2, 4), (2, 5, 6),
                                             (1, 3, 5), (2, 1, 6), (2, 3, 3)])})

    # 04 边界：全是正数，答案是区间和
    out.append({"id": "04", "input": _input(6, [3, 1, 4, 1, 5, 9],
                                            [(2, 1, 6), (2, 2, 5), (1, 1, 100),
                                             (2, 1, 6), (2, 4, 4)])})

    # 05 小数据：含 0 与交替符号
    out.append({"id": "05", "input": _input(8, [0, 5, -3, 0, -2, 7, -1, 0],
                                            [(2, 1, 8), (2, 1, 4), (2, 5, 8),
                                             (1, 3, 6), (2, 1, 8), (2, 3, 5)])})

    # 06 极值：正负 1e9 交替
    out.append({"id": "06", "input": _input(7, [big, -big, big, -big, big, -big, big],
                                            [(2, 1, 7), (2, 1, 2), (2, 2, 6),
                                             (1, 2, big), (2, 1, 7), (1, 1, -big)])})

    # 07 中等随机
    n = 2000
    out.append({"id": "07", "input": _input(n, [rng.randint(-100000, 100000) for _ in range(n)],
                                            _random_ops(rng, 2000, n, -100000, 100000))})

    # 08 大数据：n = q = 50000 随机
    n = 50000
    out.append({"id": "08", "input": _input(n, [rng.randint(-big, big) for _ in range(n)],
                                            _random_ops(rng, 50000, n, -big, big))})

    # 09 大数据：全是 ±1，整段询问
    n = 50000
    alt = [1 if i % 2 == 0 else -1 for i in range(n)]
    out.append({"id": "09", "input": _input(n, alt, [(2, 1, n)] * 50000)})

    # 10 大数据：全 0，反复把同一个位置改成正数
    n = 50000
    ops = []
    for i in range(50000):
        ops.append((1, i % n + 1, i % 1000 + 1))
        ops.append((2, 1, n))
    out.append({"id": "10", "input": _input(n, [0] * n, ops)})

    return out
