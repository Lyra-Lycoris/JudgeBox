import random


def pack(n, w):
    rows = [" ".join(str(x) for x in row) for row in w]
    return "%d\n%s\n" % (n, "\n".join(rows))


def rnd_matrix(rng, n, hi):
    w = [[rng.randint(0, hi) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        w[i][i] = 0
    return w


def cases():
    rng = random.Random(20261114)
    out = []
    # 01 样例
    out.append({"id": "01", "input": pack(4, [
        [0, 3, 9, 2],
        [3, 0, 4, 8],
        [9, 4, 0, 1],
        [2, 8, 1, 0],
    ])})
    # 02 n=1 边界
    out.append({"id": "02", "input": pack(1, [[0]])})
    # 03 n=2 边界
    out.append({"id": "03", "input": pack(2, [[0, 5], [7, 0]])})
    # 04 全 0（长度相同的费用）
    out.append({"id": "04", "input": pack(5, [[0] * 5 for _ in range(5)])})
    # 05 随机小数据
    out.append({"id": "05", "input": pack(8, rnd_matrix(rng, 8, 20))})
    # 06 随机中等
    out.append({"id": "06", "input": pack(10, rnd_matrix(rng, 10, 1000))})
    # 07 大数据、费用接近上限
    out.append({"id": "07", "input": pack(12, rnd_matrix(rng, 12, 10 ** 9))})
    # 08 随机 n=16
    out.append({"id": "08", "input": pack(16, rnd_matrix(rng, 16, 10 ** 9))})
    # 09 全相同权重（最大 n）
    out.append({"id": "09", "input": pack(18, [[0 if i == j else 7 for j in range(18)]
                                               for i in range(18)])})
    # 10 大数据 n=18
    out.append({"id": "10", "input": pack(18, rnd_matrix(rng, 18, 10 ** 9))})
    return out
