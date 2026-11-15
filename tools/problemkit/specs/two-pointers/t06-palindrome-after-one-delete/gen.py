import random


def build_palindrome(rng, length):
    half = length // 2
    left = [rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(half)]
    middle = [] if length % 2 == 0 else [rng.choice("abcdefghijklmnopqrstuvwxyz")]
    return "".join(left + middle + left[::-1])


def cases():
    rng = random.Random(20261121)
    n = 200000
    pal = build_palindrome(rng, n)
    pal_odd = build_palindrome(rng, n - 1)
    inserted = list(pal_odd)
    inserted.insert(n // 3, rng.choice("abcdefghijklmnopqrstuvwxyz"))
    broken = list(pal)
    broken[n // 5] = rng.choice("abcdefghijklmnopqrstuvwxyz")
    broken[n // 2 + 7] = rng.choice("abcdefghijklmnopqrstuvwxyz")
    return [
        {"id": "01", "input": "aba\n"},
        {"id": "02", "input": "abca\n"},
        {"id": "03", "input": "abc\n"},
        {"id": "04", "input": "a\n"},
        {"id": "05", "input": "ab\n"},
        {"id": "06", "input": "aaab\n"},
        {"id": "07", "input": "a" * n + "\n"},
        {"id": "08", "input": pal + "\n"},
        {"id": "09", "input": "".join(inserted) + "\n"},
        {"id": "10", "input": "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(2000)) + "\n"},
        {"id": "11", "input": "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n)) + "\n"},
        {"id": "12", "input": "".join(broken) + "\n"},
    ]
