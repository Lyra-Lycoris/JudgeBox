import random


def cases():
    rng = random.Random(20261118)
    out = [{"id": "01", "input": "1 16 1\n"}]
    out.append({"id": "02", "input": "1 1 1\n"})
    out.append({"id": "03", "input": "1 10 0\n"})
    out.append({"id": "04", "input": "1024 1024 1\n"})
    out.append({"id": "05", "input": "1024 1024 2\n"})
    out.append({"id": "06", "input": "1 1000000000000000000 30\n"})
    out.append({"id": "07", "input": "500000000000000000 1000000000000000000 25\n"})
    out.append({"id": "08", "input": "1 1000000000000000000 60\n"})
    out.append({"id": "09", "input": "1 1000000000000000000 0\n"})
    out.append({"id": "10", "input": "1000000000000000000 1000000000000000000 24\n"})

    a = rng.randint(1, 500000)
    b = rng.randint(a, 1000000)
    out.append({"id": "11", "input": "%d %d %d\n" % (a, b, rng.randint(0, 20))})
    out.append({"id": "12", "input": "1 1048575 20\n"})
    return out
