#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, string s) {
    long long m = (long long)s.size();
    if (m <= 1) return 0;
    string t = s + s;
    long long i = 0, j = 1, k = 0;
    while (i < m && j < m && k < m) {
        char a = t[(size_t)(i + k)];
        char b = t[(size_t)(j + k)];
        if (a == b) {
            ++k;
        } else if (a > b) {
            i = i + k + 1;
            if (i <= j) i = j + 1;
            k = 0;
        } else {
            j = j + k + 1;
            if (j <= i) j = i + 1;
            k = 0;
        }
    }
    return min(i, j);
}
