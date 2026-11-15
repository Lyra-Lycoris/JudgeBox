from collections import Counter


def solve(n: int, a: list[int]) -> int:
    return max(Counter(a).values())
