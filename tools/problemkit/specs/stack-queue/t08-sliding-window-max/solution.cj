package t08_sliding_window_max

func solve(n: Int64, k: Int64, a: Array<Int64>): Array<Int64> {
    let window = Array<Int64>(n + 1, repeat: 0)
    var head = 0
    var tail = 0
    let answer = Array<Int64>(n - k + 1, repeat: 0)
    var count = 0
    for (i in 0..n) {
        while (tail > head && a[window[tail - 1]] <= a[i]) {
            tail -= 1
        }
        window[tail] = i
        tail += 1
        if (window[head] <= i - k) {
            head += 1
        }
        if (i >= k - 1) {
            answer[count] = a[window[head]]
            count += 1
        }
    }
    return answer
}
