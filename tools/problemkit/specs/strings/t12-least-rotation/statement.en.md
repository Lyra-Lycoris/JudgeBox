# Lexicographically Smallest Rotation

You are given a lowercase string $s$ of length $n$. For every index $i$ ($0 \le i < n$), let $r_i$ be the string obtained by rotating $s$ left by $i$ positions:

$$r_i = s[i..n-1] + s[0..i-1].$$

For example, with $s = \text{baca}$:

- $r_0 = \text{baca}$
- $r_1 = \text{acab}$
- $r_2 = \text{caba}$
- $r_3 = \text{abac}$

Find the lexicographically smallest $r_i$ and print its index $i$. If several indices give the same smallest string, print the **smallest** such index.

### Input

- The first line contains one integer $n$, the length of the string.
- The second line contains a lowercase string $s$ of length $n$.

### Output

Print one integer $i$ ($0 \le i < n$), the starting index of the lexicographically smallest rotation; in case of ties, the smallest index.

### Constraints

- $1 \le n \le 2 \times 10^5$.
- $s$ consists of lowercase English letters `a` to `z` only and has length exactly $n$.

Hint: enumerating all $n$ rotations and comparing them is $O(n^2)$ and will not pass; an $O(n)$ or $O(n \log n)$ algorithm is needed.

### Sample explanation

Sample 1: $n = 4$, $s = \text{baca}$. The four rotations are $\text{baca}$, $\text{acab}$, $\text{caba}$ and $\text{abac}$; the smallest one is $\text{abac}$, obtained at index $3$, so the answer is `3`.
