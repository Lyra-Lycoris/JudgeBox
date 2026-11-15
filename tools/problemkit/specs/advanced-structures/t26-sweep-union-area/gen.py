import random


BIG = 10 ** 9


def _input(rects):
    parts = ["%d\n" % len(rects)]
    for x1, y1, x2, y2 in rects:
        parts.append("%d %d %d %d\n" % (x1, y1, x2, y2))
    return "".join(parts)


def _rand_rect(rng, low, high):
    while True:
        x1 = rng.randint(low, high)
        x2 = rng.randint(low, high)
        if x1 == x2:
            continue
        y1 = rng.randint(low, high)
        y2 = rng.randint(low, high)
        if y1 == y2:
            continue
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        return (x1, y1, x2, y2)


def cases():
    rng = random.Random(20261152)
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input([(0, 0, 2, 2), (1, 1, 3, 3), (2, 0, 4, 1)])})

    # 02 边界：n = 1，最大坐标范围
    out.append({"id": "02", "input": _input([(-BIG, -BIG, BIG, BIG)])})

    # 03 两个完全不相交的矩形
    out.append({"id": "03", "input": _input([(0, 0, 1, 1), (2, 2, 3, 3)])})

    # 04 两个完全相同的矩形（完全重叠）
    out.append({"id": "04", "input": _input([(5, 5, 15, 25), (5, 5, 15, 25)])})

    # 05 三层嵌套
    out.append({"id": "05", "input": _input([(0, 0, 10, 10), (2, 2, 8, 8), (4, 4, 6, 6)])})

    # 06 相邻拼接的三条竖条，内部边界相接
    out.append({"id": "06", "input": _input([(0, 0, 1, 10), (1, 0, 2, 10), (2, 0, 3, 10)])})

    # 07 小数据随机
    out.append({"id": "07", "input": _input([_rand_rect(rng, -10, 10) for _ in range(10)])})

    # 08 大数据：n = 2000，坐标范围极大
    out.append({"id": "08", "input": _input([_rand_rect(rng, -BIG, BIG) for _ in range(2000)])})

    # 09 大数据：n = 2000，坐标范围很小，重叠严重
    out.append({"id": "09", "input": _input([_rand_rect(rng, 0, 1000) for _ in range(2000)])})

    # 10 大数据：n = 2000，全部是同一个矩形
    out.append({"id": "10", "input": _input([(0, 0, BIG, BIG)] * 2000)})

    return out
