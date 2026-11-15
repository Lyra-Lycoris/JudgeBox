def solve(n: int, a: list[int], b: list[int]) -> int:
    answer = 0
    prev_pos = 0
    prev_neg = 0
    for i in range(n):
        d = b[i] - a[i]
        pos = d if d > 0 else 0
        neg = -d if d < 0 else 0
        if pos > prev_pos:
            answer += pos - prev_pos
        if neg > prev_neg:
            answer += neg - prev_neg
        prev_pos = pos
        prev_neg = neg
    return answer
