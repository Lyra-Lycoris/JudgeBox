# Counting Subarrays with Sum Divisible by K

You are given an integer sequence $a_1, a_2, \dots, a_n$ and a positive integer $k$. Count how many **non-empty contiguous segments** have a sum divisible by $k$.

Let $P_0 = 0$ and $P_i = a_1 + a_2 + \dots + a_i$. The sum of the segment $a_{l}, \dots, a_{r}$ is $P_r - P_{l-1}$, which is divisible by $k$ if and only if

$$P_r \equiv P_{l-1} \pmod{k}.$$

So the task becomes counting pairs of indices $0 \le i < j \le n$ with $P_i \equiv P_j \pmod{k}$.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $k$.

### Output

One integer: the number of non-empty contiguous segments whose sum is divisible by $k$.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le k \le 10^9$
- $-10^9 \le a_i \le 10^9$
- The answer does not exceed $\frac{(n+1)n}{2}$ and fits in a 64-bit integer

### Sample explanation

The sequence is $4, 5, 0, 2, 3$ with $k = 5$. The prefix sums are $0, 4, 9, 9, 11, 14$, whose remainders modulo $5$ are $0, 4, 4, 4, 1, 4$.

The remainder $4$ appears $4$ times and contributes $\binom{4}{2} = 6$ pairs; the remainders $0$ and $1$ appear once each and contribute nothing. Hence the answer is $6$.

The segments are $[5]$, $[5,0]$, $[5,0,2,3]$, $[0]$, $[0,2,3]$ and $[2,3]$, with sums $5, 5, 10, 0, 5, 5$.
