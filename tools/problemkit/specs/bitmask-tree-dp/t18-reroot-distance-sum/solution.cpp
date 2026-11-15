#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& p) {
    int N = (int)n;
    vector<long long> sz((size_t)N + 1, 1), depth((size_t)N + 1, 0), f((size_t)N + 1, 0);
    for (int i = N; i >= 2; --i) sz[(int)p[i - 2]] += sz[i];
    for (int i = 2; i <= N; ++i) {
        depth[i] = depth[(int)p[i - 2]] + 1;
        f[1] += depth[i];
    }
    for (int i = 2; i <= N; ++i) {
        int par = (int)p[i - 2];
        f[i] = f[par] + n - 2 * sz[i];
    }
    vector<long long> answer(f.begin() + 1, f.end());
    return answer;
}
