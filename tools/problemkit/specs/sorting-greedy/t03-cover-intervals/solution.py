def solve(n: int, l: list[int], r: list[int], m: int) -> int:
    SHIFT = 1000000000
    BASE = 2000000001
    keys = sorted((l[i] + SHIFT) * BASE + (r[i] + SHIFT) for i in range(n))
    i = 0
    cur = 0
    count = 0
    while cur < m:
        best = -1
        while i < n and keys[i] // BASE - SHIFT <= cur:
            rr = keys[i] % BASE - SHIFT
            if rr > best:
                best = rr
            i += 1
        if best <= cur:
            return -1
        cur = best
        count += 1
    return count
