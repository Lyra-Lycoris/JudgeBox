# Minimum Bit Operations to Zero

Given a non-negative integer $n$. You may apply any of the following three operations to the current value $x$, as many times as you like:

- **decrement**: $x \leftarrow x - 1$ (requires $x > 0$);
- **increment**: $x \leftarrow x + 1$;
- **halve**: $x \leftarrow x / 2$ (requires $x$ to be even).

What is the minimum number of operations needed to turn $x$ into $0$?

### Input

A single line with one integer $n$.

### Output

A single line with one integer: the minimum number of operations.

### Constraints

- $0 \le n \le 10^{18}$.

The answer never exceeds $130$, so it fits into a 64-bit integer.

### Sample explanation

**Sample 1**: $n = 8$. Halve three times, then decrement once:

$$8 \to 4 \to 2 \to 1 \to 0$$

That is $4$ operations, and no shorter sequence exists, so the output is `4`.

**Sample 2**: $n = 3$. Incrementing first costs $3 \to 4 \to 2 \to 1 \to 0$, four steps; it is better to decrement first:

$$3 \to 2 \to 1 \to 0$$

which takes $3$ operations, so the output is `3`.

### Hint

When $x$ is even, halving is always at least as good: incrementing or decrementing keeps the value in the same range and only adds extra work.

The interesting decision is whether an odd $x$ should be decremented or incremented. Let $x > 3$ be odd:

- if $x \equiv 1 \pmod 4$, then $x - 1$ is divisible by $4$ and can be halved twice in a row, so **decrement**;
- if $x \equiv 3 \pmod 4$, then $x + 1$ is divisible by $4$, so **increment**.

For $x = 1$ just decrement to $0$. $x = 3$ is the only exception: decrementing ($3 \to 2 \to 1 \to 0$) beats incrementing ($3 \to 4 \to 2 \to 1 \to 0$).

Every constant number of operations at least halves the value, so the total complexity is $O(\log n)$.
