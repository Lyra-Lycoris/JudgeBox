#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long k, const vector<long long>& a) {
    int N = (int)n;
    vector<long long> dp((size_t)N, 0);
    vector<int> q((size_t)N + 1, 0);
    dp[0] = a[0];
    int head = 0, tail = 1;  // q[head..tail) 是候选下标
    for (int i = 1; i < N; ++i) {
        long long left = (long long)i - k;
        while (head < tail && q[head] < left) ++head;
        dp[i] = a[i] + dp[q[head]];
        while (head < tail && dp[q[tail - 1]] >= dp[i]) --tail;
        q[tail++] = i;
    }
    return dp[N - 1];
}
