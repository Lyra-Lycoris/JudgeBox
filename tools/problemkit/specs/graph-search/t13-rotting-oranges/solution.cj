package t13_rotting_oranges

func solve(n: Int64, m: Int64, grid: Array<Array<Int64>>): Int64 {
    let total = n * m
    let dist = Array<Int64>(total, repeat: -1)
    let queue = Array<Int64>(total, repeat: 0)
    var head: Int64 = 0
    var tail: Int64 = 0
    var fresh: Int64 = 0
    for (i in 0..n) {
        for (j in 0..m) {
            let value = grid[i][j]
            if (value == 2) {
                dist[i * m + j] = 0
                queue[tail] = i * m + j
                tail += 1
            } else if (value == 1) {
                fresh += 1
            }
        }
    }
    if (fresh == 0) {
        return 0
    }
    var minutes: Int64 = 0
    while (head < tail) {
        let cur = queue[head]
        head += 1
        let x = cur / m
        let y = cur - x * m
        let nd = dist[cur] + 1
        if (x > 0 && dist[cur - m] == -1 && grid[x - 1][y] == 1) {
            dist[cur - m] = nd
            queue[tail] = cur - m
            tail += 1
            fresh -= 1
            if (nd > minutes) {
                minutes = nd
            }
        }
        if (x + 1 < n && dist[cur + m] == -1 && grid[x + 1][y] == 1) {
            dist[cur + m] = nd
            queue[tail] = cur + m
            tail += 1
            fresh -= 1
            if (nd > minutes) {
                minutes = nd
            }
        }
        if (y > 0 && dist[cur - 1] == -1 && grid[x][y - 1] == 1) {
            dist[cur - 1] = nd
            queue[tail] = cur - 1
            tail += 1
            fresh -= 1
            if (nd > minutes) {
                minutes = nd
            }
        }
        if (y + 1 < m && dist[cur + 1] == -1 && grid[x][y + 1] == 1) {
            dist[cur + 1] = nd
            queue[tail] = cur + 1
            tail += 1
            fresh -= 1
            if (nd > minutes) {
                minutes = nd
            }
        }
    }
    if (fresh > 0) {
        return -1
    }
    return minutes
}
