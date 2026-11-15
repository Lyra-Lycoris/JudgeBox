def solve(n: int) -> list[int]:
    return [1 if i % 2 == 0 else 2 for i in range(n)]
