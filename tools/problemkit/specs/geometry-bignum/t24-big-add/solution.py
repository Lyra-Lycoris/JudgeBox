def solve(a: str, b: str) -> str:
    i = len(a) - 1
    j = len(b) - 1
    carry = 0
    digits = []
    while i >= 0 or j >= 0 or carry > 0:
        total = carry
        if i >= 0:
            total += ord(a[i]) - 48
            i -= 1
        if j >= 0:
            total += ord(b[j]) - 48
            j -= 1
        digits.append(chr(48 + total % 10))
        carry = total // 10
    digits.reverse()
    return "".join(digits)
