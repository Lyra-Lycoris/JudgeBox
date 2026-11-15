# Big Integer Addition

Two non-negative integers $a$ and $b$ are given as decimal strings, each possibly $10^5$ digits long. Compute their sum $a+b$.

The result can be far outside the range of 64-bit integers (a $10^5$-digit number has about $3\times10^5$ binary bits), so you have to implement big integer addition yourself: add digit by digit from the least significant position, propagating carries.

### Input

- The first line contains the decimal string $a$;
- the second line contains the decimal string $b$.

Both strings consist of the digits `0`–`9` and contain no leading zeros (unless the number is `0`, in which case the string is the single character `0`).

### Output

One decimal string: the decimal representation of $a+b$.

The output must not contain leading zeros (if $a+b=0$, print the single character `0`).

### Constraints

$1 \le |a|, |b| \le 100000$, where $|a|$ and $|b|$ are the lengths of the two strings.

The time limit is 2000 ms; addition is linear, so an $O(|a|+|b|)$ digit-by-digit algorithm passes comfortably.

### Sample explanation

In the sample $a = 12345678901234567890$ and $b = 98765432109876543210$. Adding digit by digit from the least significant position gives
$$12345678901234567890 + 98765432109876543210 = 111111111011111111100,$$
so the output is `111111111011111111100`.

Note that the most significant digit produces a carry, so the result has one digit more than either addend.

### Hint

Write $a = \overline{a_{n-1}\dots a_1 a_0}$ and $b = \overline{b_{m-1}\dots b_1 b_0}$ with the least significant digits $a_0$ and $b_0$. Starting from $k = 0$, repeatedly compute
$$s_k = a_k + b_k + c_k, \quad d_k = s_k \bmod 10, \quad c_{k+1} = \lfloor s_k / 10 \rfloor,$$
treating missing digits as $0$ and starting with $c_0 = 0$. Stop when both numbers are exhausted and the carry is $0$, then print the digits $d_k$ in reverse order.

Only digits $0$–$9$ and a carry of $0$ or $1$ are involved; do not try to convert the numbers to 64-bit integers.
