# Pairs with Equal Value and Index Differences

Given $n$ integers $a_1, a_2, \dots, a_n$. An index pair $(i, j)$ with $1 \le i < j \le n$ is called an **equal-difference pair** when

$$|a_i - a_j| = |i - j|,$$

that is, the absolute difference of the values equals the absolute difference of the indices. Count how many such index pairs exist.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

Print one integer: the number of distinct index pairs $(i, j)$ satisfying the condition.

### Constraints

$1 \le n \le 200000$, $|a_i| \le 10^9$.

The answer can be as large as $\frac{n(n-1)}{2} \approx 2 \times 10^{10}$, so a 64-bit integer is required.

### Sample explanation

In sample 1, $n = 5$ and the sequence is $1, 2, 3, 5, 4$. Checking every pair:

| Pair | $\lvert a_i - a_j \rvert$ | $\lvert i - j \rvert$ | Valid |
| --- | --- | --- | --- |
| (1, 2) | 1 | 1 | yes |
| (1, 3) | 2 | 2 | yes |
| (1, 4) | 4 | 3 | no |
| (1, 5) | 3 | 4 | no |
| (2, 3) | 1 | 1 | yes |
| (2, 4) | 3 | 2 | no |
| (2, 5) | 2 | 3 | no |
| (3, 4) | 2 | 1 | no |
| (3, 5) | 1 | 2 | no |
| (4, 5) | 1 | 1 | yes |

Four pairs satisfy the condition, so the answer is `4`.

### Hint

Splitting the absolute value shows that the condition is equivalent to $a_i - i = a_j - j$ or $a_i + i = a_j + j$. Count the pairs sharing each of the two kinds of keys.
