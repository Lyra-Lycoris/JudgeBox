#include <bits/stdc++.h>
using namespace std;

bool solve(long long n, long long m, long long s, const vector<vector<long long>>& e) {
    const long long INF = (1LL << 62);
    vector<long long> dist(n + 1, INF);
    dist[s] = 0;
    for (long long round = 0; round < n; ++round) {
        bool changed = false;
        for (long long i = 0; i < m; ++i) {
            long long u = e[i][0], v = e[i][1], w = e[i][2];
            if (dist[u] >= INF) continue;
            long long nd = dist[u] + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                changed = true;
            }
        }
        if (!changed) return false;
    }
    return true;
}
