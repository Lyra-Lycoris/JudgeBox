import random


def pack(n, w):
    rows = [" ".join(str(x) for x in row) for row in w]
    return "%d\n%s\n" % (n, "\n".join(rows))


def dense(rng, n, hi=10 ** 9):
    w = [[rng.randint(0, hi) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        w[i][i] = 0
    return w


def sparse(rng, n, miss=0.25, hi=10 ** 9):
    w = [[rng.randint(0, hi) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        w[i][i] = 0
    for i in range(n):
        for j in range(n):
            if i != j and rng.random() < miss:
                w[i][j] = -1
    return w


def cases():
    rng = random.Random(20261114)
    out = []
    out.append({"id": "01", "input": pack(4, [
        [0, 5, -1, 9],
        [7, 0, 4, -1],
        [-1, 6, 0, 3],
        [2, -1, 8, 0],
    ])})
    out.append({"id": "02", "input": pack(1, [[0]])})
    out.append({"id": "03", "input": pack(2, [[0, 5], [7, 0]])})
    out.append({"id": "04", "input": pack(2, [[0, 5], [-1, 0]])})
    out.append({"id": "05", "input": pack(3, [[0, 4, -1], [-1, 0, 6], [-1, -1, 0]])})
    out.append({"id": "06", "input": pack(6, dense(rng, 6, 100))})
    out.append({"id": "07", "input": pack(12, sparse(rng, 12, 0.25, 10 ** 9))})
    out.append({"id": "08", "input": pack(18, dense(rng, 18, 10 ** 9))})
    out.append({"id": "09", "input": pack(18, sparse(rng, 18, 0.3, 10 ** 9))})
    w = dense(rng, 10, 1000)
    for j in range(1, 10):
        w[0][j] = -1
    out.append({"id": "10", "input": pack(10, w)})
    return out
