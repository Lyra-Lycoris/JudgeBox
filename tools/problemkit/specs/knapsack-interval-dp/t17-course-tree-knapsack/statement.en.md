# Tree Knapsack: Pick k Courses for Maximum Profit

A university offers $n$ courses numbered $1 \sim n$. Course $i$ has one prerequisite $p_i$: $p_i = 0$ means there is no prerequisite, otherwise course $p_i$ must be taken before course $i$. Course $i$ gives profit $v_i$ (which may be negative).

You must take **exactly** $k$ courses while respecting the prerequisites: if course $i$ is taken and $p_i \ne 0$, then $p_i$ must be taken as well (this requirement propagates along the prerequisite chain). Maximize the sum of profits of the chosen courses.

It is guaranteed that $p$ describes a forest (no cycles) and $1 \le k \le n$, so a valid selection always exists.

### Input

- The first line contains two integers $n$ and $k$, separated by a single space.
- The second line contains $n$ integers $p_1, p_2, \dots, p_n$: the prerequisite of each course.
- The third line contains $n$ integers $v_1, v_2, \dots, v_n$: the profit of each course.

Consecutive integers are separated by single spaces.

### Output

One integer: the maximum total profit of exactly $k$ courses. The answer may be negative.

### Constraints

$1 \le n \le 200$, $1 \le k \le n$, $0 \le p_i \le n$, $p_i \ne i$, $-10^{9} \le v_i \le 10^{9}$.

### Sample explanation

Sample 1: $n = 4$, $k = 2$, $p = (0, 1, 1, 2)$, $v = (3, 2, 5, 4)$. Course $1$ has no prerequisite; courses $2$ and $3$ require course $1$; course $4$ requires course $2$.

The valid selections of exactly $2$ courses are $\{1, 2\}$ with profit $3 + 2 = 5$ and $\{1, 3\}$ with profit $3 + 5 = 8$. The set $\{1, 4\}$ is invalid because taking $4$ requires taking $2$. Hence the answer is $8$.
