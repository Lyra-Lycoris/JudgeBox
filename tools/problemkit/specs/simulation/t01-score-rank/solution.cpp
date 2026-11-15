#include <bits/stdc++.h>
using namespace std;

struct Student {
    long long id;
    long long total;
    long long chinese;
};

vector<long long> solve(long long n, const vector<long long>& ids, const vector<long long>& chinese,
                        const vector<long long>& math, const vector<long long>& english) {
    vector<Student> students(n);
    for (long long i = 0; i < n; ++i) {
        students[i].id = ids[i];
        students[i].chinese = chinese[i];
        students[i].total = chinese[i] + math[i] + english[i];
    }
    sort(students.begin(), students.end(), [](const Student& a, const Student& b) {
        if (a.total != b.total) return a.total > b.total;
        if (a.chinese != b.chinese) return a.chinese > b.chinese;
        return a.id < b.id;
    });
    vector<long long> answer(n);
    for (long long i = 0; i < n; ++i) answer[i] = students[i].id;
    return answer;
}
