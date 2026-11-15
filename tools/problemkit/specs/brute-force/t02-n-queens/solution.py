def solve(n: int) -> int:
    col = [False] * n
    d1 = [False] * (2 * n)
    d2 = [False] * (2 * n)

    def dfs(row: int) -> int:
        if row == n:
            return 1
        total = 0
        for c in range(n):
            a = row + c
            b = row - c + n
            if col[c] or d1[a] or d2[b]:
                continue
            col[c] = d1[a] = d2[b] = True
            total += dfs(row + 1)
            col[c] = d1[a] = d2[b] = False
        return total

    return dfs(0)
