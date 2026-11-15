def solve(n: int) -> int:
    best = 0
    last = -1
    pos = 0
    while n > 0:
        if n & 1:
            if last >= 0:
                gap = pos - last - 1
                if gap > best:
                    best = gap
            last = pos
        n >>= 1
        pos += 1
    return best
