def solve(n: int, a: list[int], m: int, queries: list[list[int]]) -> list[int]:
    values = sorted(set(a))
    rank = {v: i for i, v in enumerate(values)}
    uniq = len(values)

    depth = 1
    while (1 << depth) < uniq:
        depth += 1
    max_nodes = n * (depth + 1) + 2

    left_child = [0] * max_nodes
    right_child = [0] * max_nodes
    total = [0] * max_nodes
    root = [0] * (n + 1)
    nodes = 0

    for i in range(n):
        pos = rank[a[i]]
        prev = root[i]
        nodes += 1
        node = nodes
        total[node] = total[prev] + 1
        left_child[node] = left_child[prev]
        right_child[node] = right_child[prev]
        root[i + 1] = node

        lo, hi = 0, uniq - 1
        cur_new, cur_old = node, prev
        while lo < hi:
            mid = (lo + hi) >> 1
            nodes += 1
            child = nodes
            if pos <= mid:
                old_child = left_child[cur_old]
                total[child] = total[old_child] + 1
                left_child[child] = left_child[old_child]
                right_child[child] = right_child[old_child]
                left_child[cur_new] = child
                cur_new = child
                cur_old = old_child
                hi = mid
            else:
                old_child = right_child[cur_old]
                total[child] = total[old_child] + 1
                left_child[child] = left_child[old_child]
                right_child[child] = right_child[old_child]
                right_child[cur_new] = child
                cur_new = child
                cur_old = old_child
                lo = mid + 1

    answer = []
    for t in range(m):
        l, r, k = queries[t]
        root_r = root[r]
        root_l = root[l - 1]
        lo, hi = 0, uniq - 1
        while lo < hi:
            mid = (lo + hi) >> 1
            left_count = total[left_child[root_r]] - total[left_child[root_l]]
            if k <= left_count:
                root_r = left_child[root_r]
                root_l = left_child[root_l]
                hi = mid
            else:
                k -= left_count
                root_r = right_child[root_r]
                root_l = right_child[root_l]
                lo = mid + 1
        answer.append(values[lo])
    return answer
