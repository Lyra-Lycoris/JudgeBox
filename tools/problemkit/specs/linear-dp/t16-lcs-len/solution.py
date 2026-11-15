def solve(s: str, t: str) -> int:
    m = len(t)
    prev = [0] * (m + 1)
    for ch in s:
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if ch == t[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                a = prev[j]
                b = cur[j - 1]
                cur[j] = a if a >= b else b
        prev = cur
    return prev[m]
