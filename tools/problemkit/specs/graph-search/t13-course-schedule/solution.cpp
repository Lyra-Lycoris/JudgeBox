#include <bits/stdc++.h>
using namespace std;

bool solve(long long n, long long m, const vector<vector<long long>>& e) {
    int N = (int) n;
    int M = (int) m;
    vector<int> deg(N + 1, 0), indeg(N + 1, 0), start(N + 2, 0);
    for (int i = 0; i < M; ++i) {
        int a = (int) e[i][0];
        int b = (int) e[i][1];
        ++deg[a];
        ++indeg[b];
    }
    for (int v = 1; v <= N; ++v) start[v + 1] = start[v] + deg[v];
    vector<int> cursor(start);
    vector<int> adj(M > 0 ? M : 1, 0);
    for (int i = 0; i < M; ++i) {
        int a = (int) e[i][0];
        int b = (int) e[i][1];
        adj[cursor[a]++] = b;
    }
    vector<int> queue(N);
    int head = 0, tail = 0;
    for (int v = 1; v <= N; ++v) {
        if (indeg[v] == 0) queue[tail++] = v;
    }
    long long seen = 0;
    while (head < tail) {
        int u = queue[head++];
        ++seen;
        for (int k = start[u]; k < start[u + 1]; ++k) {
            int b = adj[k];
            if (--indeg[b] == 0) queue[tail++] = b;
        }
    }
    return seen == n;
}
