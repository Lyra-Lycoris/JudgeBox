def solve(n: int, a: list[int], q: int, ops: list[list[int]]) -> list[int]:
    NEG = -(1 << 62)
    size = 1
    while size < n:
        size <<= 1

    mx = [NEG] * (2 * size)
    lz = [0] * (2 * size)
    for i in range(n):
        mx[size + i] = a[i]
    for i in range(size - 1, 0, -1):
        x = mx[i + i]
        y = mx[i + i + 1]
        mx[i] = x if x > y else y

    def add(k, nl, nr, ql, qr, v):
        if qr <= nl or nr <= ql:
            return
        if ql <= nl and nr <= qr:
            mx[k] += v
            lz[k] += v
            return
        mid = (nl + nr) >> 1
        c = k + k
        add(c, nl, mid, ql, qr, v)
        add(c + 1, mid, nr, ql, qr, v)
        x = mx[c]
        y = mx[c + 1]
        mx[k] = (x if x > y else y) + lz[k]

    def query(k, nl, nr, ql, qr, acc):
        if qr <= nl or nr <= ql:
            return NEG
        if ql <= nl and nr <= qr:
            return mx[k] + acc
        acc += lz[k]
        mid = (nl + nr) >> 1
        c = k + k
        x = query(c, nl, mid, ql, qr, acc)
        y = query(c + 1, mid, nr, ql, qr, acc)
        return x if x > y else y

    answer = []
    for t, l, r, x in ops:
        if t == 1:
            add(1, 0, size, l - 1, r, x)
        else:
            answer.append(query(1, 0, size, l - 1, r, 0))
    return answer
