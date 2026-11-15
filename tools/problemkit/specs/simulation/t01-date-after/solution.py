def _is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_before_year(year):
    t = year - 1
    return t * 365 + t // 4 - t // 100 + t // 400


def _day_of_year(year, month, day):
    cum = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
    value = cum[month - 1] + day - 1
    if month > 2 and _is_leap(year):
        value += 1
    return value


def _days_in_month(year, month):
    if month == 2:
        return 29 if _is_leap(year) else 28
    if month in (4, 6, 9, 11):
        return 30
    return 31


def solve(y: int, m: int, d: int, k: int) -> str:
    total = _days_before_year(y) + _day_of_year(y, m, d) + k
    lo, hi = 1, 1 + total // 365 + 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if _days_before_year(mid) <= total:
            lo = mid
        else:
            hi = mid - 1
    year = lo
    doy = total - _days_before_year(year)
    month = 1
    while True:
        length = _days_in_month(year, month)
        if doy < length:
            break
        doy -= length
        month += 1
    return "%04d-%02d-%02d" % (year, month, doy + 1)
