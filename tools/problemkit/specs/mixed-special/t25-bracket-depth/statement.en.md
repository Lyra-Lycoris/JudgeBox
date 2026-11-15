# Construct a Bracket Sequence with Nesting Depth k

You are given two integers $n$ and $k$ ($n$ is guaranteed to be even and $1 \le k \le n/2$).

Construct a **valid bracket sequence** of length $n$ whose **maximum nesting depth** is exactly $k$.

A string of length $n$ is a valid bracket sequence if and only if: it consists only of `(` and `)`, in every prefix the number of `(` is at least the number of `)`, and the whole string contains the same number of both brackets.

The nesting depth of a sequence is the maximum value of "number of `(` minus number of `)`" over all prefixes.

This problem uses a **special judge** (SPJ): any valid bracket sequence is accepted.

### Input

A single line with two integers $n$ and $k$, separated by one space.

### Output

Print one string of length $n$ consisting only of `(` and `)`: your bracket sequence. The string must not contain spaces.

### Constraints

$2 \le n \le 200000$, $n$ is even, $1 \le k \le n/2$.

### Sample explanation

Sample 1: $n = 6$, $k = 2$. The output `(())()` is valid, its prefix depths are $1, 2, 1, 0, 1, 0$, so the maximum depth is $2$ as required.

`()()()` has maximum depth $1$ and `((()))` has maximum depth $3$, so neither satisfies $k = 2$.

### Hint

First place $k$ opening brackets and then $k$ closing brackets; at that point the depth reaches $k$. Append the remaining $n-2k$ characters as pairs `()`; they never push the depth above $1$, so the maximum depth stays $k$.
