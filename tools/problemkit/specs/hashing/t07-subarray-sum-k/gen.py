import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261120)
    out = [
        {"id": "01", "input": "5 3\n1 1 1 1 1\n"},
        {"id": "02", "input": "1 5\n5\n"},
        {"id": "03", "input": "1 0\n7\n"},
        {"id": "04", "input": "4 0\n1 -1 1 -1\n"},
        {"id": "05", "input": "5 -3\n-1 -2 0 -3 6\n"},
        {"id": "06", "input": "3 100000000000000\n0 0 0\n"},
    ]

    # 中等规模：取值在 [-5, 5]，k = 3
    n = 1000
    a = [rng.randint(-5, 5) for _ in range(n)]
    out.append({"id": "07", "input": "%d 3\n%s\n" % (n, _line(a))})

    # 中等规模：全部为 0，k = 0，答案为 n*(n+1)/2
    n = 1000
    a = [0] * n
    out.append({"id": "08", "input": "%d 0\n%s\n" % (n, _line(a))})

    # 大数据：全部为 0，k = 0
    n = 200000
    a = [0] * n
    out.append({"id": "09", "input": "%d 0\n%s\n" % (n, _line(a))})

    # 大数据：全部为 1，k = 100000
    n = 200000
    a = [1] * n
    out.append({"id": "10", "input": "%d 100000\n%s\n" % (n, _line(a))})

    # 大数据：取值在 [-1000, 1000]，k = 0
    n = 200000
    a = [rng.randint(-1000, 1000) for _ in range(n)]
    out.append({"id": "11", "input": "%d 0\n%s\n" % (n, _line(a))})

    # 大数据：全部为 -1，k = -5
    n = 200000
    a = [-1] * n
    out.append({"id": "12", "input": "%d -5\n%s\n" % (n, _line(a))})
    return out
