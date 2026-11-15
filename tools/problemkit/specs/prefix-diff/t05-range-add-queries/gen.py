import random


def _line(values):
    return " ".join(str(x) for x in values)


def _input(n, a, ops):
    parts = ["%d\n" % n, _line(a) + "\n", "%d\n" % len(ops)]
    for l, r, v in ops:
        parts.append("%d %d %d\n" % (l, r, v))
    return "".join(parts)


def _random_ops(rng, q, n, low, high):
    ops = []
    for _ in range(q):
        l = rng.randint(1, n)
        r = rng.randint(l, n)
        ops.append((l, r, rng.randint(low, high)))
    return ops


def cases():
    rng = random.Random(20261115)
    n = 200000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _input(5, [1, 2, 3, 4, 5], [(1, 3, 10), (2, 5, -4)])})

    # 02 边界：n = 1，恰好抵消成 0
    out.append({"id": "02", "input": _input(1, [1000000000], [(1, 1, -1000000000)])})

    # 03 边界：全部相同，只改中间一段
    out.append({"id": "03", "input": _input(6, [5] * 6, [(2, 5, -5)])})

    # 04 边界：全是负数，操作为 0
    out.append({"id": "04", "input": _input(4, [-3, -1, -4, -1], [(1, 4, 0)])})

    # 05 极值：三次全段加 1e9
    out.append({"id": "05", "input": _input(6, [0] * 6,
                                            [(1, 6, 1000000000), (1, 6, 1000000000), (1, 6, 1000000000)])})

    # 06 大数据：随机数组 + 40000 次随机操作（输入约 3.5 MiB）
    a = [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
    out.append({"id": "06", "input": _input(n, a, _random_ops(rng, 40000, n, -10 ** 9, 10 ** 9))})

    # 07 大数据：初始全 0 + 100000 次随机操作
    out.append({"id": "07", "input": _input(n, [0] * n, _random_ops(rng, 100000, n, -10 ** 9, 10 ** 9))})

    # 08 大数据：单点操作 100000 次，每个位置恰好被减回 0
    ops = [(i, i, -1000000000) for i in range(1, 100001)]
    out.append({"id": "08", "input": _input(100000, [1000000000] * 100000, ops)})

    # 09 中等随机
    out.append({"id": "09", "input": _input(1000, [rng.randint(-1000, 1000) for _ in range(1000)],
                                            _random_ops(rng, 1000, 1000, -1000, 1000))})

    # 10 大数据：正负交替，整段加上 1e9
    alt = [1000000000 if i % 2 == 0 else -1000000000 for i in range(n)]
    out.append({"id": "10", "input": _input(n, alt, [(1, n, 1000000000)])})
    return out
