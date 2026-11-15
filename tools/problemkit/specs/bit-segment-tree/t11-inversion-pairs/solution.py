def solve(n: int, a: list[int]) -> int:
    values = sorted(set(a))
    m = len(values)
    rank = {v: i + 1 for i, v in enumerate(values)}
    tree = [0] * (m + 1)
    answer = 0
    for k, x in enumerate(a):
        p = rank[x]
        not_greater = 0
        i = p
        while i > 0:
            not_greater += tree[i]
            i -= i & -i
        answer += k - not_greater
        i = p
        while i <= m:
            tree[i] += 1
            i += i & -i
    return answer
