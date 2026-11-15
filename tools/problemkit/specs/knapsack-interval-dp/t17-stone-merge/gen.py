import random


def _join(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261118)
    out = []

    # 01 样例
    out.append({"id": "01", "input": "4\n1 3 5 2\n"})

    # 02 只有一堆
    out.append({"id": "02", "input": "1\n5\n"})

    # 03 两堆最大值
    out.append({"id": "03", "input": "2\n1000000000 1000000000\n"})

    # 04 200 堆全相同
    n = 200
    out.append({"id": "04", "input": "%d\n%s\n" % (n, _join([1] * n))})

    # 05 大数据：随机
    n = 200
    a = [rng.randint(1, 10 ** 9) for _ in range(n)]
    out.append({"id": "05", "input": "%d\n%s\n" % (n, _join(a))})

    # 06 小数据
    out.append({"id": "06", "input": "3\n1 2 3\n"})

    # 07 递减
    n = 200
    a = [(n - i) * 1000000 for i in range(1, n + 1)]
    out.append({"id": "07", "input": "%d\n%s\n" % (n, _join(a))})

    # 08 随机中等
    n = 100
    a = [rng.randint(1, 100) for _ in range(n)]
    out.append({"id": "08", "input": "%d\n%s\n" % (n, _join(a))})

    # 09 两堆相同
    out.append({"id": "09", "input": "2\n7 7\n"})

    # 10 大小交替
    n = 200
    a = [1 if i % 2 == 0 else 10 ** 9 for i in range(n)]
    out.append({"id": "10", "input": "%d\n%s\n" % (n, _join(a))})

    return out
