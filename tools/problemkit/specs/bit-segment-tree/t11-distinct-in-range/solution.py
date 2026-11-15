def solve(n: int, a: list[int], q: int, queries: list[list[int]]) -> list[int]:
    head = [-1] * (n + 1)
    nxt = [-1] * q
    for j, (l, r) in enumerate(queries):
        nxt[j] = head[r]
        head[r] = j

    tree = [0] * (n + 1)
    last = {}
    answer = [0] * q

    for r in range(1, n + 1):
        x = a[r - 1]
        old = last.get(x, 0)
        if old:
            i = old
            while i <= n:
                tree[i] -= 1
                i += i & -i
        last[x] = r
        i = r
        while i <= n:
            tree[i] += 1
            i += i & -i

        upto = 0
        i = r
        while i > 0:
            upto += tree[i]
            i -= i & -i

        j = head[r]
        while j != -1:
            s = 0
            i = queries[j][0] - 1
            while i > 0:
                s += tree[i]
                i -= i & -i
            answer[j] = upto - s
            j = nxt[j]

    return answer
