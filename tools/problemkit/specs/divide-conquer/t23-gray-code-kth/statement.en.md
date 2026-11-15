# The k-th Gray Code

An $n$-bit Gray code is a sequence of $2^n$ $n$-bit binary numbers (leading zeros allowed) such that any two consecutive terms differ in exactly one bit, and the first and last terms also differ in exactly one bit.

A Gray code can be constructed **recursively**:

- for $n = 1$ the sequence is $[0, 1]$;
- for $n > 1$, let $G$ be the $(n-1)$-bit Gray code. Write every term of $G$ with a leading $0$, then write the terms of $G$ in **reverse** order with a leading $1$; the concatenation is the $n$-bit Gray code.

For example, the sequence for $n = 3$ (in decimal) is

$$0,\ 1,\ 3,\ 2,\ 6,\ 7,\ 5,\ 4.$$

Given $n$ and $k$ ($0 \le k < 2^n$), find the decimal value of the term with index $k$ (0-based) in this sequence.

### Input

One line with two integers $n$ and $k$, separated by a single space.

### Output

A single integer: the decimal value of the $k$-th Gray code term.

### Constraints

- $1 \le n \le 60$
- $0 \le k \le 2^n - 1$, so $k$ is always a valid index

The answer is at most $2^{60} - 1 = 1152921504606846975$, which fits in a signed 64-bit integer.

### Sample explanation

Sample 1: $n = 3$ gives $0, 1, 3, 2, 6, 7, 5, 4$; the term at index $5$ is $7$, so the output is `7`.

Sample 2: $n = 1$ gives $0, 1$; the term at index $1$ is $1$, so the output is `1`.

Sample 3: $n = 2$ gives $0, 1, 3, 2$; the term at index $2$ is $3$, so the output is `3`.

### Hint

Follow the recursive definition: for the current bit length $h$, let $half = 2^{h-1}$. If $k < half$, the $k$-th term is in the first half (leading bit $0$) and equals the $k$-th term of the $(h-1)$-bit Gray code. Otherwise it is in the second half (leading bit $1$), which is the reverse of the first half, so it corresponds to index $2 \cdot half - 1 - k$ of the $(h-1)$-bit Gray code; the answer is $half$ plus the answer of that subproblem. The recursion depth is $O(n)$.

An equivalent closed form is (with $k$ in binary)

$$G(k) = k \oplus (k \gg 1).$$
