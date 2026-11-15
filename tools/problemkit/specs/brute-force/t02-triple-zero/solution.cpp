#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    vector<long long> v(a.begin(), a.end());
    sort(v.begin(), v.end());
    long long total = 0;
    for (long long i = 0; i + 2 < n; ++i) {
        long long l = i + 1, r = n - 1;
        while (l < r) {
            long long s = v[i] + v[l] + v[r];
            if (s == 0) {
                if (v[l] == v[r]) {
                    long long c = r - l + 1;
                    total += c * (c - 1) / 2;
                    break;
                }
                long long cl = 1, cr = 1;
                while (l + cl < r && v[l + cl] == v[l]) ++cl;
                while (r - cr > l && v[r - cr] == v[r]) ++cr;
                total += cl * cr;
                l += cl;
                r -= cr;
            } else if (s < 0) {
                ++l;
            } else {
                --r;
            }
        }
    }
    return total;
}
