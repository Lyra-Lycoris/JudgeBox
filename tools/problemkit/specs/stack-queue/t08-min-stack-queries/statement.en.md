# Min Stack Query Results

Maintain a stack that supports the following operations:

- push an integer $v$ onto the top of the stack;
- pop the top element;
- query the minimum of all elements currently in the stack.

For compact input, operations are encoded as integers: the $i$-th operation is `op[i]`, where $1$ means push `val[i]`, $2$ means pop the top, and $3$ means query the minimum. When `op[i]` is not $1$, `val[i]` is always $0$ and can be ignored.

Execute the $m$ operations in order and output the answer of every query in the order the queries happen.

### Input

- The first line contains one integer $m$, the number of operations.
- The second line contains $m$ integers `op[0], op[1], ..., op[m-1]`, separated by single spaces.
- The third line contains $m$ integers `val[0], val[1], ..., val[m-1]`, separated by single spaces.

### Output

One line with $q$ integers separated by single spaces: the minimum of the stack at the time of each query (`op[i] = 3`), where $q$ is the number of queries ($q \ge 1$).

### Constraints

- $1 \le m \le 200000$;
- `op[i]` is $1$, $2$ or $3$;
- if `op[i] = 1` then $|val[i]| \le 10^9$, otherwise `val[i] = 0`;
- the operations are valid: every pop and every query happens while the stack is non-empty;
- there is at least one query ($q \ge 1$).

### Sample explanation

Sample 1: the operations are

1. `push 5`, the stack is $[5]$;
2. `push -3`, the stack is $[5, -3]$;
3. `getMin`, the minimum is $-3$;
4. `pop`, removing $-3$, the stack is $[5]$;
5. `getMin`, the minimum is $5$;
6. `getMin`, the minimum is still $5$.

There are $3$ queries with answers $-3, 5, 5$, so the output is `-3 5 5`.

Sample 2: two $2$s are pushed, the minimum is $2$, then the top element is popped. There is $1$ query, so the output is `2`.
