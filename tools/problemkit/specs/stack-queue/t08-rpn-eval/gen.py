import random

SEED = 20261114
MAX_ABS = 10 ** 9
WRAP = 20


class Overflow(Exception):
    pass


def trunc_div(a, b):
    quotient = abs(a) // abs(b)
    return quotient if (a < 0) == (b < 0) else -quotient


def build_rpn(rng, ops_count, ops="+-*/", leaf_bound=1000):
    """随机生成一个运算数个数为 ops_count+1 的合法逆波兰表达式。"""
    tokens = []
    stack = []
    ops_left = ops_count
    leaves_left = ops_count + 1
    while ops_left > 0 or leaves_left > 0:
        size = len(stack)
        if leaves_left == 0:
            take_op = True
        elif ops_left == 0:
            take_op = False
        elif size < 2 or size == ops_left + 1:
            take_op = False
        else:
            take_op = rng.random() < 0.45
        if not take_op:
            value = rng.randint(-leaf_bound, leaf_bound)
            stack.append(value)
            tokens.append(str(value))
            leaves_left -= 1
            continue
        op = rng.choice(ops)
        b = stack.pop()
        a = stack.pop()
        if op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                op = "+"
                result = a + b
            else:
                result = trunc_div(a, b)
        elif op == "-":
            result = a - b
        else:
            result = a + b
        if abs(result) > MAX_ABS:
            raise Overflow
        stack.append(result)
        tokens.append(op)
        ops_left -= 1
    assert len(stack) == 1
    return tokens


def expression(rng, ops_count, ops="+-*/", leaf_bound=1000):
    for _ in range(1000):
        try:
            return build_rpn(rng, ops_count, ops, leaf_bound)
        except Overflow:
            continue
    raise RuntimeError("无法生成满足范围要求的表达式")


def pack(tokens):
    lines = []
    for start in range(0, len(tokens), WRAP):
        lines.append(" ".join(tokens[start:start + WRAP]))
    return "%d\n%s\n" % (len(tokens), "\n".join(lines))


def cases():
    rng = random.Random(SEED)
    deep = ["1"]
    for _ in range(99999):
        deep.append("1")
        deep.append("+")
    return [
        {"id": "01", "input": "5\n3 4 + 2 *\n"},
        {"id": "02", "input": "3\n-7 2 /\n"},
        {"id": "03", "input": "1\n42\n"},
        {"id": "04", "input": "7\n5 1 2 + 4 * + 3 -\n"},
        {"id": "05", "input": "1\n-1000000000\n"},
        {"id": "06", "input": pack(expression(rng, 20, "+-*/", 10))},
        {"id": "07", "input": pack(expression(rng, 200, "+-*", 5))},
        {"id": "08", "input": pack(expression(rng, 2000, "/-", 100000))},
        {"id": "09", "input": pack(deep)},
        {"id": "10", "input": pack(expression(rng, 99999, "+-", 1000))},
        {"id": "11", "input": pack(expression(rng, 20000, "+*/", 3))},
    ]
