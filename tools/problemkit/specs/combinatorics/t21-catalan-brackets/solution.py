MOD = 1000000007


def solve(n: int) -> int:
    numerator = 1
    denominator = 1
    for i in range(1, n + 1):
        numerator = numerator * ((n + i) % MOD) % MOD
        denominator = denominator * (i % MOD) % MOD
    denominator = denominator * ((n + 1) % MOD) % MOD
    return numerator * pow(denominator, MOD - 2, MOD) % MOD
