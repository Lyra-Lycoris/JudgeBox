import random

LIMIT = 10 ** 9


def _lines(rows):
    return "\n".join(" ".join(str(v) for v in row) for row in rows)


def cases():
    rng = random.Random(20261118)
    out = []

    # 01 样例：正常相交、端点接触、平行不交、共线重叠、共线分离、点在段上
    sample = [
        (0, 0, 4, 4, 0, 4, 4, 0),
        (0, 0, 4, 0, 4, 0, 4, 4),
        (0, 0, 4, 0, 0, 1, 4, 1),
        (0, 0, 4, 0, 1, 0, 3, 0),
        (0, 0, 1, 0, 2, 0, 3, 0),
        (2, 2, 2, 2, 0, 0, 4, 4),
    ]
    out.append({"id": "01", "input": "6\n%s\n" % _lines(sample)})

    # 02 两条线段都退化成一个相同的点
    out.append({"id": "02", "input": "1\n5 5 5 5 5 5 5 5\n"})

    # 03 退化成点的线段落在另一条线段上
    out.append({"id": "03", "input": "1\n2 2 2 2 0 0 4 4\n"})

    # 04 退化成点的线段在另一条线段之外
    out.append({"id": "04", "input": "1\n9 9 9 9 0 0 4 4\n"})

    # 05 两条完全相同的极值线段
    out.append({"id": "05", "input": "1\n-1000000000 -1000000000 1000000000 1000000000 -1000000000 -1000000000 1000000000 1000000000\n"})

    # 06 极值坐标下的十字相交
    out.append({"id": "06", "input": "1\n-1000000000 0 1000000000 0 0 -1000000000 0 1000000000\n"})

    # 07 小坐标随机
    rows = []
    for _ in range(1000):
        rows.append([rng.randint(-3, 3) for _ in range(8)])
    out.append({"id": "07", "input": "%d\n%s\n" % (len(rows), _lines(rows))})

    # 08 大数据：全范围随机
    rows = [[rng.randint(-LIMIT // 10, LIMIT // 10) for _ in range(8)] for _ in range(50000)]
    out.append({"id": "08", "input": "%d\n%s\n" % (len(rows), _lines(rows))})

    # 09 大数据：共享一个端点，答案全为 YES
    rows = []
    for _ in range(50000):
        p = [rng.randint(-1000000, 1000000), rng.randint(-1000000, 1000000)]
        rows.append([rng.randint(-LIMIT // 10, LIMIT // 10), rng.randint(-LIMIT // 10, LIMIT // 10), p[0], p[1],
                     p[0], p[1], rng.randint(-LIMIT // 10, LIMIT // 10), rng.randint(-LIMIT // 10, LIMIT // 10)])
    out.append({"id": "09", "input": "%d\n%s\n" % (len(rows), _lines(rows))})

    # 10 大数据：密集小坐标网格随机
    rows = [[rng.randint(-5, 5) for _ in range(8)] for _ in range(100000)]
    out.append({"id": "10", "input": "%d\n%s\n" % (len(rows), _lines(rows))})
    return out
