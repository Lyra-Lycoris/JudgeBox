def solve(s: str, t: str) -> int:
    m = len(t)
    prev = list(range(m + 1))
    for i in range(1, len(s) + 1):
        cur = [i] + [0] * m
        ch = s[i - 1]
        for j in range(1, m + 1):
            best = prev[j] + 1
            x = cur[j - 1] + 1
            if x < best:
                best = x
            sub = prev[j - 1] + (0 if ch == t[j - 1] else 1)
            if sub < best:
                best = sub
            cur[j] = best
        prev = cur
    return prev[m]
