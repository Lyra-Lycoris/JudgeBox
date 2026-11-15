def solve(n: int) -> list[int]:
    p = [(n + 1) // 2]
    hi = n
    lo = 1
    while len(p) < n:
        p.append(hi)
        hi -= 1
        if len(p) < n:
            p.append(lo)
            lo += 1
    return p
