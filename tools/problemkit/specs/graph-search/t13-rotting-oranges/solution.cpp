#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<vector<long long>>& grid) {
    long long total = n * m;
    vector<int> dist((size_t) total, -1);
    vector<int> queue((size_t) total, 0);
    long long head = 0, tail = 0;
    long long fresh = 0;
    for (long long i = 0; i < n; ++i) {
        for (long long j = 0; j < m; ++j) {
            if (grid[i][j] == 2) {
                dist[i * m + j] = 0;
                queue[tail++] = (int) (i * m + j);
            } else if (grid[i][j] == 1) {
                ++fresh;
            }
        }
    }
    if (fresh == 0) return 0;
    long long minutes = 0;
    while (head < tail) {
        int cur = queue[head++];
        long long x = cur / m;
        long long y = cur % m;
        long long nd = dist[cur] + 1;
        if (x > 0 && dist[cur - m] == -1 && grid[x - 1][y] == 1) {
            dist[cur - m] = (int) nd;
            queue[tail++] = cur - (int) m;
            --fresh;
            if (nd > minutes) minutes = nd;
        }
        if (x + 1 < n && dist[cur + m] == -1 && grid[x + 1][y] == 1) {
            dist[cur + m] = (int) nd;
            queue[tail++] = cur + (int) m;
            --fresh;
            if (nd > minutes) minutes = nd;
        }
        if (y > 0 && dist[cur - 1] == -1 && grid[x][y - 1] == 1) {
            dist[cur - 1] = (int) nd;
            queue[tail++] = cur - 1;
            --fresh;
            if (nd > minutes) minutes = nd;
        }
        if (y + 1 < m && dist[cur + 1] == -1 && grid[x][y + 1] == 1) {
            dist[cur + 1] = (int) nd;
            queue[tail++] = cur + 1;
            --fresh;
            if (nd > minutes) minutes = nd;
        }
    }
    return fresh > 0 ? -1 : minutes;
}
