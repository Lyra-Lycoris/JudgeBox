MOD = 1000000007


def solve(n: int, p: int, q: int) -> int:
    inv = pow((p + q) % MOD, MOD - 2, MOD)
    pa = p % MOD * inv % MOD
    pb = q % MOD * inv % MOD
    e1 = 0  # E[i+1]
    e2 = 0  # E[i+2]
    cur = 0
    for _ in range(n):
        cur = (1 + pa * e1 + pb * e2) % MOD
        e2 = e1
        e1 = cur
    return cur
