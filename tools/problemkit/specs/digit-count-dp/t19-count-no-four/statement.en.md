# Count Integers Without Digit 4

Given two positive integers $l$ and $r$, count how many integers in the closed interval $[l, r]$ have **no digit $4$** in their decimal representation.

### Input

A single line with two integers $l$ and $r$ separated by a space.

### Output

One integer: the number of integers in the interval that do not contain the digit $4$.

### Constraints

- $1 \le l \le r \le 10^{18}$

### Sample explanation

In $[1, 10]$ the integers without the digit $4$ are $1, 2, 3, 5, 6, 7, 8, 9, 10$, so the answer is $9$.

Write the interval as a difference of prefixes: let $f(x)$ be the number of integers in $[0, x]$ whose decimal representation has no digit $4$; the answer is $f(r) - f(l-1)$. Scan the digits from the most significant one: if the current digit is chosen smaller than the digit of $x$, all remaining positions are free and contribute $9^{\text{remaining positions}}$ possibilities (nine allowed digits, $0 \sim 9$ except $4$); as soon as a digit equals $4$, no number with this prefix is valid any more. One prefix count costs $O(\log_{10} r)$.
