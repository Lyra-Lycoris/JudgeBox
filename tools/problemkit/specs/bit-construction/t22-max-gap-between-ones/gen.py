import random


def _pack(values):
    return "%d\n%s\n" % (len(values), "\n".join(str(v) for v in values))


def cases():
    rng = random.Random(20261115)
    out = [
        {"id": "01", "input": "3\n9\n5\n100\n"},
        {"id": "02", "input": "1\n0\n"},
        {"id": "03", "input": "4\n2\n4\n8\n16\n"},
        {"id": "04", "input": "3\n576460752303423489\n576460752303423488\n1\n"},
        {"id": "05", "input": "5\n3\n7\n15\n576460752303423487\n288230376151711743\n"},
        {"id": "06", "input": _pack([rng.randint(0, 10 ** 18) for _ in range(1000)])},
        {"id": "07", "input": "1\n1000000000000000000\n"},
        {"id": "08", "input": _pack([rng.randint(0, 10 ** 18) for _ in range(200000)])},
        {"id": "09", "input": _pack([10 ** 18 if i % 2 == 0 else (1 << (i % 60)) for i in range(200000)])},
        {"id": "10", "input": _pack([(1 << (59 - i % 60)) | 1 for i in range(200000)])},
    ]
    return out
