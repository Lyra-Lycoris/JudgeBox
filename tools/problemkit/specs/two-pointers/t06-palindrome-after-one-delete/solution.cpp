#include <bits/stdc++.h>
using namespace std;

bool isPalindromeRange(const string& s, long long left, long long right) {
    while (left < right) {
        if (s[left] != s[right]) return false;
        left++;
        right--;
    }
    return true;
}

bool solve(string s) {
    long long left = 0, right = (long long)s.size() - 1;
    while (left < right) {
        if (s[left] == s[right]) {
            left++;
            right--;
        } else {
            return isPalindromeRange(s, left + 1, right) || isPalindromeRange(s, left, right - 1);
        }
    }
    return true;
}
