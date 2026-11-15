def solve(n: int, a: list[int], q: int, queries: list[list[int]]) -> list[int]:
    lg = [0] * (n + 1)
    for i in range(2, n + 1):
        lg[i] = lg[i >> 1] + 1

    table = [a]
    j = 1
    while (1 << j) <= n:
        prev = table[-1]
        half = 1 << (j - 1)
        table.append([x if x >= y else y for x, y in zip(prev, prev[half:])])
        j += 1

    answer = []
    for l, r in queries:
        level = lg[r - l + 1]
        row = table[level]
        x = row[l - 1]
        y = row[r - (1 << level)]
        answer.append(x if x >= y else y)
    return answer
