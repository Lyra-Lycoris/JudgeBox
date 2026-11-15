#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long a, long long b) {
    long long x = a, y = b;
    while (y != 0) {
        long long t = x % y;
        x = y;
        y = t;
    }
    if (x == 0) return {0, 0};
    return {x, a / x * b};
}
