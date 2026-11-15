# Task Scheduler: Minimum Total Time

There is one processor and $n$ tasks; every task takes exactly $1$ unit of time. Tasks are grouped by type, and to avoid overheating, **two tasks of the same type must be at least $c$ units of time apart**: if two same-type tasks start at times $x$ and $y$, then $|x - y| \ge c + 1$. The processor may stay idle while waiting.

The tasks may be executed in any order. Find the **minimum total time** needed to finish every task (time starts at $0$, and the total time is the finishing moment of the last task).

### Input

The first line contains two integers $n$ and $c$.

The second line contains $n$ integers: the type of each task.

### Output

Print one integer: the minimum total time.

### Constraints

- $1 \le n \le 200000$
- $0 \le c \le 10^9$
- $1 \le$ task type $\le 10^9$

### Sample Explanation

The types are $1,1,1,2,2,2$ with $c=2$. One optimal schedule is $1,2,\text{idle},1,2,\text{idle},1,2$, which takes $8$ units of time.
