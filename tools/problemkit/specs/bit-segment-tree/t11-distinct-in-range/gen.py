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
    rng = random.Random(20261127)
    big = 1000000000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(6, [1, 2, 1, 3, 2, 1],
                                            [(1, 6), (1, 3), (2, 4), (4, 4)])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": _input(1, [5], [(1, 1), (1, 1)])})

    # 03 边界：全部相同
    out.append({"id": "03", "input": _input(8, [7] * 8,
                                            [(1, 8), (1, 1), (3, 5), (2, 7), (8, 8)])})

    # 04 边界：全部不同
    out.append({"id": "04", "input": _input(8, list(range(1, 9)),
                                            [(1, 8), (2, 3), (5, 8), (4, 4)])})

    # 05 极值：正负 1e9 交替
    out.append({"id": "05", "input": _input(7, [big, -big, big, -big, big, -big, big],
                                            [(1, 7), (1, 2), (2, 6), (3, 3)])})

    # 06 中等随机：值域很小，重复很多
    n = 2000
    out.append({"id": "06", "input": _input(n, [rng.randint(1, 50) for _ in range(n)],
                                            _random_queries(rng, 2000, n))})

    # 07 大数据：n = 100000，q = 100000，值域 1e9
    n = 100000
    out.append({"id": "07", "input": _input(n, [rng.randint(1, big) for _ in range(n)],
                                            _random_queries(rng, 100000, n))})

    # 08 大数据：n = 200000，q = 50000
    n = 200000
    out.append({"id": "08", "input": _input(n, [rng.randint(1, big) for _ in range(n)],
                                            _random_queries(rng, 50000, n))})

    # 09 大数据：所有数都相同，答案恒为 1
    n = 200000
    out.append({"id": "09", "input": _input(n, [123456789] * n,
                                            _random_queries(rng, 50000, n))})

    # 10 大数据：全部不同，答案为区间长度
    n = 100000
    out.append({"id": "10", "input": _input(n, list(range(1, n + 1)),
                                            _random_queries(rng, 100000, n))})

    return out
