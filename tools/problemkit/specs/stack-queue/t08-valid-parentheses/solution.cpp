#include <bits/stdc++.h>
using namespace std;

bool solve(string s) {
    vector<char> stack;
    stack.reserve(s.size());
    for (char c : s) {
        if (c == '(') stack.push_back(')');
        else if (c == '[') stack.push_back(']');
        else if (c == '{') stack.push_back('}');
        else {
            if (stack.empty() || stack.back() != c) return false;
            stack.pop_back();
        }
    }
    return stack.empty();
}
