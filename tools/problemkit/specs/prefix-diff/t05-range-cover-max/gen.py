import random


def _input(n, segs):
    return "%d\n%d\n" % (n, len(segs)) + "".join("%d %d\n" % (l, r) for l, r in segs)


def _random_segs(rng, q, n):
    segs = []
    for _ in range(q):
        l = rng.randint(1, n)
        r = rng.randint(l, n)
        segs.append((l, r))
    return segs


def cases():
    rng = random.Random(20261119)
    n = 200000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(6, [(1, 4), (3, 5), (5, 6)])})

    # 02 边界：n = 1，只有一个位置
    out.append({"id": "02", "input": _input(1, [(1, 1)])})

    # 03 边界：只覆盖中间，两端为 0
    out.append({"id": "03", "input": _input(5, [(2, 4)])})

    # 04 边界：所有操作完全相同，整段都被覆盖 q 次
    out.append({"id": "04", "input": _input(10, [(1, 10)] * 3)})

    # 05 边界：互不相交，最大覆盖次数为 1
    out.append({"id": "05", "input": _input(8, [(1, 2), (3, 3), (5, 6), (8, 8)])})

    # 06 大数据：200000 次随机覆盖
    out.append({"id": "06", "input": _input(n, _random_segs(rng, n, n))})

    # 07 大数据：每次都是整段，答案 (q, 1)
    out.append({"id": "07", "input": _input(n, [(1, n)] * n)})

    # 08 大数据：每次都是单点且互不相同，答案 (1, 1)
    out.append({"id": "08", "input": _input(n, [(i, i) for i in range(1, n + 1)])})

    # 09 中等：随机
    out.append({"id": "09", "input": _input(1000, _random_segs(rng, 1000, 1000))})

    # 10 大数据：所有区间都包含中点，中点附近覆盖次数最大
    segs = []
    for _ in range(n):
        l = rng.randint(1, 100000)
        r = rng.randint(100000, n)
        segs.append((l, r))
    out.append({"id": "10", "input": _input(n, segs)})

    # 11 大数据：区间向右平移，最左侧覆盖次数最大
    segs = [(1, n - i) for i in range(0, n)]
    out.append({"id": "11", "input": _input(n, segs)})
    return out
