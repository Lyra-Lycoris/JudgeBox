import random


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "0000\n0202\n5\n0201 0101 0102 1212 2002\n"},
        {"id": "02", "input": "1234\n1234\n0\n"},
        {"id": "03", "input": "0000\n0009\n1\n0009\n"},
        {"id": "04", "input": "0000\n0009\n1\n0000\n"},
        {"id": "05", "input": "0000\n9000\n0\n"},
        {"id": "06", "input": "0000\n5555\n8\n1000 9000 0100 0900 0010 0090 0001 0009\n"},
        {"id": "07", "input": "0000\n9999\n0\n"},
        {"id": "08", "input": "1111\n2222\n1\n0000\n"},
    ]

    def add(prefix, count, start="0000", target="9999"):
        dead = set()
        while len(dead) < count:
            code = "%04d" % rng.randrange(10000)
            if code != start and code != target:
                dead.add(code)
        codes = sorted(dead)
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%s\n%s\n%d\n%s\n" % (start, target, len(codes), " ".join(codes))})

    add("", 100, "0000", "0202")
    add("", 500, "1234", "9876")
    add("", 300, "0000", "9999")
    add("", 50, "5555", "0000")
    return out
