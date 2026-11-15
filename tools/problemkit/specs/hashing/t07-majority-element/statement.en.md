# Majority Element

Given $n$ integers $a_1, a_2, \dots, a_n$, it is guaranteed that some value occurs **strictly more than** $\lfloor n/2 \rfloor$ times. Find that value.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

Print one integer: the value that occurs more than half of the time.

### Constraints

$1 \le n \le 200000$, $|a_i| \le 10^9$. The answer is guaranteed to exist and to be unique.

### Sample explanation

In sample 1, $n = 7$ and the sequence is $2, 2, 1, 1, 1, 2, 2$:

- $2$ occurs $4$ times, and $4 > 7/2 = 3.5$;
- $1$ occurs $3$ times.

So the majority element is $2$ and the answer is `2`.
