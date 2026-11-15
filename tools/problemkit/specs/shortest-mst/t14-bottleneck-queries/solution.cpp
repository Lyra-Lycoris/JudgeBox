#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long m, long long q,
                        const vector<vector<long long>>& e,
                        const vector<vector<long long>>& queries) {
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

    vector<int> head(n + 1, -1), to(2 * (n - 1)), nxt(2 * (n - 1));
    vector<long long> wt(2 * (n - 1));
    int cnt = 0;
    long long used = 0;
    for (int k = 0; k < m && used < n - 1; ++k) {
        int i = order[k];
        int u = (int)e[i][0], v = (int)e[i][1];
        int ru = find(u), rv = find(v);
        if (ru == rv) continue;
        parent[ru] = rv;
        to[cnt] = v;
        wt[cnt] = e[i][2];
        nxt[cnt] = head[u];
        head[u] = cnt;
        ++cnt;
        to[cnt] = u;
        wt[cnt] = e[i][2];
        nxt[cnt] = head[v];
        head[v] = cnt;
        ++cnt;
        ++used;
    }

    int LOG = 1;
    while ((1LL << LOG) <= n) ++LOG;
    vector<vector<int>> up(LOG, vector<int>(n + 1, 0));
    vector<vector<long long>> mx(LOG, vector<long long>(n + 1, 0));
    vector<int> depth(n + 1, 0);
    vector<char> seen(n + 1, 0);
    vector<int> stack;
    seen[1] = 1;
    stack.push_back(1);
    while (!stack.empty()) {
        int u = stack.back();
        stack.pop_back();
        for (int i = head[u]; i != -1; i = nxt[i]) {
            int v = to[i];
            if (seen[v]) continue;
            seen[v] = 1;
            depth[v] = depth[u] + 1;
            up[0][v] = u;
            mx[0][v] = wt[i];
            stack.push_back(v);
        }
    }
    for (int k = 1; k < LOG; ++k) {
        for (int v = 1; v <= n; ++v) {
            int mid = up[k - 1][v];
            up[k][v] = up[k - 1][mid];
            mx[k][v] = max(mx[k - 1][v], mx[k - 1][mid]);
        }
    }

    vector<long long> answer;
    answer.reserve(q);
    for (int t = 0; t < q; ++t) {
        int u = (int)queries[t][0], v = (int)queries[t][1];
        long long best = 0;
        if (depth[u] < depth[v]) swap(u, v);
        int diff = depth[u] - depth[v];
        for (int k = 0; diff; ++k, diff >>= 1) {
            if (diff & 1) {
                best = max(best, mx[k][u]);
                u = up[k][u];
            }
        }
        if (u != v) {
            for (int k = LOG - 1; k >= 0; --k) {
                if (up[k][u] != up[k][v]) {
                    best = max(best, max(mx[k][u], mx[k][v]));
                    u = up[k][u];
                    v = up[k][v];
                }
            }
            best = max(best, max(mx[0][u], mx[0][v]));
        }
        answer.push_back(best);
    }
    return answer;
}
