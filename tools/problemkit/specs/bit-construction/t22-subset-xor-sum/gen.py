import random


def _pack(values):
    return "%d\n%s\n" % (len(values), " ".join(str(v) for v in values))


def cases():
    rng = random.Random(20261115)
    out = [
        {"id": "01", "input": "2\n1 2\n"},
        {"id": "02", "input": "1\n0\n"},
        {"id": "03", "input": "1\n1000000000\n"},
        {"id": "04", "input": "3\n5 5 5\n"},
        {"id": "05", "input": "2\n0 0\n"},
    ]

    out.append({"id": "06", "input": _pack([rng.randint(0, 10 ** 9) for _ in range(1000)])})
    out.append({"id": "07", "input": _pack([0] * 200000)})
    out.append({"id": "08", "input": _pack([999999999] * 200000)})
    out.append({"id": "09", "input": _pack([rng.randint(0, 10 ** 9) for _ in range(200000)])})
    out.append({"id": "10", "input": _pack([10 ** 9] * 199999 + [1])})
    return out
