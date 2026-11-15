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

long long solve(long long n, long long k, const vector<vector<long long>>& rel, long long q,
                const vector<vector<long long>>& qs) {
    Dsu dsu((int)n);
    for (long long i = 0; i < k; ++i) {
        dsu.unite((int)rel[i][0], (int)rel[i][1]);
    }
    long long answer = 0;
    for (long long i = 0; i < q; ++i) {
        if (dsu.find((int)qs[i][0]) == dsu.find((int)qs[i][1])) ++answer;
    }
    return answer;
}
