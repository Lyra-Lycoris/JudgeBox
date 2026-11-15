MOD = 1000000007


def solve(n: int) -> int:
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, (prev1 + prev2) % MOD
    return prev1
