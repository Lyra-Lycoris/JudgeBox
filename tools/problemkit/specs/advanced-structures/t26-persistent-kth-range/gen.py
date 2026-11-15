import random


def _line(values):
    return " ".join(str(x) for x in values)


def _input(n, a, queries):
    parts = ["%d\n" % n, _line(a) + "\n", "%d\n" % len(queries)]
    for l, r, k in queries:
        parts.append("%d %d %d\n" % (l, r, k))
    return "".join(parts)


def _random_queries(rng, m, n):
    queries = []
    for _ in range(m):
        l = rng.randint(1, n)
        r = rng.randint(l, n)
        k = rng.randint(1, r - l + 1)
        queries.append((l, r, k))
    return queries


def cases():
    rng = random.Random(20261153)
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(5, [3, 1, 4, 1, 5],
                                            [(1, 5, 1), (3, 5, 2), (2, 4, 2)])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": _input(1, [-1000000000], [(1, 1, 1)])})

    # 03 边界：全部元素相同
    n = 10
    out.append({"id": "03", "input": _input(n, [4] * n,
                                            [(1, n, 1), (2, 9, 3), (5, 5, 1),
                                             (1, 10, 10), (3, 7, 2)])})

    # 04 小数据：带负数与 0
    out.append({"id": "04", "input": _input(12, [0, -5, 7, -5, 3, 0, -1, 7, 2, -5, 0, 9],
                                            [(1, 12, 1), (1, 12, 12), (2, 7, 3),
                                             (4, 11, 5), (1, 6, 2), (6, 12, 4)])})

    # 05 中等：n = m = 1000
    n, m = 1000, 1000
    out.append({"id": "05", "input": _input(n, [rng.randint(-10**9, 10**9) for _ in range(n)],
                                            _random_queries(rng, m, n))})

    # 06 大数据：n = m = 50000，取值很大
    n, m = 50000, 50000
    out.append({"id": "06", "input": _input(n, [rng.randint(-10**9, 10**9) for _ in range(n)],
                                            _random_queries(rng, m, n))})

    # 07 大数据：n = m = 50000，取值只有 1..100
    n, m = 50000, 50000
    out.append({"id": "07", "input": _input(n, [rng.randint(1, 100) for _ in range(n)],
                                            _random_queries(rng, m, n))})

    # 08 大数据：n = m = 50000，全部是整段询问
    n, m = 50000, 50000
    queries = [(1, n, rng.randint(1, n)) for _ in range(m)]
    out.append({"id": "08", "input": _input(n, [rng.randint(-10**9, 10**9) for _ in range(n)],
                                            queries)})

    # 09 大数据：n = m = 50000，有序数组，询问总是第 1 小或第 len 小
    n, m = 50000, 50000
    a = list(range(-25000, 25000))
    queries = []
    for _ in range(m):
        l = rng.randint(1, n)
        r = rng.randint(l, n)
        if rng.random() < 0.5:
            queries.append((l, r, 1))
        else:
            queries.append((l, r, r - l + 1))
    out.append({"id": "09", "input": _input(n, a, queries)})

    # 10 大数据：n = m = 30000，取值接近 ±1e9
    n, m = 30000, 30000
    out.append({"id": "10", "input": _input(n, [rng.choice([-1, 1]) * rng.randint(10**9 - 1000, 10**9) for _ in range(n)],
                                            _random_queries(rng, m, n))})

    return out
