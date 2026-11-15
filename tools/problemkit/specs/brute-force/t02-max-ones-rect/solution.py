def solve(n: int, m: int, g: list[list[int]]) -> int:
    best = 0
    for top in range(n):
        heights = [0] * m
        for bottom in range(top, n):
            row = g[bottom]
            for c in range(m):
                heights[c] = heights[c] + 1 if row[c] else 0
            stack = []
            for c in range(m + 1):
                h = heights[c] if c < m else 0
                while stack and heights[stack[-1]] >= h:
                    ph = heights[stack.pop()]
                    left = stack[-1] if stack else -1
                    area = ph * (c - left - 1)
                    if area > best:
                        best = area
                stack.append(c)
    return best
