# Maximum Average of a Fixed-Length Window

Given an integer array $a$ of length $n$ and an integer $k$ with $1 \le k \le n$, consider all contiguous subarrays of length **exactly $k$**. Find the largest average among them and output it.

An average may not be a terminating decimal, and to avoid any floating point trouble, print the answer as a **reduced fraction** $p/q$:

- $q > 0$;
- $\gcd(|p|, q) = 1$;
- the format is `p/q` with no spaces, for example `7/2`, `-5/2`, `22/1`.

### Input

The first line contains two integers $n$ and $k$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$ separated by single spaces.

### Output

One line with the string `p/q`: the maximum average over all windows of length $k$, as a reduced fraction with a positive denominator.

### Constraints

- $1 \le k \le n \le 200000$
- $|a_i| \le 10^9$
- A window sum can reach about $2 \times 10^{14}$, so use 64-bit integers

### Sample explanation

Sample 1: $n = 3$, $k = 2$, array $1, 3, 4$. The windows are $[1, 3]$ (average $2$) and $[3, 4]$ (average $3.5$); the maximum is $7/2$.

Sample 2: the only element is $5$, so the average is $5$, printed as `5/1`.

Sample 3: $k = n = 4$, the only window is $-1, -2, -3, -4$ with sum $-10$, so the average is $-10/4 = -5/2$.
