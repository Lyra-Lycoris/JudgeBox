# Permutations of a Multiset

Given $n$ integers (possibly repeated), treat them as a multiset and count its **distinct** permutations, modulo $10^9+7$.

Two permutations differ only if some position holds different numbers; swapping equal numbers does not create a new permutation.

For $n = 3$ with the array $1, 1, 2$ the distinct permutations are $1,1,2$, $1,2,1$ and $2,1,1$, so the answer is $3$.

If the distinct values occur $c_1, c_2, \dots, c_m$ times, the answer is

$$\frac{n!}{c_1!\, c_2! \cdots c_m!}.$$

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$ separated by spaces.

### Output

One integer: the number of distinct permutations modulo $10^9+7$.

### Constraints

- $1 \le n \le 200000$
- $|a_i| \le 10^9$

### Sample explanation

Sample 1: $n = 3$ with the array $1, 1, 2$. Swapping the two equal $1$s gives the same permutation, so there are $3! / 2! = 3$ distinct permutations and the answer is $3$.

Sample 2: $n = 1$ with the array $-5$; there is only one permutation, so the answer is $1$.
