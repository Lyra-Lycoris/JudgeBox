import random


def pack(n, s, edges):
    lines = ["%d %d %d" % (n, len(edges), s)]
    lines.extend("%d %d %d" % e for e in edges)
    return "\n".join(lines) + "\n"


def cases():
    rng = random.Random(20261114)
    out = []

    # 01 样例
    out.append({"id": "01", "input": pack(4, 1, [(1, 2, 2), (1, 3, 5), (2, 3, 1), (2, 4, 6), (3, 4, 2)])})

    # 02 边界：只有一个点，一条边也没有
    out.append({"id": "02", "input": pack(1, 1, [])})

    # 03 重边 + 自环，起点是 2 号点
    out.append({"id": "03", "input": pack(2, 2, [(2, 1, 7), (2, 1, 3), (1, 1, 0)])})

    # 04 图不连通，后半部分的点不可达
    out.append({"id": "04", "input": pack(5, 1, [(1, 2, 4), (2, 3, 1), (4, 5, 9)])})

    # 05 长链，每条边都是最大边权，考察 64 位整数
    out.append({"id": "05", "input": pack(6, 1, [(i, i + 1, 10 ** 9) for i in range(1, 6)])})

    # 06 菊花图，所有边权为 0
    n = 100000
    out.append({"id": "06", "input": pack(n, 1, [(1, i, 0) for i in range(2, n + 1)])})

    # 07 随机中等有向图
    n = 1000
    edges = [(rng.randint(1, n), rng.randint(1, n), rng.randint(0, 10 ** 9)) for _ in range(5000)]
    out.append({"id": "07", "input": pack(n, 1, edges)})

    # 08 随机大图：先连成一条链保证连通，再补随机边
    n = 100000
    edges = [(i, i + 1, rng.randint(0, 10 ** 9)) for i in range(1, n)]
    while len(edges) < 150000:
        edges.append((rng.randint(1, n), rng.randint(1, n), rng.randint(0, 10 ** 9)))
    out.append({"id": "08", "input": pack(n, 1, edges)})

    # 09 顶点数很小的稠密图，存在多条等长的最优前缀
    out.append({"id": "09", "input": pack(5, 1, [(1, 2, 4), (1, 3, 4), (2, 4, 4), (3, 4, 4), (4, 5, 4), (1, 5, 100)])})

    # 10 大菊花，边权全为 1
    n = 200000
    out.append({"id": "10", "input": pack(n, 1, [(1, i, 1) for i in range(2, n + 1)])})

    return out
