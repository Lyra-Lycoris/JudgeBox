#include <bits/stdc++.h>
using namespace std;

long long solve(long long k, string s) {
    if (k <= 0 || s.empty()) return 0;
    vector<long long> count(256, 0);
    long long distinct = 0, best = 0, left = 0;
    long long total = (long long)s.size();
    for (long long right = 0; right < total; ++right) {
        unsigned char c = (unsigned char)s[right];
        if (count[c] == 0) distinct++;
        count[c]++;
        while (distinct > k) {
            unsigned char d = (unsigned char)s[left];
            count[d]--;
            if (count[d] == 0) distinct--;
            left++;
        }
        best = max(best, right - left + 1);
    }
    return best;
}
