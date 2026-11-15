#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<vector<long long>>& e) {
    vector<int> parent(n + 1);
    for (int i = 0; i <= n; ++i) parent[i] = i;
    function<int(int)> find = [&](int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    };
    vector<int> order(m);
    for (int i = 0; i < m; ++i) order[i] = i;
    sort(order.begin(), order.end(), [&](int a, int b) { return e[a][2] < e[b][2]; });
    long long total = 0, used = 0;
    for (int k = 0; k < m && used < n - 1; ++k) {
        int i = order[k];
        int u = (int)e[i][0], v = (int)e[i][1];
        int ru = find(u), rv = find(v);
        if (ru != rv) {
            parent[ru] = rv;
            total += e[i][2];
            ++used;
        }
    }
    return total;
}
