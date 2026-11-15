#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<string>& words, long long q, const vector<string>& queries) {
    long long total = 0;
    for (const string& w : words) total += (long long)w.size();
    long long capacity = total + 2;
    vector<int> child((size_t)(capacity * 26), 0);
    vector<int> passing((size_t)capacity, 0);
    int used = 0;
    for (const string& w : words) {
        int current = 0;
        for (char ch : w) {
            int key = current * 26 + (ch - 'a');
            if (child[(size_t)key] == 0) child[(size_t)key] = ++used;
            current = child[(size_t)key];
            ++passing[(size_t)current];
        }
    }
    vector<long long> answer((size_t)q, 0);
    for (long long j = 0; j < q; ++j) {
        const string& query = queries[(size_t)j];
        int current = 0;
        bool found = true;
        for (char ch : query) {
            int nxt = child[(size_t)(current * 26 + (ch - 'a'))];
            if (nxt == 0) {
                found = false;
                break;
            }
            current = nxt;
        }
        answer[(size_t)j] = found ? passing[(size_t)current] : 0;
    }
    return answer;
}
