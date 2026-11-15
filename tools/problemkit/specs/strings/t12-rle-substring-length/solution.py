import bisect


def _cost(length: int) -> int:
    if length <= 1:
        return 1
    return 1 + len(str(length))


def solve(n: int, s: str, q: int, qs: list[list[int]]) -> list[int]:
    m = len(s)
    run_end = []
    prefix = [0]
    index = 0
    while index < m:
        j = index + 1
        while j < m and s[j] == s[index]:
            j += 1
        run_end.append(j)
        prefix.append(prefix[-1] + _cost(j - index))
        index = j
    answer = []
    for pair in qs:
        left = pair[0]
        right = pair[1]
        low = bisect.bisect_right(run_end, left - 1)
        high = bisect.bisect_right(run_end, right - 1)
        if low == high:
            answer.append(_cost(right - left + 1))
        else:
            total = _cost(run_end[low] - (left - 1))
            total += _cost(right - run_end[high - 1])
            total += prefix[high] - prefix[low + 1]
            answer.append(total)
    return answer
