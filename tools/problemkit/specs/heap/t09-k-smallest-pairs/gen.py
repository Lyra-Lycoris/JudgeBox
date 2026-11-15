import random


def pack(k, a, b):
    return "%d %d %d\n%s\n%s\n" % (len(a), len(b), k,
                                   " ".join(str(x) for x in a),
                                   " ".join(str(x) for x in b))


def cases():
    rng = random.Random(20260905)
    out = [{"id": "01", "input": pack(3, [1, 7, 11], [2, 4, 6])}]
    out.append({"id": "02", "input": pack(1, [-5], [-7])})
    out.append({"id": "03", "input": pack(5, [0, 0, 0, 0], [0, 0, 0])})
    out.append({"id": "04", "input": pack(4, [-3, -1, 2], [-4, 0, 5])})
    out.append({"id": "05", "input": pack(4, [-1000000000, 1000000000],
                                         [-1000000000, 1000000000])})
    out.append({"id": "06", "input": pack(1, [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])})
    out.append({"id": "07", "input": pack(12, [0, 1, 2, 3], [10, 20, 30])})
    out.append({"id": "08", "input": pack(100000,
                                         sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(1000)),
                                         sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(1000)))})
    out.append({"id": "09", "input": pack(100000,
                                         sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(100000)),
                                         sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(100000)))})
    out.append({"id": "10", "input": pack(100000,
                                         sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(100000)),
                                         [0])})
    return out
