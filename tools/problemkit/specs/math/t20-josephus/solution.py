def solve(n: int, k: int) -> int:
    if n <= 1:
        return 1
    if k == 1:
        return n
    f = 0
    m = 1
    while m < n:
        t = (m - f - 1) // (k - 1)
        if t <= 0:
            f = (f + k) % (m + 1)
            m += 1
        else:
            if t > n - m:
                t = n - m
            f += t * k
            m += t
    return f + 1
