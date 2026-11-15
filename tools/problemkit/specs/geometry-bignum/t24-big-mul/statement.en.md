# Big Integer Multiplication

Two non-negative integers $a$ and $b$ are given as decimal strings, each at most $5000$ digits long. Compute their product $a\times b$.

The product can have up to $10^4$ digits, far outside the range of 64-bit integers, so you must implement big integer multiplication yourself (long multiplication).

### Input

- The first line contains the decimal string $a$;
- the second line contains the decimal string $b$.

Both strings consist of the digits `0`–`9` and contain no leading zeros (unless the number is `0`, in which case the string is the single character `0`).

### Output

One decimal string: the decimal representation of $a\times b$ without leading zeros (if the product is $0$, print the single character `0`).

### Constraints

$1 \le |a|, |b| \le 5000$, where $|a|$ and $|b|$ are the lengths of the two strings.

Long multiplication performs $|a|\cdot|b| \le 2.5\times 10^7$ multiply-add operations, which fits in the 2000 ms limit when accumulating in 64-bit integers.

### Sample explanation

In the sample $a = 123456789$ and $b = 987654321$; digit-by-digit long multiplication gives
$$123456789 \times 987654321 = 121932631112635269,$$
so the output is `121932631112635269`.

### Hint

Store both numbers as digit arrays in reverse order (index $0$ is the least significant digit). If $A_i$ is the $i$-th digit of $a$ and $B_j$ the $j$-th digit of $b$, then position $i+j$ of the product accumulates $A_i \cdot B_j$. First accumulate all products in one array (each cell holds at most about $5000 \times 81$, so 64-bit integers do not overflow), then propagate all carries from the least significant position:

$$c_{k+1} \mathrel{+}= \left\lfloor \frac{c_k}{10} \right\rfloor, \qquad c_k \leftarrow c_k \bmod 10.$$

Finally strip the extra leading zeros at the top and print the digits in reverse order. The total complexity is $O(|a|\cdot|b|)$.

Remember to special-case a zero factor, otherwise the output would have leading zeros.
