#include <bits/stdc++.h>
using namespace std;

bool isLeapYear(long long year) {
    return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
}

long long daysBeforeYear(long long year) {
    long long t = year - 1;
    return t * 365 + t / 4 - t / 100 + t / 400;
}

long long dayOfYear(long long year, long long month, long long day) {
    const long long cum[13] = {0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334};
    long long value = cum[month] + day - 1;
    if (month > 2 && isLeapYear(year)) value += 1;
    return value;
}

long long daysInMonth(long long year, long long month) {
    if (month == 2) return isLeapYear(year) ? 29 : 28;
    if (month == 4 || month == 6 || month == 9 || month == 11) return 30;
    return 31;
}

string padNumber(long long value, int width) {
    string text = to_string(value);
    while ((int)text.size() < width) text = "0" + text;
    return text;
}

string solve(long long y, long long m, long long d, long long k) {
    long long total = daysBeforeYear(y) + dayOfYear(y, m, d) + k;
    long long lo = 1, hi = 1 + total / 365 + 2;
    while (lo < hi) {
        long long mid = (lo + hi + 1) / 2;
        if (daysBeforeYear(mid) <= total) lo = mid; else hi = mid - 1;
    }
    long long year = lo;
    long long doy = total - daysBeforeYear(year);
    long long month = 1;
    while (true) {
        long long length = daysInMonth(year, month);
        if (doy < length) break;
        doy -= length;
        month += 1;
    }
    return padNumber(year, 4) + "-" + padNumber(month, 2) + "-" + padNumber(doy + 1, 2);
}
