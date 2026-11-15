#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    unordered_map<long long, long long> counts;
    counts.reserve(a.size() * 2 + 16);
    long long best = 0;
    for (long long x : a) {
        long long current = ++counts[x];
        if (current > best) best = current;
    }
    return best;
}
