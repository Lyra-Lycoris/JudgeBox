#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<vector<long long>>& e) {
    int N = (int) n;
    int M = (int) m;
    vector<int> deg(N + 1, 0), indeg(N + 1, 0), start(N + 2, 0), rstart(N + 2, 0);
    vector<char> hasSelf(N + 1, 0);
    for (int i = 0; i < M; ++i) {
        int a = (int) e[i][0];
        int b = (int) e[i][1];
        ++deg[a];
        ++indeg[b];
        if (a == b) hasSelf[a] = 1;
    }
    for (int v = 1; v <= N; ++v) {
        start[v + 1] = start[v] + deg[v];
        rstart[v + 1] = rstart[v] + indeg[v];
    }
    vector<int> cursor(start), rcursor(rstart);
    vector<int> adj(M > 0 ? M : 1, 0), radj(M > 0 ? M : 1, 0);
    for (int i = 0; i < M; ++i) {
        int a = (int) e[i][0];
        int b = (int) e[i][1];
        adj[cursor[a]++] = b;
        radj[rcursor[b]++] = a;
    }
    vector<char> visited(N + 1, 0);
    vector<int> order(N, 0);
    vector<int> stackArr(N, 0);
    vector<int> it(start);
    int on = 0;
    for (int s = 1; s <= N; ++s) {
        if (visited[s]) continue;
        visited[s] = 1;
        int sp = 1;
        stackArr[0] = s;
        while (sp > 0) {
            int u = stackArr[sp - 1];
            if (it[u] < start[u + 1]) {
                int v = adj[it[u]++];
                if (!visited[v]) {
                    visited[v] = 1;
                    stackArr[sp++] = v;
                }
            } else {
                order[on++] = u;
                --sp;
            }
        }
    }
    vector<int> comp(N + 1, -1);
    vector<int> sizes;
    for (int idx = N - 1; idx >= 0; --idx) {
        int s = order[idx];
        if (comp[s] != -1) continue;
        int cid = (int) sizes.size();
        comp[s] = cid;
        int size = 0;
        int sp = 1;
        stackArr[0] = s;
        while (sp > 0) {
            int u = stackArr[--sp];
            ++size;
            for (int k = rstart[u]; k < rstart[u + 1]; ++k) {
                int v = radj[k];
                if (comp[v] == -1) {
                    comp[v] = cid;
                    stackArr[sp++] = v;
                }
            }
        }
        sizes.push_back(size);
    }
    long long answer = 0;
    for (int cid = 0; cid < (int) sizes.size(); ++cid) {
        if (sizes[cid] > 1) answer += sizes[cid];
    }
    for (int v = 1; v <= N; ++v) {
        if (hasSelf[v] && sizes[comp[v]] == 1) ++answer;
    }
    return answer;
}
