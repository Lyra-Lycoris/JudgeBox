#include <bits/stdc++.h>
using namespace std;

// driver：只负责读 stdin、调用选手的 solve、写 stdout。不要在这里写题解。
long long solve(long long a, long long b);

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long a, b;
    cin >> a >> b;
    cout << solve(a, b) << '\n';
    return 0;
}
