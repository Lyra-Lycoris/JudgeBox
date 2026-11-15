def solve(n: int, g: list[int], m: int, s: list[int]) -> int:
    gg = sorted(g)
    ss = sorted(s)
    i = 0
    j = 0
    while i < n and j < m:
        if ss[j] >= gg[i]:
            i += 1
        j += 1
    return i
