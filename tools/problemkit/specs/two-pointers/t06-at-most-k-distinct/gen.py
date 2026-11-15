import random


def cases():
    rng = random.Random(20261116)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    n = 200000
    return [
        {"id": "01", "input": "2\neceba\n"},
        {"id": "02", "input": "1\naaabbb\n"},
        {"id": "03", "input": "0\nabc\n"},
        {"id": "04", "input": "3\na\n"},
        {"id": "05", "input": "2\n" + "a" * n + "\n"},
        {"id": "06", "input": "1\n" + "".join(rng.choice("abc") for _ in range(n)) + "\n"},
        {"id": "07", "input": "5\n" + "".join(rng.choice(alphabet[:10]) for _ in range(n)) + "\n"},
        {"id": "08", "input": "100\n" + "".join(rng.choice(alphabet) for _ in range(n)) + "\n"},
        {"id": "09", "input": "2\nabcabcabc\n"},
        {"id": "10", "input": "2\nabaccc\n"},
        {"id": "11", "input": "4\n" + "".join(rng.choice(alphabet[:6]) for _ in range(n)) + "\n"},
        {"id": "12", "input": "62\n" + alphabet * 3000 + "\n"},
    ]
