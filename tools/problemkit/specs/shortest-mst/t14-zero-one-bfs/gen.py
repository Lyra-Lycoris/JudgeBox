import random


def pack(grid):
    lines = ["%d %d" % (len(grid), len(grid[0]))]
    lines.extend(" ".join(str(v) for v in row) for row in grid)
    return "\n".join(lines) + "\n"


def cases():
    rng = random.Random(20261120)
    out = []

    # 01 样例
    out.append({"id": "01", "input": pack([[0, 0, 1, 1], [1, 0, 1, 0], [1, 1, 1, 0]])})

    # 02 边界：只有一个格子，起点不计代价
    out.append({"id": "02", "input": pack([[1]])})

    # 03 一行，全是 1
    out.append({"id": "03", "input": pack([[1] * 500])})

    # 04 一行，全是 0
    out.append({"id": "04", "input": pack([[0] * 500])})

    # 05 500 x 500 全是 0
    out.append({"id": "05", "input": pack([[0] * 500 for _ in range(500)])})

    # 06 500 x 500 全是 1
    out.append({"id": "06", "input": pack([[1] * 500 for _ in range(500)])})

    # 07 500 x 500 随机 0/1
    out.append({"id": "07", "input": pack([[rng.randint(0, 1) for _ in range(500)] for _ in range(500)])})

    # 08 500 x 500，0 很少，路径基本只能踩 1
    out.append({"id": "08", "input": pack([[0 if rng.random() < 0.05 else 1 for _ in range(500)]
                                          for _ in range(500)])})

    # 09 500 行 1 列
    out.append({"id": "09", "input": pack([[rng.randint(0, 1)] for _ in range(500)])})

    # 10 棋盘格
    out.append({"id": "10", "input": pack([[(i + j) % 2 for j in range(500)] for i in range(500)])})

    return out
