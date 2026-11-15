import random

DIGITS = 5000


def _random_number(length, rng):
    digits = [str(rng.randint(1, 9))]
    digits += [str(rng.randint(0, 9)) for _ in range(length - 1)]
    return "".join(digits)


def _case(a, b):
    return {"input": a + "\n" + b + "\n"}


def cases():
    rng = random.Random(20261121)
    out = []

    # 01 样例
    out.append(dict(id="01", **_case("123456789", "987654321")))

    # 02 乘以 0
    out.append(dict(id="02", **_case("0", "123456789012345678901234567890")))

    # 03 最小规模
    out.append(dict(id="03", **_case("1", "1")))

    # 04 两个 5000 位的全 9 数
    out.append(dict(id="04", **_case("9" * DIGITS, "9" * DIGITS)))

    # 05 两个 5000 位随机数
    out.append(dict(id="05", **_case(_random_number(DIGITS, rng), _random_number(DIGITS, rng))))

    # 06 10 的幂乘以随机大数
    out.append(dict(id="06", **_case("1" + "0" * (DIGITS - 1), _random_number(DIGITS, rng))))

    # 07 一位数乘以 5000 位数
    out.append(dict(id="07", **_case("9", _random_number(DIGITS, rng))))

    # 08 5000 位数乘以一位数
    out.append(dict(id="08", **_case(_random_number(DIGITS, rng), "7")))

    # 09 两个 2500 位随机数
    out.append(dict(id="09", **_case(_random_number(2500, rng), _random_number(2500, rng))))

    # 10 4999 个 9 乘以 9
    out.append(dict(id="10", **_case("9" * (DIGITS - 1), "9")))
    return out
