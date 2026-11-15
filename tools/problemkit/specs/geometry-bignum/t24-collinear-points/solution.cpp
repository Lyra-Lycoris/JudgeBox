#include <bits/stdc++.h>
using namespace std;

bool solve(long long x1, long long y1, long long x2, long long y2, long long x3, long long y3) {
    long long cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1);
    return cross == 0;
}
