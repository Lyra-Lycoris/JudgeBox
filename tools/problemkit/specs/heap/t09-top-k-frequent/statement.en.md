# Top K Frequent Elements

Given $n$ integers, find the $k$ **distinct** values that appear most often. Order of the output: higher frequency first; among equal frequencies, the smaller value first.

### Input

The first line contains two integers $n$ and $k$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$.

### Output

One line with the $k$ chosen values in the required order, separated by spaces.

### Constraints

- $1 \le n \le 200000$
- $1 \le k \le$ the number of distinct values in the array
- $|a_i| \le 10^9$

### Sample Explanation

For $[1, 1, 1, 2, 2, 3]$: the value $1$ appears $3$ times, $2$ appears $2$ times and $3$ appears once. The top two are $1$ and $2$, so the output is `1 2`.
