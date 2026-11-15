import random


def _grid(rows):
    return "".join(" ".join(str(v) for v in row) + "\n" for row in rows)


def cases():
    rng = random.Random(20261119)
    out = []

    # 01 样例：前三列三行之和为 18
    sample = [[1, 2, -3, 4], [-5, 6, 7, -8], [9, -1, 2, 3]]
    out.append({"id": "01", "input": "3 4\n" + _grid(sample)})

    # 02 边界 1 x 1，唯一的元素是负数
    out.append({"id": "02", "input": "1 1\n-7\n"})

    # 03 边界 1 x 1，唯一的元素是正数
    out.append({"id": "03", "input": "1 1\n42\n"})

    # 04 1 x 500 全为 -1，答案必须选非空子矩形，所以是 -1
    out.append({"id": "04", "input": "1 500\n" + _grid([[-1] * 500])})

    # 05 60 x 500 全为 1，整张矩阵最优
    out.append({"id": "05", "input": "60 500\n" + _grid([[1] * 500 for _ in range(60)])})

    # 06 60 x 500 全为 -1000000000
    out.append({"id": "06", "input": "60 500\n" + _grid([[-1000000000] * 500 for _ in range(60)])})

    # 07 60 x 500 小范围随机
    out.append({"id": "07", "input": "60 500\n" + _grid(
        [[rng.randint(-10, 10) for _ in range(500)] for _ in range(60)])})

    # 08 60 x 500 全范围随机
    out.append({"id": "08", "input": "60 500\n" + _grid(
        [[rng.randint(-10 ** 9, 10 ** 9) for _ in range(500)] for _ in range(60)])})

    # 09 只有一列
    out.append({"id": "09", "input": "60 1\n" + _grid([[rng.randint(-1000, 1000)] for _ in range(60)])})

    # 10 上下是负数、中间一行全为正数：最优子矩形只取中间那几行
    block = [[-1000000000] * 500 for _ in range(20)]
    block += [[1000000000] * 500 for _ in range(20)]
    block += [[-1000000000] * 500 for _ in range(20)]
    out.append({"id": "10", "input": "60 500\n" + _grid(block)})

    return out
