#include <bits/stdc++.h>
using namespace std;

bool solve(long long k, const vector<string>& w) {
    for (long long i = 1; i < k; ++i) if (w[i] != w[0]) return false;
    return true;
}
