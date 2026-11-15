def solve(n: int, k: int, p: int) -> int:
    if k < 0 or k > n:
        return 0
    if k > n - k:
        k = n - k
    numerator = 1
    denominator = 1
    for i in range(1, k + 1):
        numerator = numerator * ((n - k + i) % p) % p
        denominator = denominator * (i % p) % p
    return numerator * pow(denominator, p - 2, p) % p
