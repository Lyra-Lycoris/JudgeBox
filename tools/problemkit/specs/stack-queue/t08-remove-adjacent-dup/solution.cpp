#include <bits/stdc++.h>
using namespace std;

string solve(long long k, string s) {
    vector<char> chars;
    vector<long long> counts;
    chars.reserve(s.size());
    counts.reserve(s.size());
    for (char c : s) {
        if (!chars.empty() && chars.back() == c) {
            if (++counts.back() == k) {
                chars.pop_back();
                counts.pop_back();
            }
        } else {
            chars.push_back(c);
            counts.push_back(1);
        }
    }
    string answer;
    answer.reserve(s.size());
    for (size_t i = 0; i < chars.size(); ++i) {
        answer.append((size_t) counts[i], chars[i]);
    }
    return answer;
}
