from array import array


def solve(n: int, a: list[int]) -> int:
    N = n
    if N <= 1:
        return 0
    w = N + 1
    size = w * w
    dp = array('q', bytes(8 * size))
    opt = array('i', bytes(4 * size))
    row = [i * w for i in range(w)]
    pre = [0] * w
    for i in range(1, w):
        pre[i] = pre[i - 1] + a[i - 1]
    for i in range(1, w):
        opt[row[i] + i] = i
    for length in range(2, w):
        for l in range(1, N - length + 2):
            r = l + length - 1
            base = row[l]
            lo = opt[base + r - 1]
            hi = opt[row[l + 1] + r]
            limit = r - 1
            if hi > limit:
                hi = limit
            best = -1
            bestk = lo
            for k in range(lo, hi + 1):
                v = dp[base + k] + dp[row[k + 1] + r]
                if best < 0 or v < best:
                    best = v
                    bestk = k
            dp[base + r] = best + pre[r] - pre[l - 1]
            opt[base + r] = bestk
    return dp[row[1] + N]
