def solve(n: int, rects: list[list[int]]) -> int:
    events = []
    ys = []
    for x1, y1, x2, y2 in rects:
        events.append((x1, 1, y1, y2))
        events.append((x2, -1, y1, y2))
        ys.append(y1)
        ys.append(y2)

    ys = sorted(set(ys))
    index = {y: i for i, y in enumerate(ys)}
    events.sort()

    k = len(ys)
    cover = [0] * (4 * k + 8)
    seglen = [0] * (4 * k + 8)

    def update(node, left, right, ql, qr, delta):
        if qr <= left or right <= ql:
            return
        if ql <= left and right <= qr:
            cover[node] += delta
        else:
            mid = (left + right) >> 1
            update(node << 1, left, mid, ql, qr, delta)
            update(node << 1 | 1, mid, right, ql, qr, delta)
        if cover[node] > 0:
            seglen[node] = ys[right] - ys[left]
        elif right - left == 1:
            seglen[node] = 0
        else:
            seglen[node] = seglen[node << 1] + seglen[node << 1 | 1]

    total = 0
    previous = events[0][0]
    for x, delta, y1, y2 in events:
        total += (x - previous) * seglen[1]
        update(1, 0, k - 1, index[y1], index[y2], delta)
        previous = x
    return total
