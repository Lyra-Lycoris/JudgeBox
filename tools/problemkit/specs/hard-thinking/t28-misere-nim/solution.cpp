#include <bits/stdc++.h>
using namespace std;

bool solve(long long n, const vector<long long>& a) {
    long long x = 0;
    bool allOne = true;
    for (long long v : a) {
        x ^= v;
        if (v != 1) allOne = false;
    }
    if (allOne) return n % 2 == 0;
    return x != 0;
}
