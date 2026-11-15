#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& e) {
    if (n == 1) return 1;
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

    vector<int> parent(N + 1, 1), order(N, 0);
    vector<char> visited(N + 1, 0);
    int cnt = 0;
    order[cnt++] = 1;
    visited[1] = 1;
    for (int i = 0; i < cnt; ++i) {
        int u = order[i];
        for (int j = head[u]; j < head[u + 1]; ++j) {
            int v = adj[j];
            if (!visited[v]) {
                visited[v] = 1;
                parent[v] = u;
                order[cnt++] = v;
            }
        }
    }

    vector<long long> size(N + 1, 1);
    for (int i = N - 1; i > 0; --i) {
        int v = order[i];
        size[parent[v]] += size[v];
    }
    vector<long long> maxPart(N + 1, 0);
    for (int v = 1; v <= N; ++v) maxPart[v] = n - size[v];
    for (int i = 1; i < N; ++i) {
        int v = order[i], p = parent[v];
        if (size[v] > maxPart[p]) maxPart[p] = size[v];
    }
    for (int v = 1; v <= N; ++v) {
        if (maxPart[v] * 2 <= n) return v;
    }
    return 1;
}
