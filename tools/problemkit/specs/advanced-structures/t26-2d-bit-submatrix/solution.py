def solve(n: int, m: int, a: list[list[int]], q: int, ops: list[list[int]]) -> list[int]:
    pre = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        row = a[i - 1]
        pi = pre[i]
        pj = pre[i - 1]
        s = 0
        for j in range(1, m + 1):
            s += row[j - 1]
            pi[j] = pj[j] + s

    bit = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        li = i - (i & -i)
        bi = bit[i]
        pi = pre[i]
        pli = pre[li]
        for j in range(1, m + 1):
            lj = j - (j & -j)
            bi[j] = pi[j] - pli[j] - pi[lj] + pli[lj]

    def prefix(x, y):
        s = 0
        i = x
        while i > 0:
            bi = bit[i]
            j = y
            while j > 0:
                s += bi[j]
                j -= j & -j
            i -= i & -i
        return s

    answer = []
    for op in ops:
        t = op[0]
        x = op[1]
        y = op[2]
        if t == 1:
            v = op[3]
            i = x
            while i <= n:
                bi = bit[i]
                j = y
                while j <= m:
                    bi[j] += v
                    j += j & -j
                i += i & -i
        else:
            x2 = op[3]
            y2 = op[4]
            answer.append(prefix(x2, y2) - prefix(x - 1, y2)
                          - prefix(x2, y - 1) + prefix(x - 1, y - 1))
    return answer
