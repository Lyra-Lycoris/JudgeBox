import random


def pack(values):
    return "%d\n%s\n" % (len(values), " ".join(str(x) for x in values))


def cases():
    rng = random.Random(20261225)
    out = [{"id": "01", "input": pack([10, 1, 100])}]
    out.append({"id": "02", "input": pack([1])})
    out.append({"id": "03", "input": pack([2])})
    out.append({"id": "04", "input": pack([2, 2, 2, 2, 2])})
    out.append({"id": "05", "input": pack([10 ** 7])})
    out.append({"id": "06", "input": pack([3, 5, 7, 11, 13, 97, 100, 1000, 99991, 10 ** 7])})
    out.append({"id": "07", "input": pack([rng.randint(1, 10 ** 7) for _ in range(200000)])})
    out.append({"id": "08", "input": pack([rng.randint(1, 1000) for _ in range(200000)])})
    out.append({"id": "09", "input": pack([10 ** 7 - i for i in range(100000)])})
    out.append({"id": "10", "input": pack([10 ** 7] * 200000)})
    return out
