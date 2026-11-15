def solve(n: int, target: int, a: list[int]) -> int:
    i, j = 0, n - 1
    count = 0
    while i < j:
        total = a[i] + a[j]
        if total < target:
            i += 1
        elif total > target:
            j -= 1
        else:
            if a[i] == a[j]:
                m = j - i + 1
                count += m * (m - 1) // 2
                break
            left_count = 1
            while i + left_count < j and a[i + left_count] == a[i]:
                left_count += 1
            right_count = 1
            while j - right_count > i and a[j - right_count] == a[j]:
                right_count += 1
            count += left_count * right_count
            i += left_count
            j -= right_count
    return count
