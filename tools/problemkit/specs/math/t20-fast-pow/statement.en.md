# Fast Modular Exponentiation

Given three integers $a, b, m$, compute $a^b \bmod m$. This problem uses the convention $0^0 = 1$.

Because $b$ can be as large as $10^{18}$, multiplying $a$ exactly $b$ times is far too slow. Use fast exponentiation instead: write $b$ in binary and repeatedly square the base while accumulating the result, which answers one query in $O(\log b)$ multiplications.

### Input

A single line with three integers $a, b, m$, separated by single spaces.

### Output

One line with a single integer: the value of $a^b \bmod m$, which lies in $[0, m-1]$.

### Constraints

$0 \le a \le 10^9$, $0 \le b \le 10^{18}$, $1 \le m \le 10^9$.

The answer and every intermediate product fit in a 64-bit signed integer.

### Sample explanation

With $a = 2$, $b = 10$, $m = 1000$: $2^{10} = 1024$ and $1024 \bmod 1000 = 24$, so the output is `24`.
