# Two Numbers Appearing Once

Given $n$ integers $a_1, a_2, \dots, a_n$, **exactly two of them appear once** and every other integer appears **exactly twice**.

Find those two integers and output them in **increasing** order.

### Input

- The first line contains one integer $n$.
- The second line contains $n$ integers $a_1, a_2, \dots, a_n$, separated by single spaces.

### Output

One line with the two integers in increasing order, separated by one space.

### Constraints

- $2 \le n \le 200000$, and $n$ is even;
- $-10^9 \le a_i \le 10^9$, so the input may contain negative numbers.

The input is guaranteed to contain exactly two values occurring once and all other values occurring exactly twice, so the answer is unique.

Negative numbers are stored in two's complement, so the bit tricks below work for them as well.

### Sample explanation

**Sample 1**: $n = 6$ and the array is $1, 2, 1, 3, 2, 5$.

Here $1$ appears twice and $2$ appears twice, while $3$ and $5$ appear once each, so the output is `3 5`.

**Sample 2**: $n = 2$ and the array is $-4, 9$. Both values appear once, so the output is `-4 9`.

### Hint

XOR all numbers together; values appearing twice cancel out and we get $x = p \oplus q$, where $p, q$ are the answers. Since $p \ne q$ we have $x \ne 0$.

Let `lowbit = x & (-x)`, the lowest set bit of $x$. The values $p$ and $q$ must differ in this bit, so split the array into two groups by that bit and XOR each group separately; one group yields $p$ and the other yields $q$.

This is $O(n)$ time and $O(1)$ extra space. A hash map that counts occurrences ($O(n)$ space) is also accepted.
