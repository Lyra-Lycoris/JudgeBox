def solve(n: int, m: int, grid: list[list[int]]) -> int:
    total = n * m
    dist = [-1] * total
    queue = [0] * total
    head = 0
    tail = 0
    fresh = 0
    for i in range(n):
        row = grid[i]
        base = i * m
        for j in range(m):
            value = row[j]
            if value == 2:
                dist[base + j] = 0
                queue[tail] = base + j
                tail += 1
            elif value == 1:
                fresh += 1
    if fresh == 0:
        return 0
    minutes = 0
    while head < tail:
        cur = queue[head]
        head += 1
        x = cur // m
        y = cur - x * m
        d = dist[cur]
        nd = d + 1
        if x > 0:
            nxt = cur - m
            if dist[nxt] == -1 and grid[x - 1][y] == 1:
                dist[nxt] = nd
                fresh -= 1
                queue[tail] = nxt
                tail += 1
                if nd > minutes:
                    minutes = nd
        if x + 1 < n:
            nxt = cur + m
            if dist[nxt] == -1 and grid[x + 1][y] == 1:
                dist[nxt] = nd
                fresh -= 1
                queue[tail] = nxt
                tail += 1
                if nd > minutes:
                    minutes = nd
        if y > 0:
            nxt = cur - 1
            if dist[nxt] == -1 and grid[x][y - 1] == 1:
                dist[nxt] = nd
                fresh -= 1
                queue[tail] = nxt
                tail += 1
                if nd > minutes:
                    minutes = nd
        if y + 1 < m:
            nxt = cur + 1
            if dist[nxt] == -1 and grid[x][y + 1] == 1:
                dist[nxt] = nd
                fresh -= 1
                queue[tail] = nxt
                tail += 1
                if nd > minutes:
                    minutes = nd
    if fresh > 0:
        return -1
    return minutes
