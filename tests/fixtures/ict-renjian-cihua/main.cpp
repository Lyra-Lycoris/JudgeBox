#include <bits/stdc++.h>
using namespace std;

vector<string> solve(const string& verse, const vector<string>& words);

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int cases = 0;
    if (!(cin >> cases)) return 0;
    for (int t = 0; t < cases; ++t) {
        string verse;
        int count = 0;
        cin >> verse >> count;
        vector<string> words(static_cast<size_t>(count));
        for (auto& word : words) cin >> word;
        auto answers = solve(verse, words);
        cout << answers.size() << '\n';
        for (const auto& answer : answers) cout << answer << '\n';
    }
    return 0;
}
