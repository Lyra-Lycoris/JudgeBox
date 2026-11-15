#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long m, const vector<long long>& op, const vector<long long>& val) {
    vector<long long> stack;
    vector<long long> minimum;
    vector<long long> answer;
    stack.reserve(m);
    minimum.reserve(m);
    for (long long i = 0; i < m; ++i) {
        if (op[i] == 1) {
            long long v = val[i];
            stack.push_back(v);
            minimum.push_back(minimum.empty() ? v : min(minimum.back(), v));
        } else if (op[i] == 2) {
            stack.pop_back();
            minimum.pop_back();
        } else {
            answer.push_back(minimum.back());
        }
    }
    return answer;
}
