package t01_robot_moves

func solve(s: String): Array<Int64> {
    let dx = [0, 1, 0, -1]
    let dy = [1, 0, -1, 0]
    var facing = 0
    var x = 0
    var y = 0
    for (ch in s.toRuneArray()) {
        if (ch == r'L') {
            facing = (facing + 3) % 4
        } else if (ch == r'R') {
            facing = (facing + 1) % 4
        } else if (ch == r'F') {
            x += dx[facing]
            y += dy[facing]
        } else if (ch == r'B') {
            x -= dx[facing]
            y -= dy[facing]
        }
    }
    return [x, y]
}
