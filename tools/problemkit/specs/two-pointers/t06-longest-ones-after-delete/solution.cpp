#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    long long best = 0, zeros = 0, left = 0;
    for (long long right = 0; right < n; ++right) {
        if (a[right] == 0) zeros++;
        while (zeros > 1) {
            if (a[left] == 0) zeros--;
            left++;
        }
        best = max(best, right - left + 1);
    }
    return best > 0 ? best - 1 : 0;
}
