# Euler's Totient Function

For a positive integer $n$, Euler's totient function $\varphi(n)$ counts how many integers in $1 \dots n$ are coprime with $n$ (with the convention $\varphi(1) = 1$).

If the prime factorization of $n$ is $n = p_1^{e_1} p_2^{e_2} \cdots p_k^{e_k}$, then

$$\varphi(n) = n \prod_{i=1}^{k}\left(1 - \frac{1}{p_i}\right).$$

Because $n \le 10^{12}$, it is enough to test all $2 \le p \le \sqrt{n}$: whenever a prime factor $p$ is found, divide all factors $p$ out of $n$ and multiply the answer by $(1 - 1/p)$. If the remaining value is greater than $1$ after the loop, it is itself a prime factor and must be handled once more. The complexity is $O(\sqrt{n})$.

### Input

A single line with one integer $n$.

### Output

One line with a single integer: the value of $\varphi(n)$.

### Constraints

$1 \le n \le 10^{12}$. The answer is at most $10^{12}$ and fits in a 64-bit signed integer.

### Sample explanation

$n = 36 = 2^2 \times 3^2$, hence

$$\varphi(36) = 36 \times \left(1 - \frac{1}{2}\right) \times \left(1 - \frac{1}{3}\right) = 36 \times \frac{1}{2} \times \frac{2}{3} = 12.$$

There are $12$ integers in $1 \dots 36$ coprime with $36$, for example $1, 5, 7, 11, \dots$
