# Number of Digits of a Factorial

Given $T$ positive integers $n$, find for every $n$ how many decimal digits the number $n! = 1\times 2\times \cdots \times n$ has.

For example $5! = 120$ has $3$ digits and $10! = 3628800$ has $7$ digits.

### Input

- The first line contains one integer $T$, the number of queries.
- Each of the next $T$ lines contains one integer $n$.

### Output

Print $T$ lines, each containing the number of decimal digits of the corresponding $n!$.

### Constraints

$1 \le T \le 100000$ and $1 \le n \le 10^9$.

Note that $n$ can be as large as $10^9$; then $n!$ has more than eight billion digits, so the factorial itself can never be computed. Neither is it possible to sum $\log_{10} i$ for every query in $O(n)$ time ($10^9$ operations do not fit in the limit). Use a constant-time formula.

### Sample explanation

The sample contains five queries:

- $1! = 1$ has $1$ digit;
- $2! = 2$ has $1$ digit;
- $5! = 120$ has $3$ digits;
- $10! = 3628800$ has $7$ digits;
- $20! = 2432902008176640000$ has $19$ digits.

So the output is `1`, `1`, `3`, `7`, `19`.

### Hint

A positive integer $m$ has $\lfloor \log_{10} m \rfloor + 1$ decimal digits, hence
$$d(n) = \left\lfloor \log_{10}(n!) \right\rfloor + 1, \qquad \log_{10}(n!) = \sum_{i=1}^{n} \log_{10} i .$$
Summing directly is $O(n)$. Using Stirling's formula
$$\ln(n!) = n\ln n - n + \frac{1}{2}\ln(2\pi n) + \frac{1}{12n} - O\!\left(\frac{1}{n^{3}}\right)$$
and converting to base $10$ gives
$$\log_{10}(n!) \approx n\log_{10} n - n\log_{10} e + \frac{1}{2}\log_{10}(2\pi n) + \frac{1}{12n\ln 10},$$
so every query is $O(1)$. For small $n$ (say $n \le 20$) it is safer to compute the integer factorial and count its digits.

The floating point error is far below $10^{-6}$, and the test data guarantees that no answer sits close enough to a rounding boundary for that error to matter.
