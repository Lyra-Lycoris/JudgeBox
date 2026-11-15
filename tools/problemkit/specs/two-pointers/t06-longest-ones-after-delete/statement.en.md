# Longest Run of Ones After Deleting One Element

Given an array $a$ that contains only $0$ and $1$, you must delete **exactly one** element, so the array length becomes $n - 1$. Print the length of the longest contiguous run of $1$s in the resulting array.

Notes:

- You must delete exactly one element, deleting nothing is not allowed;
- the deleted element may be a $1$ or a $0$;
- if the array becomes empty (that is $n = 1$), the answer is $0$.

### Input

The first line contains one integer $n$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$, each of them $0$ or $1$, separated by single spaces.

### Output

One integer: the length of the longest run of $1$s after deleting one element.

### Constraints

- $1 \le n \le 200000$
- $a_i \in \{0, 1\}$

### Sample explanation

Sample 1: $a = [1, 1, 0, 1]$. Deleting the single $0$ gives $[1, 1, 1]$ with a run of length $3$.

Sample 2: $a = [1, 0, 1, 0, 1]$. No deletion merges the runs into anything longer than $2$; deleting a middle $0$ gives $[1, 1, 0, 1]$, so the answer is $2$.

Sample 3: $a = [0, 0, 1, 1, 1, 0, 0]$. Deleting the leftmost or the rightmost $0$ keeps the middle $111$ intact, so the answer is $3$.
