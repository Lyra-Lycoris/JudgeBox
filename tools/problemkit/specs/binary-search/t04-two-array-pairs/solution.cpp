#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a, long long m, const vector<long long>& b, long long x) {
    vector<long long> c = b;
    sort(c.begin(), c.end());
    long long ans = 0;
    for (long long v : a) {
        long long need = x - v;
        ans += upper_bound(c.begin(), c.end(), need) - c.begin();
    }
    return ans;
}
