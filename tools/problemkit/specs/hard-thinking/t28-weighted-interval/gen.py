import random


def _input(intervals):
    parts = ["%d\n" % len(intervals)]
    for l, r, w in intervals:
        parts.append("%d %d %d\n" % (l, r, w))
    return "".join(parts)


def _random(rng, n, hi_l, max_len, hi_w):
    out = []
    for _ in range(n):
        l = rng.randint(1, hi_l)
        out.append((l, l + rng.randint(0, max_len), rng.randint(1, hi_w)))
    return out


def cases():
    rng = random.Random(20261122)
    out = []

    def add(intervals):
        out.append({"id": "%02d" % (len(out) + 1), "input": _input(intervals)})

    # 01 样例
    add([(1, 3, 5), (2, 5, 6), (4, 6, 5), (6, 7, 4)])

    # 02 边界：n = 1，坐标与权重都取到上限
    add([(1, 10 ** 9, 10 ** 9)])

    # 03 边界：所有区间重合在同一个整点上，只能选一个
    add([(7, 7, w) for w in (3, 100, 7, 42, 1)])

    # 04 边界：首尾相接的链，只有相隔一格的区间才互不重叠
    add([(1, 2, 5), (2, 3, 100), (3, 4, 5)])

    # 05 边界：一个大区间套住若干小区间，选内部更划算
    add([(1, 10, 1), (2, 3, 5), (4, 5, 6), (6, 7, 7), (9, 10, 100)])

    # 06 随机小数据
    add(_random(rng, 20, 30, 10, 100))

    # 07 随机中等数据：坐标为 10^6 级，权重为 10^9 级
    add(_random(rng, 1000, 10 ** 6, 10 ** 5, 10 ** 9))

    # 08 随机大数据：n = 200000，坐标 <= 10^5，区间很短、重叠密集
    add(_random(rng, 200000, 100000, 1000, 999))

    # 09 随机大数据：n = 200000，坐标 <= 2*10^5，区间长度随机
    add(_random(rng, 200000, 200000, 200000, 999))

    # 10 随机大数据：n = 100000，坐标与权重都是 10^9 级，答案达到 10^14 量级
    add(_random(rng, 100000, 10 ** 9, 10 ** 7, 10 ** 9))

    # 11 大数据：n = 200000 个长度为 1 的区间，全部互不重叠，必须全部选中
    add([(i, i, rng.randint(1, 99999)) for i in range(1, 200001)])

    # 12 大数据：n = 200000 的相邻链 [i, i+1]，只能隔一个选一个
    add([(i, i + 1, rng.randint(1, 999)) for i in range(1, 200001)])

    return out
