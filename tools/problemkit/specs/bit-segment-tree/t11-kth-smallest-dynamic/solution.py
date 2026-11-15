def solve(q: int, ops: list[list[int]]) -> list[int]:
    values = sorted({op[1] for op in ops if op[0] == 1})
    m = len(values)
    rank = {v: i + 1 for i, v in enumerate(values)}
    tree = [0] * (m + 1)

    highest = 0
    while (1 << (highest + 1)) <= m:
        highest += 1
    step0 = 1 << highest if m > 0 else 0

    answer = []
    for t, x in ops:
        if t == 1 or t == 2:
            i = rank[x]
            delta = 1 if t == 1 else -1
            while i <= m:
                tree[i] += delta
                i += i & -i
        else:
            k = x
            pos = 0
            step = step0
            while step:
                nxt = pos + step
                if nxt <= m and tree[nxt] < k:
                    pos = nxt
                    k -= tree[nxt]
                step >>= 1
            answer.append(values[pos])
    return answer
