def solve(n: int, a: list[int], q: int, ops: list[list[int]]) -> list[int]:
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        tree[i] += a[i - 1]
        up = i + (i & -i)
        if up <= n:
            tree[up] += tree[i]

    answer = []
    for t, x, y in ops:
        if t == 1:
            i = x
            while i <= n:
                tree[i] += y
                i += i & -i
        else:
            s = 0
            i = y
            while i > 0:
                s += tree[i]
                i -= i & -i
            i = x - 1
            while i > 0:
                s -= tree[i]
                i -= i & -i
            answer.append(s)
    return answer
