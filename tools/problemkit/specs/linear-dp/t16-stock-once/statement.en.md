# Best Time to Buy and Sell Stock

You are given an array $a$ of length $n$, where $a_i$ is the price of a stock on day $i$.

You may complete **at most one** transaction: choose a day $l$ to buy one share and a later day $r$ ($l \le r$) to sell it. You are also allowed to do nothing at all.

Compute the maximum profit of such a transaction (sell price minus buy price). If no profit is possible, the profit is $0$.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

A single integer: the maximum profit. Print `0` if you do not trade.

### Constraints

$1 \le n \le 200000$, $0 \le a_i \le 10^9$.

The answer fits in a 64-bit integer.

### Sample explanation

Sample 1: $n = 6$ and the prices are $7, 1, 5, 3, 6, 4$.

- Buy on day $2$ at price $1$ and sell on day $5$ at price $6$: profit $6 - 1 = 5$.
- This is the best buy-then-sell combination, so the output is `5`.

### Hint

Scan from left to right while keeping the minimum price $mn$ seen so far. For each day $i$, selling there yields $a_i - mn$; update the answer first, then update $mn$ with $a_i$. The complexity is $O(n)$ time and $O(1)$ extra space.
