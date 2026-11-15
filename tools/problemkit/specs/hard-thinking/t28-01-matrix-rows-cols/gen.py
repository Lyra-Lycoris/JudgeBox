import random


def _case(n, m, r, c):
    return "%d %d\n%s\n%s\n" % (n, m, " ".join(str(x) for x in r), " ".join(str(x) for x in c))


def cases():
    rng = random.Random(20261118)
    out = []

    def add_matrix(mat):
        n = len(mat)
        m = len(mat[0])
        r = [sum(row) for row in mat]
        c = [0] * m
        for i in range(n):
            for j in range(m):
                c[j] += mat[i][j]
        out.append({"id": "%02d" % (len(out) + 1), "input": _case(n, m, r, c)})

    def random_matrix(n, m, density):
        return [[1 if rng.random() < density else 0 for _ in range(m)] for _ in range(n)]

    # 01：样例
    add_matrix([[1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    # 02：最小的格子
    add_matrix([[1]])
    # 03：全零
    add_matrix([[0] * 6 for _ in range(6)])
    # 04：只有一行
    add_matrix([[1, 1, 1, 0, 0]])
    # 05：全一
    add_matrix([[1] * 4 for _ in range(4)])
    # 06：单位矩阵
    add_matrix([[1 if i == j else 0 for j in range(8)] for i in range(8)])
    # 07：随机中等规模，密度 0.5
    add_matrix(random_matrix(20, 30, 0.5))
    # 08：随机中规模，密度 0.2
    add_matrix(random_matrix(60, 40, 0.2))
    # 09：上三角，行列和都各不相同
    add_matrix([[1 if j >= i else 0 for j in range(300)] for i in range(300)])
    # 10：随机大规模，密度 0.5
    add_matrix(random_matrix(300, 300, 0.5))
    # 11：随机大规模，密度 0.05
    add_matrix(random_matrix(300, 300, 0.05))
    # 12：随机大规模，密度 0.9
    add_matrix(random_matrix(250, 300, 0.9))
    return out
