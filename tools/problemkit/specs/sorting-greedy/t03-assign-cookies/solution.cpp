#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& g, long long m, const vector<long long>& s) {
    vector<long long> gg = g, ss = s;
    sort(gg.begin(), gg.end());
    sort(ss.begin(), ss.end());
    long long i = 0, j = 0;
    while (i < n && j < m) {
        if (ss[j] >= gg[i]) ++i;
        ++j;
    }
    return i;
}
