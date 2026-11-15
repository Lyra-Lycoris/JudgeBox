def solve(n: int, a: list[int]) -> int:
    best = mx = mn = a[0]
    for x in a[1:]:
        c1 = mx * x
        c2 = mn * x
        mx = max(x, c1, c2)
        mn = min(x, c1, c2)
        if mx > best:
            best = mx
    return best
