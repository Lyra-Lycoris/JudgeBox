def solve(n: int) -> int:
    MOD = 1000000007
    factorial_n = 1
    for i in range(2, n + 1):
        factorial_n = factorial_n * i % MOD
    upper = 1
    for i in range(n + 1, 2 * n + 1):
        upper = upper * i % MOD
    binomial = upper * pow(factorial_n, MOD - 2, MOD) % MOD
    return binomial * pow(n + 1, MOD - 2, MOD) % MOD
