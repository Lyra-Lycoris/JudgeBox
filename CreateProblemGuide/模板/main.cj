package demo

import std.convert.Parsable

// driver：只负责读 stdin、调用选手的 solve、写 stdout。不要在这里写题解。
main(): Unit {
    let a = Int64.parse(readln().trimAscii())
    let b = Int64.parse(readln().trimAscii())
    println(solve(a, b))
}
