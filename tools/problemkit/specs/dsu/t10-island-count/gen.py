import random


def _grid(rows):
    return "".join(" ".join(str(v) for v in row) + "\n" for row in rows)


def cases():
    rng = random.Random(20261117)
    out = []

    # 01 样例：左上 2x2 一块、中间一个 1、右下两个 1 连成一块
    sample = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1],
    ]
    out.append({"id": "01", "input": "4 5\n" + _grid(sample)})

    # 02 边界：1 x 1 的陆地
    out.append({"id": "02", "input": "1 1\n1\n"})

    # 03 边界：1 x 1 的海水
    out.append({"id": "03", "input": "1 1\n0\n"})

    # 04 500 x 500 全是陆地：只有一座岛
    out.append({"id": "04", "input": "500 500\n" + _grid([[1] * 500 for _ in range(500)])})

    # 05 500 x 500 全是海水：没有岛
    out.append({"id": "05", "input": "500 500\n" + _grid([[0] * 500 for _ in range(500)])})

    # 06 500 x 500 棋盘格：每块陆地都孤立，共 125000 座岛
    board = [[(r + c) % 2 for c in range(500)] for r in range(500)]
    out.append({"id": "06", "input": "500 500\n" + _grid(board)})

    # 07 500 x 500 随机，陆地比例 30%
    grid = [[1 if rng.random() < 0.3 else 0 for _ in range(500)] for _ in range(500)]
    out.append({"id": "07", "input": "500 500\n" + _grid(grid)})

    # 08 500 x 500 随机，陆地比例 60%
    grid = [[1 if rng.random() < 0.6 else 0 for _ in range(500)] for _ in range(500)]
    out.append({"id": "08", "input": "500 500\n" + _grid(grid)})

    # 09 只有一行，全是陆地
    out.append({"id": "09", "input": "1 500\n" + _grid([[1] * 500])})

    # 10 只有一列，全是陆地
    out.append({"id": "10", "input": "500 1\n" + _grid([[1] for _ in range(500)])})

    # 11 只有对角线上的 1：四连通下是 3 座岛
    out.append({"id": "11", "input": "3 3\n" + _grid([[1, 0, 0], [0, 1, 0], [0, 0, 1]])})

    # 12 竖条纹：奇数列整列是陆地，共 250 座岛
    stripes = [[1 if c % 2 == 0 else 0 for c in range(500)] for _ in range(500)]
    out.append({"id": "12", "input": "500 500\n" + _grid(stripes)})

    return out
