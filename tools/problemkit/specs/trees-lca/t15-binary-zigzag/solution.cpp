#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, long long r, const vector<long long>& ch) {
    vector<long long> answer;
    answer.reserve((size_t)n);
    vector<long long> cur, nxt;
    cur.push_back(r);
    bool forward = true;
    while (!cur.empty()) {
        if (forward) {
            for (long long v : cur) answer.push_back(v);
        } else {
            for (int i = (int)cur.size() - 1; i >= 0; --i) answer.push_back(cur[i]);
        }
        nxt.clear();
        for (long long v : cur) {
            size_t base = (size_t)(2 * (v - 1));
            long long l = ch[base], rr = ch[base + 1];
            if (l != 0) nxt.push_back(l);
            if (rr != 0) nxt.push_back(rr);
        }
        cur.swap(nxt);
        forward = !forward;
    }
    return answer;
}
