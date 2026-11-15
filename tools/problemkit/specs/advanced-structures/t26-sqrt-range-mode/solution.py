from bisect import bisect_left, bisect_right


def solve(n: int, a: list[int], q: int, ops: list[list[int]]) -> list[int]:
    values = sorted(set(a))
    index = {v: i for i, v in enumerate(values)}
    comp = [index[v] for v in a]
    m = len(values)

    pos = [[] for _ in range(m)]
    for i, v in enumerate(comp):
        pos[v].append(i)

    # 块大小在「预处理 O(n^2/B)」与「询问 O(qB)」之间取平衡。
    B = max(1, int(0.4 * n / (q ** 0.5)))
    nb = (n + B - 1) // B

    # table_c[s][t] / table_v[s][t]: 第 s 块到第 t 块（完整块）的众数出现次数与取值下标
    table_c = [[0] * nb for _ in range(nb)]
    table_v = [[-1] * nb for _ in range(nb)]
    for s in range(nb):
        cnt = [0] * m
        row_c = table_c[s]
        row_v = table_v[s]
        bc = 0
        bv = -1
        start = s * B
        for j in range(s, nb):
            end = (j + 1) * B
            if end > n:
                end = n
            for i in range(start, end):
                v = comp[i]
                c = cnt[v] + 1
                cnt[v] = c
                if c > bc or (c == bc and v < bv):
                    bc = c
                    bv = v
            row_c[j] = bc
            row_v[j] = bv
            start = end

    bl_ = bisect_left
    br_ = bisect_right
    answer = []
    for t in range(q):
        l = ops[t][0] - 1
        r = ops[t][1] - 1
        bl = l // B
        br = r // B
        if bl == br:
            d = {}
            bc = 0
            bv = -1
            for i in range(l, r + 1):
                v = comp[i]
                c = d.get(v, 0) + 1
                d[v] = c
                if c > bc or (c == bc and v < bv):
                    bc = c
                    bv = v
        else:
            if bl + 1 < br:
                bc = table_c[bl + 1][br - 1]
                bv = table_v[bl + 1][br - 1]
            else:
                bc = 0
                bv = -1
            end = (bl + 1) * B
            for i in range(l, end):
                v = comp[i]
                p = pos[v]
                c = br_(p, r) - bl_(p, l)
                if c > bc or (c == bc and v < bv):
                    bc = c
                    bv = v
            for i in range(br * B, r + 1):
                v = comp[i]
                p = pos[v]
                c = br_(p, r) - bl_(p, l)
                if c > bc or (c == bc and v < bv):
                    bc = c
                    bv = v
        answer.append(values[bv])
    return answer
