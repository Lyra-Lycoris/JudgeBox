#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<string>& words) {
    unordered_set<string> groups;
    groups.reserve(words.size() * 2 + 16);
    string key;
    for (const string& word : words) {
        key = word;
        sort(key.begin(), key.end());
        groups.insert(key);
    }
    return (long long)groups.size();
}
