#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    long long candidate = a[0];
    long long balance = 0;
    for (long long x : a) {
        if (balance == 0) candidate = x;
        balance += (x == candidate) ? 1 : -1;
    }
    return candidate;
}
