import random


def pack(c, tasks):
    return "%d %d\n%s\n" % (len(tasks), c, " ".join(str(x) for x in tasks))


def cases():
    rng = random.Random(20260903)
    out = [{"id": "01", "input": pack(2, [1, 1, 1, 2, 2, 2])}]
    out.append({"id": "02", "input": pack(0, [5])})
    out.append({"id": "03", "input": pack(3, [7] * 6)})
    out.append({"id": "04", "input": pack(0, [3, 1, 3, 1, 3])})
    out.append({"id": "05", "input": pack(1000000000, [1, 2, 3, 4, 5])})
    out.append({"id": "06", "input": pack(1, [1000000000, 1000000000, 2, 2, 2, 3])})

    n = 2000
    out.append({"id": "07", "input": pack(5, [rng.randint(1, 20) for _ in range(n)])})

    n = 200000
    out.append({"id": "08", "input": pack(1000, [rng.randint(1, 50000) for _ in range(n)])})

    out.append({"id": "09", "input": pack(1000000000, [1] * 200000)})
    out.append({"id": "10", "input": pack(7, [1] * 100000 + [2] * 100000)})
    return out
