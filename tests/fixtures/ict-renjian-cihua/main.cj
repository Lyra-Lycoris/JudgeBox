package ict02

import std.convert.Parsable

// 批量输入：用例数；每组依次给诗句、词数及逐行排列的词。
main(): Unit {
    let cases = Int64.parse(readln().trimAscii())
    for (_ in 0..cases) {
        let verse = readln().trimAscii()
        let count = Int64.parse(readln().trimAscii())
        let words = Array(count) {_ => readln().trimAscii()}
        let answers = solve(verse, words)
        println(answers.size)
        for (answer in answers) {
            println(answer)
        }
    }
}
