import random


def _grid_text(rows):
    return "".join(" ".join(str(x) for x in row) + "\n" for row in rows)


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "4 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1\n"},
        {"id": "02", "input": "1 1\n1\n"},
        {"id": "03", "input": "1 1\n0\n"},
        {"id": "04", "input": "5 5\n" + _grid_text([[0] * 5 for _ in range(5)])},
        {"id": "05", "input": "1 6\n1 1 1 1 1 1\n"},
    ]

    def add(n, m, rows):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d %d\n%s" % (n, m, _grid_text(rows))})

    add(500, 500, [[1] * 500 for _ in range(500)])

    # 棋盘格：所有 1 互不四连通
    board = [[(i + j) % 2 for j in range(500)] for i in range(500)]
    add(500, 500, board)

    g = [[0] * 500 for _ in range(500)]
    for i in range(500):
        for j in range(500):
            if rng.random() < 0.5:
                g[i][j] = 1
    add(500, 500, g)

    g = [[0] * 100 for _ in range(100)]
    for i in range(100):
        for j in range(100):
            if rng.random() < 0.3:
                g[i][j] = 1
    add(100, 100, g)

    add(500, 1, [[1] for _ in range(500)])

    g = [[0] * 60 for _ in range(60)]
    for i in range(60):
        for j in range(60):
            if rng.random() < 0.65:
                g[i][j] = 1
    add(60, 60, g)
    return out
