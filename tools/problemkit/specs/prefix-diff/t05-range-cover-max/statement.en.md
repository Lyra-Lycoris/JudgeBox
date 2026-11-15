# Most Frequently Covered Position

A hallway has $n$ consecutive positions numbered $1$ to $n$. There are $q$ cover operations; the $i$-th one gives two integers $l_i, r_i$ and covers every position in $[l_i, r_i]$ once (segments may overlap or be identical).

Let $c_x$ be the number of operations covering position $x$, i.e. the number of indices with $l_i \le x \le r_i$. Output:

1. the maximum coverage $M = \max_x c_x$;
2. the smallest position $p$ with $c_p = M$.

### Input

The first line contains one integer $n$.

The second line contains one integer $q$.

Each of the next $q$ lines contains two integers $l_i, r_i$ describing one cover operation.

### Output

One line with two integers $M$ and $p$ separated by a space.

### Constraints

- $1 \le n \le 2 \times 10^5$
- $1 \le q \le 2 \times 10^5$
- $1 \le l_i \le r_i \le n$

### Sample explanation

The three operations cover $[1,4]$, $[3,5]$ and $[5,6]$. The coverage counts are

$$c_1=1,\ c_2=1,\ c_3=2,\ c_4=2,\ c_5=2,\ c_6=1.$$

The maximum coverage is $2$ and the leftmost position attaining it is $3$, so the output is `2 3`.
