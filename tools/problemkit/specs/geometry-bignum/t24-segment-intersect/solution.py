def _cross(ax, ay, bx, by, cx, cy):
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)


def _between(lo1, lo2, value):
    return min(lo1, lo2) <= value <= max(lo1, lo2)


def _on_segment(ax, ay, bx, by, px, py):
    return _between(ax, bx, px) and _between(ay, by, py)


def solve(ax: int, ay: int, bx: int, by: int,
          cx: int, cy: int, dx: int, dy: int) -> bool:
    d1 = _cross(ax, ay, bx, by, cx, cy)
    d2 = _cross(ax, ay, bx, by, dx, dy)
    d3 = _cross(cx, cy, dx, dy, ax, ay)
    d4 = _cross(cx, cy, dx, dy, bx, by)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
            ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    if d1 == 0 and _on_segment(ax, ay, bx, by, cx, cy):
        return True
    if d2 == 0 and _on_segment(ax, ay, bx, by, dx, dy):
        return True
    if d3 == 0 and _on_segment(cx, cy, dx, dy, ax, ay):
        return True
    if d4 == 0 and _on_segment(cx, cy, dx, dy, bx, by):
        return True
    return False
