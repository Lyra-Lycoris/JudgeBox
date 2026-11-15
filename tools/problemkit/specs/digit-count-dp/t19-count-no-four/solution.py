def solve(l: int, r: int) -> int:
    def count_no_four(x: int) -> int:
        if x < 0:
            return 0
        digits = [int(ch) for ch in str(x)]
        length = len(digits)
        power = [1] * (length + 1)
        for i in range(1, length + 1):
            power[i] = power[i - 1] * 9
        total = 0
        for pos in range(length - 1, -1, -1):
            cur = digits[length - 1 - pos]
            smaller = 0
            for v in range(cur):
                if v != 4:
                    smaller += 1
            total += smaller * power[pos]
            if cur == 4:
                return total
        return total + 1

    return count_no_four(r) - count_no_four(l - 1)
