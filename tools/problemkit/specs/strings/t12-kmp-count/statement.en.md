# Count Pattern Occurrences

You are given a text string $s$ of length $n$ and a pattern string $p$ of length $m$, both consisting of lowercase English letters.

Count how many times $p$ occurs in $s$ as a **contiguous substring**. Occurrences may **overlap**: every start position $i$ ($1 \le i \le n - m + 1$) with $s[i..i+m-1] = p$ counts as one occurrence, and distinct starts are counted separately.

For example, with $s = \text{ababababa}$ and $p = \text{aba}$, the matching starts are $1, 3, 5, 7$ (1-based), so the answer is $4$.

### Input

- The first line contains one integer $n$, the length of the text.
- The second line contains a lowercase string $s$ of length $n$.
- The third line contains one integer $m$, the length of the pattern.
- The fourth line contains a lowercase string $p$ of length $m$.

### Output

Print one integer: the number of occurrences of $p$ in $s$, counting overlapping matches separately.

### Constraints

- $1 \le m \le n \le 2 \times 10^5$.
- $s$ and $p$ consist of lowercase English letters `a` to `z` only, with lengths exactly $n$ and $m$.

### Sample explanation

Sample 1: $n = 9$, $s = \text{ababababa}$, $m = 3$, $p = \text{aba}$.

Checking every 1-based start position:

| Start | Substring | Equals $p$ |
| --- | --- | --- |
| 1 | aba | yes |
| 2 | bab | no |
| 3 | aba | yes |
| 4 | bab | no |
| 5 | aba | yes |
| 6 | bab | no |
| 7 | aba | yes |

There are $4$ occurrences, so the answer is `4`.
