from collections import deque


def solve(n: int, k: int, a: list[int]) -> int:
    dp = [0] * n
    dp[0] = a[0]
    dq = deque([0])
    for i in range(1, n):
        left = i - k
        while dq[0] < left:
            dq.popleft()
        dp[i] = a[i] + dp[dq[0]]
        cur = dp[i]
        while dq and dp[dq[-1]] >= cur:
            dq.pop()
        dq.append(i)
    return dp[-1]
