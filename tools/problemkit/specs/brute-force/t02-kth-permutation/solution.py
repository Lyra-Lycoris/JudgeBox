def solve(n: int, k: int) -> list[int]:
    p = list(range(1, n + 1))
    for _ in range(k - 1):
        i = n - 2
        while i >= 0 and p[i] >= p[i + 1]:
            i -= 1
        if i < 0:
            break
        j = n - 1
        while p[j] <= p[i]:
            j -= 1
        p[i], p[j] = p[j], p[i]
        p[i + 1:] = reversed(p[i + 1:])
    return p
