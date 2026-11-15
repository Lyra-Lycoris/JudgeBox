    static void sweepUpdate(int node, int left, int right, int ql, int qr, long delta,
                            long[] cover, long[] seglen, long[] ys) {
        if (qr <= left || right <= ql) return;
        if (ql <= left && right <= qr) {
            cover[node] += delta;
        } else {
            int mid = (left + right) >>> 1;
            sweepUpdate(node << 1, left, mid, ql, qr, delta, cover, seglen, ys);
            sweepUpdate((node << 1) | 1, mid, right, ql, qr, delta, cover, seglen, ys);
        }
        if (cover[node] > 0) {
            seglen[node] = ys[right] - ys[left];
        } else if (right - left == 1) {
            seglen[node] = 0;
        } else {
            seglen[node] = seglen[node << 1] + seglen[(node << 1) | 1];
        }
    }

    static int sweepLowerBound(long[] arr, int len, long x) {
        int lo = 0, hi = len;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (arr[mid] < x) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    static long solve(long n, long[][] rects) {
        int sz = (int) n;
        int totalEvents = 2 * sz;
        long off = 1000000001L;
        long base = totalEvents + 1L;
        long[] keys = new long[totalEvents];
        long[] eY1 = new long[totalEvents];
        long[] eY2 = new long[totalEvents];
        long[] ys = new long[totalEvents];
        int idx = 0, yc = 0;
        for (int i = 0; i < sz; ++i) {
            long x1 = rects[i][0], y1 = rects[i][1], x2 = rects[i][2], y2 = rects[i][3];
            keys[idx] = ((((x1 + off) * 2) * base) + idx);
            eY1[idx] = y1;
            eY2[idx] = y2;
            idx++;
            keys[idx] = ((((x2 + off) * 2 + 1) * base) + idx);
            eY1[idx] = y1;
            eY2[idx] = y2;
            idx++;
            ys[yc++] = y1;
            ys[yc++] = y2;
        }
        Arrays.sort(keys);
        Arrays.sort(ys);
        int k = 0;
        for (int i = 0; i < yc; ++i) {
            if (i == 0 || ys[i] != ys[i - 1]) ys[k++] = ys[i];
        }
        long[] cover = new long[4 * k + 8];
        long[] seglen = new long[4 * k + 8];

        long total = 0;
        long previous = (keys[0] / base) / 2 - off;
        for (int t = 0; t < totalEvents; ++t) {
            long rest = keys[t] / base;
            int e = (int) (keys[t] % base);
            long type = rest & 1L;
            long x = rest / 2 - off;
            total += (x - previous) * seglen[1];
            int ql = sweepLowerBound(ys, k, eY1[e]);
            int qr = sweepLowerBound(ys, k, eY2[e]);
            sweepUpdate(1, 0, k - 1, ql, qr, type == 0 ? 1L : -1L, cover, seglen, ys);
            previous = x;
        }
        return total;
    }
