import random

LIMIT = 10000


def _lines(rows):
    return "\n".join(" ".join(str(v) for v in row) for row in rows)


def _rand_line(rng, limit):
    while True:
        x1 = rng.randint(-limit, limit)
        y1 = rng.randint(-limit, limit)
        x2 = rng.randint(-limit, limit)
        y2 = rng.randint(-limit, limit)
        if (x1, y1) != (x2, y2):
            return x1, y1, x2, y2


def cases():
    rng = random.Random(20261116)
    out = []

    # 01 样例：距离 4、距离 4 但 d=3、点在直线上、距离 12/5
    out.append({"id": "01", "input": "4\n0 0 10 0 3 4 4\n0 0 10 0 3 4 3\n0 0 10 0 5 0 0\n0 0 3 4 3 0 2\n"})

    # 02 点在直线上，d = 0
    out.append({"id": "02", "input": "1\n-10000 -10000 10000 10000 5000 5000 0\n"})

    # 03 距离恰好等于极值 d
    out.append({"id": "03", "input": "1\n-10000 0 10000 0 0 10000 10000\n"})

    # 04 距离只比 d 大 1
    out.append({"id": "04", "input": "1\n-10000 0 10000 0 0 10000 9999\n"})

    # 05 竖直线，距离恰好 10000
    out.append({"id": "05", "input": "1\n0 -10000 0 10000 10000 0 10000\n"})

    # 06 距离为 1/sqrt(2) 的无理数情形
    out.append({"id": "06", "input": "2\n0 0 1 1 1 0 0\n0 0 1 1 1 0 1\n"})

    # 07 小坐标随机
    rows = []
    for _ in range(1000):
        x1, y1, x2, y2 = _rand_line(rng, 20)
        rows.append([x1, y1, x2, y2, rng.randint(-20, 20), rng.randint(-20, 20), rng.randint(0, 20)])
    out.append({"id": "07", "input": "%d\n%s\n" % (len(rows), _lines(rows))})

    # 08 大数据：全范围随机
    rows = []
    for _ in range(100000):
        x1, y1, x2, y2 = _rand_line(rng, LIMIT)
        rows.append([x1, y1, x2, y2, rng.randint(-LIMIT, LIMIT), rng.randint(-LIMIT, LIMIT), rng.randint(0, LIMIT)])
    out.append({"id": "08", "input": "%d\n%s\n" % (len(rows), _lines(rows))})

    # 09 大数据：距离恰好等于 d，答案全为 YES
    rows = []
    for _ in range(100000):
        d = rng.randint(0, LIMIT)
        rows.append([-LIMIT, 0, LIMIT, 0, rng.randint(-LIMIT, LIMIT), d, d])
    out.append({"id": "09", "input": "%d\n%s\n" % (len(rows), _lines(rows))})

    # 10 大数据：d = 0 且点在直线上
    rows = []
    for _ in range(100000):
        t = rng.randint(-3000, 3000)
        rows.append([0, 0, 1, 2, t, 2 * t, 0])
    out.append({"id": "10", "input": "%d\n%s\n" % (len(rows), _lines(rows))})
    return out
