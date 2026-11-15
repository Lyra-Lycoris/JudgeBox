def solve(n: int, a: list[int]) -> int:
    order = [idx for _, idx in sorted(zip(a, range(n)))]
    bit = [0] * (n + 1)
    answer = 0
    seen = 0
    for idx in order:
        pos = idx + 1
        s = 0
        t = pos
        while t > 0:
            s += bit[t]
            t -= t & (-t)
        answer += seen - s
        seen += 1
        t = pos
        while t <= n:
            bit[t] += 1
            t += t & (-t)
    return answer
