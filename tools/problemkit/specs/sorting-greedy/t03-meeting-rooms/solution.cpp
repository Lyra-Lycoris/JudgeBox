#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& s, const vector<long long>& e) {
    vector<long long> ss = s, ee = e;
    sort(ss.begin(), ss.end());
    sort(ee.begin(), ee.end());
    long long i = 0, j = 0, cur = 0, best = 0;
    while (i < n) {
        if (ss[i] < ee[j]) {
            ++cur;
            if (cur > best) best = cur;
            ++i;
        } else {
            --cur;
            ++j;
        }
    }
    return best;
}
