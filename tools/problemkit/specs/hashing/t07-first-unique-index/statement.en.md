# First Unique Character Position

Given a string $s$ of length $n$ consisting only of lowercase English letters, find the **first** character that occurs exactly once and print its position (positions are $1$-based). If no such character exists, print `-1`.

### Input

- The first line contains one integer $n$, the length of the string.
- The second line contains a lowercase string $s$ of length exactly $n$.

### Output

Print one integer:

- the $1$-based position of the first character occurring exactly once, if it exists;
- otherwise `-1`.

### Constraints

$1 \le n \le 10^6$ and $s$ consists only of lowercase letters `a` to `z`.

### Sample explanation

In sample 1, $s = \text{abacabad}$ with $n = 8$. The occurrence counts are:

| Character | a | b | c | d |
| --- | --- | --- | --- | --- |
| Count | 4 | 2 | 1 | 1 |

Scanning from the left, the characters occurring exactly once are `c` (position $4$) and then `d` (position $8$). The first one is `c`, so the answer is `4`.
