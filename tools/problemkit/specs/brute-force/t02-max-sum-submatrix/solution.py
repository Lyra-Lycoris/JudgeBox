def solve(n: int, m: int, g: list[list[int]]) -> int:
    answer = g[0][0]
    for top in range(n):
        sums = [0] * m
        for bottom in range(top, n):
            row = g[bottom]
            for c in range(m):
                sums[c] += row[c]
            cur = sums[0]
            best = sums[0]
            for c in range(1, m):
                cur = sums[c] if cur < 0 else cur + sums[c]
                if cur > best:
                    best = cur
            if best > answer:
                answer = best
    return answer
