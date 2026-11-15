# Stone Merge with One Free Merge

There are $n$ piles of stones; pile $i$ has $a_i$ stones. One operation chooses any two piles and merges them into one pile; the cost of the operation is the total number of stones in those two piles.

You must perform $n-1$ operations to merge everything into one pile, and **at most one** of those operations is free (its cost is counted as $0$); every other operation costs its pile-sum as usual. Find the **minimum total cost**.

For $n = 1$ no operation is needed, so the total cost is $0$.

### Input

The first line contains an integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

### Output

Print one integer: the minimum total cost.

### Constraints

- $1 \le n \le 200000$
- $0 \le a_i \le 10^9$

### Sample Explanation

The piles are $4, 3, 2, 6$. Merge $3$ and $2$ for cost $5$, leaving $4, 5, 6$; merge $4$ and $5$ for cost $9$, leaving $6, 9$; merge $6$ and $9$ using the free operation, so it costs $0$. The total cost is $5 + 9 = 14$.
