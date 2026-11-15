def solve(n: int, m: int, grid: list[list[int]]) -> int:
    total = n * m
    seen = bytearray(total)
    stack = [0] * total
    count = 0
    for s in range(total):
        if seen[s]:
            continue
        x = s // m
        y = s - x * m
        if grid[x][y] != 1:
            continue
        count += 1
        top = 0
        stack[top] = s
        top += 1
        seen[s] = 1
        while top > 0:
            top -= 1
            cur = stack[top]
            x = cur // m
            y = cur - x * m
            nxt = cur - m
            if x > 0 and not seen[nxt] and grid[x - 1][y] == 1:
                seen[nxt] = 1
                stack[top] = nxt
                top += 1
            nxt = cur + m
            if x + 1 < n and not seen[nxt] and grid[x + 1][y] == 1:
                seen[nxt] = 1
                stack[top] = nxt
                top += 1
            nxt = cur - 1
            if y > 0 and not seen[nxt] and grid[x][y - 1] == 1:
                seen[nxt] = 1
                stack[top] = nxt
                top += 1
            nxt = cur + 1
            if y + 1 < m and not seen[nxt] and grid[x][y + 1] == 1:
                seen[nxt] = 1
                stack[top] = nxt
                top += 1
    return count
