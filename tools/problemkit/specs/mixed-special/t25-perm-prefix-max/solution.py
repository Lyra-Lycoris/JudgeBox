def solve(n: int, k: int) -> list[int]:
    return list(range(1, k)) + list(range(n, k - 1, -1))
