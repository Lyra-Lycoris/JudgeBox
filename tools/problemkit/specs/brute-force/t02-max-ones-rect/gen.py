import random


def _grid(rows):
    return "".join(" ".join(str(v) for v in row) + "\n" for row in rows)


def cases():
    rng = random.Random(20261117)
    out = []

    # 01 样例：第 2、3 列的前三行组成 3 x 2 = 6
    sample = [[1, 0, 1, 1], [1, 0, 1, 1], [1, 1, 1, 1]]
    out.append({"id": "01", "input": "3 4\n" + _grid(sample)})

    # 02 边界 1 x 1，唯一的格子是 1
    out.append({"id": "02", "input": "1 1\n1\n"})

    # 03 边界 1 x 1，唯一的格子是 0
    out.append({"id": "03", "input": "1 1\n0\n"})

    # 04 60 x 60 全 1，答案为 3600
    out.append({"id": "04", "input": "60 60\n" + _grid([[1] * 60 for _ in range(60)])})

    # 05 60 x 60 全 0，答案为 0
    out.append({"id": "05", "input": "60 60\n" + _grid([[0] * 60 for _ in range(60)])})

    # 06 棋盘格，最大面积只能是 1
    board = [[(r + c) % 2 for c in range(60)] for r in range(60)]
    out.append({"id": "06", "input": "60 60\n" + _grid(board)})

    # 07 60 x 60 随机，1 的密度 50%
    half = [[1 if rng.random() < 0.5 else 0 for _ in range(60)] for _ in range(60)]
    out.append({"id": "07", "input": "60 60\n" + _grid(half)})

    # 08 60 x 60 随机，1 的密度 90%（存在大片连通区域）
    dense = [[1 if rng.random() < 0.9 else 0 for _ in range(60)] for _ in range(60)]
    out.append({"id": "08", "input": "60 60\n" + _grid(dense)})

    # 09 只有一行
    out.append({"id": "09", "input": "1 60\n" + _grid([[1] * 60])})

    # 10 只有一列
    out.append({"id": "10", "input": "60 1\n" + _grid([[1] for _ in range(60)])})

    # 11 阶梯状结构
    stair = [[1 if c <= r else 0 for c in range(60)] for r in range(60)]
    out.append({"id": "11", "input": "60 60\n" + _grid(stair)})

    return out
