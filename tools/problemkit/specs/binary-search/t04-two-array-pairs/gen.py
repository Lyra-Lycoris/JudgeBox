import random


def pack(a, b, x):
    return "%d\n%s\n%d\n%s\n%d\n" % (len(a), " ".join(str(v) for v in a), len(b), " ".join(str(v) for v in b), x)


def cases():
    rng = random.Random(20261128)
    out = [{"id": "01", "input": pack([1, 2, 3], [4, 5, 6], 7)}]
    out.append({"id": "02", "input": pack([5], [5], 9)})
    out.append({"id": "03", "input": pack([1, 2], [1, 2], 100)})
    out.append({"id": "04", "input": pack([-5, -1], [-3, 10], -4)})
    out.append({"id": "05", "input": pack([1, 1, 1], [1, 1, 1], 2)})
    out.append({"id": "06", "input": pack([-10 ** 9], [-10 ** 9], -2 * 10 ** 9)})
    out.append({"id": "07", "input": pack([10 ** 9], [10 ** 9], 2 * 10 ** 9)})
    out.append({"id": "08", "input": pack([10 ** 9], [10 ** 9], 2 * 10 ** 9 - 1)})

    n = 1000
    out.append({"id": "09", "input": pack([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)],
                                          [rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)],
                                          rng.randint(-10 ** 9, 10 ** 9))})

    n = 200000
    out.append({"id": "10", "input": pack([rng.randint(-10 ** 9, 10 ** 9) for _ in range(n)],
                                          [rng.randint(-10 ** 5, 10 ** 5) for _ in range(n)],
                                          0)})

    a = [i // 3 for i in range(n)]
    b = [i // 2 for i in range(n)]
    out.append({"id": "11", "input": pack(a, b, n // 2)})

    out.append({"id": "12", "input": pack([10 ** 9] * n, [0] * n, 10 ** 9)})
    return out
