import random


def pack(n, parents):
    if n <= 1:
        return "%d\n" % n
    return "%d\n%s\n" % (n, " ".join(str(x) for x in parents))


def chain(n):
    return [i - 1 for i in range(2, n + 1)]


def star(n):
    return [1] * (n - 1)


def random_parents(rng, n):
    return [rng.randint(1, i - 1) for i in range(2, n + 1)]


def cases():
    rng = random.Random(20261117)
    out = []
    out.append({"id": "01", "input": pack(5, [1, 1, 2, 2])})
    out.append({"id": "02", "input": pack(1, [])})
    out.append({"id": "03", "input": pack(2, [1])})
    out.append({"id": "04", "input": pack(6, chain(6))})
    out.append({"id": "05", "input": pack(6, star(6))})
    out.append({"id": "06", "input": pack(7, [1, 2, 2, 3, 3, 3])})
    out.append({"id": "07", "input": pack(100, random_parents(rng, 100))})
    out.append({"id": "08", "input": pack(5000, random_parents(rng, 5000))})
    out.append({"id": "09", "input": pack(200000, chain(200000))})
    out.append({"id": "10", "input": pack(200000, star(200000))})
    out.append({"id": "11", "input": pack(200000, random_parents(rng, 200000))})
    return out
