#include <bits/stdc++.h>
using namespace std;

long long solve(long long k, const vector<long long>& v, const vector<long long>& c) {
    long long cand = 0, balance = 0;
    for (long long i = 0; i < k; ++i) {
        long long cnt = c[i];
        if (balance == 0) {
            cand = v[i];
            balance = cnt;
        } else if (v[i] == cand) {
            balance += cnt;
        } else if (cnt < balance) {
            balance -= cnt;
        } else {
            cand = v[i];
            balance = cnt - balance;
        }
    }
    return cand;
}
