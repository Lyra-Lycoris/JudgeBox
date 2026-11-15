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

bool solve(long long n, long long m, const vector<vector<long long>>& e) {
    Dsu dsu((int)n);
    for (long long i = 0; i < m; ++i) {
        if (!dsu.unite((int)e[i][0], (int)e[i][1])) return true;
    }
    return false;
}
