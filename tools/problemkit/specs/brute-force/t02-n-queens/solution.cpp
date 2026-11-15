#include <bits/stdc++.h>
using namespace std;

long long nqDfs(long long row, long long n, vector<char>& col, vector<char>& d1, vector<char>& d2) {
    if (row == n) return 1;
    long long total = 0;
    for (long long c = 0; c < n; ++c) {
        long long a = row + c;
        long long b = row - c + n;
        if (col[c] || d1[a] || d2[b]) continue;
        col[c] = d1[a] = d2[b] = 1;
        total += nqDfs(row + 1, n, col, d1, d2);
        col[c] = d1[a] = d2[b] = 0;
    }
    return total;
}

long long solve(long long n) {
    vector<char> col(n, 0), d1(2 * n, 0), d2(2 * n, 0);
    return nqDfs(0, n, col, d1, d2);
}
