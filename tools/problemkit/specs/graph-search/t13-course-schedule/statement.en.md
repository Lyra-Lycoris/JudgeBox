# Course Schedule

You have to finish $n$ courses numbered $1 \sim n$.

The school gives $m$ prerequisite constraints. Each constraint is a pair of integers $a, b$ meaning that **course $a$ must be finished before course $b$** (think of it as a directed edge $a \to b$).

The same constraint may be given more than once, and a constraint with $a = b$ is possible as well. Decide whether some order of the $n$ courses satisfies every constraint (that is, whether the courses can be arranged in a sequence where $a$ appears before $b$ for every constraint).

### Input

- The first line contains two integers $n$ and $m$, separated by a single space.
- The next $m$ lines each contain two integers $a$ and $b$, separated by a single space, meaning course $a$ must be finished before course $b$.

When $m = 0$, nothing follows the first line.

### Output

Print one line: `YES` if all courses can be finished, otherwise `NO`.

### Constraints

- $1 \le n \le 200000$
- $0 \le m \le 200000$
- $1 \le a, b \le n$
- Time limit 2000 ms, memory limit 256 MB

### Samples

**Input 1**

```
4 3
1 2
1 3
3 4
```

**Output 1**

```
YES
```

**Input 2**

```
3 3
1 2
2 3
3 1
```

**Output 2**

```
NO
```

### Sample explanation

Sample 1: the constraints are "$1$ before $2$", "$1$ before $3$" and "$3$ before $4$". Taking the courses in the order $1, 2, 3, 4$ satisfies all of them, so the answer is `YES`.

Sample 2: the constraints require $1$ before $2$, $2$ before $3$ and $3$ before $1$, which form a cycle. They cannot all hold, so the answer is `NO`.
