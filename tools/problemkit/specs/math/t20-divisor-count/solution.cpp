#include <bits/stdc++.h>
using namespace std;

long long solve(long long n) {
    long long count = 0;
    for (long long d = 1; d * d <= n; ++d) {
        if (n % d == 0) {
            count += (d * d == n) ? 1 : 2;
        }
    }
    return count;
}
