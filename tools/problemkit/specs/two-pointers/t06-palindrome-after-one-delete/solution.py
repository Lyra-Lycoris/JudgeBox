def is_palindrome_range(s: str, left: int, right: int) -> bool:
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


def solve(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] == s[right]:
            left += 1
            right -= 1
        else:
            return is_palindrome_range(s, left + 1, right) or is_palindrome_range(s, left, right - 1)
    return True
