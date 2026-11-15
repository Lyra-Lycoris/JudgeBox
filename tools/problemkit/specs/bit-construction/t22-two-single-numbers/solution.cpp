#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a) {
    long long x = 0;
    for (long long v : a) x ^= v;
    long long lowbit = x & (-x);
    long long p = 0, q = 0;
    for (long long v : a) {
        if (v & lowbit) p ^= v;
        else q ^= v;
    }
    vector<long long> answer;
    if (p < q) {
        answer.push_back(p);
        answer.push_back(q);
    } else {
        answer.push_back(q);
        answer.push_back(p);
    }
    return answer;
}
