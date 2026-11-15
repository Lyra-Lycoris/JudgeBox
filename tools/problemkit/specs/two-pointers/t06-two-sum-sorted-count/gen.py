import random


def cases():
    rng = random.Random(20261117)
    n = 200000
    zeros = " ".join(["0"] * n)
    small = sorted(rng.randint(0, 3) for _ in range(n))
    ladder = list(range(n))
    r2000 = sorted(rng.randint(-10 ** 9, 10 ** 9) for _ in range(2000))
    wide = sorted(rng.randint(0, 10 ** 9) for _ in range(n))
    pair_target = wide[123] + wide[190000]
    return [
        {"id": "01", "input": "5 5\n1 2 3 4 5\n"},
        {"id": "02", "input": "3 4\n2 2 2\n"},
        {"id": "03", "input": "1 5\n5\n"},
        {"id": "04", "input": "6 -4\n-5 -3 -1 2 4 7\n"},
        {"id": "05", "input": "3 100\n1 2 3\n"},
        {"id": "06", "input": "2 2\n1 1\n"},
        {"id": "07", "input": "200000 0\n" + zeros + "\n"},
        {"id": "08", "input": "200000 2000000000\n" + " ".join(["1000000000"] * n) + "\n"},
        {"id": "09", "input": "200000 3\n" + " ".join(str(x) for x in small) + "\n"},
        {"id": "10", "input": "2000 %d\n" % rng.randint(-10 ** 9, 10 ** 9) + " ".join(str(x) for x in r2000) + "\n"},
        {"id": "11", "input": "200000 %d\n" % pair_target + " ".join(str(x) for x in wide) + "\n"},
        {"id": "12", "input": "200000 199999\n" + " ".join(str(x) for x in ladder) + "\n"},
    ]
