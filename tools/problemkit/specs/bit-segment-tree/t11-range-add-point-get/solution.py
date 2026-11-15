def solve(n: int, a: list[int], q: int, ops: list[list[int]]) -> list[int]:
    tree = [0] * (n + 2)
    answer = []
    for t, l, r, v in ops:
        if t == 1:
            i = l
            while i <= n:
                tree[i] += v
                i += i & -i
            i = r + 1
            while i <= n:
                tree[i] -= v
                i += i & -i
        else:
            s = 0
            i = l
            while i > 0:
                s += tree[i]
                i -= i & -i
            answer.append(a[l - 1] + s)
    return answer
