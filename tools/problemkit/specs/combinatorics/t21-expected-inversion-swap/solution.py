MOD = 1000000007


def solve(n: int, a: list[int]) -> int:
    if n < 2:
        return 0

    values = sorted(set(a))
    order = {v: i for i, v in enumerate(values)}
    ranks = [order[x] for x in a]
    m = len(values)

    cnt = [0] * m
    for r in ranks:
        cnt[r] += 1

    less_cnt = [0] * m
    running = 0
    for i in range(m):
        less_cnt[i] = running
        running += cnt[i]
    greater_cnt = [n - less_cnt[i] - cnt[i] for i in range(m)]

    tree = [0] * (m + 1)
    inv_count = 0
    k = 0
    for r in ranks:
        i = r + 1
        seen = 0
        while i:
            seen += tree[i]
            i &= i - 1
        inv_count += k - seen
        k += 1
        i = r + 1
        while i <= m:
            tree[i] += 1
            i += i & -i

    equal_pairs = 0
    for c in cnt:
        equal_pairs += c * (c - 1) // 2

    total_pairs = n * (n - 1) // 2
    untouched = (n - 2) * (n - 3) // 2

    total = untouched % MOD * (inv_count % MOD) % MOD
    total = (total + total_pairs - inv_count - equal_pairs) % MOD

    weighted = 0
    last = n - 1
    for k, r in enumerate(ranks):
        weighted += k * greater_cnt[r] + (last - k) * less_cnt[r]
    total = (total + weighted) % MOD

    total = (total - 2 * (inv_count % MOD)) % MOD
    return total * pow(total_pairs % MOD, MOD - 2, MOD) % MOD
