import random


def pack(x):
    return "%d\n" % x


def cases():
    rng = random.Random(20261127)
    out = [{"id": "01", "input": pack(7)}]
    out.append({"id": "02", "input": pack(0)})
    out.append({"id": "03", "input": pack(1)})
    out.append({"id": "04", "input": pack(4)})
    out.append({"id": "05", "input": pack(2)})
    out.append({"id": "06", "input": pack(999999999999)})
    out.append({"id": "07", "input": pack(10 ** 12)})
    out.append({"id": "08", "input": pack(999999999)})
    out.append({"id": "09", "input": pack(3)})
    out.append({"id": "10", "input": pack(rng.randint(0, 10 ** 6))})
    out.append({"id": "11", "input": pack(rng.randint(0, 10 ** 12))})
    out.append({"id": "12", "input": pack(123456789012)})
    return out
