#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<vector<long long>>& grid) {
    int N = (int) n;
    int M = (int) m;
    long long total = n * m;
    vector<char> seen((size_t) total, 0);
    vector<int> stack((size_t) total, 0);
    long long count = 0;
    for (long long s = 0; s < total; ++s) {
        long long sx = s / m;
        long long sy = s % m;
        if (grid[sx][sy] != 1 || seen[s]) continue;
        ++count;
        int top = 0;
        stack[top++] = (int) s;
        seen[s] = 1;
        while (top > 0) {
            int cur = stack[--top];
            int x = cur / M;
            int y = cur - x * M;
            if (x > 0 && !seen[cur - M] && grid[x - 1][y] == 1) {
                seen[cur - M] = 1;
                stack[top++] = cur - M;
            }
            if (x + 1 < N && !seen[cur + M] && grid[x + 1][y] == 1) {
                seen[cur + M] = 1;
                stack[top++] = cur + M;
            }
            if (y > 0 && !seen[cur - 1] && grid[x][y - 1] == 1) {
                seen[cur - 1] = 1;
                stack[top++] = cur - 1;
            }
            if (y + 1 < M && !seen[cur + 1] && grid[x][y + 1] == 1) {
                seen[cur + 1] = 1;
                stack[top++] = cur + 1;
            }
        }
    }
    return count;
}
