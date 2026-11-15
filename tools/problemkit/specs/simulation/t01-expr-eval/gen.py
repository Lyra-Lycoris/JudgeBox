import random

LIMIT = 10 ** 12


def _trunc_div(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def _factor(rng, limit, depth):
    if depth > 0 and rng.random() < 0.3:
        text, value = _expr(rng, limit, depth - 1, 2)
        return "(" + text + ")", value
    value = rng.randint(0, min(99, limit))
    return str(value), value


def _term(rng, limit, depth):
    text, value = _factor(rng, limit, depth)
    for _ in range(rng.randint(0, 2)):
        if rng.random() < 0.5:
            f_text, f_value = _factor(rng, limit, depth)
            product = value * f_value
            if abs(product) > limit:
                break
            text += "*" + f_text
            value = product
        else:
            f_text, f_value = _factor(rng, limit, depth)
            if f_value == 0:
                f_text, f_value = "1", 1
            text += "/" + f_text
            value = _trunc_div(value, f_value)
    return text, value


def _expr(rng, limit, depth, terms):
    text, value = _term(rng, limit, depth)
    for _ in range(rng.randint(0, terms)):
        op = "+" if rng.random() < 0.5 else "-"
        t_text, t_value = _term(rng, limit, depth)
        candidate = value + t_value if op == "+" else value - t_value
        if abs(candidate) > limit:
            break
        text += op + t_text
        value = candidate
    return text, value


def _big_flat(rng, target, limit):
    text, value = _term(rng, limit, 0)
    while len(text) < target - 20:
        op = "+" if rng.random() < 0.5 else "-"
        f_text, f_value = _factor(rng, limit, 0)
        candidate = value + f_value if op == "+" else value - f_value
        if abs(candidate) > limit:
            op = "+" if value < 0 else "-"
            candidate = value + f_value if op == "+" else value - f_value
        text += op + f_text
        value = candidate
    return text, value


def _big_mixed(rng, target, limit, depth):
    text, value = _term(rng, limit, depth)
    while len(text) < target - 20:
        choice = rng.random()
        if choice < 0.45 or abs(value) > 10 ** 6:
            op = "+" if rng.random() < 0.5 else "-"
            f_text, f_value = _factor(rng, limit, depth)
            candidate = value + f_value if op == "+" else value - f_value
            if abs(candidate) > limit:
                op = "+" if value < 0 else "-"
                candidate = value + f_value if op == "+" else value - f_value
            text += op + f_text
            value = candidate
        elif choice < 0.7:
            factor = rng.randint(2, 9)
            text += "*" + str(factor)
            value *= factor
        else:
            factor = rng.randint(2, 9)
            text += "/" + str(factor)
            value = _trunc_div(value, factor)
    return text, value


def cases():
    rng = random.Random(20261114)
    fixed = [
        "(1+2)*3",
        "7/2",
        "7-10",
        "((1+2)*(3+4))",
        "(3-10)/2",
        "1000000*1000000",
        "2*(3+4*(5-1))",
        "1-2-3-4",
        "999999999+1",
    ]
    out = [{"id": "%02d" % (i + 1), "input": text + "\n"} for i, text in enumerate(fixed)]
    flat, flat_value = _big_flat(rng, 200000, LIMIT)
    out.append({"id": "10", "input": flat + "\n"})
    mixed, mixed_value = _big_mixed(rng, 200000, LIMIT, 2)
    out.append({"id": "11", "input": mixed + "\n"})
    nested, nested_value = _big_mixed(rng, 150000, LIMIT, 3)
    out.append({"id": "12", "input": nested + "\n"})
    return out
