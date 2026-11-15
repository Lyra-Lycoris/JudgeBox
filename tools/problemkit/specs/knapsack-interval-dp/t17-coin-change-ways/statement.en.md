# Complete Knapsack: Coin Change Ways

There are $n$ kinds of coins; the $i$-th kind has denomination $c_i$ and you may use it as many times as you want. Count the number of ways to make exactly $target$.

Two ways are considered the same when every denomination is used the same number of times (the order of coins does not matter). Since the count can be huge, output it modulo $1000000007$.

### Input

- The first line contains two integers $n$ and $target$, separated by a single space.
- The second line contains $n$ integers $c_1, c_2, \dots, c_n$, separated by single spaces.

### Output

One integer: the number of ways modulo $1000000007$.

### Constraints

$1 \le n \le 100$, $1 \le target \le 5000$, $1 \le c_i \le 5000$, and all $c_i$ are pairwise distinct.

### Sample explanation

Sample 1: $n = 3$, $target = 5$, denominations $(1, 2, 5)$. The ways to make $5$ are $1+1+1+1+1$, $1+1+1+2$, $1+2+2$ and $5$, so the answer is `4`.
