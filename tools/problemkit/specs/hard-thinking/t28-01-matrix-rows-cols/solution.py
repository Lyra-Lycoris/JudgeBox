def solve(n: int, m: int, r: list[int], c: list[int]) -> list[int]:
    SHIFT = 100000
    BIG = 99999
    rem = list(c)
    result = [0] * (n * m)
    row_keys = sorted(r[i] * SHIFT + (BIG - i) for i in range(n))
    for t in range(n - 1, -1, -1):
        key = row_keys[t]
        i = BIG - key % SHIFT
        need = key // SHIFT
        if need == 0:
            continue
        col_keys = [rem[j] * SHIFT + (BIG - j) for j in range(m)]
        col_keys.sort()
        base = i * m
        for p in range(need):
            ck = col_keys[m - 1 - p]
            j = BIG - ck % SHIFT
            result[base + j] = 1
            rem[j] -= 1
    return result
