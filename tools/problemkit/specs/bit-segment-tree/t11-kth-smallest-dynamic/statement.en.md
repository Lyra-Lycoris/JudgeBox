# Dynamic K-th Smallest

Maintain a multiset of integers, initially empty. Then $q$ operations follow, each of one of three kinds:

- `1 v`: insert one copy of $v$;
- `2 v`: erase one copy of $v$ (it is guaranteed that at least one $v$ is currently present);
- `3 k`: ask for the $k$-th smallest value currently in the set (it is guaranteed that $1 \le k \le$ the current number of elements).

Apply all operations in order and answer every query in order.

### Input

The first line contains one integer $q$.

Each of the next $q$ lines contains two integers $t, v$:

- $t = 1$ means insert $v$;
- $t = 2$ means erase one copy of $v$;
- $t = 3$ means ask for the $v$-th smallest value (the second integer is $k = v$).

There is at least one operation with $t = 3$.

### Output

One line with the answers of all queries in the order they appear, separated by single spaces.

### Constraints

- $1 \le q \le 2 \times 10^5$
- For insertions and erasures $1 \le v \le 10^9$
- For queries $1 \le k \le$ the current number of elements
- Every erasure is guaranteed to find the value present

### Sample explanation

The set is empty at the beginning.

After `1 5`, `1 3`, `1 9` the set is $\{3, 5, 9\}$.

`3 1` asks for the 1st smallest value, which is $3$.

`3 3` asks for the 3rd smallest value, which is $9$.

`2 3` erases one $3$, so the set becomes $\{5, 9\}$.

`3 1` asks for the 1st smallest value, which is $5$.

Hence the output is `3 9 5`.
