#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& e, long long q,
                        const vector<long long>& queries) {
    int N = (int)n;
    int m = (int)e.size() / 2;
    vector<int> deg(N + 2, 0);
    for (int i = 0; i < m; ++i) {
        deg[(int)e[2 * i]]++;
        deg[(int)e[2 * i + 1]]++;
    }
    vector<int> head(N + 2, 0);
    for (int i = 1; i <= N; ++i) head[i + 1] = head[i] + deg[i];
    vector<int> adj(2 * m);
    vector<int> pos = head;
    for (int i = 0; i < m; ++i) {
        int u = (int)e[2 * i], v = (int)e[2 * i + 1];
        adj[pos[u]++] = v;
        adj[pos[v]++] = u;
    }

    vector<int> parent(N + 1, 1), depth(N + 1, 0);
    vector<char> visited(N + 1, 0);
    vector<int> queue(N + 1);
    int qh = 0, qt = 0;
    queue[qt++] = 1;
    visited[1] = 1;
    while (qh < qt) {
        int u = queue[qh++];
        for (int i = head[u]; i < head[u + 1]; ++i) {
            int v = adj[i];
            if (!visited[v]) {
                visited[v] = 1;
                parent[v] = u;
                depth[v] = depth[u] + 1;
                queue[qt++] = v;
            }
        }
    }

    int LOG = 1;
    while ((1 << LOG) <= N) ++LOG;
    vector<vector<int>> up(LOG, vector<int>(N + 1, 1));
    for (int v = 1; v <= N; ++v) up[0][v] = parent[v];
    for (int k = 1; k < LOG; ++k)
        for (int v = 1; v <= N; ++v) up[k][v] = up[k - 1][up[k - 1][v]];

    vector<long long> answer(q, 0);
    for (long long t = 0; t < q; ++t) {
        int u = (int)queries[2 * t], v = (int)queries[2 * t + 1];
        int du = depth[u], dv = depth[v];
        int a = u, b = v;
        if (depth[a] < depth[b]) swap(a, b);
        int diff = depth[a] - depth[b];
        for (int k = 0; k < LOG; ++k)
            if ((diff >> k) & 1) a = up[k][a];
        if (a != b) {
            for (int k = LOG - 1; k >= 0; --k) {
                if (up[k][a] != up[k][b]) {
                    a = up[k][a];
                    b = up[k][b];
                }
            }
            a = up[0][a];
        }
        answer[t] = (long long)du + dv - 2LL * depth[a];
    }
    return answer;
}
