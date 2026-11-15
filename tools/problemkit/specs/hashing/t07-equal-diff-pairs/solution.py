def solve(n: int, a: list[int]) -> int:
    diff_counts = {}
    sum_counts = {}
    answer = 0
    for i, value in enumerate(a):
        index = i + 1
        key = value - index
        answer += diff_counts.get(key, 0)
        diff_counts[key] = diff_counts.get(key, 0) + 1
        key = value + index
        answer += sum_counts.get(key, 0)
        sum_counts[key] = sum_counts.get(key, 0) + 1
    return answer
