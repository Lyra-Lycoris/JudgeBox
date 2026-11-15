package t13_maze_shortest_path

func solve(n: Int64, m: Int64, grid: Array<Array<Int64>>): Int64 {
    if (n <= 0 || m <= 0) {
        return -1
    }
    if (grid[0][0] != 0 || grid[n - 1][m - 1] != 0) {
        return -1
    }
    let total = n * m
    let dist = Array<Int64>(total, repeat: -1)
    let queue = Array<Int64>(total, repeat: 0)
    var head: Int64 = 0
    var tail: Int64 = 0
    dist[0] = 0
    queue[tail] = 0
    tail += 1
    while (head < tail) {
        let cur = queue[head]
        head += 1
        let x = cur / m
        let y = cur - x * m
        let d = dist[cur] + 1
        if (x > 0 && grid[x - 1][y] == 0 && dist[cur - m] == -1) {
            dist[cur - m] = d
            queue[tail] = cur - m
            tail += 1
        }
        if (x + 1 < n && grid[x + 1][y] == 0 && dist[cur + m] == -1) {
            dist[cur + m] = d
            queue[tail] = cur + m
            tail += 1
        }
        if (y > 0 && grid[x][y - 1] == 0 && dist[cur - 1] == -1) {
            dist[cur - 1] = d
            queue[tail] = cur - 1
            tail += 1
        }
        if (y + 1 < m && grid[x][y + 1] == 0 && dist[cur + 1] == -1) {
            dist[cur + 1] = d
            queue[tail] = cur + 1
            tail += 1
        }
    }
    return dist[total - 1]
}
