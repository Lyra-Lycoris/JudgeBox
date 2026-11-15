def solve(n: int, a: list[int]) -> int:
    best = current = a[0]
    for x in a[1:]:
        current = current + x if current > 0 else x
        if current > best:
            best = current
    return best
