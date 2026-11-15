package t01_score_rank

import std.sort.*

struct Student {
    Student(let id: Int64, let total: Int64, let chinese: Int64) {}
}

func compareStudent(a: Student, b: Student): Ordering {
    if (a.total != b.total) {
        return if (a.total > b.total) {
            Ordering.LT
        } else {
            Ordering.GT
        }
    }
    if (a.chinese != b.chinese) {
        return if (a.chinese > b.chinese) {
            Ordering.LT
        } else {
            Ordering.GT
        }
    }
    if (a.id < b.id) {
        return Ordering.LT
    }
    if (a.id > b.id) {
        return Ordering.GT
    }
    return Ordering.EQ
}

func solve(n: Int64, ids: Array<Int64>, chinese: Array<Int64>, math: Array<Int64>,
           english: Array<Int64>): Array<Int64> {
    let students = Array<Student>(n) {
        i => Student(ids[i], chinese[i] + math[i] + english[i], chinese[i])
    }
    sort(students, by: compareStudent)
    let answer = Array<Int64>(n, repeat: 0)
    for (i in 0..n) {
        answer[i] = students[i].id
    }
    return answer
}
