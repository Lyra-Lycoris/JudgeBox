MOD = 1000000007


def solve(n: int, m: int, blocked: list[int]) -> int:
    full = 1 << m
    valid = [s for s in range(full) if (s & (s << 1)) == 0]
    comp = {}
    for s in valid:
        lst = []
        for t in valid:
            if (s & t) == 0 and ((s << 1) & t) == 0 and ((s >> 1) & t) == 0:
                lst.append(t)
        comp[s] = lst
    dp = [0] * full
    b0 = blocked[0]
    for s in valid:
        if (s & b0) == 0:
            dp[s] = 1
    for row in range(1, n):
        b = blocked[row]
        ndp = [0] * full
        for s in valid:
            if s & b:
                continue
            total = 0
            for t in comp[s]:
                total += dp[t]
            ndp[s] = total % MOD
        dp = ndp
    ans = 0
    for s in valid:
        ans += dp[s]
    return ans % MOD
