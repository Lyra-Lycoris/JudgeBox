def solve(n: int, begin: str, end: str, w: list[str]) -> int:
    if begin == end:
        return 1
    target = -1
    for i in range(n):
        if w[i] == end:
            target = i
            break
    if target < 0:
        return 0
    bidx = -1
    for i in range(n):
        if w[i] == begin:
            bidx = i
            break

    buckets = {}
    for i in range(n):
        word = w[i]
        for j in range(len(word)):
            key = word[:j] + "*" + word[j + 1:]
            group = buckets.get(key)
            if group is None:
                buckets[key] = [i]
            else:
                group.append(i)

    dist = [-1] * (n + 1)
    dist[n] = 1
    if bidx >= 0:
        dist[bidx] = 1
    queue = [n]
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        step = dist[u] + 1
        word = begin if u == n else w[u]
        for j in range(len(word)):
            key = word[:j] + "*" + word[j + 1:]
            group = buckets.pop(key, None)
            if group is None:
                continue
            for v in group:
                if dist[v] != -1:
                    continue
                dist[v] = step
                if v == target:
                    return step
                queue.append(v)
    return 0
