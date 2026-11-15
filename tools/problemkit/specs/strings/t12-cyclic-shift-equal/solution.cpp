#include <bits/stdc++.h>
using namespace std;

bool solve(long long n, string s, string t) {
    if (s.size() != t.size()) return false;
    long long m = (long long)s.size();
    string doubled = s + s;
    const long long bases[2] = {131, 137};
    const long long mods[2] = {1000000007LL, 1000000009LL};
    for (int k = 0; k < 2; ++k) {
        long long base = bases[k], mod = mods[k];
        long long power = 1;
        for (long long i = 0; i < m; ++i) power = power * base % mod;
        long long target = 0;
        for (char ch : t) target = (target * base + ch) % mod;
        vector<long long> prefix(doubled.size() + 1, 0);
        for (size_t i = 0; i < doubled.size(); ++i) {
            prefix[i + 1] = (prefix[i] * base + doubled[i]) % mod;
        }
        bool matched = false;
        for (long long i = 0; i < m; ++i) {
            long long value = (prefix[i + m] - prefix[i] * power % mod + mod) % mod;
            if (value == target) {
                matched = true;
                break;
            }
        }
        if (!matched) return false;
    }
    return true;
}
