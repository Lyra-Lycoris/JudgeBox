# Count Valid Bracket Sequences

A string consisting only of `(` and `)` is a **valid bracket sequence** if and only if it can be reduced to the empty string by repeatedly deleting an adjacent pair `()`. Equivalently, every prefix contains at least as many `(` as `)` and the whole string contains equally many of both.

Given $n$, count the valid bracket sequences of length $2n$ (that is, with $n$ pairs of brackets) modulo $10^9+7$.

### Input

A single line with one integer $n$.

### Output

One integer: the number of valid bracket sequences of length $2n$, modulo $10^9+7$.

### Constraints

- $1 \le n \le 10^6$

### Sample explanation

For $n = 3$ the valid sequences of length $6$ are `((()))`, `(()())`, `(())()`, `()(())`, `()()()`, so the output is $5$.

### Hint

The answer is the $n$-th Catalan number

$$C_n = \frac{1}{n+1}\binom{2n}{n} = \frac{(2n)!}{(n+1)!\,n!}$$

Computing factorials directly overflows, so modular inverses modulo $10^9+7$ are required. Since $10^9+7$ is prime and $n+1 < 10^9+7$, Fermat's little theorem gives $a^{-1} \equiv a^{10^9+5} \pmod{10^9+7}$, computable with fast exponentiation.

Concretely: compute $n!$ and $\prod_{i=n+1}^{2n} i$ (their product is $(2n)!/n!$), so $\binom{2n}{n} = \left(\prod_{i=n+1}^{2n} i\right) \cdot (n!)^{-1}$; finally multiply by $(n+1)^{-1}$. The total complexity is $O(n + \log 10^9)$.
