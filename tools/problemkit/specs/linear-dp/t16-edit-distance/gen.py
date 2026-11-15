import random

ALPHABET4 = "abcd"
ALPHABET26 = "abcdefghijklmnopqrstuvwxyz"


def _rand(rng, length, alphabet):
    return "".join(rng.choice(alphabet) for _ in range(length))


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "kitten\nsitting\n"},
        {"id": "02", "input": "a\na\n"},
        {"id": "03", "input": "a\nb\n"},
        {"id": "04", "input": "abc\nabc\n"},
        {"id": "05", "input": "abcd\ndcba\n"},
        {"id": "06", "input": "intention\nexecution\n"},
    ]

    def add(s, t):
        out.append({"id": "%02d" % (len(out) + 1), "input": "%s\n%s\n" % (s, t)})

    add(_rand(rng, 1200, ALPHABET26), _rand(rng, 1200, ALPHABET26))

    same = _rand(rng, 2000, ALPHABET26)
    add(same, same)

    add(_rand(rng, 2000, ALPHABET4), _rand(rng, 2000, ALPHABET4))
    add(_rand(rng, 2000, ALPHABET26), _rand(rng, 2000, ALPHABET26))
    add("a" * 2000, "b" * 2000)
    add(_rand(rng, 2000, ALPHABET4), _rand(rng, 40, ALPHABET4))
    return out
