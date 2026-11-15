import random


def _grid_text(rows):
    return "".join(" ".join(str(x) for x in row) + "\n" for row in rows)


def _blank(n, m):
    return [[0] * m for _ in range(n)]


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "3 5\n0 0 1 0 0\n0 0 1 0 0\n0 0 0 0 0\n"},
        {"id": "02", "input": "1 1\n0\n"},
        {"id": "03", "input": "1 1\n1\n"},
        {"id": "04", "input": "3 3\n0 1 0\n0 1 0\n0 1 0\n"},
        {"id": "05", "input": "1 2\n0 0\n"},
    ]

    def add(n, m, rows):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d %d\n%s" % (n, m, _grid_text(rows))})

    g = _blank(50, 50)
    for i in range(50):
        for j in range(50):
            if rng.random() < 0.30:
                g[i][j] = 1
    g[0][0] = 0
    g[49][49] = 0
    add(50, 50, g)

    g = _blank(120, 200)
    for i in range(120):
        for j in range(200):
            if rng.random() < 0.28:
                g[i][j] = 1
    g[0][0] = 0
    g[119][199] = 0
    add(120, 200, g)

    # 全空的 500 x 500 迷宫：答案是 998
    add(500, 500, _blank(500, 500))

    # 蛇形通道：只有一条极长的路径，用来卡掉搜索剪枝不到位的写法
    n, m = 499, 500
    g = _blank(n, m)
    for r in range(0, n, 2):
        for c in range(m):
            g[r][c] = 0
    for r in range(1, n, 2):
        for c in range(m):
            g[r][c] = 1
        if (r // 2) % 2 == 0:
            g[r][m - 1] = 0
        else:
            g[r][0] = 0
    g[n - 1][m - 1] = 0
    add(n, m, g)

    # 随机 5 x 7 小迷宫
    g = _blank(5, 7)
    for i in range(5):
        for j in range(7):
            if rng.random() < 0.2:
                g[i][j] = 1
    g[0][0] = 0
    g[4][6] = 0
    add(5, 7, g)
    return out
