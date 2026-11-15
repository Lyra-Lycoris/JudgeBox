import random


def _line(values):
    return " ".join(str(x) for x in values)


def _input(n, a, queries):
    parts = ["%d\n" % n, _line(a) + "\n", "%d\n" % len(queries)]
    for l, r in queries:
        parts.append("%d %d\n" % (l, r))
    return "".join(parts)


def _random_queries(rng, q, n, whole_ratio=0.0):
    queries = []
    for _ in range(q):
        if whole_ratio and rng.random() < whole_ratio:
            queries.append((1, n))
        else:
            l = rng.randint(1, n)
            r = rng.randint(l, n)
            queries.append((l, r))
    return queries


def cases():
    rng = random.Random(20261151)
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(6, [1, 2, 2, 3, 1, 3],
                                            [(1, 6), (2, 3), (1, 3), (4, 6)])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": _input(1, [-1000000000],
                                            [(1, 1), (1, 1), (1, 1)])})

    # 03 边界：全部相同
    out.append({"id": "03", "input": _input(9, [7] * 9,
                                            [(1, 9), (2, 8), (4, 4), (3, 7)])})

    # 04 并列众数：必须输出较小的那个数
    out.append({"id": "04", "input": _input(
        12, [5, 1, 5, 2, 1, 2, 3, 3, 4, 4, 5, 1],
        [(1, 12), (1, 4), (5, 8), (2, 6), (3, 10), (7, 12)])})

    # 05 中等：n = q = 2000，取值很小
    n, q = 2000, 2000
    out.append({"id": "05", "input": _input(n, [rng.randint(1, 50) for _ in range(n)],
                                            _random_queries(rng, q, n))})

    # 06 大数据：n = 50000，q = 2000，取值很大
    n, q = 50000, 2000
    out.append({"id": "06", "input": _input(n, [rng.randint(-10**9, 10**9) for _ in range(n)],
                                            _random_queries(rng, q, n))})

    # 07 大数据：n = 50000，q = 8000，取值只有 1..1000
    n, q = 50000, 8000
    out.append({"id": "07", "input": _input(n, [rng.randint(1, 1000) for _ in range(n)],
                                            _random_queries(rng, q, n))})

    # 08 大数据：n = 50000，q = 8000，一半是整段询问
    n, q = 50000, 8000
    out.append({"id": "08", "input": _input(n, [rng.randint(1, 30) for _ in range(n)],
                                            _random_queries(rng, q, n, whole_ratio=0.5))})

    # 09 询问密集：n = 5000，q = 50000
    n, q = 5000, 50000
    out.append({"id": "09", "input": _input(n, [rng.randint(1, 100) for _ in range(n)],
                                            _random_queries(rng, q, n))})

    # 10 边界：n = 50000，只有一次整段询问，元素互不相同
    n = 50000
    a = list(range(1, n + 1))
    rng.shuffle(a)
    out.append({"id": "10", "input": _input(n, a, [(1, n)])})

    return out
