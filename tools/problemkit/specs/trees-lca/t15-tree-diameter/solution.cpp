#include <bits/stdc++.h>
using namespace std;

static int bfsFarthest(const vector<int>& head, const vector<int>& adj, int n, int src, vector<int>& dist) {
    for (int i = 0; i <= n; ++i) dist[i] = -1;
    vector<int> q(n + 1);
    int qh = 0, qt = 0;
    q[qt++] = src;
    dist[src] = 0;
    while (qh < qt) {
        int u = q[qh++];
        for (int i = head[u]; i < head[u + 1]; ++i) {
            int v = adj[i];
            if (dist[v] < 0) {
                dist[v] = dist[u] + 1;
                q[qt++] = v;
            }
        }
    }
    int far = src;
    for (int i = 1; i <= n; ++i) {
        if (dist[i] > dist[far]) far = i;
    }
    return far;
}

long long solve(long long n, const vector<long long>& e) {
    if (n <= 1) return 0;
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
    vector<int> dist(N + 1, -1);
    int a = bfsFarthest(head, adj, N, 1, dist);
    int b = bfsFarthest(head, adj, N, a, dist);
    return dist[b];
}
