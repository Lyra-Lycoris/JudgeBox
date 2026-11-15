import random


def cases():
    rng = random.Random(20261114)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    n = 200000
    return [
        {"id": "01", "input": "abcabcbb\n"},
        {"id": "02", "input": "bbbbb\n"},
        {"id": "03", "input": "pwwkew\n"},
        {"id": "04", "input": "a\n"},
        {"id": "05", "input": "a" * n + "\n"},
        {"id": "06", "input": "abba\n"},
        {"id": "07", "input": "dvdf\n"},
        {"id": "08", "input": alphabet + "\n"},
        {"id": "09", "input": "".join(rng.choice(alphabet[:20]) for _ in range(1000)) + "\n"},
        {"id": "10", "input": "".join(rng.choice(alphabet) for _ in range(n)) + "\n"},
        {"id": "11", "input": "".join(rng.choice("abc") for _ in range(n)) + "\n"},
        {"id": "12", "input": (alphabet * 4000)[:n] + "\n"},
    ]
