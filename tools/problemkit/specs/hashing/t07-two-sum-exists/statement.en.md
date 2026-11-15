# Two Sum Existence

Given an integer sequence $a_1, a_2, \dots, a_n$ of length $n$ and an integer $target$, decide whether there are two **distinct** indices $i < j$ such that

$$a_i + a_j = target.$$

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.
- The third line contains one integer $target$.

### Output

Print a single line `YES` if such a pair exists, otherwise print `NO`.

### Constraints

$1 \le n \le 200000$, $|a_i| \le 10^9$, $|target| \le 2 \times 10^9$.

### Sample explanation

In sample 1, $n = 4$, the sequence is $2, 7, 11, 15$ and $target = 9$. Choosing $a_1 = 2$ and $a_2 = 7$ gives a sum of exactly $9$, so the answer is `YES`.

The two indices must be different: for $n = 1$ the answer is always `NO`.
