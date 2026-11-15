import random


def _line(values):
    return " ".join(str(x) for x in values)


def _input(n, a, ops):
    parts = ["%d\n" % n, _line(a) + "\n", "%d\n" % len(ops)]
    for op in ops:
        parts.append(_line(op) + "\n")
    return "".join(parts)


def _random_ops(rng, q, n, a, vmax, update_p=0.5):
    vals = list(a)
    total = sum(vals)
    ops = []
    for _ in range(q):
        if total == 0 or rng.random() < update_p:
            x = rng.randint(1, n)
            v = rng.randint(0, vmax)
            total += v - vals[x - 1]
            vals[x - 1] = v
            ops.append((1, x, v))
        else:
            ops.append((2, rng.randint(1, total), 0))
    if not any(op[0] == 2 for op in ops):
        if total == 0:
            x = rng.randint(1, n)
            ops.append((1, x, 1))
            total = 1
        ops.append((2, rng.randint(1, total), 0))
    return ops


def cases():
    rng = random.Random(20261145)
    big = 1000000000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(4, [1, 0, 2, 1],
                                            [(2, 1, 0), (2, 2, 0), (2, 4, 0),
                                             (1, 2, 3), (2, 5, 0)])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": _input(1, [3],
                                            [(2, 1, 0), (2, 3, 0), (1, 1, big),
                                             (2, 1, 0), (2, big, 0)])})

    # 03 边界：每个数正好出现一次
    out.append({"id": "03", "input": _input(10, [1] * 10,
                                            [(2, 1, 0), (2, 10, 0), (2, 5, 0),
                                             (1, 3, 0), (2, 3, 0), (2, 9, 0)])})

    # 04 边界：只有一个数出现
    out.append({"id": "04", "input": _input(6, [0, 0, 4, 0, 0, 0],
                                            [(2, 1, 0), (2, 4, 0), (2, 2, 0),
                                             (1, 1, 2), (2, 1, 0), (2, 5, 0)])})

    # 05 极值：所有数的重数都是 1e9
    out.append({"id": "05", "input": _input(5, [big, big, big, big, big],
                                            [(2, 1, 0), (2, big, 0), (2, 3 * big, 0),
                                             (1, 3, 0), (2, 3 * big, 0), (2, 4 * big, 0)])})

    # 06 中等随机：n = 1000, q = 1000
    n, q = 1000, 1000
    a0 = [rng.randint(0, 5) for _ in range(n)]
    out.append({"id": "06", "input": _input(n, a0, _random_ops(rng, q, n, a0, 5))})

    # 07 大数据随机：n = q = 150000
    n, q = 150000, 150000
    a0 = [rng.randint(0, 3) for _ in range(n)]
    out.append({"id": "07", "input": _input(n, a0, _random_ops(rng, q, n, a0, big))})

    # 08 大数据：每个数出现一次，询问全是随机 k
    n = 150000
    ops = []
    for _ in range(75000):
        ops.append((2, rng.randint(1, n), 0))
    ops.append((2, 1, 0))
    ops.append((2, n, 0))
    out.append({"id": "08", "input": _input(n, [1] * n, ops)})

    # 09 大数据：只有 a_1 非零，反复整块搬移
    n = 150000
    a0 = [big] + [0] * (n - 1)
    ops = []
    total = big
    for _ in range(75000):
        t = rng.randint(1, 2)
        if t == 1:
            x = rng.randint(1, n)
            v = rng.randint(0, big)
            total += v - a0[x - 1]
            a0[x - 1] = v
            ops.append((1, x, v))
        else:
            ops.append((2, rng.randint(1, total), 0))
    if total == 0:
        ops.append((1, 1, 1))
        total = 1
    ops.append((2, 1, 0))
    out.append({"id": "09", "input": _input(n, [big] + [0] * (n - 1), ops)})

    # 10 大数据：重数都很小，询问集中在两端
    n = 150000
    init = [rng.randint(0, 2) for _ in range(n)]
    a0 = list(init)
    total = sum(a0)
    ops = []
    for _ in range(75000):
        if total == 0 or rng.random() < 0.5:
            x = rng.randint(1, n)
            v = rng.randint(0, 2)
            total += v - a0[x - 1]
            a0[x - 1] = v
            ops.append((1, x, v))
        else:
            k = rng.choice([1, total, max(1, total // 2), rng.randint(1, total)])
            ops.append((2, k, 0))
    if total == 0:
        ops.append((1, 1, 1))
        total = 1
    ops.append((2, rng.randint(1, total), 0))
    out.append({"id": "10", "input": _input(n, init, ops)})

    return out
