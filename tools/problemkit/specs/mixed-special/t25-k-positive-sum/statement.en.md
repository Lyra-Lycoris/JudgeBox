# Construct k Positive Integers with Sum s

You are given two integers $s$ and $k$.

Construct $k$ **positive integers** whose sum is exactly $s$.

This problem uses a **special judge** (SPJ): any valid answer is accepted; it does not have to match the reference output.

### Input

A single line with two integers $s$ and $k$, separated by one space.

### Output

Print $k$ positive integers: your construction. The numbers may be separated by spaces or newlines. You must print exactly $k$ numbers and every number must be at least $1$.

### Constraints

$1 \le k \le s \le 10^9$, and also $k \le 200000$.

### Sample explanation

Sample 1: $s = 10$, $k = 3$. The output `1 1 8` is valid: all three numbers are positive and $1 + 1 + 8 = 10$.

Other valid answers are `2 3 5`, `3 3 4` or `1 4 5`, while `1 2 6` sums to $9$ and `0 5 5` contains a non-positive number, so neither is valid.

### Hint

Let the first $k-1$ numbers be the minimum value $1$; their sum is $k-1$. Give the rest, $s-(k-1)$, to the last number. Since $s \ge k$, the last number is at least $1$.
