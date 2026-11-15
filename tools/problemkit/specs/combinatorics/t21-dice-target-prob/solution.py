MOD = 1000000007
INV6 = 166666668


def solve(n: int) -> int:
    p = [0] * (n + 1)
    pre = [0] * (n + 1)
    p[0] = 1
    pre[0] = 1
    for i in range(1, n + 1):
        window = pre[i - 1]
        if i >= 7:
            window -= pre[i - 7]
        p[i] = window % MOD * INV6 % MOD
        pre[i] = (pre[i - 1] + p[i]) % MOD
    return p[n]
