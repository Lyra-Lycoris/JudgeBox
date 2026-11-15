import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261121)
    out = [
        {"id": "01", "input": "5\n1 2 3 5 4\n"},
        {"id": "02", "input": "1\n5\n"},
        {"id": "03", "input": "2\n1 2\n"},
        {"id": "04", "input": "2\n1 5\n"},
        {"id": "05", "input": "6\n7 7 7 7 7 7\n"},
        {"id": "06", "input": "8\n-4 -3 -2 -1 0 1 2 3\n"},
        {"id": "07", "input": "5\n5 4 3 2 1\n"},
    ]

    # 中等规模：取值很小，碰撞很多
    n = 1000
    a = [rng.randint(-10, 10) for _ in range(n)]
    out.append({"id": "08", "input": "%d\n%s\n" % (n, _line(a))})

    # 中等规模：连续整数打乱顺序，仍有不少下标对满足条件
    n = 1000
    a = list(range(-500, -500 + n))
    rng.shuffle(a)
    out.append({"id": "09", "input": "%d\n%s\n" % (n, _line(a))})

    # 大数据：a[i] = i（不打断），所有下标对都满足条件，答案为 n*(n-1)/2
    n = 200000
    a = list(range(1, n + 1))
    out.append({"id": "10", "input": "%d\n%s\n" % (n, _line(a))})

    # 大数据：a[i] = 2*i，任何一对都不满足条件，答案为 0
    n = 200000
    a = [2 * i for i in range(1, n + 1)]
    out.append({"id": "11", "input": "%d\n%s\n" % (n, _line(a))})

    # 大数据：全随机，答案很小
    n = 200000
    a = [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
    out.append({"id": "12", "input": "%d\n%s\n" % (n, _line(a))})
    return out
