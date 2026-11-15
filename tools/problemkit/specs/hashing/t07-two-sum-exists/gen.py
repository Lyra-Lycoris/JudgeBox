import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "4\n2 7 11 15\n9\n"},
        {"id": "02", "input": "1\n5\n10\n"},
        {"id": "03", "input": "2\n3 3\n6\n"},
        {"id": "04", "input": "5\n-1 -2 -3 -4 -5\n-8\n"},
        {"id": "05", "input": "6\n7 7 7 7 7 7\n15\n"},
        {"id": "06", "input": "6\n0 0 0 0 0 0\n0\n"},
    ]

    # 中等规模随机数据，答案一定为 YES
    n = 1000
    a = [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
    i, j = rng.sample(range(n), 2)
    out.append({"id": "07", "input": "%d\n%s\n%d\n" % (n, _line(a), a[i] + a[j])})

    # 中等规模正数随机数据，答案一定为 NO（最大和为 2*10^9-2）
    n = 5000
    a = [rng.randint(1, 10 ** 9 - 1) for _ in range(n)]
    out.append({"id": "08", "input": "%d\n%s\n%d\n" % (n, _line(a), 2 * 10 ** 9)})

    # 大数据：答案一定为 YES
    n = 200000
    a = [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
    i, j = rng.sample(range(n), 2)
    out.append({"id": "09", "input": "%d\n%s\n%d\n" % (n, _line(a), a[i] + a[j])})

    # 大数据：答案一定为 NO
    n = 200000
    a = [rng.randint(1, 10 ** 9 - 1) for _ in range(n)]
    out.append({"id": "10", "input": "%d\n%s\n%d\n" % (n, _line(a), 2 * 10 ** 9)})
    return out
