import random

DIGITS = 100000


def _random_number(length, rng):
    digits = [str(rng.randint(1, 9))]
    digits += [str(rng.randint(0, 9)) for _ in range(length - 1)]
    return "".join(digits)


def _case(a, b):
    return {"input": a + "\n" + b + "\n"}


def cases():
    rng = random.Random(20261120)
    out = []

    # 01 样例
    out.append(dict(id="01", **_case("12345678901234567890", "98765432109876543210")))

    # 02 零加零
    out.append(dict(id="02", **_case("0", "0")))

    # 03 零加一个大数
    out.append(dict(id="03", **_case("0", "999999999999999999999999")))

    # 04 两个十万位的全 9 数，答案会产生新的最高位
    out.append(dict(id="04", **_case("9" * DIGITS, "9" * DIGITS)))

    # 05 两个十万位随机数
    out.append(dict(id="05", **_case(_random_number(DIGITS, rng), _random_number(DIGITS, rng))))

    # 06 十万位 + 一位
    out.append(dict(id="06", **_case(_random_number(DIGITS, rng), "7")))

    # 07 长度相差很大的两个数
    out.append(dict(id="07", **_case(_random_number(99999, rng), _random_number(12345, rng))))

    # 08 连续进位：1 后面跟 99999 个 0，再加 1
    out.append(dict(id="08", **_case("1" + "0" * 99999, "1")))

    # 09 最小的非零情况
    out.append(dict(id="09", **_case("1", "1")))

    # 10 十万位全 9 加 1
    out.append(dict(id="10", **_case("9" * DIGITS, "1")))
    return out
