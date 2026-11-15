#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a) {
    long long notTake = 0;
    long long take = a[0];
    for (long long i = 1; i < n; ++i) {
        long long newTake = notTake + a[i];
        long long newNot = max(notTake, take);
        notTake = newNot;
        take = newTake;
    }
    return max(notTake, take);
}
