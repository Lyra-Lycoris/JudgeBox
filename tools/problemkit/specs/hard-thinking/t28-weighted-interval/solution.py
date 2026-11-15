from bisect import bisect_left


def solve(n: int, seg: list[list[int]]) -> int:
    order = sorted((r, l, w) for l, r, w in seg)
    ends = [item[0] for item in order]
    dp = [0] * (n + 1)
    for i in range(n):
        l = order[i][1]
        w = order[i][2]
        k = bisect_left(ends, l)  # 右端点严格小于 l 的区间个数
        best = dp[k] + w
        dp[i + 1] = dp[i] if dp[i] > best else best
    return dp[n]
