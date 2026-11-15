#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long k, const vector<long long>& a) {
    unordered_map<long long, long long> counts;
    counts.reserve(a.size() * 2 + 16);
    counts[0] = 1;
    long long prefix = 0;
    long long answer = 0;
    for (long long x : a) {
        prefix += x;
        auto hit = counts.find(prefix - k);
        if (hit != counts.end()) answer += hit->second;
        ++counts[prefix];
    }
    return answer;
}
