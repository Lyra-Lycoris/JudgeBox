# Remove Adjacent Duplicates

You are given a string $s$ of lowercase letters and an integer $k$ with $k \ge 2$.

Repeatedly perform the following operation until the string contains no $k$ equal characters in a row:

- choose any block of exactly $k$ identical adjacent characters and delete all of them, joining the remaining parts together.

After a deletion the characters on both sides may become adjacent, which can create new deletable blocks. It can be shown that the final string does not depend on the order of deletions. Print that final string.

### Input

- The first line contains one integer $k$.
- The second line contains the string $s$ of lowercase letters without whitespace.

### Output

One line with the final string. If every character is deleted, print an empty line.

### Constraints

- $2 \le k \le 200000$;
- $1 \le |s| \le 200000$;
- $s$ contains only lowercase letters `a` to `z`.

Hint: simulating the deletions one by one takes $O(|s|^2)$ time in the worst case and will not pass the largest tests.

### Sample explanation

Sample 1: $s = $ `abbaca`, $k = 2$.

- Delete the two `b` characters in the middle, obtaining `aaca`;
- delete the two leading `a` characters, obtaining `ca`;
- no two equal neighbours remain, so the answer is `ca`.

Sample 2: $s = $ `aaabb`, $k = 3$.

- Delete the three leading `a` characters, obtaining `bb`;
- `bb` has only two characters, fewer than $k = 3$, so nothing can be deleted and the answer is `bb`.
