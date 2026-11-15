# Range Add and Restore

You are given an integer sequence $a_1, a_2, \dots, a_n$; initially the $i$-th position holds $a_i$.

Then $q$ operations follow. The $j$-th operation gives three integers $l_j, r_j, v_j$ and adds $v_j$ to every element of the segment $[l_j, r_j]$:

$$a_i \leftarrow a_i + v_j \quad (l_j \le i \le r_j).$$

Apply all operations in order, then output the whole sequence.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

The third line contains one integer $q$.

Each of the next $q$ lines contains three integers $l_j, r_j, v_j$, describing one range-add operation.

### Output

One line with $n$ integers separated by spaces: the sequence after all operations.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le q \le 2 \times 10^5$
- $1 \le l_j \le r_j \le n$
- $-10^9 \le a_i, v_j \le 10^9$
- Every element stays inside $[-2 \times 10^{14}, 2 \times 10^{14}]$ at all times

### Sample explanation

The initial sequence is $1, 2, 3, 4, 5$.

The first operation adds $10$ to $[1, 3]$, so the sequence becomes $11, 12, 13, 4, 5$.

The second operation adds $-4$ to $[2, 5]$, so the sequence becomes $11, 8, 9, 0, 1$.
