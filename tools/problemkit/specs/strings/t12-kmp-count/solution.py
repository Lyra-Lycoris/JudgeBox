def solve(n: int, s: str, m: int, p: str) -> int:
    if m <= 0 or m > len(s):
        return 0
    pi = [0] * m
    k = 0
    for i in range(1, m):
        while k and p[i] != p[k]:
            k = pi[k - 1]
        if p[i] == p[k]:
            k += 1
        pi[i] = k
    count = 0
    k = 0
    for ch in s:
        while k and ch != p[k]:
            k = pi[k - 1]
        if ch == p[k]:
            k += 1
            if k == m:
                count += 1
                k = pi[k - 1]
    return count
