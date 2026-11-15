def solve(s: str) -> list[int]:
    dx = (0, 1, 0, -1)
    dy = (1, 0, -1, 0)
    facing = 0
    x = 0
    y = 0
    for ch in s:
        if ch == "L":
            facing = (facing + 3) % 4
        elif ch == "R":
            facing = (facing + 1) % 4
        elif ch == "F":
            x += dx[facing]
            y += dy[facing]
        elif ch == "B":
            x -= dx[facing]
            y -= dy[facing]
    return [x, y]
