package t01_queue_windows

func solve(n: Int64, k: Int64, arrive: Array<Int64>, serve: Array<Int64>): Int64 {
    let heap = MinHeap(k)
    for (_ in 0..k) {
        heap.push(0)
    }
    var total = 0
    for (i in 0..n) {
        let free = heap.pop()
        var start = free
        if (arrive[i] > free) {
            start = arrive[i]
        }
        total += start - arrive[i]
        heap.push(start + serve[i])
    }
    return total
}

class MinHeap {
    private var data: Array<Int64>
    private var heapSize: Int64

    init(capacity: Int64) {
        this.data = Array<Int64>(max(capacity, 1), repeat: 0)
        this.heapSize = 0
    }

    func push(value: Int64): Unit {
        var index = this.heapSize
        this.data[index] = value
        this.heapSize += 1
        while (index > 0) {
            let parent = (index - 1) / 2
            if (this.data[parent] > this.data[index]) {
                let temp = this.data[parent]
                this.data[parent] = this.data[index]
                this.data[index] = temp
                index = parent
            } else {
                break
            }
        }
    }

    func pop(): Int64 {
        let top = this.data[0]
        this.heapSize -= 1
        this.data[0] = this.data[this.heapSize]
        var index = 0
        while (true) {
            let left = 2 * index + 1
            let right = left + 1
            var smallest = index
            if (left < this.heapSize && this.data[left] < this.data[smallest]) {
                smallest = left
            }
            if (right < this.heapSize && this.data[right] < this.data[smallest]) {
                smallest = right
            }
            if (smallest == index) {
                break
            }
            let temp = this.data[smallest]
            this.data[smallest] = this.data[index]
            this.data[index] = temp
            index = smallest
        }
        return top
    }
}
