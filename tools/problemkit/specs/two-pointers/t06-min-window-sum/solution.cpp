#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long s, const vector<long long>& a) {
    long long best = -1, sum = 0, left = 0;
    for (long long right = 0; right < n; ++right) {
        sum += a[right];
        while (sum >= s) {
            long long length = right - left + 1;
            if (best < 0 || length < best) best = length;
            sum -= a[left];
            left++;
        }
    }
    return best < 0 ? 0 : best;
}
