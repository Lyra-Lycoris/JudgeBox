def solve(n: int, a: list[int], q: int, ops: list[list[int]]) -> list[int]:
    size = 1
    level = 0
    while size < n:
        size <<= 1
        level += 1

    total = [0] * (size << 1)
    lazy = [None] * size
    total[size:size + n] = a
    for i in range(size - 1, 0, -1):
        total[i] = total[i << 1] + total[i << 1 | 1]

    answer = []
    for left, right, value in ops:
        l = left - 1 + size
        r = right + size
        l0 = l
        r0 = r

        # 把两条边界路径上的标记推下去
        for i in range(level, 0, -1):
            if (l0 >> i) << i != l0:
                k = l0 >> i
                t = lazy[k]
                if t is not None:
                    c = k << 1
                    total[c] = t * (size >> (c.bit_length() - 1))
                    if c < size:
                        lazy[c] = t
                    c += 1
                    total[c] = t * (size >> (c.bit_length() - 1))
                    if c < size:
                        lazy[c] = t
                    lazy[k] = None
            if (r0 >> i) << i != r0:
                k = (r0 - 1) >> i
                t = lazy[k]
                if t is not None:
                    c = k << 1
                    total[c] = t * (size >> (c.bit_length() - 1))
                    if c < size:
                        lazy[c] = t
                    c += 1
                    total[c] = t * (size >> (c.bit_length() - 1))
                    if c < size:
                        lazy[c] = t
                    lazy[k] = None

        # 区间赋值
        while l < r:
            if l & 1:
                total[l] = value * (size >> (l.bit_length() - 1))
                if l < size:
                    lazy[l] = value
                l += 1
            if r & 1:
                r -= 1
                total[r] = value * (size >> (r.bit_length() - 1))
                if r < size:
                    lazy[r] = value
            l >>= 1
            r >>= 1

        # 自底向上重算边界路径
        for i in range(1, level + 1):
            if (l0 >> i) << i != l0:
                k = l0 >> i
                total[k] = total[k << 1] + total[k << 1 | 1]
            if (r0 >> i) << i != r0:
                k = (r0 - 1) >> i
                total[k] = total[k << 1] + total[k << 1 | 1]

        answer.append(total[1])
    return answer
