def solve(n: int, a: list[int]) -> list[int]:
    x = 0
    for v in a:
        x ^= v
    lowbit = x & (-x)
    p = 0
    q = 0
    for v in a:
        if v & lowbit:
            p ^= v
        else:
            q ^= v
    return [p, q] if p < q else [q, p]
