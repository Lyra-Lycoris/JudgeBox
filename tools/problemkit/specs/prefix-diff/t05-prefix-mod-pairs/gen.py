import random


def _line(values):
    return " ".join(str(x) for x in values)


def _case(a, k):
    return "%d\n%s\n%d\n" % (len(a), _line(a), k)


def cases():
    rng = random.Random(20261118)
    n = 200000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _case([4, 5, 0, 2, 3], 5)})

    # 02 边界：n = 1，k = 1，整段必然被整除
    out.append({"id": "02", "input": _case([5], 1)})

    # 03 边界：n = 1，无法整除
    out.append({"id": "03", "input": _case([1], 1000000000)})

    # 04 边界：全是 0，任意子段都整除
    out.append({"id": "04", "input": _case([0] * 5, 7)})

    # 05 边界：有负数，取模后仍能配对
    out.append({"id": "05", "input": _case([-3, -1, -4, -1], 2)})

    # 06 大数据：k = 1，答案为 n(n+1)/2 = 20000100000
    out.append({"id": "06", "input": _case([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)], 1)})

    # 07 大数据：随机数组，k = 1e9
    out.append({"id": "07", "input": _case([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)], 1000000000)})

    # 08 大数据：每个元素都等于 k，前缀余数恒为 0
    out.append({"id": "08", "input": _case([1000000000] * n, 1000000000)})

    # 09 大数据：小范围随机，k = 4
    out.append({"id": "09", "input": _case([rng.randint(0, 3) for _ in range(n)], 4)})

    # 10 大数据：正负交替，k = 2
    out.append({"id": "10", "input": _case([1 if i % 2 == 0 else -1 for i in range(n)], 2)})

    # 11 中等：k = 7
    out.append({"id": "11", "input": _case([rng.randint(-1000, 1000) for _ in range(1000)], 7)})
    return out
