#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<vector<long long>>& g) {
    long long total = n * m;
    vector<int> cell(total);
    for (long long i = 0; i < n; ++i)
        for (long long j = 0; j < m; ++j) cell[i * m + j] = (int)g[i][j];
    const int INF = 1 << 30;
    vector<int> dist(total, INF);
    deque<int> dq;
    dist[0] = 0;
    dq.push_back(0);
    while (!dq.empty()) {
        int u = dq.front();
        dq.pop_front();
        int du = dist[u];
        int r = u / (int)m, c = u % (int)m;
        int count = 0;
        int nb[4];
        if (r > 0) nb[count++] = u - (int)m;
        if (r + 1 < n) nb[count++] = u + (int)m;
        if (c > 0) nb[count++] = u - 1;
        if (c + 1 < m) nb[count++] = u + 1;
        for (int k = 0; k < count; ++k) {
            int v = nb[k];
            int nd = du + cell[v];
            if (nd < dist[v]) {
                dist[v] = nd;
                if (cell[v] == 0) dq.push_front(v);
                else dq.push_back(v);
            }
        }
    }
    return dist[total - 1];
}
