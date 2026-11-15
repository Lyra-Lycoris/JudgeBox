import random


def pack(s, e):
    return "%d\n%s\n%s\n" % (len(s), " ".join(str(x) for x in s), " ".join(str(x) for x in e))


def cases():
    rng = random.Random(20260305)
    out = [{"id": "01", "input": pack([0, 5, 6], [10, 8, 9])}]
    out.append({"id": "02", "input": pack([5], [9])})
    out.append({"id": "03", "input": pack([1] * 5, [2] * 5)})
    out.append({"id": "04", "input": pack([0, 1, 2], [1, 2, 3])})
    out.append({"id": "05", "input": pack([-1000000000, 0], [0, 1000000000])})
    out.append({"id": "06", "input": pack([-5, -4, -3, -2], [-1, 0, 1, 2])})

    def random_case(n, lo, hi, max_len):
        s, e = [], []
        for _ in range(n):
            a = rng.randint(lo, hi - 1)
            b = min(hi, a + rng.randint(1, max_len))
            s.append(a)
            e.append(b)
        return pack(s, e)

    out.append({"id": "07", "input": random_case(2000, -10 ** 6, 10 ** 6, 1000)})
    out.append({"id": "08", "input": random_case(100000, -10 ** 9, 10 ** 9, 10 ** 6)})
    out.append({"id": "09", "input": random_case(100000, -1000, 1000, 2000)})
    return out
