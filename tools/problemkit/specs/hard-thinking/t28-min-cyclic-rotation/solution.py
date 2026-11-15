def solve(n: int, a: list[int]) -> list[int]:
    i, j, k = 0, 1, 0
    while i < n and j < n and k < n:
        x = a[(i + k) % n]
        y = a[(j + k) % n]
        if x == y:
            k += 1
        elif x > y:
            i = i + k + 1
            if i == j:
                i += 1
            k = 0
        else:
            j = j + k + 1
            if i == j:
                j += 1
            k = 0
    s = i if i < j else j
    if s >= n:
        s = 0
    return a[s:] + a[:s]
