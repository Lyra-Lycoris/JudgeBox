import random

LIMIT = 10 ** 9


def _lines(rows):
    return "\n".join(" ".join(str(v) for v in row) for row in rows)


def cases():
    rng = random.Random(20261115)
    out = []

    # 01 样例
    out.append({"id": "01", "input": "4\n0 0 1 1 2 2\n0 0 1 1 2 3\n0 0 0 5 0 -7\n-3 4 0 0 3 -4\n"})

    # 02 三点全部重合
    out.append({"id": "02", "input": "1\n7 -7 7 -7 7 -7\n"})

    # 03 极值共线：(x,y) = (-1e9,-1e9), (0,0), (1e9,1e9)
    out.append({"id": "03", "input": "1\n-1000000000 -1000000000 0 0 1000000000 1000000000\n"})

    # 04 极值附近几乎共线，仅差 1
    out.append({"id": "04", "input": "1\n-1000000000 -1000000000 0 0 1000000000 999999999\n"})

    # 05 手工边界组：重合点、竖直线、水平线、负坐标
    rows = [
        [5, 5, 5, 5, 5, 5],
        [1, 2, 1, 2, 3, 4],
        [0, 0, 1, 0, 0, 1],
        [-1, -1, -2, -2, -3, -3],
        [1000000000, 0, -1000000000, 0, 0, 1],
        [0, 0, 2, 4, 1, 2],
        [0, 0, 2, 4, 3, 6],
        [0, 0, 0, 0, 1000000000, -1000000000],
    ]
    out.append({"id": "05", "input": "%d\n%s\n" % (len(rows), _lines(rows))})

    # 06 小坐标随机
    small = [[rng.randint(-10, 10) for _ in range(6)] for _ in range(1000)]
    out.append({"id": "06", "input": "%d\n%s\n" % (len(small), _lines(small))})

    # 07 中等坐标随机
    mid = [[rng.randint(-1000000, 1000000) for _ in range(6)] for _ in range(1000)]
    out.append({"id": "07", "input": "%d\n%s\n" % (len(mid), _lines(mid))})

    # 08 大数据：一半刻意构造共线，一半全范围随机
    big = []
    for _ in range(25000):
        ax = rng.randint(-1000, 1000)
        ay = rng.randint(-1000, 1000)
        bx = rng.randint(-1000, 1000)
        by = rng.randint(-1000, 1000)
        k = rng.randint(-3, 3)
        big.append([ax, ay, bx, by, ax + k * (bx - ax), ay + k * (by - ay)])
    for _ in range(25000):
        big.append([rng.randint(-LIMIT, LIMIT) for _ in range(6)])
    out.append({"id": "08", "input": "%d\n%s\n" % (len(big), _lines(big))})

    # 09 大数据：全部为同一个点
    n = 100000
    out.append({"id": "09", "input": "%d\n%s\n" % (n, _lines([[0, 0, 0, 0, 0, 0]] * n))})

    # 10 大数据：极值上的竖直线与水平线，全部共线
    big2 = []
    for _ in range(60000):
        if rng.random() < 0.5:
            x = rng.randint(-LIMIT, LIMIT)
            big2.append([x, -LIMIT, x, 0, x, LIMIT])
        else:
            y = rng.randint(-LIMIT, LIMIT)
            big2.append([-LIMIT, y, 0, y, LIMIT, y])
    out.append({"id": "10", "input": "%d\n%s\n" % (len(big2), _lines(big2))})
    return out
