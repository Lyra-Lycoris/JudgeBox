def solve(n: int, k: int, a: list[int]) -> int:
    counts = {0: 1}
    prefix = 0
    answer = 0
    for x in a:
        prefix += x
        answer += counts.get(prefix - k, 0)
        counts[prefix] = counts.get(prefix, 0) + 1
    return answer
