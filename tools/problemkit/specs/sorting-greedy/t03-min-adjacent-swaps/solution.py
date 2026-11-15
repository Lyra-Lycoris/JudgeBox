def solve(n: int, a: list[int]) -> int:
    SHIFT = 1000000000
    BASE = 1 << 20
    keys = sorted((a[i] + SHIFT) * BASE + i for i in range(n))
    perm = [0] * n
    for p in range(n):
        perm[keys[p] % BASE] = p + 1
    tree = [0] * (n + 1)
    total = 0
    for i in range(n):
        v = perm[i]
        s = 0
        while v > 0:
            s += tree[v]
            v -= v & (-v)
        total += i - s
        v = perm[i]
        while v <= n:
            tree[v] += 1
            v += v & (-v)
    return total
