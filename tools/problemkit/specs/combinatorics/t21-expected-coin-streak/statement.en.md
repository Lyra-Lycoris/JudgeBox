# Expected Tosses for n Consecutive Heads

A fair coin shows heads with probability $1/2$ on every toss. Keep tossing until **the first time** $n$ consecutive heads appear.

Compute the expected total number of tosses $E_n$. It can be shown that $E_n$ is always an integer; print

$$E_n \bmod (10^9+7).$$

For example $n = 1$ needs $2$ tosses on average before the first head, $n = 2$ gives $E_2 = 6$, and $n = 3$ gives $E_3 = 14$.

### Input

A single integer $n$.

### Output

One integer: $E_n$ modulo $10^9+7$, lying in $[0, 10^9+6]$.

### Constraints

- $1 \le n \le 10^{18}$

### Sample explanation

Sample 1: $n = 2$. Let $E_k$ be the expected number of remaining tosses when the current streak is $k$ heads. Then $E_2 = 0$, $E_1 = 1 + \frac{1}{2}E_2 + \frac{1}{2}E_0$ and $E_0 = 1 + \frac{1}{2}E_1 + \frac{1}{2}E_0$, which yield $E_0 = 6$, so the answer is $6$.

Sample 2: $n = 1$; the first head appears after $2$ tosses on average, so the answer is $2$.
