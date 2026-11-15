import random


def pack(a):
    return "%d\n%s\n" % (len(a), " ".join(str(x) for x in a))


def cases():
    rng = random.Random(20260906)
    out = [{"id": "01", "input": pack([4, 3, 2, 6])}]
    out.append({"id": "02", "input": pack([7])})
    out.append({"id": "03", "input": pack([1000000000, 1000000000])})
    out.append({"id": "04", "input": pack([5, 5, 5, 5, 5])})
    out.append({"id": "05", "input": pack([0, 0, 0, 0, 0, 0])})
    out.append({"id": "06", "input": pack([0, 1000000000, 1, 0, 999999999])})

    out.append({"id": "07", "input": pack([rng.randint(0, 10 ** 9) for _ in range(2000)])})
    out.append({"id": "08", "input": pack([rng.randint(0, 10 ** 9) for _ in range(200000)])})
    out.append({"id": "09", "input": pack([1000000000] * 200000)})
    return out
