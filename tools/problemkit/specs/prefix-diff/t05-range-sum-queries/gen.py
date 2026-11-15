import random


def _line(values):
    return " ".join(str(x) for x in values)


def _case(n, a, l, r):
    return "%d\n%s\n%d %d\n" % (n, _line(a), l, r)


def _random_case(rng, n, low, high):
    a = [rng.randint(low, high) for _ in range(n)]
    l = rng.randint(1, n)
    r = rng.randint(l, n)
    return _case(n, a, l, r)


def cases():
    rng = random.Random(20261114)
    n = 200000
    out = []

    # 01 样例：两组小数据
    out.append({"id": "01", "input": "2\n" + _case(3, [1, 2, 3], 1, 3)
                + _case(4, [-1, 5, -2, 4], 2, 3)})

    # 02 边界：n = 1，元素为最小值
    out.append({"id": "02", "input": "1\n" + _case(1, [-1000000000], 1, 1)})

    # 03 边界：全部相同且为负数，查询后缀
    out.append({"id": "03", "input": "1\n" + _case(5, [-7] * 5, 2, 5)})

    # 04 边界：单点查询，序列有正有负
    out.append({"id": "04", "input": "1\n" + _case(6, [3, -1, 4, -1, 5, -9], 3, 3)})

    # 05 中等随机
    out.append({"id": "05", "input": "1\n" + _random_case(rng, 1000, -10 ** 9, 10 ** 9)})

    # 06 大数据：全为 1e9，询问整个序列
    out.append({"id": "06", "input": "1\n" + _case(n, [1000000000] * n, 1, n)})

    # 07 大数据：全为 -1e9，询问整个序列
    out.append({"id": "07", "input": "1\n" + _case(n, [-1000000000] * n, 1, n)})

    # 08 大数据：全范围随机
    out.append({"id": "08", "input": "1\n" + _random_case(rng, n, -10 ** 9, 10 ** 9)})

    # 09 多组中等数据
    parts = ["5\n"]
    for _ in range(5):
        parts.append(_random_case(rng, 2000, -1000, 1000))
    out.append({"id": "09", "input": "".join(parts)})

    # 10 大数据：正负交替，整段和为 0
    out.append({"id": "10", "input": "1\n" + _case(n, [1000000000 if i % 2 == 0 else -1000000000
                                                      for i in range(n)], 1, n)})
    return out
