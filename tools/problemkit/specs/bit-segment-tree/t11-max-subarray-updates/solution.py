def solve(n: int, a: list[int], q: int, ops: list[list[int]]) -> list[int]:
    NEG = -(1 << 62)
    size = 1
    while size < n:
        size <<= 1

    total = [0] * (size << 1)
    pref = [NEG] * (size << 1)
    suff = [NEG] * (size << 1)
    best = [NEG] * (size << 1)

    for i in range(n):
        k = size + i
        v = a[i]
        total[k] = v
        pref[k] = v
        suff[k] = v
        best[k] = v

    for k in range(size - 1, 0, -1):
        lc = k << 1
        rc = lc | 1
        total[k] = total[lc] + total[rc]
        x = pref[lc]
        y = total[lc] + pref[rc]
        pref[k] = x if x >= y else y
        x = suff[rc]
        y = total[rc] + suff[lc]
        suff[k] = x if x >= y else y
        b = best[lc]
        if best[rc] > b:
            b = best[rc]
        cross = suff[lc] + pref[rc]
        if cross > b:
            b = cross
        best[k] = b

    answer = []
    for t, x, y in ops:
        if t == 1:
            k = size + x - 1
            total[k] = y
            pref[k] = y
            suff[k] = y
            best[k] = y
            k >>= 1
            while k:
                lc = k << 1
                rc = lc | 1
                total[k] = total[lc] + total[rc]
                p = pref[lc]
                alt = total[lc] + pref[rc]
                if alt > p:
                    p = alt
                pref[k] = p
                s = suff[rc]
                alt = total[rc] + suff[lc]
                if alt > s:
                    s = alt
                suff[k] = s
                b = best[lc]
                if best[rc] > b:
                    b = best[rc]
                cross = suff[lc] + pref[rc]
                if cross > b:
                    b = cross
                best[k] = b
                k >>= 1
        else:
            l = size + x - 1
            r = size + y
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
                    nsum = ls + total[l]
                    p = lp
                    alt = ls + pref[l]
                    if alt > p:
                        p = alt
                    s = suff[l]
                    alt = total[l] + lsf
                    if alt > s:
                        s = alt
                    b = lb
                    if best[l] > b:
                        b = best[l]
                    cross = lsf + pref[l]
                    if cross > b:
                        b = cross
                    ls, lp, lsf, lb = nsum, p, s, b
                    l += 1
                if r & 1:
                    r -= 1
                    nsum = total[r] + rs
                    p = pref[r]
                    alt = total[r] + rp
                    if alt > p:
                        p = alt
                    s = rsf
                    alt = rs + suff[r]
                    if alt > s:
                        s = alt
                    b = best[r]
                    if rb > b:
                        b = rb
                    cross = suff[r] + rp
                    if cross > b:
                        b = cross
                    rs, rp, rsf, rb = nsum, p, s, b
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
