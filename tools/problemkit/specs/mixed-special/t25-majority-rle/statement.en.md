# Majority Element of a Run-Length Encoded Array

You are given an integer array described by **run-length encoding**.

The encoding consists of $k$ runs; the $i$-th run means "the value $v_i$ occurs $c_i$ times in a row". The runs are concatenated, so the whole array has length $N = c_1 + c_2 + \dots + c_k$.

It is **guaranteed** that some value occurs **strictly more than** $N/2$ times in the whole array (such a value is of course unique).

Find that value.

### Input

- The first line contains one integer $k$.
- The second line contains $k$ integers $v_1, \dots, v_k$.
- The third line contains $k$ integers $c_1, \dots, c_k$.

### Output

A single integer: the value that occurs strictly more than $N/2$ times.

### Constraints

$1 \le k \le 200000$, $0 \le v_i \le 10^9$, $1 \le c_i \le 10^9$, $N = \sum c_i \le 2 \times 10^{14}$.

Since $N$ can be as large as $2 \times 10^{14}$, expanding the array is impossible; the encoding itself must be processed.

### Sample explanation

Sample 1: $k = 4$ with runs "$1$ twice", "$2$ once", "$1$ three times", "$3$ once". The expanded array is $1, 1, 2, 1, 1, 1, 3$ and $N = 7$. The value $1$ appears $5$ times and $5 > 7/2 = 3.5$, so the output is `1`.

### Hint

The core of Boyer–Moore voting is cancelling pairs of different values. Keep a candidate $\text{cand}$ and a remaining count $\text{balance}$. For a run "$v_i$ repeated $c_i$ times":

- if $\text{balance} = 0$: set $\text{cand} = v_i$ and $\text{balance} = c_i$;
- if $v_i = \text{cand}$: add $c_i$ to $\text{balance}$;
- otherwise the run cancels against the candidate: the smaller of $\text{balance}$ and $c_i$ disappears, i.e. $\text{balance} = |\text{balance} - c_i|$, and $\text{cand}$ becomes $v_i$ when $c_i > \text{balance}$.

Because the majority value occurs more than half the time, it always survives the cancellation, so the final $\text{cand}$ is the answer. The complexity is $O(k)$.
