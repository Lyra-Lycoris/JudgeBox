def solve(x1: int, y1: int, x2: int, y2: int, px: int, py: int, d: int) -> bool:
    dx = x2 - x1
    dy = y2 - y1
    cross = dx * (py - y1) - dy * (px - x1)
    len2 = dx * dx + dy * dy
    return cross * cross <= d * d * len2
