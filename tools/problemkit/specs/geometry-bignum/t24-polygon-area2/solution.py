def solve(n: int, xs: list[int], ys: list[int]) -> int:
    total = 0
    px = xs[n - 1]
    py = ys[n - 1]
    for i in range(n):
        cx = xs[i]
        cy = ys[i]
        total += px * cy - cx * py
        px = cx
        py = cy
    return abs(total)
