# Counting Valid Bracket Substrings

You are given a string $s$ of length $n$ consisting only of `(` and `)`. Count how many **contiguous substrings** of $s$ are valid bracket sequences.

A string is a valid bracket sequence if and only if its length is even and, scanning it from left to right:

- at every moment the number of `(` seen so far is at least the number of `)` seen so far;
- at the end the numbers of `(` and `)` are equal.

Map `(` to $+1$ and `)` to $-1$, and let $P_0 = 0$, $P_i = P_{i-1} + (\text{$1$ if } s_i = \texttt{(} \text{ else } -1)$. Then the substring $s_{l}\dots s_{r}$ is valid exactly when

$$P_r = P_{l-1} \quad\text{and}\quad \min_{l \le i \le r} P_i \ge P_{l-1}.$$

Enumerating both endpoints takes $O(n^2)$; prefix sums plus a monotonic stack count everything in $O(n)$.

### Input

One line with a single string $s$ (no spaces).

### Output

One integer: the number of valid bracket substrings.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $s$ contains only `(` and `)`
- The answer does not exceed $\frac{n(n+1)}{2}$ and fits in a 64-bit integer

### Sample explanation

For $s = \texttt{()()}$ the valid contiguous substrings are:

- characters $1$ to $2$: `()`;
- characters $3$ to $4$: `()`;
- characters $1$ to $4$: `()()`.

There are $3$ of them, so the output is $3$.

### Hint

Process the prefix sums $P_j$ for $j = 0, 1, \dots, n$ in order. If some index $i$ has $P_i > P_j$, then no substring starting at $i$ can end at $j$ or later, so $P_i$ can be removed from the candidates. Keep the still-useful prefix values in a strictly increasing stack and an array with the current count of every prefix value. When handling $P_j$, first pop and clear all values greater than $P_j$, then add the count of $P_j$ to the answer, and finally increase the count of $P_j$ by one.
