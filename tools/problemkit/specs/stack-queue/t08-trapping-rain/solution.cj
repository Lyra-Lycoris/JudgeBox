package t08_trapping_rain

func solve(n: Int64, h: Array<Int64>): Int64 {
    var left = 0
    var right = n - 1
    var leftMax = 0
    var rightMax = 0
    var water = 0
    while (left <= right) {
        if (h[left] <= h[right]) {
            if (h[left] >= leftMax) {
                leftMax = h[left]
            } else {
                water += leftMax - h[left]
            }
            left += 1
        } else {
            if (h[right] >= rightMax) {
                rightMax = h[right]
            } else {
                water += rightMax - h[right]
            }
            right -= 1
        }
    }
    return water
}
