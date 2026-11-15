import random


def pack(points):
    return "%d\n" % len(points) + "".join("%d %d\n" % p for p in points)


def cases():
    rng = random.Random(20261118)
    out = []

    # 01 样例
    out.append({"id": "01", "input": pack([(0, 0), (1, 1), (3, 0), (4, 5)])})

    # 02 边界：只有一个点
    out.append({"id": "02", "input": pack([(123456789, -987654321)])})

    # 03 两个点重合
    out.append({"id": "03", "input": pack([(5, 5), (5, 5)])})

    # 04 三个点共线
    out.append({"id": "04", "input": pack([(0, 0), (5, 0), (12, 0)])})

    # 05 1200 个点，坐标全范围随机
    n = 1200
    out.append({"id": "05", "input": pack([(rng.randint(-10 ** 9, 10 ** 9), rng.randint(-10 ** 9, 10 ** 9))
                                          for _ in range(n)])})

    # 06 1200 个点全部重合
    n = 1200
    out.append({"id": "06", "input": pack([(7, -7)] * n)})

    # 07 1200 个点落在 40 x 30 的网格上，大量等距
    n = 1200
    out.append({"id": "07", "input": pack([(i % 40, i // 40) for i in range(n)])})

    # 08 1200 个点排成一条等差数列
    n = 1200
    out.append({"id": "08", "input": pack([(i * 1000000, -i * 1000000) for i in range(n)])})

    # 09 1200 个点只在两个极端位置之间交替，考察 int64
    n = 1200
    out.append({"id": "09", "input": pack([(-10 ** 9, -10 ** 9) if i % 2 == 0 else (10 ** 9, 10 ** 9)
                                          for i in range(n)])})

    # 10 1200 个点聚成三个簇
    centers = [(-10 ** 9, 0), (0, 10 ** 9), (10 ** 9, -10 ** 9)]
    points = []
    for i in range(1200):
        cx, cy = centers[i % 3]
        points.append((cx + rng.randint(-1000, 1000), cy + rng.randint(-1000, 1000)))
    out.append({"id": "10", "input": pack(points)})

    return out
