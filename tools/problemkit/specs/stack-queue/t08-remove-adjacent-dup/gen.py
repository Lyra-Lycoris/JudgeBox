import random

SEED = 20261114


def final_form(s, k):
    """与参考解相同的栈式算法，用于确认用例答案非空。"""
    stack = []
    for ch in s:
        if stack and stack[-1][0] == ch:
            stack[-1][1] += 1
            if stack[-1][1] == k:
                stack.pop()
        else:
            stack.append([ch, 1])
    return "".join(ch * count for ch, count in stack)


def make_case(k, s):
    """把 (k, s) 打包成输入；保证最终结果非空，不出现空答案。"""
    if final_form(s, k) == "":
        s = (s[:199999] if len(s) >= 200000 else s) + "z"
    assert final_form(s, k) != "", (k, s[:20])
    return "%d\n%s\n" % (k, s)


def blocks(rng, total, min_len, max_len):
    alphabet = "abcdefghij"
    parts = []
    length = 0
    while length < total:
        ch = rng.choice(alphabet)
        run = min(rng.randint(min_len, max_len), total - length)
        parts.append(ch * run)
        length += run
    return "".join(parts)


def cases():
    rng = random.Random(SEED)
    random_two = "".join(rng.choice("abc") for _ in range(200000))
    random_three = "".join(rng.choice("abcd") for _ in range(200000))
    return [
        {"id": "01", "input": "2\nabbaca\n"},
        {"id": "02", "input": "3\naaabb\n"},
        {"id": "03", "input": make_case(2, "a")},
        {"id": "04", "input": make_case(2, "aaaaa")},
        {"id": "05", "input": make_case(2, "abbaa")},
        {"id": "06", "input": make_case(3, "abbbba")},
        {"id": "07", "input": make_case(99999, "a" * 200000)},
        {"id": "08", "input": make_case(2, random_two)},
        {"id": "09", "input": make_case(3, random_three)},
        {"id": "10", "input": make_case(4, blocks(rng, 200000, 1, 8))},
        {"id": "11", "input": make_case(2, "a" * 199999)},
        {"id": "12", "input": make_case(2, "ab" * 100000)},
    ]


if __name__ == "__main__":
    for case in cases():
        k, s = case["input"].split("\n")[0], case["input"].split("\n")[1]
        print(case["id"], "k=%s" % k, "n=%d" % len(s), "->", repr(final_form(s, int(k))[:20]))
