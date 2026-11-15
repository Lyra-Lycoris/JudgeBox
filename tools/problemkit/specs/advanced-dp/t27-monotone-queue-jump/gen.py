import random


def line(values):
    return " ".join(str(x) for x in values)


def pack(n, k, a):
    return "%d %d\n%s\n" % (n, k, line(a))


def cases():
    rng = random.Random(20261115)
    big = 10 ** 9
    out = []

    # 01 样例
    out.append({"id": "01", "input": pack(6, 2, [1, 3, 2, 5, 4, 1])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": pack(1, 1, [-5])})

    # 03 边界：k = 1，必须逐块走
    out.append({"id": "03", "input": pack(2, 1, [-3, -4])})

    # 04 边界：k = n，全是负数，尽量多站石头
    out.append({"id": "04", "input": pack(5, 5, [-1, -2, -3, -4, -5])})

    # 05 边界：全是正数，尽量少站石头
    out.append({"id": "05", "input": pack(8, 3, [big] * 8)})

    # 06 中等随机
    n = 1000
    out.append({"id": "06", "input": pack(n, 7, [rng.randint(-100000, 100000) for _ in range(n)])})

    # 07 大数据：k = 1，答案是全部之和
    n = 200000
    out.append({"id": "07", "input": pack(n, 1, [rng.randint(-big, big) for _ in range(n)])})

    # 08 大数据：k = n，负权重
    n = 200000
    out.append({"id": "08", "input": pack(n, n, [-big] * n)})

    # 09 大数据：k = 1000，随机正负
    n = 200000
    out.append({"id": "09", "input": pack(n, 1000, [rng.randint(-big, big) for _ in range(n)])})

    # 10 大数据：k = 447，全正数
    n = 200000
    out.append({"id": "10", "input": pack(n, 447, [big] * n)})

    # 11 大数据：k = 2，正负交替
    n = 200000
    out.append({"id": "11", "input": pack(n, 2, [big if i % 2 == 0 else -big for i in range(n)])})

    return out
