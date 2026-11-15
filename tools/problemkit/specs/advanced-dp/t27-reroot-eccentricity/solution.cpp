#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& p) {
    int N = (int)n;
    vector<long long> down((size_t)N + 1, 0), up((size_t)N + 1, 0);
    vector<long long> best1((size_t)N + 1, 0), best2((size_t)N + 1, 0);
    vector<int> who((size_t)N + 1, 0);
    for (int i = N; i >= 2; --i) {
        int par = (int)p[i - 2];
        long long val = down[i] + 1;
        if (val > best1[par]) {
            best2[par] = best1[par];
            best1[par] = val;
            who[par] = i;
        } else if (val > best2[par]) {
            best2[par] = val;
        }
        if (val > down[par]) down[par] = val;
    }
    for (int i = 2; i <= N; ++i) {
        int par = (int)p[i - 2];
        long long sib = (who[par] == i) ? best2[par] : best1[par];
        long long base = (up[par] > sib) ? up[par] : sib;
        up[i] = base + 1;
    }
    vector<long long> ans((size_t)N, 0);
    for (int i = 1; i <= N; ++i) ans[i - 1] = (down[i] > up[i]) ? down[i] : up[i];
    return ans;
}
