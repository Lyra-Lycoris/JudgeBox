#include <bits/stdc++.h>
using namespace std;

long long solve(string s) {
    long long n = (long long) s.size();
    vector<long long> counts(2 * n + 1, 0);
    vector<long long> stack(n + 1, 0);
    long long top = 0;
    long long prefix = 0;
    long long answer = 0;
    counts[n] = 1;
    stack[0] = 0;
    top = 1;
    for (char c : s) {
        prefix += (c == '(') ? 1 : -1;
        while (top > 0 && stack[top - 1] > prefix) {
            counts[stack[top - 1] + n] = 0;
            --top;
        }
        answer += counts[prefix + n];
        counts[prefix + n] += 1;
        if (top == 0 || stack[top - 1] < prefix) {
            stack[top] = prefix;
            ++top;
        }
    }
    return answer;
}
