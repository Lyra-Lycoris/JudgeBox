import random


def cases():
    rng = random.Random(20261116)
    out = [{"id": "01", "input": "1 20 1\n"}]
    out.append({"id": "02", "input": "1 9 0\n"})
    out.append({"id": "03", "input": "1 9 9\n"})
    out.append({"id": "04", "input": "1 1 0\n"})
    out.append({"id": "05", "input": "10 10 0\n"})
    out.append({"id": "06", "input": "1000000000000000000 1000000000000000000 1\n"})

    a = rng.randint(1, 10 ** 8)
    b = rng.randint(a, 10 ** 9)
    out.append({"id": "07", "input": "%d %d %d\n" % (a, b, rng.randint(0, 9))})

    out.append({"id": "08", "input": "1 1000000000000000000 0\n"})

    a = rng.randint(1, 10 ** 17)
    b = rng.randint(a, 10 ** 18)
    out.append({"id": "09", "input": "%d %d 5\n" % (a, b)})

    out.append({"id": "10", "input": "1 1000000000000000000 9\n"})
    out.append({"id": "11", "input": "1 1000000000000000000 2\n"})
    out.append({"id": "12", "input": "482 1000000000000000000 3\n"})
    return out
