# Sum of XOR over All Subsets

Given $n$ non-negative integers $a_1, a_2, \dots, a_n$.

Consider **all** $2^n$ subsets of these $n$ numbers, including the empty subset. For each subset, take the **bitwise XOR** of all its elements (the XOR of the empty subset is defined as $0$), which gives a value.

Compute the **sum** of the XOR values of all $2^n$ subsets, modulo $10^9+7$.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

A single integer: the sum of the XOR values of all subsets, modulo $10^9+7$.

### Constraints

- $1 \le n \le 200000$;
- $0 \le a_i \le 10^9$.

The total sum can be enormous (there are $2^n$ subsets), so only its value modulo $10^9+7$ is required.

### Sample explanation

**Sample 1**: $n = 2$ and the array is $1, 2$. The four subsets are:

| Subset | XOR |
| --- | --- |
| $\varnothing$ | $0$ |
| $\{1\}$ | $1$ |
| $\{2\}$ | $2$ |
| $\{1, 2\}$ | $1 \oplus 2 = 3$ |

The sum is $0 + 1 + 2 + 3 = 6$, so the output is `6`.

**Sample 2**: $n = 3$ and the array is $5, 5, 5$. Among the $8$ subsets, the empty subset contributes $0$, the three single-element subsets contribute $5$ each, the three two-element subsets contribute $5 \oplus 5 = 0$, and the full subset contributes $5 \oplus 5 \oplus 5 = 5$. The sum is $5 + 5 + 5 + 5 = 20$, so the output is `20`.

### Hint

**Split by bit**: the answer is the sum over all bits of that bit's contribution, and different bits do not interact.

Consider bit $b$ (worth $2^b$). If bit $b$ is $0$ in every $a_i$, then bit $b$ is $0$ in every subset XOR and the contribution is $0$.

Otherwise, pick any element $e$ whose bit $b$ is $1$. Pair up the $2^n$ subsets by whether they contain $e$: pair a subset $S$ with $S'$ obtained by toggling $e$. Within a pair the two subset XORs differ only in bit $b$, so exactly one subset of each pair has bit $b$ set, giving $2^{n-1}$ such subsets. That bit contributes $2^b \cdot 2^{n-1}$.

Therefore

$$\text{answer} = \left(a_1 \mathrel{|} a_2 \mathrel{|} \cdots \mathrel{|} a_n\right) \cdot 2^{n-1} \bmod (10^9+7),$$

and $2^{n-1} \bmod (10^9+7)$ is computed with binary exponentiation in $O(n + \log n)$ total time.
