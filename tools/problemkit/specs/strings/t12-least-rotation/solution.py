def solve(n: int, s: str) -> int:
    m = len(s)
    if m <= 1:
        return 0
    doubled = s + s
    i, j, k = 0, 1, 0
    while i < m and j < m and k < m:
        a = doubled[i + k]
        b = doubled[j + k]
        if a == b:
            k += 1
        elif a > b:
            i = i + k + 1
            if i <= j:
                i = j + 1
            k = 0
        else:
            j = j + k + 1
            if j <= i:
                j = i + 1
            k = 0
    return min(i, j)
