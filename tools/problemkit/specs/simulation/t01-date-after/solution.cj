package t01_date_after

func isLeapYear(year: Int64): Bool {
    return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0)
}

func daysBeforeYear(year: Int64): Int64 {
    let t = year - 1
    return t * 365 + t / 4 - t / 100 + t / 400
}

func dayOfYear(year: Int64, month: Int64, day: Int64): Int64 {
    let cum = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    var value = cum[month] + day - 1
    if (month > 2 && isLeapYear(year)) {
        value += 1
    }
    return value
}

func daysInMonth(year: Int64, month: Int64): Int64 {
    if (month == 2) {
        return if (isLeapYear(year)) {
            29
        } else {
            28
        }
    }
    if (month == 4 || month == 6 || month == 9 || month == 11) {
        return 30
    }
    return 31
}

func padNumber(value: Int64, width: Int64): String {
    var text = value.toString()
    while (text.size < width) {
        text = "0" + text
    }
    return text
}

func solve(y: Int64, m: Int64, d: Int64, k: Int64): String {
    let total = daysBeforeYear(y) + dayOfYear(y, m, d) + k
    var lo = 1
    var hi = 1 + total / 365 + 2
    while (lo < hi) {
        let mid = (lo + hi + 1) / 2
        if (daysBeforeYear(mid) <= total) {
            lo = mid
        } else {
            hi = mid - 1
        }
    }
    let year = lo
    var doy = total - daysBeforeYear(year)
    var month = 1
    while (true) {
        let length = daysInMonth(year, month)
        if (doy < length) {
            break
        }
        doy -= length
        month += 1
    }
    return padNumber(year, 4) + "-" + padNumber(month, 2) + "-" + padNumber(doy + 1, 2)
}
