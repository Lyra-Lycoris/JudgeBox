#include <bits/stdc++.h>
using namespace std;

long long solve(long long n) {
    if (n <= 20) {
        long long fact = 1;
        for (long long i = 2; i <= n; ++i) fact *= i;
        long long digits = 0;
        while (fact > 0) {
            fact /= 10;
            ++digits;
        }
        return digits;
    }
    double x = (double)n;
    double value = x * log10(x)
                 - x * 0.4342944819032518
                 + 0.5 * log10(6.283185307179586 * x)
                 + 1.0 / (12.0 * x * 2.302585092994046);
    return (long long)floor(value) + 1;
}
