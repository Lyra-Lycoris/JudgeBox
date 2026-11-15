# Number of Triples Summing to Zero

Given an integer array $a$ of length $n$ (which is **not sorted**), count the index triples $(i, j, k)$ with $i < j < k$ and $a_i + a_j + a_k = 0$.

Elements may repeat; triples with different indices count separately.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$ separated by single spaces.

### Output

One integer: the number of valid triples.

### Constraints

- $1 \le n \le 2000$
- $|a_i| \le 10^9$
- The answer is at most about $\binom{2000}{3} \approx 1.33 \times 10^9$, so use 64-bit integers

### Sample explanation

Sample 1: $a = [-1, 0, 1, 2, -1, -4]$. The valid triples are $(-1, 0, 1)$ (twice, since $-1$ appears twice) and $(-1, -1, 2)$, so the answer is $3$.

Sample 2: any three of the five zeros sum to zero, giving $\binom{5}{3} = 10$ triples.

Sample 3: every triple of $[1, 2, 3, 4]$ has a positive sum, so the answer is $0$.
