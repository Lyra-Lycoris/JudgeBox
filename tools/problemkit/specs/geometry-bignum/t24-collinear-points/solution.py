def solve(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int) -> bool:
    cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    return cross == 0
