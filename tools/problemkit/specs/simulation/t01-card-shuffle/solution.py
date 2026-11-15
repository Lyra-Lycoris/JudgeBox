def solve(n: int, k: int, p: list[int]) -> list[int]:
    perm = [value - 1 for value in p]
    answer = [0] * n
    visited = [False] * n
    for start in range(n):
        if visited[start]:
            continue
        cycle = []
        current = start
        while not visited[current]:
            visited[current] = True
            cycle.append(current)
            current = perm[current]
        length = len(cycle)
        shift = k % length
        for j in range(length):
            answer[cycle[j]] = cycle[(j - shift) % length] + 1
    return answer
