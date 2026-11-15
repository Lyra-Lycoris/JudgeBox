package t13_island_count

func solve(n: Int64, m: Int64, grid: Array<Array<Int64>>): Int64 {
    let total = n * m
    let seen = Array<Int64>(total, repeat: 0)
    let stack = Array<Int64>(total, repeat: 0)
    var count: Int64 = 0
    for (s in 0..total) {
        if (seen[s] != 0) {
            continue
        }
        let sx = s / m
        let sy = s - sx * m
        if (grid[sx][sy] != 1) {
            continue
        }
        count += 1
        var top: Int64 = 0
        stack[top] = s
        top += 1
        seen[s] = 1
        while (top > 0) {
            top -= 1
            let cur = stack[top]
            let x = cur / m
            let y = cur - x * m
            var nxt = cur - m
            if (x > 0 && seen[nxt] == 0 && grid[x - 1][y] == 1) {
                seen[nxt] = 1
                stack[top] = nxt
                top += 1
            }
            nxt = cur + m
            if (x + 1 < n && seen[nxt] == 0 && grid[x + 1][y] == 1) {
                seen[nxt] = 1
                stack[top] = nxt
                top += 1
            }
            nxt = cur - 1
            if (y > 0 && seen[nxt] == 0 && grid[x][y - 1] == 1) {
                seen[nxt] = 1
                stack[top] = nxt
                top += 1
            }
            nxt = cur + 1
            if (y + 1 < m && seen[nxt] == 0 && grid[x][y + 1] == 1) {
                seen[nxt] = 1
                stack[top] = nxt
                top += 1
            }
        }
    }
    return count
}
