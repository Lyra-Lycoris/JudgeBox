import random


def cases():
    rng = random.Random(20261114)
    out = [{"id": "01", "input": "1 10\n"}]
    out.append({"id": "02", "input": "4 4\n"})
    out.append({"id": "03", "input": "1 1\n"})
    out.append({"id": "04", "input": "1 1000000000000000000\n"})
    out.append({"id": "05", "input": "999999999999999999 1000000000000000000\n"})
    out.append({"id": "06", "input": "444444444444444444 444444444444444449\n"})

    a = rng.randint(1, 500000)
    b = rng.randint(a, 1000000)
    out.append({"id": "07", "input": "%d %d\n" % (a, b)})

    a = rng.randint(1, 10 ** 12)
    b = rng.randint(a, 10 ** 12)
    out.append({"id": "08", "input": "%d %d\n" % (a, b)})

    out.append({"id": "09", "input": "1 987654321987654321\n"})
    out.append({"id": "10", "input": "500000000000000000 500000000000000000\n"})
    return out
