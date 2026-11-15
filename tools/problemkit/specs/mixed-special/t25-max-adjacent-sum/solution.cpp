#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n) {
    vector<long long> p;
    p.reserve((size_t)n);
    p.push_back((n + 1) / 2);
    long long hi = n, lo = 1;
    while ((long long)p.size() < n) {
        p.push_back(hi);
        --hi;
        if ((long long)p.size() < n) {
            p.push_back(lo);
            ++lo;
        }
    }
    return p;
}
