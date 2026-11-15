def solve(m: int, nums: list[int], ops: list[str]) -> int:
    NEG = -4000000000000000000
    POS = 4000000000000000000
    mx = [[NEG] * m for _ in range(m)]
    mn = [[POS] * m for _ in range(m)]
    for i in range(m):
        mx[i][i] = nums[i]
        mn[i][i] = nums[i]
    for length in range(2, m + 1):
        for i in range(0, m - length + 1):
            j = i + length - 1
            for k in range(i, j):
                a1 = mx[i][k]
                a2 = mn[i][k]
                b1 = mx[k + 1][j]
                b2 = mn[k + 1][j]
                op = ops[k]
                if op == '+':
                    cands = (a1 + b1, a2 + b2)
                elif op == '-':
                    cands = (a1 - b2, a2 - b1)
                else:
                    cands = (a1 * b1, a1 * b2, a2 * b1, a2 * b2)
                for c in cands:
                    if c > mx[i][j]:
                        mx[i][j] = c
                    if c < mn[i][j]:
                        mn[i][j] = c
    return mx[0][m - 1]
