MOD = 1000000007


def solve(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    numerator = 1
    denominator = 1
    for i in range(k):
        numerator = numerator * ((n - i) % MOD) % MOD
        denominator = denominator * (i + 1) % MOD
    return numerator * pow(denominator, MOD - 2, MOD) % MOD
