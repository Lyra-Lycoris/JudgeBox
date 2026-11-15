def solve(n: int, cost: int, a: list[int]) -> int:
    S = [0] * (n + 1)
    s = 0
    for i in range(n):
        s += a[i]
        S[i + 1] = s
    ms = [0] * (n + 2)
    bs = [0] * (n + 2)
    head = 0
    tail = 1
    answer = 0
    for i in range(1, n + 1):
        si = S[i]
        x = -2 * si
        while head + 1 < tail and ms[head + 1] * x + bs[head + 1] <= ms[head] * x + bs[head]:
            head += 1
        best = ms[head] * x + bs[head]
        dpi = best + si * si + cost
        if i == n:
            answer = dpi
        # 加入直线：斜率 m = S[i]，截距 b = dp[i] + S[i]^2
        m = si
        b = dpi + si * si
        while tail - head >= 2:
            m1 = ms[tail - 2]
            b1 = bs[tail - 2]
            m2 = ms[tail - 1]
            b2 = bs[tail - 1]
            # 中间直线废掉的条件：x12 <= x23，两边同乘正数后取反
            if (b2 - b1) * (m - m2) >= (b - b2) * (m2 - m1):
                tail -= 1
            else:
                break
        ms[tail] = m
        bs[tail] = b
        tail += 1
    return answer
