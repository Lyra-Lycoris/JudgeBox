# Cyclic Shift Equality

You are given two lowercase English strings $s$ and $t$, both of length $n$.

A **cyclic shift** moves the first character of a string to its end (a left rotation by one), or equivalently moves the last character to the front. You may apply a cyclic shift any number of times, including zero times.

Decide whether $t$ can be obtained from $s$ by some number of cyclic shifts.

For example, with $s = \text{abcde}$, shifting left twice gives $\text{cdeab}$, so for $t = \text{cdeab}$ the answer is `YES`. For $t = \text{abced}$ the two strings use the same multiset of characters, but $t$ is not a cyclic shift of $s$, so the answer is `NO`.

### Input

- The first line contains one integer $n$, the common length of the two strings.
- The second line contains a lowercase string $s$ of length $n$.
- The third line contains a lowercase string $t$ of length $n$.

### Output

Print `YES` if $t$ is a cyclic shift of $s$, otherwise print `NO`.

### Constraints

- $1 \le n \le 2 \times 10^5$.
- $s$ and $t$ consist of lowercase English letters `a` to `z` only, and both have length exactly $n$.

### Sample explanation

Sample 1: $n = 5$, $s = \text{abcde}$ and $t = \text{cdeab}$. Shifting $s$ left by two positions yields $\text{cdeab}$, so the answer is `YES`.
