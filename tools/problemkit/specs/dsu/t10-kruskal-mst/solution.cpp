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

long long solve(long long n, long long m, const vector<vector<long long>>& e) {
    vector<int> order((size_t)m);
    for (long long i = 0; i < m; ++i) order[(size_t)i] = (int)i;
    sort(order.begin(), order.end(), [&](int a, int b) { return e[a][2] < e[b][2]; });

    Dsu dsu((int)n);
    long long total = 0;
    long long used = 0;
    for (long long t = 0; t < m; ++t) {
        int i = order[(size_t)t];
        if (dsu.unite((int)e[i][0], (int)e[i][1])) {
            total += e[i][2];
            ++used;
        }
    }
    if (used != n - 1) return -1;
    return total;
}
