import random


def _line(values):
    return " ".join(str(x) for x in values)


def _input(n, m, a, ops):
    parts = ["%d %d\n" % (n, m)]
    for row in a:
        parts.append(_line(row) + "\n")
    parts.append("%d\n" % len(ops))
    for op in ops:
        parts.append(_line(op) + "\n")
    return "".join(parts)


def _grid(rng, n, m, low, high):
    return [[rng.randint(low, high) for _ in range(m)] for _ in range(n)]


def _random_ops(rng, q, n, m, limit, update_p=0.5):
    ops = []
    for _ in range(q):
        if rng.random() < update_p:
            ops.append((1, rng.randint(1, n), rng.randint(1, m), rng.randint(-limit, limit), 0))
        else:
            x1 = rng.randint(1, n)
            x2 = rng.randint(x1, n)
            y1 = rng.randint(1, m)
            y2 = rng.randint(y1, m)
            ops.append((2, x1, y1, x2, y2))
    return ops


def cases():
    rng = random.Random(20261142)
    big = 1000000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(3, 4, [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
                                            [(2, 1, 1, 2, 2), (1, 2, 2, 100, 0),
                                             (2, 1, 1, 2, 2), (2, 2, 2, 3, 4)])})

    # 02 边界：1 × 1
    out.append({"id": "02", "input": _input(1, 1, [[-5]],
                                            [(2, 1, 1, 1, 1), (1, 1, 1, 7, 0),
                                             (2, 1, 1, 1, 1), (1, 1, 1, -big, 0),
                                             (2, 1, 1, 1, 1)])})

    # 03 小数据：全负数
    out.append({"id": "03", "input": _input(4, 5, [[-3, -1, -4, -1, -5],
                                                  [-9, -2, -6, -5, -3],
                                                  [-5, -8, -9, -7, -9],
                                                  [-3, -2, -3, -8, -4]],
                                            [(2, 1, 1, 4, 5), (2, 2, 2, 3, 4), (1, 3, 3, 100, 0),
                                             (2, 1, 1, 4, 5), (2, 3, 3, 3, 3), (1, 1, 1, -big, 0),
                                             (2, 1, 1, 2, 2)])})

    # 04 极值：±1e6 交替
    g = [[big if (i + j) % 2 == 0 else -big for j in range(6)] for i in range(6)]
    out.append({"id": "04", "input": _input(6, 6, g,
                                            [(2, 1, 1, 6, 6), (2, 1, 1, 3, 3), (1, 2, 2, big, 0),
                                             (2, 1, 1, 6, 6), (2, 2, 2, 2, 2), (2, 1, 1, 1, 1)])})

    # 05 单行：n = 1, m = 500
    n, m = 1, 500
    out.append({"id": "05", "input": _input(n, m, _grid(rng, n, m, -1000, 1000),
                                            _random_ops(rng, 2000, n, m, 1000))})

    # 06 单列：n = 500, m = 1
    n, m = 500, 1
    out.append({"id": "06", "input": _input(n, m, _grid(rng, n, m, -1000, 1000),
                                            _random_ops(rng, 2000, n, m, 1000))})

    # 07 中等：50 × 50，q = 1000
    n, m = 50, 50
    out.append({"id": "07", "input": _input(n, m, _grid(rng, n, m, -big, big),
                                            _random_ops(rng, 1000, n, m, 1000))})

    # 08 大数据随机：500 × 500，q = 30000
    n, m = 500, 500
    out.append({"id": "08", "input": _input(n, m, _grid(rng, n, m, -big, big),
                                            _random_ops(rng, 30000, n, m, 1000))})

    # 09 大数据：整矩阵询问
    n, m = 500, 500
    ops = [(1, rng.randint(1, n), rng.randint(1, m), rng.randint(-1000, 1000), 0) for _ in range(100)]
    for _ in range(29900):
        ops.append((2, 1, 1, n, m))
    ops.append((2, 1, 1, 1, 1))
    out.append({"id": "09", "input": _input(n, m, _grid(rng, n, m, -1000, 1000), ops)})

    # 10 大数据：先大量单点修改，再大量小矩形询问
    n, m = 500, 500
    ops = _random_ops(rng, 30000, n, m, 1000, update_p=0.5)
    ops.append((2, 1, 1, n, m))
    out.append({"id": "10", "input": _input(n, m, _grid(rng, n, m, -big, big), ops)})

    return out
