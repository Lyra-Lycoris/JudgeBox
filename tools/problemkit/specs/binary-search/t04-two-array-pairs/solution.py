import bisect


def solve(n: int, a: list[int], m: int, b: list[int], x: int) -> int:
    c = sorted(b)
    ans = 0
    for v in a:
        ans += bisect.bisect_right(c, x - v)
    return ans
