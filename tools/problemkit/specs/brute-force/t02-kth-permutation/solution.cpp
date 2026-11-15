#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long k) {
    vector<long long> p(n);
    for (long long i = 0; i < n; ++i) p[i] = i + 1;
    for (long long step = 1; step < k; ++step) {
        long long i = n - 2;
        while (i >= 0 && p[i] >= p[i + 1]) --i;
        if (i < 0) break;
        long long j = n - 1;
        while (p[j] <= p[i]) --j;
        swap(p[i], p[j]);
        reverse(p.begin() + i + 1, p.end());
    }
    return p;
}
