#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long m, long long s, const vector<vector<long long>>& e) {
    vector<int> head(n + 1, -1), nxt(m), to(m);
    vector<long long> wt(m);
    for (int i = 0; i < m; ++i) {
        int u = (int)e[i][0];
        to[i] = (int)e[i][1];
        wt[i] = e[i][2];
        nxt[i] = head[u];
        head[u] = i;
    }
    const long long INF = (1LL << 62);
    vector<long long> dist(n + 1, INF);
    dist[s] = 0;
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
    pq.push({0, (int)s});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue;
        for (int i = head[u]; i != -1; i = nxt[i]) {
            int v = to[i];
            long long nd = d + wt[i];
            if (nd < dist[v]) {
                dist[v] = nd;
                pq.push({nd, v});
            }
        }
    }
    vector<long long> answer(n);
    for (long long i = 1; i <= n; ++i) answer[i - 1] = dist[i] >= INF ? -1 : dist[i];
    return answer;
}
