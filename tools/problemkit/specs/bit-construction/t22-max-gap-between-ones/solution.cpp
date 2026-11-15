#include <bits/stdc++.h>
using namespace std;

long long solve(long long n) {
    long long best = 0;
    long long last = -1;
    long long pos = 0;
    while (n > 0) {
        if (n & 1LL) {
            if (last >= 0) {
                long long gap = pos - last - 1;
                if (gap > best) best = gap;
            }
            last = pos;
        }
        n >>= 1;
        ++pos;
    }
    return best;
}
