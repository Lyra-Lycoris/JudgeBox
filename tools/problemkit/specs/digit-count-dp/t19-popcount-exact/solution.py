def solve(l: int, r: int, k: int) -> int:
    size = 62
    comb = [[0] * size for _ in range(size)]
    for i in range(size):
        comb[i][0] = 1
        for j in range(1, i + 1):
            comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j]

    def count_up_to(x: int) -> int:
        if x < 0 or k < 0:
            return 0
        res = 0
        used = 0
        ok = True
        for bit in range(60, -1, -1):
            if (x >> bit) & 1:
                need = k - used
                if 0 <= need <= bit:
                    res += comb[bit][need]
                used += 1
                if used > k:
                    ok = False
                    break
        if ok and used == k:
            res += 1
        return res

    return count_up_to(r) - count_up_to(l - 1)
