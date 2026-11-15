import random


def pack(n, a):
    return "%d\n%s\n" % (n, " ".join(str(x) for x in a))


def cases():
    rng = random.Random(20261118)
    big = 10 ** 9
    out = []

    # 01 样例
    out.append({"id": "01", "input": pack(4, [5, 1, 1, 5])})

    # 02 边界：n = 1，负数
    out.append({"id": "02", "input": pack(1, [-7])})

    # 03 边界：n = 1，正数
    out.append({"id": "03", "input": pack(1, [9])})

    # 04 边界：n = 2，全负（只能取空集）
    out.append({"id": "04", "input": pack(2, [-3, -5])})

    # 05 边界：n = 3，全负
    out.append({"id": "05", "input": pack(3, [-1, -2, -3])})

    # 06 边界：n = 3，全正（三角形，最多取一个）
    out.append({"id": "06", "input": pack(3, [9, 8, 7])})

    # 07 小数据：正负混合
    out.append({"id": "07", "input": pack(6, [4, -1, 3, -2, 7, -5])})

    # 08 大数据：全正，环形只能隔一个取
    n = 200000
    out.append({"id": "08", "input": pack(n, [big] * n)})

    # 09 大数据：正负交替
    n = 200000
    out.append({"id": "09", "input": pack(n, [big if i % 2 == 0 else -big for i in range(n)])})

    # 10 大数据：随机
    n = 200000
    out.append({"id": "10", "input": pack(n, [rng.randint(-big, big) for _ in range(n)])})

    # 11 大数据：全 1，n 为奇数
    n = 199999
    out.append({"id": "11", "input": pack(n, [1] * n)})

    return out
