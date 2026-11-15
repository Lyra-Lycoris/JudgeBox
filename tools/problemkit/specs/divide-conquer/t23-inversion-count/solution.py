def solve(n: int, a: list[int]) -> int:
    src = list(a)
    buf = [0] * n
    total = 0
    width = 1
    while width < n:
        i = 0
        while i < n:
            mid = min(i + width, n)
            hi = min(i + 2 * width, n)
            left, right, k = i, mid, i
            while left < mid and right < hi:
                if src[left] <= src[right]:
                    buf[k] = src[left]
                    left += 1
                else:
                    buf[k] = src[right]
                    right += 1
                    total += mid - left
                k += 1
            while left < mid:
                buf[k] = src[left]
                left += 1
                k += 1
            while right < hi:
                buf[k] = src[right]
                right += 1
                k += 1
            i += 2 * width
        src, buf = buf, src
        width *= 2
    return total
