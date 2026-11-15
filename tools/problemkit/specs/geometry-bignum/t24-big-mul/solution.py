import sys

try:
    sys.set_int_max_str_digits(0)
except AttributeError:
    pass


def solve(a: str, b: str) -> str:
    return str(int(a) * int(b))
