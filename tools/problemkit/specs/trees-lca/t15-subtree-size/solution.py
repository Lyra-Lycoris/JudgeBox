def solve(n: int, p: list[int]) -> list[int]:
    size = [0] + [1] * n
    for v in range(n, 1, -1):
        size[p[v - 2]] += size[v]
    return size[1:]
