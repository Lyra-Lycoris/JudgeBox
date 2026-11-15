#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a, long long q,
                        const vector<vector<long long>>& queries) {
    vector<long long> lg(n + 1, 0);
    for (long long i = 2; i <= n; ++i) lg[i] = lg[i / 2] + 1;
    vector<vector<long long>> table;
    table.push_back(a);
    for (long long j = 1; (1LL << j) <= n; ++j) {
        long long len = n - (1LL << j) + 1, half = 1LL << (j - 1);
        vector<long long> row(len);
        for (long long i = 0; i < len; ++i)
            row[i] = max(table[j - 1][i], table[j - 1][i + half]);
        table.push_back(row);
    }
    vector<long long> answer;
    for (long long k = 0; k < q; ++k) {
        long long l = queries[k][0], r = queries[k][1];
        long long level = lg[r - l + 1];
        long long start = r - (1LL << level);
        answer.push_back(max(table[level][l - 1], table[level][start]));
    }
    return answer;
}
