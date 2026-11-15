import random


def _grid_text(rows):
    return "".join(" ".join(str(x) for x in row) + "\n" for row in rows)


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "3 3\n2 1 1\n1 1 0\n0 1 1\n"},
        {"id": "02", "input": "1 1\n0\n"},
        {"id": "03", "input": "1 1\n1\n"},
        {"id": "04", "input": "1 3\n2 0 1\n"},
        {"id": "05", "input": "1 2\n2 1\n"},
    ]

    def add(n, m, rows):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d %d\n%s" % (n, m, _grid_text(rows))})

    add(2, 2, [[1, 1], [1, 1]])
    add(1, 1, [[2]])

    g = [[0] * 100 for _ in range(100)]
    for i in range(100):
        for j in range(100):
            r = rng.random()
            if r < 0.05:
                g[i][j] = 0
            elif r < 0.10:
                g[i][j] = 2
            else:
                g[i][j] = 1
    add(100, 100, g)

    # 只有一个腐烂橘子，其余全新鲜：答案是 998
    g = [[1] * 500 for _ in range(500)]
    g[0][0] = 2
    add(500, 500, g)

    # 中间一列全是空格，右侧永远无法被感染
    g = [[1] * 500 for _ in range(500)]
    for i in range(500):
        g[i][250] = 0
    g[0][0] = 2
    add(500, 500, g)

    g = [[0] * 500 for _ in range(500)]
    for i in range(500):
        for j in range(500):
            r = rng.random()
            if r < 0.20:
                g[i][j] = 0
            elif r < 0.40:
                g[i][j] = 2
            else:
                g[i][j] = 1
    g[0][0] = 2
    add(500, 500, g)

    g = [[1] * 300 for _ in range(300)]
    for i in range(300):
        for j in range(300):
            if rng.random() < 0.03:
                g[i][j] = 0
    g[0][0] = 2
    g[149][149] = 2
    g[299][299] = 2
    add(300, 300, g)
    return out
