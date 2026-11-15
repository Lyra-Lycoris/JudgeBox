# K-th Smallest via Binary Lifting on a Fenwick Tree

There is a multiset whose values come from $1 \sim n$: the value $i$ appears exactly $a_i$ times ($a_i$ may be $0$, meaning $i$ is absent). Write all elements of the multiset in non-decreasing order; the $k$-th element of that list is called the $k$-th smallest value.

Initially you are given $a_1, a_2, \dots, a_n$, then $q$ operations follow, each of one of two kinds:

- `1 x v`: set $a_x$ to $v$;
- `2 k 0`: output the $k$-th smallest value currently in the multiset.

Every query guarantees $1 \le k \le$ the current number of elements, i.e. $\sum a_i$.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $q$.

Each of the next $q$ lines contains three integers $t, x, v$:

- for $t = 1$, $x$ is an index and $v$ is the new multiplicity, i.e. $a_x \leftarrow v$;
- for $t = 2$, $x$ is $k$ itself and the third integer is always $0$ (it is ignored).

There is at least one operation with $t = 2$.

### Output

One line with the answers of all queries in the order they appear, separated by single spaces.

### Constraints

- $1 \le n \le 1.5 \times 10^5$, $1 \le q \le 1.5 \times 10^5$
- $0 \le a_i, v \le 10^9$
- Every query guarantees $1 \le k \le \sum_{i=1}^{n} a_i$

### Sample explanation

Initially $a = (1, 0, 2, 1)$, so the multiset is $\{1, 3, 3, 4\}$.

`2 1 0` asks for the $1$-st smallest value: $1$.

`2 2 0` asks for the $2$-nd smallest value: $3$.

`2 4 0` asks for the $4$-th smallest value: $4$.

`1 2 3` sets $a_2 = 3$, so the multiset becomes $\{1, 2, 2, 2, 3, 3, 4\}$.

`2 5 0` asks for the $5$-th smallest value: $3$.

Hence the output is `1 3 4 3`.
