def solve(n: int, m: int, cond: list[list[int]]) -> int:
    BITS = 60

    def count_upto(zero_mask: int, one_mask: int) -> int:
        """[0, n] 中同时满足「这些位必须为 0」「这些位必须为 1」的整数个数。"""
        if zero_mask & one_mask:
            return 0
        both = zero_mask | one_mask
        total = 0
        ok = True
        for i in range(BITS - 1, -1, -1):
            nb = (n >> i) & 1
            if (one_mask >> i) & 1:
                if nb == 0:
                    ok = False
                    break
            elif nb == 1:
                # 把这一位放 0，后面 i 位里没被限制的自由位可以任意取
                free = i - bin(both & ((1 << i) - 1)).count("1")
                total += 1 << free
                if (zero_mask >> i) & 1:
                    # 平走的分支要求这一位是 1，与「必须为 0」冲突
                    ok = False
                    break
        if ok:
            total += 1
        if one_mask == 0:
            total -= 1  # 去掉 x = 0
        return total

    groups = [0] * (m + 1)
    for mask in range(1, 1 << m):
        zero_mask = 0
        one_mask = 0
        size = 0
        for i in range(m):
            if (mask >> i) & 1:
                size += 1
                t, x = cond[i]
                if t == 1:
                    zero_mask |= x - 1  # k = 2^p 的倍数 <=> 低 p 位全 0
                else:
                    one_mask |= 1 << x
        if zero_mask & one_mask:
            continue
        groups[size] += count_upto(zero_mask, one_mask)

    answer = 0
    for size in range(1, m + 1):
        if size & 1:
            answer += groups[size]
        else:
            answer -= groups[size]
    return answer
