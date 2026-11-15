import random


def _line(values):
    return " ".join(str(x) for x in values)


def _case(a):
    return "%d\n%s\n" % (len(a), _line(a))


def cases():
    rng = random.Random(20261117)
    n = 200000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _case([-2, 1, -3, 4, -1, 2, 1, -5])})

    # 02 边界：n = 1，正的最大值
    out.append({"id": "02", "input": _case([1000000000])})

    # 03 边界：n = 1，负的最小值
    out.append({"id": "03", "input": _case([-1000000000])})

    # 04 边界：全为负数，只能取单个元素
    out.append({"id": "04", "input": _case([-5, -1, -9, -3])})

    # 05 边界：n = 2，两数之和仍为负
    out.append({"id": "05", "input": _case([-5, -3])})

    # 06 全为正数，整段最优：答案 2e14
    out.append({"id": "06", "input": _case([1000000000] * n)})

    # 07 全为负数：答案是最大的单个元素
    out.append({"id": "07", "input": _case([-1000000000] * n)})

    # 08 大数据随机
    out.append({"id": "08", "input": _case([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)])})

    # 09 中等：正负交替
    out.append({"id": "09", "input": _case([1000 if i % 3 == 0 else -999 for i in range(1000)])})

    # 10 大数据：中间一整块极大正数，两侧是极小负数
    block = [-1000000000] * 100000 + [1000000000] * 50000 + [-1000000000] * 50000
    out.append({"id": "10", "input": _case(block)})

    # 11 大数据：先单调递减再单调递增
    out.append({"id": "11", "input": _case([-(i + 1) * 5000 for i in range(100000)]
                                          + [(i + 1) * 5000 for i in range(100000)])})
    return out
