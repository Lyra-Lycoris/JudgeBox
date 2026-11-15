#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<vector<long long>>& e) {
    vector<int> head(n + 1, -1), nxt(2 * m), to(2 * m);
    vector<long long> wt(2 * m);
    for (int i = 0; i < m; ++i) {
        int u = (int)e[i][0], v = (int)e[i][1];
        long long w = e[i][2];
        to[2 * i] = v; wt[2 * i] = w; nxt[2 * i] = head[u]; head[u] = 2 * i;
        to[2 * i + 1] = u; wt[2 * i + 1] = w; nxt[2 * i + 1] = head[v]; head[v] = 2 * i + 1;
    }
    const long long INF = (1LL << 62);
    vector<long long> d1(n + 1, INF), d2(n + 1, INF);
    d1[1] = 0;
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
    pq.push({0, 1});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > d2[u]) continue;
        for (int i = head[u]; i != -1; i = nxt[i]) {
            int v = to[i];
            long long nd = d + wt[i];
            if (nd < d1[v]) {
                d2[v] = d1[v];
                d1[v] = nd;
                pq.push({nd, v});
            } else if (nd > d1[v] && nd < d2[v]) {
                d2[v] = nd;
                pq.push({nd, v});
            }
        }
    }
    return d2[n] >= INF ? -1 : d2[n];
}
