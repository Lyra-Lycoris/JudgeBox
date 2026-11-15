def solve(l: int, r: int, k: int) -> int:
    cnt = [[0] * 10 for _ in range(19)]
    for last in range(10):
        cnt[0][last] = 1
    for rem in range(1, 19):
        for last in range(10):
            total = 0
            for v in range(10):
                if abs(v - last) <= k:
                    total += cnt[rem - 1][v]
            cnt[rem][last] = total

    def count_up_to(x: int) -> int:
        if x <= 0:
            return 0
        digits = [int(ch) for ch in str(x)]
        length = len(digits)
        res = 0
        for shorter in range(1, length):
            for first in range(1, 10):
                res += cnt[shorter - 1][first]
        for pos in range(length - 1, -1, -1):
            cur = digits[length - 1 - pos]
            lo = 1 if pos == length - 1 else 0
            for v in range(lo, cur):
                if pos < length - 1 and abs(v - digits[length - 1 - pos - 1]) > k:
                    continue
                res += cnt[pos][v]
            if pos < length - 1 and abs(cur - digits[length - 1 - pos - 1]) > k:
                return res
        return res + 1

    return count_up_to(r) - count_up_to(l - 1)
