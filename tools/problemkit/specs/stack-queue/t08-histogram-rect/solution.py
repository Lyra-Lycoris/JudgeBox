def solve(n: int, h: list[int]) -> int:
    stack = []
    best = 0
    for i in range(n + 1):
        cur = h[i] if i < n else 0
        while stack and h[stack[-1]] >= cur:
            height = h[stack.pop()]
            left = stack[-1] if stack else -1
            area = height * (i - left - 1)
            if area > best:
                best = area
        stack.append(i)
    return best
