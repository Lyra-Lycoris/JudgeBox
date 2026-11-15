#include <bits/stdc++.h>
using namespace std;

struct Dsu {
    vector<int> parent, rk;

    explicit Dsu(int n) : parent(n + 1), rk(n + 1, 0) {
        for (int i = 0; i <= n; ++i) parent[i] = i;
    }

    int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (rk[a] < rk[b]) swap(a, b);
        parent[b] = a;
        if (rk[a] == rk[b]) ++rk[a];
        return true;
    }
};

bool solve(long long n, long long k, const vector<vector<long long>>& cons) {
    Dsu dsu((int)n);
    for (long long i = 0; i < k; ++i) {
        if (cons[i][0] == 0) dsu.unite((int)cons[i][1], (int)cons[i][2]);
    }

    int nn = (int)n;
    vector<int> id(nn + 1, -1);
    int cnt = 0;
    for (int v = 1; v <= nn; ++v) {
        int r = dsu.find(v);
        if (id[r] < 0) id[r] = cnt++;
    }

    vector<vector<int>> adj(cnt);
    vector<int> indeg(cnt, 0);
    for (long long i = 0; i < k; ++i) {
        if (cons[i][0] != 1) continue;
        int u = id[dsu.find((int)cons[i][1])];
        int v = id[dsu.find((int)cons[i][2])];
        if (u == v) return false;
        adj[u].push_back(v);
        ++indeg[v];
    }

    vector<int> order(cnt);
    int head = 0, tail = 0;
    for (int i = 0; i < cnt; ++i) {
        if (indeg[i] == 0) order[tail++] = i;
    }
    int seen = 0;
    while (head < tail) {
        int u = order[head++];
        ++seen;
        for (int v : adj[u]) {
            if (--indeg[v] == 0) order[tail++] = v;
        }
    }
    return seen == cnt;
}
