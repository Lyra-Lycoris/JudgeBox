def solve(n: int, w: list[list[int]]) -> list[int]:
    INF = 10 ** 18
    d = [[INF if x < 0 else x for x in row] for row in w]
    for i in range(n):
        d[i][i] = 0
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik >= INF:
                continue
            d[i] = [x if x <= dik + y else dik + y for x, y in zip(d[i], dk)]
    answer = []
    for row in d:
        for x in row:
            answer.append(-1 if x >= INF else x)
    return answer
