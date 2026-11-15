# Stone Merge Minimum Cost

There are $n$ piles of stones in a row; the $i$-th pile has $a_i$ stones.

In one operation you may merge two adjacent piles: the new pile has the sum of their stones, and the cost of the operation equals that sum. After $n - 1$ operations all stones form a single pile. Find the minimum total cost.

Only adjacent piles can be merged, so the order of merges (equivalently, the way parentheses are placed) changes the total cost.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

One integer: the minimum total cost of merging everything into one pile.

### Constraints

$1 \le n \le 200$, $1 \le a_i \le 10^{9}$. The answer does not exceed $4 \times 10^{13}$.

### Sample explanation

Sample 1: $n = 4$, piles $(1, 3, 5, 2)$.

- Merge piles $1$ and $2$ with cost $1 + 3 = 4$; the row becomes $(4, 5, 2)$.
- Merge piles $2$ and $3$ with cost $5 + 2 = 7$; the row becomes $(4, 7)$.
- Merge the last two piles with cost $4 + 7 = 11$.

The total cost is $4 + 7 + 11 = 22$, which is optimal.
