#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long q, const vector<vector<long long>>& segs) {
    vector<long long> diff(n + 1, 0);
    for (long long i = 0; i < q; ++i) {
        long long l = segs[i][0], r = segs[i][1];
        diff[l - 1] += 1;
        diff[r] -= 1;
    }
    long long cur = 0, best = -1, bestPos = 1;
    for (long long i = 0; i < n; ++i) {
        cur += diff[i];
        if (cur > best) {
            best = cur;
            bestPos = i + 1;
        }
    }
    return {best, bestPos};
}
