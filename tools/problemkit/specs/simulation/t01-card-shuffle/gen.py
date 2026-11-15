import random

BIG_K = 10 ** 18


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "4 1\n2 3 4 1\n"},
        {"id": "02", "input": "1 %d\n1\n" % BIG_K},
        {"id": "03", "input": "5 0\n3 1 5 2 4\n"},
        {"id": "04", "input": "5 %d\n1 2 3 4 5\n" % BIG_K},
        {"id": "05", "input": "4 %d\n4 3 2 1\n" % BIG_K},
        {"id": "06", "input": "6 7\n2 3 1 5 6 4\n"},
    ]

    def add(n, k, perm):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d %d\n%s\n" % (n, k, _line(perm))})

    n = 200000
    perm = list(range(1, n + 1))
    perm = perm[1:] + perm[:1]  # 一个大循环：位置 i 的卡片移动到 i+1
    add(n, BIG_K, perm)

    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    add(n, BIG_K, perm)

    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    add(n, 1, perm)

    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    add(n, 0, perm)

    perm = list(range(1, n + 1))
    for i in range(0, n - 1, 2):
        perm[i], perm[i + 1] = perm[i + 1], perm[i]
    add(n, BIG_K - 1, perm)

    perm = list(range(1, 1001))
    rng.shuffle(perm)
    add(1000, 999999999999, perm)
    return out
