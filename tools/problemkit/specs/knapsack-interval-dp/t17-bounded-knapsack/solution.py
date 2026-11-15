def solve(n: int, cap: int, w: list[int], v: list[int], c: list[int]) -> int:
    dp = [0] * (cap + 1)
    for i in range(n):
        wi = w[i]
        vi = v[i]
        rest = c[i]
        block = 1
        while rest > 0:
            take = block if block < rest else rest
            bw = wi * take
            bv = vi * take
            if bw <= cap:
                for j in range(cap, bw - 1, -1):
                    cand = dp[j - bw] + bv
                    if cand > dp[j]:
                        dp[j] = cand
            rest -= take
            block *= 2
    return dp[cap]
