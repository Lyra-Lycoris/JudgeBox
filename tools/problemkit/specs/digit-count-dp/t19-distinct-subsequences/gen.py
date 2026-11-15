import random


def pack(s):
    return "%d\n%s\n" % (len(s), s)


def cases():
    rng = random.Random(20261119)
    out = [{"id": "01", "input": pack("aba")}]
    out.append({"id": "02", "input": pack("a")})
    out.append({"id": "03", "input": pack("aaaa")})
    out.append({"id": "04", "input": pack("abc")})

    s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(1000))
    out.append({"id": "05", "input": pack(s)})

    s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(200000))
    out.append({"id": "06", "input": pack(s)})

    out.append({"id": "07", "input": pack("a" * 200000)})

    s = "".join(rng.choice("ab") for _ in range(200000))
    out.append({"id": "08", "input": pack(s)})

    s = "".join(rng.choice("abc") for _ in range(100))
    out.append({"id": "09", "input": pack(s)})

    out.append({"id": "10", "input": pack("ab" * 100000)})
    return out
