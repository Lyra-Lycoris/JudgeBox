#include <bits/stdc++.h>
using namespace std;

struct DsuWeighted {
    vector<int> parent, sz;
    vector<long long> diff;  // diff[x] = value[x] - value[parent[x]]

    explicit DsuWeighted(int n) : parent(n + 1), sz(n + 1, 1), diff(n + 1, 0) {
        for (int i = 0; i <= n; ++i) parent[i] = i;
    }

    int find(int x) {
        int root = x;
        long long total = 0;
        while (parent[root] != root) {
            total += diff[root];
            root = parent[root];
        }
        int cur = x;
        long long remain = total;
        while (parent[cur] != cur) {
            int nxt = parent[cur];
            long long old = diff[cur];
            parent[cur] = root;
            diff[cur] = remain;
            remain -= old;
            cur = nxt;
        }
        return root;
    }

    // value[a] - value[b] = c；返回 false 表示与已知信息矛盾
    bool merge(int a, int b, long long c) {
        int ra = find(a);
        long long da = diff[a];
        int rb = find(b);
        long long db = diff[b];
        if (ra == rb) return da - db == c;
        if (sz[ra] < sz[rb]) {
            parent[ra] = rb;
            diff[ra] = -(da - db - c);
            sz[rb] += sz[ra];
        } else {
            parent[rb] = ra;
            diff[rb] = da - db - c;
            sz[ra] += sz[rb];
        }
        return true;
    }
};

bool solve(long long n, long long k, const vector<vector<long long>>& rel) {
    DsuWeighted dsu((int)n);
    for (long long i = 0; i < k; ++i) {
        if (!dsu.merge((int)rel[i][0], (int)rel[i][1], rel[i][2])) return false;
    }
    return true;
}
