def solve(n: int, m: int, g: list[list[int]], q: int, queries: list[list[int]]) -> list[int]:
    pre = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        row = pre[i]
        prev = pre[i - 1]
        src = g[i - 1]
        running = 0
        for j in range(1, m + 1):
            running += src[j - 1]
            row[j] = prev[j] + running
    answer = []
    for x1, y1, x2, y2 in queries:
        answer.append(pre[x2][y2] - pre[x1 - 1][y2] - pre[x2][y1 - 1] + pre[x1 - 1][y1 - 1])
    return answer
