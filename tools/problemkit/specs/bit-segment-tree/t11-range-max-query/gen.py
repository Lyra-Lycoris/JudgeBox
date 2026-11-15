import random


def _line(values):
    return " ".join(str(x) for x in values)


def _input(n, a, queries):
    parts = ["%d\n" % n, _line(a) + "\n", "%d\n" % len(queries)]
    for l, r in queries:
        parts.append("%d %d\n" % (l, r))
    return "".join(parts)


def _random_queries(rng, q, n):
    out = []
    for _ in range(q):
        l = rng.randint(1, n)
        r = rng.randint(l, n)
        out.append((l, r))
    return out


def cases():
    rng = random.Random(20261124)
    big = 1000000000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(6, [1, 7, 3, 9, 2, 8],
                                            [(1, 3), (4, 6), (2, 2), (1, 6)])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": _input(1, [-5], [(1, 1)])})

    # 03 边界：全部相同
    out.append({"id": "03", "input": _input(8, [3] * 8,
                                            [(1, 8), (2, 7), (5, 5), (3, 4)])})

    # 04 边界：全是负数
    out.append({"id": "04", "input": _input(6, [-9, -2, -7, -4, -11, -3],
                                            [(1, 6), (1, 1), (3, 5), (2, 2), (6, 6)])})

    # 05 极值：正负 1e9 交替
    out.append({"id": "05", "input": _input(7, [big, -big, big, -big, big, -big, big],
                                            [(1, 1), (1, 2), (2, 6), (1, 7), (4, 4)])})

    # 06 中等随机
    n = 2000
    out.append({"id": "06", "input": _input(n, [rng.randint(-100000, 100000) for _ in range(n)],
                                            _random_queries(rng, 2000, n))})

    # 07 大数据：n = 200000，q = 100000，数值 ±1e9
    n = 200000
    out.append({"id": "07", "input": _input(n, [rng.randint(-big, big) for _ in range(n)],
                                            _random_queries(rng, 100000, n))})

    # 08 大数据：n = 100000，q = 200000，大量单点询问
    n = 100000
    a = [rng.randint(-big, big) for _ in range(n)]
    queries = []
    for _ in range(100000):
        x = rng.randint(1, n)
        queries.append((x, x))
    queries += _random_queries(rng, 100000, n)
    out.append({"id": "08", "input": _input(n, a, queries)})

    # 09 大数据：升序数组，询问整段与末尾
    n = 200000
    out.append({"id": "09", "input": _input(n, list(range(1, n + 1)),
                                            [(1, n)] * 50000 + [(1, 1)] * 50000)})

    # 10 小数据：n = 2
    out.append({"id": "10", "input": _input(2, [5, -5], [(1, 2), (1, 1), (2, 2)])})

    return out
