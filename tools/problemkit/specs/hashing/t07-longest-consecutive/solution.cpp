#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    unordered_set<long long> present;
    present.reserve(a.size() * 2 + 16);
    for (long long x : a) present.insert(x);
    long long best = 0;
    for (long long x : a) {
        if (present.count(x - 1)) continue;
        long long y = x;
        while (present.count(y + 1)) ++y;
        best = max(best, y - x + 1);
    }
    return best;
}
