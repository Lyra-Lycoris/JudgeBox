import random


def cases():
    rng = random.Random(20261115)
    out = [{"id": "01", "input": "1 10\n"}]
    out.append({"id": "02", "input": "1 1\n"})
    out.append({"id": "03", "input": "5 5\n"})
    out.append({"id": "04", "input": "9 10\n"})
    out.append({"id": "05", "input": "1 1000000000000000\n"})
    out.append({"id": "06", "input": "999999999999999 1000000000000000\n"})

    a = rng.randint(1, 500000)
    b = rng.randint(a, 1000000)
    out.append({"id": "07", "input": "%d %d\n" % (a, b)})

    a = rng.randint(1, 10 ** 12)
    b = rng.randint(a, 10 ** 12)
    out.append({"id": "08", "input": "%d %d\n" % (a, b)})

    out.append({"id": "09", "input": "1000000000000000 1000000000000000\n"})
    out.append({"id": "10", "input": "123456789 987654321\n"})
    return out
