def solve(l: int, r: int) -> int:
    power = [1] * 17
    for i in range(1, 17):
        power[i] = power[i - 1] * 10
    suffix = [0] * 17
    for i in range(1, 17):
        suffix[i] = i * 45 * power[i - 1]

    def total_up_to(x: int) -> int:
        if x < 0:
            return 0
        digits = [int(ch) for ch in str(x)]
        length = len(digits)
        result = 0
        prefix = 0
        for pos in range(length - 1, -1, -1):
            cur = digits[length - 1 - pos]
            for v in range(cur):
                result += (prefix + v) * power[pos] + suffix[pos]
            prefix += cur
        return result + prefix

    return total_up_to(r) - total_up_to(l - 1)
