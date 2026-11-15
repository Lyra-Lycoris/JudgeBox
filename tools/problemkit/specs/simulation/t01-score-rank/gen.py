import random


def _line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "4\n3 1 4 2\n90 90 80 70\n80 70 100 60\n70 80 60 60\n"},
        {"id": "02", "input": "1\n1000000000\n0\n0\n0\n"},
        {"id": "03", "input": "3\n5 2 9\n60 60 60\n60 60 60\n60 60 60\n"},
        {"id": "04", "input": "3\n7 8 9\n90 80 70\n0 10 20\n0 0 0\n"},
        {"id": "05", "input": "3\n7 3 5\n50 50 50\n50 50 50\n50 50 50\n"},
        {"id": "06", "input": "2\n2 1\n0 100\n0 0\n0 0\n"},
    ]

    def add(n, max_score):
        ids = list(range(1, n + 1))
        rng.shuffle(ids)
        chinese = [rng.randint(0, max_score) for _ in range(n)]
        math = [rng.randint(0, max_score) for _ in range(n)]
        english = [rng.randint(0, max_score) for _ in range(n)]
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d\n%s\n%s\n%s\n%s\n" % (n, _line(ids), _line(chinese),
                                                       _line(math), _line(english))})

    add(1000, 100)
    add(200000, 100)
    add(200000, 3)
    add(200000, 0)
    add(50, 100)
    add(200000, 100)
    return out
