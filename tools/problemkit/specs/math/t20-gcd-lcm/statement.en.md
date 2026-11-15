# GCD and LCM

You are given $T$ pairs of integers $(a, b)$. For each pair, find the greatest common divisor $\gcd(a, b)$ and the least common multiple $\operatorname{lcm}(a, b)$.

The following conventions are used:

- $\gcd(0, x) = x$, and in particular $\gcd(0, 0) = 0$;
- if at least one of $a$ and $b$ is $0$, then $\operatorname{lcm}(a, b) = 0$;
- for two positive integers, $\operatorname{lcm}(a, b) = a \div \gcd(a, b) \times b$.

### Input

The first line contains one integer $T$, the number of pairs. Each of the next $T$ lines contains two integers $a, b$ separated by a single space.

### Output

Print $T$ lines. Each line contains two integers: $\gcd(a, b)$ followed by $\operatorname{lcm}(a, b)$, separated by a single space.

### Constraints

$1 \le T \le 1000$, $0 \le a, b \le 10^9$. Every answer fits in a 64-bit signed integer.

### Sample explanation

The sample contains 3 pairs:

- $\gcd(12, 18) = 6$ and $\operatorname{lcm}(12, 18) = 12 \div 6 \times 18 = 36$;
- $7$ and $5$ are coprime, so the greatest common divisor is $1$ and the least common multiple is $35$;
- $10^9$ and $999999999$ are consecutive integers and hence coprime, so the least common multiple is $10^9 \times 999999999 = 999999999000000000$.
