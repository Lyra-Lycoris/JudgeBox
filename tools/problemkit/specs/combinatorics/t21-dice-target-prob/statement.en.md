# Dice Rolls Summing to a Target

Roll a fair six-sided die repeatedly. The faces are $1, 2, 3, 4, 5, 6$, each with probability $1/6$. Add up the faces. What is the probability that the running total is **exactly** $n$ at some point?

Probabilities are fractions, and this problem expects them modulo $10^9+7$:

> If the answer is the reduced fraction $p/q$ (with $q$ coprime to $10^9+7$), print
> $$p \cdot q^{-1} \bmod (10^9+7),$$
> where $q^{-1}$ is the modular inverse of $q$ modulo $10^9+7$.

The number of rolls is unbounded, so the answer is the sum of the probabilities of all ways of rolling $k$ times ($k \ge 1$) with total exactly $n$.

### Input

A single integer $n$.

### Output

One integer: the probability modulo $10^9+7$, lying in $[0, 10^9+6]$.

### Constraints

- $1 \le n \le 200000$

### Sample explanation

Sample 1: $n = 2$. Either roll $2$ once (probability $1/6$), or roll $1$ twice (probability $1/36$). The total probability is $1/6 + 1/36 = 7/36$. Since $36^{-1} \equiv 27777778$, we get $7 \times 27777778 \bmod (10^9+7) = 194444446$, so the output is `194444446`.

Sample 2: $n = 1$. Only a single roll of $1$ works, with probability $1/6$. Since $6^{-1} \equiv 166666668$, the output is `166666668`.
