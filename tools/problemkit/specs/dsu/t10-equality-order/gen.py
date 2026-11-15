import random


def _fmt(cons):
    return "".join("%d %d %d\n" % (t, u, v) for t, u, v in cons)


def _build(rng, n, k, bsize):
    """构造一定可满足的约束：把点按 bsize 分组，组内相等，组号严格递增。"""
    block = [(i - 1) // bsize for i in range(n + 1)]
    groups = block[n] + 1
    cons = []
    for b in range(groups):
        start = b * bsize + 1
        end = min(n, (b + 1) * bsize)
        for i in range(start + 1, end + 1):
            cons.append((0, start, i))
    for b in range(groups - 1):
        cons.append((1, b * bsize + 1, (b + 1) * bsize + 1))
    while len(cons) < k:
        b1 = rng.randint(0, groups - 2)
        b2 = rng.randint(b1 + 1, groups - 1)
        u = rng.randint(b1 * bsize + 1, min(n, (b1 + 1) * bsize))
        v = rng.randint(b2 * bsize + 1, min(n, (b2 + 1) * bsize))
        cons.append((1, u, v))
    return cons, block


def cases():
    rng = random.Random(20261121)
    out = []

    # 01 样例：{1,2} 与 {3,4} 内部相等，要求 {1,2} < {3,4}
    out.append({"id": "01", "input": "4 4\n" + _fmt([(0, 1, 2), (1, 2, 3), (0, 3, 4), (1, 1, 4)])})

    # 02 没有变量以外的东西，也没有约束
    out.append({"id": "02", "input": "1 0\n"})

    # 03 要求 x1 < x1，不可能成立
    out.append({"id": "03", "input": "1 1\n" + _fmt([(1, 1, 1)])})

    # 04 x1 < x2 且 x2 < x1，形成环，不可能成立
    out.append({"id": "04", "input": "2 2\n" + _fmt([(1, 1, 2), (1, 2, 1)])})

    # 05 大数据：200000 个点全部相等
    n = 200000
    out.append({"id": "05", "input": "%d %d\n" % (n, n - 1) + _fmt([(0, i, i + 1) for i in range(1, n)])})

    # 06 严格递增的链，可以满足
    out.append({"id": "06", "input": "6 5\n" + _fmt([(1, i, i + 1) for i in range(1, 6)])})

    # 07 x1 < x2 < x3 < x1，形成环，不可以满足
    out.append({"id": "07", "input": "3 3\n" + _fmt([(1, 1, 2), (1, 2, 3), (1, 3, 1)])})

    # 08 随机中等：5000 个点、8000 条约束，等式分组 + 组间严格递增，可以满足
    n, k = 5000, 8000
    cons, _ = _build(rng, n, k, 2)
    out.append({"id": "08", "input": "%d %d\n" % (n, k) + _fmt(cons)})

    # 09 同样的规模再补一条从后组指向前组的严格不等式，形成环
    cons, block = _build(rng, n, k - 1, 2)
    cons.append((1, 5000, 1))
    out.append({"id": "09", "input": "%d %d\n" % (n, k) + _fmt(cons)})

    # 10 大数据：200000 个点、200000 条约束，可以满足
    n, k = 200000, 200000
    cons, _ = _build(rng, n, k, 2)
    out.append({"id": "10", "input": "%d %d\n" % (n, k) + _fmt(cons)})

    # 11 大数据：同样的构造再补一条反向严格不等式，形成环
    cons, _ = _build(rng, n, k - 1, 2)
    cons.append((1, 200000, 1))
    out.append({"id": "11", "input": "%d %d\n" % (n, k) + _fmt(cons)})

    # 12 等式只落在同一个人身上，再加上一条严格不等式
    n = 1000
    cons = [(0, i, i) for i in range(1, n + 1)]
    cons.append((1, 1, 2))
    out.append({"id": "12", "input": "%d %d\n" % (n, len(cons)) + _fmt(cons)})

    return out
