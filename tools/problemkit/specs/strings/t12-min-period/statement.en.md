# Minimal Period

You are given a lowercase English string $s$ of length $n$.

If there is a length $d$ ($1 \le d \le n$, and $d$ divides $n$) such that $s$ is exactly $\frac{n}{d}$ copies of its own length-$d$ prefix glued together, that is

$$s[1..d] = s[d+1..2d] = \cdots = s[n-d+1..n],$$

then $d$ is called a **period length** of $s$. Print the minimal period length of $s$.

For example, $s = \text{abcabcabc}$ has period lengths $3$ (three copies of `abc`) and $9$ (itself); the minimal one is $3$.

### Input

- The first line contains one integer $n$, the length of the string.
- The second line contains a lowercase string $s$ of length $n$.

### Output

Print one integer: the minimal period length of $s$.

### Constraints

- $1 \le n \le 2 \times 10^5$.
- $s$ consists of lowercase English letters `a` to `z` only and has length exactly $n$.

### Sample explanation

Sample 1: $n = 9$, $s = \text{abcabcabc}$.

- $d = 1$: $1$ does not divide $9$, invalid.
- $d = 2$: $2$ does not divide $9$, invalid.
- $d = 3$: $s = \text{abc}\,\text{abc}\,\text{abc}$, valid.

So the minimal period length is $3$ and the answer is `3`.
