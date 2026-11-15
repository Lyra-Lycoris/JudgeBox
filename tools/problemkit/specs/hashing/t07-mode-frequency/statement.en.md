# Mode Frequency

Given $n$ integers $a_1, a_2, \dots, a_n$, find how many times the most frequent value occurs. This is the frequency of the mode; even if several values share the highest frequency, the answer is still a single number.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

Print one integer: the number of occurrences of the most frequent value.

### Constraints

$1 \le n \le 200000$, $|a_i| \le 10^9$.

### Sample explanation

In sample 1 the sequence is $1, 2, 2, 3, 3, 3, 4$:

- $1$ occurs once, $2$ occurs twice, $3$ occurs three times and $4$ occurs once;
- the most frequent value is $3$, occurring three times.

So the answer is `3`.
