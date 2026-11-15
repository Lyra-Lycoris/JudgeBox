#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, long long m, const vector<vector<long long>>& grid) {
    if (n <= 0 || m <= 0) return -1;
    if (grid[0][0] != 0 || grid[n - 1][m - 1] != 0) return -1;
    long long total = n * m;
    vector<long long> dist(total, -1);
    vector<long long> queue(total);
    long long head = 0, tail = 0;
    dist[0] = 0;
    queue[tail++] = 0;
    while (head < tail) {
        long long cur = queue[head++];
        long long x = cur / m;
        long long y = cur % m;
        long long d = dist[cur] + 1;
        if (x > 0 && grid[x - 1][y] == 0 && dist[cur - m] == -1) {
            dist[cur - m] = d;
            queue[tail++] = cur - m;
        }
        if (x + 1 < n && grid[x + 1][y] == 0 && dist[cur + m] == -1) {
            dist[cur + m] = d;
            queue[tail++] = cur + m;
        }
        if (y > 0 && grid[x][y - 1] == 0 && dist[cur - 1] == -1) {
            dist[cur - 1] = d;
            queue[tail++] = cur - 1;
        }
        if (y + 1 < m && grid[x][y + 1] == 0 && dist[cur + 1] == -1) {
            dist[cur + 1] = d;
            queue[tail++] = cur + 1;
        }
    }
    return dist[total - 1];
}
