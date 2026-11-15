# Next Greater Element

You are given an integer array $a_0, a_1, \dots, a_{n-1}$ of length $n$. For every position $i$, find the first element strictly greater than $a_i$ to its right, i.e. the smallest $j > i$ with $a_j > a_i$.

If no such $j$ exists, the answer for $i$ is $-1$.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_0, a_1, \dots, a_{n-1}$, separated by single spaces.

### Output

One line with $n$ integers: the $i$-th of them is the answer for position $i$ (the value $a_j$, or $-1$ if it does not exist), separated by single spaces.

### Constraints

- $1 \le n \le 200000$;
- $|a_i| \le 10^9$.

### Sample explanation

Sample 1: the array is $2, 1, 3, 5, 4$.

- $a_0 = 2$: the first greater element on the right is $a_2 = 3$;
- $a_1 = 1$: the first greater element on the right is $a_2 = 3$;
- $a_2 = 3$: the first greater element on the right is $a_3 = 5$;
- $a_3 = 5$ and $a_4 = 4$ have no greater element on their right, so their answers are $-1$.

The output is `3 3 5 -1 -1`.

Sample 2: the array is $4, 4, 3, 5$. The comparison must be **strict**, so the answer for $a_0 = 4$ is $a_3 = 5$ (the equal value to its right is skipped). The output is `5 5 5 -1`.
