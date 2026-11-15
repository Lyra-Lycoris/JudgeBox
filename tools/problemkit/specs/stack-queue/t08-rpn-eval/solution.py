def solve(k: int, tokens: list[str]) -> int:
    stack = []
    for token in tokens:
        if len(token) == 1 and token in "+-*/":
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            else:
                quotient = abs(a) // abs(b)
                stack.append(quotient if (a < 0) == (b < 0) else -quotient)
        else:
            stack.append(int(token))
    return stack[-1]
