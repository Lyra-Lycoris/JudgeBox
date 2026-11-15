import random


def pack(n, a):
    return "%d\n%s\n" % (n, " ".join(str(x) for x in a))


def cases():
    rng = random.Random(20261119)
    big = 10 ** 9
    out = []

    # 01 样例
    out.append({"id": "01", "input": pack(4, [1, 2, 3, 4])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": pack(1, [big])})

    # 03 边界：n = 2
    out.append({"id": "03", "input": pack(2, [5, 7])})

    # 04 小数据：全 1
    out.append({"id": "04", "input": pack(3, [1, 1, 1])})

    # 05 小数据：递增
    out.append({"id": "05", "input": pack(5, [1, 2, 3, 4, 5])})

    # 06 中等随机
    out.append({"id": "06", "input": pack(100, [rng.randint(1, big) for _ in range(100)])})

    # 07 大数据：n = 1500 随机
    n = 1500
    out.append({"id": "07", "input": pack(n, [rng.randint(1, big) for _ in range(n)])})

    # 08 大数据：全 1e9
    n = 1500
    out.append({"id": "08", "input": pack(n, [big] * n)})

    # 09 大数据：全 1
    n = 1500
    out.append({"id": "09", "input": pack(n, [1] * n)})

    # 10 大数据：递增
    n = 1500
    out.append({"id": "10", "input": pack(n, list(range(1, n + 1)))})

    # 11 大数据：小数值随机
    n = 1400
    out.append({"id": "11", "input": pack(n, [rng.randint(1, 100) for _ in range(n)])})

    return out
