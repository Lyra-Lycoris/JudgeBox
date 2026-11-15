#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long s, long long k) {
    vector<long long> v(k, 1);
    v[k - 1] = s - (k - 1);
    return v;
}
