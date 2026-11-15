def solve(n: int, k: int, a: list[int]) -> int:
    if k <= 0:
        return n * (n + 1) // 2

    values = sorted(set(a))
    rank = {value: index + 1 for index, value in enumerate(values)}
    size = len(values)
    tree = [0] * (size + 1)

    answer = 0
    window_size = 0
    inversions = 0
    right = 0
    for left in range(n):
        while right < n and inversions < k:
            pos = rank[a[right]]
            count = 0
            i = pos
            while i > 0:
                count += tree[i]
                i -= i & -i
            inversions += window_size - count
            i = pos
            while i <= size:
                tree[i] += 1
                i += i & -i
            window_size += 1
            right += 1
        if inversions >= k:
            answer += n - right + 1
        pos = rank[a[left]]
        count = 0
        i = pos - 1
        while i > 0:
            count += tree[i]
            i -= i & -i
        inversions -= count
        i = pos
        while i <= size:
            tree[i] -= 1
            i += i & -i
        window_size -= 1
    return answer
