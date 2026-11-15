#include <bits/stdc++.h>
using namespace std;

static void sweepUpdate(int node, int left, int right, int ql, int qr, int delta,
                        vector<long long>& cover, vector<long long>& seglen,
                        const vector<long long>& ys) {
    if (qr <= left || right <= ql) return;
    if (ql <= left && right <= qr) {
        cover[node] += delta;
    } else {
        int mid = (left + right) >> 1;
        sweepUpdate(node << 1, left, mid, ql, qr, delta, cover, seglen, ys);
        sweepUpdate(node << 1 | 1, mid, right, ql, qr, delta, cover, seglen, ys);
    }
    if (cover[node] > 0) {
        seglen[node] = ys[right] - ys[left];
    } else if (right - left == 1) {
        seglen[node] = 0;
    } else {
        seglen[node] = seglen[node << 1] + seglen[node << 1 | 1];
    }
}

long long solve(long long n, const vector<vector<long long>>& rects) {
    vector<array<long long, 4>> events;
    events.reserve((size_t)(2 * n));
    vector<long long> ys;
    ys.reserve((size_t)(2 * n));
    for (long long i = 0; i < n; ++i) {
        long long x1 = rects[(size_t)i][0], y1 = rects[(size_t)i][1];
        long long x2 = rects[(size_t)i][2], y2 = rects[(size_t)i][3];
        events.push_back({x1, 1, y1, y2});
        events.push_back({x2, -1, y1, y2});
        ys.push_back(y1);
        ys.push_back(y2);
    }
    sort(ys.begin(), ys.end());
    ys.erase(unique(ys.begin(), ys.end()), ys.end());
    sort(events.begin(), events.end());

    int k = (int)ys.size();
    vector<long long> cover((size_t)(4 * k + 8), 0);
    vector<long long> seglen((size_t)(4 * k + 8), 0);

    long long total = 0;
    long long previous = events[0][0];
    for (const auto& e : events) {
        total += (e[0] - previous) * seglen[1];
        int ql = (int)(lower_bound(ys.begin(), ys.end(), e[2]) - ys.begin());
        int qr = (int)(lower_bound(ys.begin(), ys.end(), e[3]) - ys.begin());
        sweepUpdate(1, 0, k - 1, ql, qr, (int)e[1], cover, seglen, ys);
        previous = e[0];
    }
    return total;
}
