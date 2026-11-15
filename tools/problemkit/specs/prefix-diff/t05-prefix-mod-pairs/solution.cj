package t05_prefix_mod_pairs

import std.sort.*

func solve(n: Int64, a: Array<Int64>, k: Int64): Int64 {
    let rems = Array<Int64>(n + 1, repeat: 0)
    var cur: Int64 = 0
    for (i in 0..n) {
        cur = (cur + a[i]) % k
        if (cur < 0) {
            cur = cur + k
        }
        rems[i + 1] = cur
    }
    sort(rems)
    var answer: Int64 = 0
    var run: Int64 = 1
    for (i in 1..n + 1) {
        if (rems[i] == rems[i - 1]) {
            run = run + 1
        } else {
            answer = answer + run * (run - 1) / 2
            run = 1
        }
    }
    answer = answer + run * (run - 1) / 2
    return answer
}
