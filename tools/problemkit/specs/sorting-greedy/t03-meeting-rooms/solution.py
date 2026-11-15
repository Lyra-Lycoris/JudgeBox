def solve(n: int, s: list[int], e: list[int]) -> int:
    ss = sorted(s)
    ee = sorted(e)
    i = 0
    j = 0
    cur = 0
    best = 0
    while i < n:
        if ss[i] < ee[j]:
            cur += 1
            if cur > best:
                best = cur
            i += 1
        else:
            cur -= 1
            j += 1
    return best
