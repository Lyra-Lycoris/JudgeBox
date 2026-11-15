#include <bits/stdc++.h>
using namespace std;

vector<long long> solve(long long n, const vector<long long>& a) {
    vector<long long> answer(n, -1);
    vector<long long> stack;
    stack.reserve(n);
    for (long long i = n - 1; i >= 0; --i) {
        while (!stack.empty() && stack.back() <= a[i]) stack.pop_back();
        if (!stack.empty()) answer[i] = stack.back();
        stack.push_back(a[i]);
    }
    return answer;
}
