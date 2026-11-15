def solve(s: int, k: int) -> list[int]:
    return [1] * (k - 1) + [s - (k - 1)]
