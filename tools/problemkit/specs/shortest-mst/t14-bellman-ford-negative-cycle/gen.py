import random


def pack(n, s, edges):
    lines = ["%d %d %d" % (n, len(edges), s)]
    lines.extend("%d %d %d" % e for e in edges)
    return "\n".join(lines) + "\n"


def cases():
    rng = random.Random(20261116)
    out = []

    # 01 样例：2 -> 3 -> 4 -> 2 是负环，从 1 可达
    out.append({"id": "01", "input": pack(4, 1, [(1, 2, 1), (2, 3, -3), (3, 4, 1), (4, 2, -1)])})

    # 02 负权自环
    out.append({"id": "02", "input": pack(1, 1, [(1, 1, -5)])})

    # 03 边界：只有一个点，没有边
    out.append({"id": "03", "input": pack(1, 1, [])})

    # 04 一棵树，不存在环
    out.append({"id": "04", "input": pack(6, 1, [(1, 2, -4), (1, 3, 7), (2, 4, -9), (4, 5, 3), (5, 6, -1)])})

    # 05 存在负环，但与 s 不连通
    out.append({"id": "05", "input": pack(6, 1, [(1, 2, 5), (2, 3, 1), (4, 5, -1), (5, 6, -1), (6, 4, -1)])})

    # 06 零权环，不是负环
    out.append({"id": "06", "input": pack(3, 2, [(2, 3, 0), (3, 2, 0), (1, 2, 4)])})

    # 07 随机图，嵌入一个从 s 可达的负环
    n, m = 500, 2000
    edges = []
    for _ in range(m - 3):
        edges.append((rng.randint(1, n), rng.randint(1, n), rng.randint(-10 ** 9, 10 ** 9)))
    edges.append((1, 2, 0))
    edges.append((2, 3, 0))
    edges.append((3, 2, -1))
    rng.shuffle(edges)
    out.append({"id": "07", "input": pack(n, 1, edges)})

    # 08 随机 DAG：只从小点连向大点，一定没有环
    n = 500
    edges = []
    for _ in range(2000):
        u = rng.randint(1, n - 1)
        v = rng.randint(u + 1, n)
        edges.append((u, v, rng.randint(-10 ** 9, 10 ** 9)))
    out.append({"id": "08", "input": pack(n, 1, edges)})

    # 09 两点之间来回，环权为 -2
    out.append({"id": "09", "input": pack(2, 1, [(1, 2, -5), (2, 1, 3)])})

    # 10 只有负权边的长链，没有环
    n = 500
    edges = [(i, i + 1, -10 ** 9) for i in range(1, n)]
    out.append({"id": "10", "input": pack(n, 1, edges)})

    return out
