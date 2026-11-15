import random


def _line(values):
    return " ".join(str(x) for x in values)


def _case(a, k):
    return "%d %d\n%s\n" % (len(a), k, _line(a))


def cases():
    rng = random.Random(20261120)
    n = 100000
    out = []

    # 01 样例
    out.append({"id": "01", "input": _case([1, 12, -5, -6, 50], 2)})

    # 02 边界：n = k = 1，只有一个负数
    out.append({"id": "02", "input": _case([-1000000000], 1)})

    # 03 边界：n = k = 1，只有一个正数
    out.append({"id": "03", "input": _case([1000000000], 1)})

    # 04 边界：全部相同
    out.append({"id": "04", "input": _case([7] * 10, 3)})

    # 05 边界：全为负数且互不相同
    out.append({"id": "05", "input": _case([-5, -11, -3, -20, -7], 2)})

    # 06 大数据：k = 1，全为 1e9，答案为 1e12
    out.append({"id": "06", "input": _case([1000000000] * n, 1)})

    # 07 大数据：k = n，只能取整段
    out.append({"id": "07", "input": _case([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)], n)})

    # 08 大数据：k = n/2，随机数组
    out.append({"id": "08", "input": _case([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)], 50000)})

    # 09 中等：随机
    out.append({"id": "09", "input": _case([rng.randint(-1000, 1000) for _ in range(1000)], 3)})

    # 10 大数据：正负交替，最大平均值就是单个 1e9
    out.append({"id": "10", "input": _case([1000000000 if i % 2 == 0 else -1000000000 for i in range(n)], 1)})

    # 11 大数据：单调递增，长度至少 k 的最优段是末尾 k 个
    out.append({"id": "11", "input": _case([i * 20000 - 1000000000 for i in range(n)], 1000)})

    # 12 大数据：先大后小再变大，最优段不在两端
    wave = [abs(i - 60000) * 30000 - 900000000 for i in range(n)]
    out.append({"id": "12", "input": _case(wave, 100)})
    return out
