MOD = 1000000007


def solve(n: int) -> int:
    return (pow(2, n + 1, MOD) - 2) % MOD
