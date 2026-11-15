def solve(n: int, a: list[int]) -> int:
    best = 0
    for i in range(n):
        ai = a[i]
        for j in range(i + 1, n):
            v = ai ^ a[j]
            if v > best:
                best = v
    return best
