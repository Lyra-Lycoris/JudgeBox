import random


def cases():
    rng = random.Random(20261114)
    n = 200000
    out = [
        {"id": "01", "input": "FFRFF\n"},
        {"id": "02", "input": "RRFF\n"},
        {"id": "03", "input": "F\n"},
        {"id": "04", "input": "B\n"},
        {"id": "05", "input": "L\n"},
        {"id": "06", "input": "LFLFLFLF\n"},
        {"id": "07", "input": "F" * n + "\n"},
        {"id": "08", "input": "B" * n + "\n"},
        {"id": "09", "input": "L" * n + "\n"},
        {"id": "10", "input": "".join(rng.choice("LRFB") for _ in range(n)) + "\n"},
        {"id": "11", "input": "".join(rng.choice("LRFB") for _ in range(1000)) + "\n"},
        {"id": "12", "input": "FRFRFRFR" * 250 + "\n"},
    ]
    return out
