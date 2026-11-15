#include <bits/stdc++.h>
using namespace std;

static long long crossOf(long long ax, long long ay, long long bx, long long by, long long cx, long long cy) {
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax);
}

static bool between(long long lo1, long long lo2, long long value) {
    long long low = min(lo1, lo2);
    long long high = max(lo1, lo2);
    return low <= value && value <= high;
}

static bool onSegment(long long ax, long long ay, long long bx, long long by, long long px, long long py) {
    return between(ax, bx, px) && between(ay, by, py);
}

bool solve(long long ax, long long ay, long long bx, long long by,
           long long cx, long long cy, long long dx, long long dy) {
    long long d1 = crossOf(ax, ay, bx, by, cx, cy);
    long long d2 = crossOf(ax, ay, bx, by, dx, dy);
    long long d3 = crossOf(cx, cy, dx, dy, ax, ay);
    long long d4 = crossOf(cx, cy, dx, dy, bx, by);
    if (((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) &&
        ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0))) {
        return true;
    }
    if (d1 == 0 && onSegment(ax, ay, bx, by, cx, cy)) return true;
    if (d2 == 0 && onSegment(ax, ay, bx, by, dx, dy)) return true;
    if (d3 == 0 && onSegment(cx, cy, dx, dy, ax, ay)) return true;
    if (d4 == 0 && onSegment(cx, cy, dx, dy, bx, by)) return true;
    return false;
}
