#include <bits/stdc++.h>
using namespace std;

int precedenceOf(char op) {
    return (op == '*' || op == '/') ? 2 : 1;
}

void applyTop(vector<long long>& values, vector<char>& ops) {
    char op = ops.back();
    ops.pop_back();
    long long b = values.back();
    values.pop_back();
    long long a = values.back();
    values.pop_back();
    long long result = 0;
    if (op == '+') {
        result = a + b;
    } else if (op == '-') {
        result = a - b;
    } else if (op == '*') {
        result = a * b;
    } else {
        long long quotient = llabs(a) / llabs(b);
        result = ((a < 0) == (b < 0)) ? quotient : -quotient;
    }
    values.push_back(result);
}

long long solve(string expr) {
    vector<long long> values;
    vector<char> ops;
    values.reserve(expr.size() + 2);
    ops.reserve(expr.size() + 2);
    int index = 0;
    int length = (int)expr.size();
    while (index < length) {
        char ch = expr[index];
        if (ch >= '0' && ch <= '9') {
            long long number = 0;
            while (index < length && expr[index] >= '0' && expr[index] <= '9') {
                number = number * 10 + (expr[index] - '0');
                ++index;
            }
            values.push_back(number);
            continue;
        }
        if (ch == '(') {
            ops.push_back(ch);
        } else if (ch == ')') {
            while (!ops.empty() && ops.back() != '(') applyTop(values, ops);
            ops.pop_back();
        } else {
            while (!ops.empty() && ops.back() != '(' && precedenceOf(ops.back()) >= precedenceOf(ch)) {
                applyTop(values, ops);
            }
            ops.push_back(ch);
        }
        ++index;
    }
    while (!ops.empty()) applyTop(values, ops);
    return values.front();
}
