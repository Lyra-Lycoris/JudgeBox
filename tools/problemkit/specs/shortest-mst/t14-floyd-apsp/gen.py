import random


def pack(rows):
    return "%d\n" % len(rows) + "".join(" ".join(str(v) for v in row) + "\n" for row in rows)


def empty_matrix(n):
    return [[0 if i == j else -1 for j in range(n)] for i in range(n)]


def cases():
    rng = random.Random(20261115)
    out = []

    # 01 样例
    out.append({"id": "01", "input": pack([[0, 3, -1, 7], [-1, 0, 2, -1], [-1, -1, 0, 1], [-1, -1, -1, 0]])})

    # 02 边界：只有一个点
    out.append({"id": "02", "input": pack([[0]])})

    # 03 两个点，只有一条边
    out.append({"id": "03", "input": pack([[0, 5], [-1, 0]])})

    # 04 三元环，最优解需要绕圈
    out.append({"id": "04", "input": pack([[0, 2, -1], [-1, 0, 3], [1, -1, 0]])})

    # 05 300 点稠密随机图
    n = 300
    rows = empty_matrix(n)
    for i in range(n):
        for j in range(n):
            if i != j and rng.random() < 0.5:
                rows[i][j] = rng.randint(0, 10 ** 9)
    out.append({"id": "05", "input": pack(rows)})

    # 06 300 点稀疏图：只有一条链
    n = 300
    rows = empty_matrix(n)
    for i in range(n - 1):
        rows[i][i + 1] = rng.randint(1, 10 ** 9)
    out.append({"id": "06", "input": pack(rows)})

    # 07 完全图，所有边权都是 10^9
    n = 300
    rows = [[0 if i == j else 10 ** 9 for j in range(n)] for i in range(n)]
    out.append({"id": "07", "input": pack(rows)})

    # 08 100 点链，考察长路径累加
    n = 100
    rows = empty_matrix(n)
    for i in range(n - 1):
        rows[i][i + 1] = 10 ** 9
    out.append({"id": "08", "input": pack(rows)})

    # 09 300 点，所有边权都是 0
    n = 300
    rows = [[0 if i == j else 0 for j in range(n)] for i in range(n)]
    out.append({"id": "09", "input": pack(rows)})

    # 10 300 点两个互不相通的团，大量 -1
    n = 300
    rows = empty_matrix(n)
    for i in range(150):
        for j in range(150):
            if i != j:
                rows[i][j] = rng.randint(1, 1000)
    for i in range(150, 300):
        for j in range(150, 300):
            if i != j:
                rows[i][j] = rng.randint(1, 1000)
    out.append({"id": "10", "input": pack(rows)})

    return out
