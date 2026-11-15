# Merge Stones

There are $n$ piles of stones in a row; the $i$-th pile has $a_i$ stones. In one operation you may pick **any two piles** and merge them into a single pile; the cost of the operation is the total number of stones in those two piles. After $n-1$ operations all stones form one pile.

Output the minimum possible total cost (the sum of the costs of all operations).

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

### Output

One integer: the minimum total cost.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $0 \le a_i \le 10^9$

### Sample explanation

The piles are $4, 3, 2, 6$. Merge $3$ and $2$ for cost $5$, leaving $4, 5, 6$; merge $4$ and $5$ for cost $9$, leaving $6, 9$; merge $6$ and $9$ for cost $15$. The total is $5 + 9 + 15 = 29$, which is optimal.

Note that the two piles do not have to be adjacent — any two piles may be merged. Every merge cost is added to the total, so it pays off to merge small piles as early as possible.
