def solve(n: int, s: str) -> int:
    m = len(s)
    if m == 0:
        return 0
    pi = [0] * m
    k = 0
    for i in range(1, m):
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    d = m - pi[m - 1]
    return d if m % d == 0 else m
