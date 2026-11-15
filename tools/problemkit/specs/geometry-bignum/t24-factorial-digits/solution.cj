package t24_factorial_digits

import std.math.*

func solve(n: Int64): Int64 {
    if (n <= 20) {
        var fact: Int64 = 1
        for (i in 2..=n) {
            fact *= i
        }
        var digits: Int64 = 0
        while (fact > 0) {
            fact /= 10
            digits += 1
        }
        return digits
    }
    let x = Float64(n)
    let value = x * log10(x) - x * 0.4342944819032518 + 0.5 * log10(6.283185307179586 * x) + 1.0 / (12.0 * x * 2.302585092994046)
    return Int64(floor(value)) + 1
}
