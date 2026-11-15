import random

SEED = 20261114
PAIRS = {"(": ")", "[": "]", "{": "}"}


def random_valid(n, rng):
    """生成一个长度为 n（n 为偶数）的合法括号序列。"""
    result = []
    stack = []
    for i in range(n):
        left = n - i
        can_open = len(stack) + 1 <= left - 1
        can_close = len(stack) > 0
        if can_open and (not can_close or rng.random() < 0.55):
            ch = rng.choice("([{")
            stack.append(ch)
            result.append(ch)
        else:
            result.append(PAIRS[stack.pop()])
    assert not stack
    return "".join(result)


def cases():
    rng = random.Random(SEED)
    big_valid = random_valid(200000, rng)
    big_broken = "]" + big_valid[1:]
    medium_valid = random_valid(2000, rng)
    return [
        {"id": "01", "input": "()[]{}\n"},
        {"id": "02", "input": "(\n"},
        {"id": "03", "input": "]\n"},
        {"id": "04", "input": "([()]){}\n"},
        {"id": "05", "input": "(" * 100000 + ")" * 100000 + "\n"},
        {"id": "06", "input": "(" * 200000 + "\n"},
        {"id": "07", "input": "]]][[[[\n"},
        {"id": "08", "input": medium_valid + "\n"},
        {"id": "09", "input": "()" * 100000 + "\n"},
        {"id": "10", "input": big_valid + "\n"},
        {"id": "11", "input": big_broken + "\n"},
    ]
