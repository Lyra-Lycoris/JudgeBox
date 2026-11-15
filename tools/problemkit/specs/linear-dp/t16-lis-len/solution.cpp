#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    vector<long long> tails;
    tails.reserve(n);
    for (long long i = 0; i < n; ++i) {
        auto it = lower_bound(tails.begin(), tails.end(), a[i]);
        if (it == tails.end()) tails.push_back(a[i]);
        else *it = a[i];
    }
    return (long long)tails.size();
}
