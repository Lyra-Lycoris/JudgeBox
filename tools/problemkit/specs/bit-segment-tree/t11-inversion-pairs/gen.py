import random


def _input(n, a):
    return "%d\n%s\n" % (n, " ".join(str(x) for x in a))


def cases():
    rng = random.Random(20261123)
    big = 1000000000
    out = []

    # 01 样例：完全逆序
    out.append({"id": "01", "input": _input(5, [5, 4, 3, 2, 1])})

    # 02 边界：n = 1
    out.append({"id": "02", "input": _input(1, [-1000000000])})

    # 03 边界：全部相同
    out.append({"id": "03", "input": _input(6, [7, 7, 7, 7, 7, 7])})

    # 04 边界：已经升序
    out.append({"id": "04", "input": _input(8, [1, 2, 3, 4, 5, 6, 7, 8])})

    # 05 小数据：含负数与重复
    out.append({"id": "05", "input": _input(7, [-1, 3, -1, 2, -5, 2, 0])})

    # 06 极值：正负 1e9 交替
    out.append({"id": "06", "input": _input(8, [big, -big, big, -big, -big, big, -big, big])})

    # 07 中等随机
    n = 2000
    out.append({"id": "07", "input": _input(n, [rng.randint(-100000, 100000) for _ in range(n)])})

    # 08 大数据：随机 ±1e9
    n = 200000
    out.append({"id": "08", "input": _input(n, [rng.randint(-big, big) for _ in range(n)])})

    # 09 大数据：全部相同
    n = 200000
    out.append({"id": "09", "input": _input(n, [0] * n)})

    # 10 大数据：严格降序，答案取到最大值
    n = 200000
    out.append({"id": "10", "input": _input(n, list(range(n, 0, -1)))})

    return out
