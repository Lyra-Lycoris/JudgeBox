#include <bits/stdc++.h>
using namespace std;

long long solve(long long k, const vector<string>& tokens) {
    vector<long long> stack;
    stack.reserve(k / 2 + 2);
    for (const string& token : tokens) {
        if (token.size() == 1 && (token[0] == '+' || token[0] == '-' || token[0] == '*' || token[0] == '/')) {
            long long b = stack.back();
            stack.pop_back();
            long long a = stack.back();
            stack.pop_back();
            long long result = 0;
            if (token[0] == '+') result = a + b;
            else if (token[0] == '-') result = a - b;
            else if (token[0] == '*') result = a * b;
            else result = a / b;
            stack.push_back(result);
        } else {
            stack.push_back(stoll(token));
        }
    }
    return stack.back();
}
