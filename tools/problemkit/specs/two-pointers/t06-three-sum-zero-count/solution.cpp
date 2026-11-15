#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    vector<long long> b = a;
    sort(b.begin(), b.end());
    long long count = 0;
    for (long long i = 0; i + 2 < n; ++i) {
        long long lo = i + 1, hi = n - 1;
        while (lo < hi) {
            long long sum = b[i] + b[lo] + b[hi];
            if (sum < 0) {
                lo++;
            } else if (sum > 0) {
                hi--;
            } else if (b[lo] == b[hi]) {
                long long m = hi - lo + 1;
                count += m * (m - 1) / 2;
                break;
            } else {
                long long lowCount = 1;
                while (lo + lowCount < hi && b[lo + lowCount] == b[lo]) lowCount++;
                long long highCount = 1;
                while (hi - highCount > lo && b[hi - highCount] == b[hi]) highCount++;
                count += lowCount * highCount;
                lo += lowCount;
                hi -= highCount;
            }
        }
    }
    return count;
}
