from collections import Counter


def solve(n: int, k: int, a: list[int]) -> list[int]:
    count = Counter(a)
    items = sorted(count.items(), key=lambda kv: (-kv[1], kv[0]))
    return [value for value, _ in items[:k]]
