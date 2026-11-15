def solve(expr: str) -> int:
    values = []
    ops = []
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

    def apply_top():
        op = ops.pop()
        b = values.pop()
        a = values.pop()
        if op == "+":
            values.append(a + b)
        elif op == "-":
            values.append(a - b)
        elif op == "*":
            values.append(a * b)
        else:
            quotient = abs(a) // abs(b)
            values.append(quotient if (a < 0) == (b < 0) else -quotient)

    index = 0
    length = len(expr)
    while index < length:
        ch = expr[index]
        if ch.isdigit():
            number = 0
            while index < length and expr[index].isdigit():
                number = number * 10 + (ord(expr[index]) - 48)
                index += 1
            values.append(number)
            continue
        if ch == "(":
            ops.append(ch)
        elif ch == ")":
            while ops and ops[-1] != "(":
                apply_top()
            ops.pop()
        else:
            while ops and ops[-1] != "(" and precedence[ops[-1]] >= precedence[ch]:
                apply_top()
            ops.append(ch)
        index += 1
    while ops:
        apply_top()
    return values[0]
