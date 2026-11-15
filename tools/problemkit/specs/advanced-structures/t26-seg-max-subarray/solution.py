def solve(n: int, a: list[int], q: int, ops: list[list[int]]) -> list[int]:
    NEG = -(1 << 62)
    size = 1
    while size < n:
        size <<= 1

    tot = [0] * (size << 1)
    pre = [NEG] * (size << 1)
    suf = [NEG] * (size << 1)
    bst = [NEG] * (size << 1)
    for i in range(n):
        k = size + i
        v = a[i]
        tot[k] = v
        pre[k] = v
        suf[k] = v
        bst[k] = v

    for k in range(size - 1, 0, -1):
        lc = k << 1
        rc = lc | 1
        tot[k] = tot[lc] + tot[rc]
        x = pre[lc]
        y = tot[lc] + pre[rc]
        pre[k] = x if x > y else y
        x = suf[rc]
        y = tot[rc] + suf[lc]
        suf[k] = x if x > y else y
        x = bst[lc]
        if bst[rc] > x:
            x = bst[rc]
        y = suf[lc] + pre[rc]
        if y > x:
            x = y
        bst[k] = x

    answer = []
    for ql, qr in ops:
        l = size + ql - 1
        r = size + qr
        ls = 0
        lp = NEG
        lsf = NEG
        lb = NEG
        rs = 0
        rp = NEG
        rsf = NEG
        rb = NEG
        while l < r:
            if l & 1:
                ns = ls + tot[l]
                p = ls + pre[l]
                if lp > p:
                    p = lp
                s = suf[l]
                alt = tot[l] + lsf
                if alt > s:
                    s = alt
                b = lb
                if bst[l] > b:
                    b = bst[l]
                cross = lsf + pre[l]
                if cross > b:
                    b = cross
                ls, lp, lsf, lb = ns, p, s, b
                l += 1
            if r & 1:
                r -= 1
                ns = tot[r] + rs
                p = pre[r]
                alt = tot[r] + rp
                if alt > p:
                    p = alt
                s = rs + suf[r]
                if rsf > s:
                    s = rsf
                b = bst[r]
                if rb > b:
                    b = rb
                cross = suf[r] + rp
                if cross > b:
                    b = cross
                rs, rp, rsf, rb = ns, p, s, b
            l >>= 1
            r >>= 1
        b = lb
        if rb > b:
            b = rb
        cross = lsf + rp
        if cross > b:
            b = cross
        answer.append(b)
    return answer
