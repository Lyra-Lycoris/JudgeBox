def solve(n: int, m: int, r: list[int], c: list[int]) -> list[int]:
    row = list(r)
    col = list(c)
    out = []
    for i in range(n):
        for j in range(m):
            x = row[i] if row[i] < col[j] else col[j]
            out.append(x)
            row[i] -= x
            col[j] -= x
    return out
