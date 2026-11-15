#include <bits/stdc++.h>
using namespace std;

bool solve(long long x1, long long y1, long long x2, long long y2, long long px, long long py, long long d) {
    long long dx = x2 - x1;
    long long dy = y2 - y1;
    long long cross = dx * (py - y1) - dy * (px - x1);
    long long len2 = dx * dx + dy * dy;
    return cross * cross <= d * d * len2;
}
