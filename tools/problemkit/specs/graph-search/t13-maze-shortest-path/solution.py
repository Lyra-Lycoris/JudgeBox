def solve(n: int, m: int, grid: list[list[int]]) -> int:
    if n <= 0 or m <= 0:
        return -1
    if grid[0][0] != 0 or grid[n - 1][m - 1] != 0:
        return -1
    total = n * m
    dist = [-1] * total
    dist[0] = 0
    queue = [0]
    head = 0
    while head < len(queue):
        cur = queue[head]
        head += 1
        x = cur // m
        y = cur - x * m
        d = dist[cur] + 1
        if x > 0 and grid[x - 1][y] == 0 and dist[cur - m] == -1:
            dist[cur - m] = d
            queue.append(cur - m)
        if x + 1 < n and grid[x + 1][y] == 0 and dist[cur + m] == -1:
            dist[cur + m] = d
            queue.append(cur + m)
        if y > 0 and grid[x][y - 1] == 0 and dist[cur - 1] == -1:
            dist[cur - 1] = d
            queue.append(cur - 1)
        if y + 1 < m and grid[x][y + 1] == 0 and dist[cur + 1] == -1:
            dist[cur + 1] = d
            queue.append(cur + 1)
    return dist[total - 1]
