def solve(n: int, a: list[int]) -> int:
    MOD = 1000000007
    mask = 0
    for v in a:
        mask |= v
    return mask % MOD * pow(2, n - 1, MOD) % MOD
