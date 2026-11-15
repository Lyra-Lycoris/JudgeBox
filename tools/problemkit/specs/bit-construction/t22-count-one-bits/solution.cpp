#include <bits/stdc++.h>
using namespace std;

long long solve(long long n) {
    long long count = 0;
    while (n > 0) {
        n &= n - 1;
        ++count;
    }
    return count;
}
