#include <bits/stdc++.h>
using namespace std;

long long solve(string s) {
    vector<long long> last(256, -1);
    long long best = 0, left = 0;
    long long total = (long long)s.size();
    for (long long right = 0; right < total; ++right) {
        unsigned char c = (unsigned char)s[right];
        if (last[c] >= left) left = last[c] + 1;
        last[c] = right;
        best = max(best, right - left + 1);
    }
    return best;
}
