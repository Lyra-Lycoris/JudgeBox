import bisect


def _kth(a: list[int], b: list[int], t: int) -> int:
    lo, hi = -1000000001, 1000000001
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if bisect.bisect_right(a, mid) + bisect.bisect_right(b, mid) >= t:
            hi = mid
        else:
            lo = mid + 1
    return lo


def solve(n: int, a: list[int], m: int, b: list[int]) -> int:
    total = n + m
    return _kth(a, b, (total + 1) // 2) + _kth(a, b, (total + 2) // 2)
