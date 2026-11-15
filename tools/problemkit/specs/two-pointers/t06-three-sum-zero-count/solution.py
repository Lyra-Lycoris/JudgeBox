def solve(n: int, a: list[int]) -> int:
    b = sorted(a)
    count = 0
    for i in range(n - 2):
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = b[i] + b[lo] + b[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            elif b[lo] == b[hi]:
                m = hi - lo + 1
                count += m * (m - 1) // 2
                break
            else:
                low_count = 1
                while lo + low_count < hi and b[lo + low_count] == b[lo]:
                    low_count += 1
                high_count = 1
                while hi - high_count > lo and b[hi - high_count] == b[hi]:
                    high_count += 1
                count += low_count * high_count
                lo += low_count
                hi -= high_count
    return count
