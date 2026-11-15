MOD = 1000000007


def solve(n: int) -> int:
    if n == 0:
        return 1
    prev2, prev1 = 1, 0
    for i in range(2, n + 1):
        prev2, prev1 = prev1, (i - 1) * (prev1 + prev2) % MOD
    return prev1
