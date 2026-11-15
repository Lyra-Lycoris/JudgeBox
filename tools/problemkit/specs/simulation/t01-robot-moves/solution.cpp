#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(string s) {
    const long long dx[4] = {0, 1, 0, -1};
    const long long dy[4] = {1, 0, -1, 0};
    int facing = 0;
    long long x = 0, y = 0;
    for (char ch : s) {
        if (ch == 'L') {
            facing = (facing + 3) % 4;
        } else if (ch == 'R') {
            facing = (facing + 1) % 4;
        } else if (ch == 'F') {
            x += dx[facing];
            y += dy[facing];
        } else if (ch == 'B') {
            x -= dx[facing];
            y -= dy[facing];
        }
    }
    return {x, y};
}
