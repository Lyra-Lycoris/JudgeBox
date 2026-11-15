#include <bits/stdc++.h>
using namespace std;

long long solve(long long n) {
    long long power = 1;
    for (long long i = 0; i < n; ++i) power *= 2;
    return power - 1;
}
