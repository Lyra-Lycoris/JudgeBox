#include <bits/stdc++.h>
using namespace std;

bool solve(long long n, const vector<long long>& a, long long target) {
    unordered_set<long long> seen;
    seen.reserve(a.size() * 2 + 16);
    for (long long x : a) {
        if (seen.find(target - x) != seen.end()) return true;
        seen.insert(x);
    }
    return false;
}
