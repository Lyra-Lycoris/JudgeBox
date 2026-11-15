#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    long long sum = 0;
    for (long long x : a) sum += x;
    return sum;
}
