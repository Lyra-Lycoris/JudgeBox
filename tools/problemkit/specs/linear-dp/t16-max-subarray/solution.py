def solve(n: int, a: list[int]) -> int:
    best = cur = a[0]
    for x in a[1:]:
        cur = cur + x if cur > 0 else x
        if cur > best:
            best = cur
    return best
