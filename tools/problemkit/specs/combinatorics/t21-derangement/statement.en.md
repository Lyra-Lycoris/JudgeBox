# Derangement Count

Rearrange $1, 2, \dots, n$. A permutation is called a **derangement** if no element stays in its original position, i.e. $p_i \ne i$ for every $i$.

Count the derangements of $n$ elements, modulo $10^9+7$.

For $n = 3$, the permutations $2,3,1$ and $3,1,2$ are derangements, while $1,3,2$, $2,1,3$, $3,2,1$ and $1,2,3$ are not, so the answer is $2$.

### Input

A single integer $n$.

### Output

One integer: the number of derangements of $n$ elements modulo $10^9+7$.

### Constraints

- $0 \le n \le 1000000$
- For $n = 0$ the empty permutation is the only one and it is a derangement by definition, so the answer is $1$; for $n = 1$ the answer is $0$

### Sample explanation

Sample 1: $n = 4$; among all $24$ permutations exactly $9$ are derangements ($2143, 2341, 2413, 3142, 3412, 3421, 4123, 4312, 4321$), so the answer is $9$.

Sample 2: $n = 0$; the empty permutation is a derangement by definition, so the answer is $1$.
