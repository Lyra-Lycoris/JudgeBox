#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long cost, const vector<long long>& a) {
    int N = (int)n;
    vector<long long> S((size_t)N + 1, 0);
    for (int i = 1; i <= N; ++i) S[i] = S[i - 1] + a[i - 1];
    vector<long long> ms((size_t)N + 2, 0), bs((size_t)N + 2, 0);
    int head = 0, tail = 1;
    long long answer = 0;
    for (int i = 1; i <= N; ++i) {
        long long si = S[i];
        long long x = -2 * si;
        while (head + 1 < tail &&
               ms[head + 1] * x + bs[head + 1] <= ms[head] * x + bs[head]) {
            ++head;
        }
        long long best = ms[head] * x + bs[head];
        long long dpi = best + si * si + cost;
        if (i == N) answer = dpi;
        long long m = si, b = dpi + si * si;
        while (tail - head >= 2) {
            long long m1 = ms[tail - 2], b1 = bs[tail - 2];
            long long m2 = ms[tail - 1], b2 = bs[tail - 1];
            if ((__int128)(b2 - b1) * (m - m2) >= (__int128)(b - b2) * (m2 - m1)) {
                --tail;
            } else {
                break;
            }
        }
        ms[tail] = m;
        bs[tail] = b;
        ++tail;
    }
    return answer;
}
