#include <bits/stdc++.h>
using namespace std;

static long long orientFind(vector<long long>& dsu, long long x) {
    while (dsu[x] != x) {
        dsu[x] = dsu[dsu[x]];
        x = dsu[x];
    }
    return x;
}

vector<long long> solve(long long n, long long m, const vector<vector<long long>>& e) {
    vector<long long> dsu(n + 1), dsuSize(n + 1, 1);
    for (long long i = 0; i <= n; ++i) dsu[i] = i;
    for (long long i = 0; i < m; ++i) {
        long long a = orientFind(dsu, e[i][0]);
        long long b = orientFind(dsu, e[i][1]);
        if (a == b) continue;
        if (dsuSize[a] < dsuSize[b]) swap(a, b);
        dsu[b] = a;
        dsuSize[a] += dsuSize[b];
    }

    vector<long long> edgeCnt(n + 1, 0);
    for (long long i = 0; i < m; ++i) ++edgeCnt[orientFind(dsu, e[i][0])];
    for (long long v = 1; v <= n; ++v) {
        if (dsu[v] == v && edgeCnt[v] > dsuSize[v]) return {-1};
    }

    vector<long long> head(n + 1, -1), to(2 * m, 0), nxt(2 * m, 0), eid(2 * m, 0);
    long long cnt = 0;
    for (long long i = 0; i < m; ++i) {
        long long a = e[i][0], b = e[i][1];
        to[cnt] = b;
        eid[cnt] = i;
        nxt[cnt] = head[a];
        head[a] = cnt++;
        to[cnt] = a;
        eid[cnt] = i;
        nxt[cnt] = head[b];
        head[b] = cnt++;
    }

    vector<char> visited(n + 1, 0);
    vector<long long> parent(n + 1, 0), depth(n + 1, 0), pedge(n + 1, -1), cur = head;
    vector<long long> answer(2 * m, 0);
    vector<long long> stack;
    stack.reserve((size_t)n + 1);
    for (long long s = 1; s <= n; ++s) {
        if (visited[s]) continue;
        visited[s] = 1;
        parent[s] = 0;
        depth[s] = 0;
        stack.clear();
        stack.push_back(s);
        while (!stack.empty()) {
            long long u = stack.back();
            long long j = cur[u];
            if (j == -1) {
                stack.pop_back();
                continue;
            }
            cur[u] = nxt[j];
            long long v = to[j], k = eid[j];
            if (k == pedge[u]) continue;
            if (!visited[v]) {
                visited[v] = 1;
                parent[v] = u;
                pedge[v] = k;
                depth[v] = depth[u] + 1;
                answer[2 * k] = u;
                answer[2 * k + 1] = v;
                stack.push_back(v);
            } else if (depth[v] < depth[u]) {
                answer[2 * k] = u;
                answer[2 * k + 1] = v;
                // 环顶到 DFS 根之间的「柄」要反向走
                long long c = v;
                while (parent[c] != 0) {
                    long long k2 = pedge[c];
                    answer[2 * k2] = c;
                    answer[2 * k2 + 1] = parent[c];
                    c = parent[c];
                }
            }
        }
    }
    return answer;
}
