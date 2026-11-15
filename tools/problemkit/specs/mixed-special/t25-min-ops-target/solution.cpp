#include <bits/stdc++.h>
using namespace std;

long long solve(long long n, const vector<long long>& a, const vector<long long>& b) {
    long long answer = 0, prevPos = 0, prevNeg = 0;
    for (long long i = 0; i < n; ++i) {
        long long d = b[i] - a[i];
        long long pos = d > 0 ? d : 0;
        long long neg = d < 0 ? -d : 0;
        if (pos > prevPos) answer += pos - prevPos;
        if (neg > prevNeg) answer += neg - prevNeg;
        prevPos = pos;
        prevNeg = neg;
    }
    return answer;
}
