import random

ALPHABET4 = "abcd"
ALPHABET26 = "abcdefghijklmnopqrstuvwxyz"


def _rand(rng, length, alphabet):
    return "".join(rng.choice(alphabet) for _ in range(length))


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "abcde\nace\n"},
        {"id": "02", "input": "a\na\n"},
        {"id": "03", "input": "a\nb\n"},
        {"id": "04", "input": "aaaa\naa\n"},
        {"id": "05", "input": "abcdefg\ngfedcba\n"},
        {"id": "06", "input": "abcbdab\nbdcaba\n"},
    ]

    def add(s, t):
        out.append({"id": "%02d" % (len(out) + 1), "input": "%s\n%s\n" % (s, t)})

    add(_rand(rng, 800, ALPHABET4), _rand(rng, 800, ALPHABET4))

    same = _rand(rng, 2000, ALPHABET26)
    add(same, same)

    add(_rand(rng, 2000, ALPHABET4), _rand(rng, 2000, ALPHABET4))
    add(_rand(rng, 2000, ALPHABET26), _rand(rng, 2000, ALPHABET26))
    add("a" * 1000 + "b" * 1000, "a" * 1000 + "c" * 1000)
    add(_rand(rng, 2000, ALPHABET4), _rand(rng, 1200, ALPHABET4))
    return out
