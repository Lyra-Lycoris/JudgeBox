# Two Sum in a Sorted Array: Number of Pairs

Given an array $a$ of $n$ integers sorted in **non-decreasing** order and an integer $\mathit{target}$, count the index pairs $(i, j)$ with $i < j$ and $a_i + a_j = \mathit{target}$.

Elements may repeat and different index pairs count separately: for $a = [2, 2, 2]$ and $\mathit{target} = 4$ the pairs $(0,1)$, $(0,2)$ and $(1,2)$ all work, so the answer is $3$.

### Input

The first line contains two integers $n$ and $\mathit{target}$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$ with $a_1 \le a_2 \le \dots \le a_n$.

### Output

One integer: the number of valid index pairs.

### Constraints

- $1 \le n \le 200000$
- $|a_i| \le 10^9$, and the array is sorted in non-decreasing order
- $|\mathit{target}| \le 2 \times 10^9$
- The answer can be large (up to about $2 \times 10^{10}$), so use 64-bit integers

### Sample explanation

Sample 1: $n = 5$, $\mathit{target} = 5$, array $1, 2, 3, 4, 5$. Only $1 + 4 = 5$ and $2 + 3 = 5$ work, so the answer is $2$.

Sample 2: $n = 3$, $\mathit{target} = 4$, array $2, 2, 2$. Every pair sums to $4$, giving $\binom{3}{2} = 3$ pairs.

Sample 3: $n = 1$, two different indices cannot be chosen, so the answer is $0$.
