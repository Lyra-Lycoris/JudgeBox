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

long long solve(long long n, long long m, const vector<vector<long long>>& g) {
    long long total = n * m;
    Dsu dsu((int)total);
    long long islands = 0;
    for (long long r = 0; r < n; ++r) {
        for (long long c = 0; c < m; ++c) {
            if (g[r][c] != 1) continue;
            ++islands;
            long long cur = r * m + c;
            if (r > 0 && g[r - 1][c] == 1) {
                if (dsu.unite((int)cur, (int)(cur - m))) --islands;
            }
            if (c > 0 && g[r][c - 1] == 1) {
                if (dsu.unite((int)cur, (int)(cur - 1))) --islands;
            }
        }
    }
    return islands;
}
