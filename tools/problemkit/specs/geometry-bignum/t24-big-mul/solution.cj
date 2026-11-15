package t24_big_mul

import std.math.numeric.*

func solve(a: String, b: String): String {
    return (BigInt.parse(a) * BigInt.parse(b)).toString()
}
