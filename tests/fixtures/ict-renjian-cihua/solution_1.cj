package ict02

import std.collection.{ArrayList, HashMap}
import std.math.numeric.BigInt

func solve(verse: String, words: Array<String>): Array<String> {
    if (verse.isEmpty()) {
        return []
    }
    return VerseSolver(WordGraph(verse, words)).run()
}

private class VerseSolver {
    let graph: WordGraph
    let memo: Array<HashMap<BigInt, Int64>>
    let path: Array<String>
    let answers = ArrayList<String>()

    init(graph: WordGraph) {
        this.graph = graph
        memo = Array(graph.edges.size) {_ => HashMap<BigInt, Int64>()}
        path = Array<String>(graph.edges.size - 1, repeat: "")
    }

    func run(): Array<String> {
        if (graph.edges[0].isEmpty()) {
            return []
        }
        collect(0, BigInt(0), 0)
        return answers.toArray()
    }

    // used 只记录“以前用过、以后仍可能出现”的词；返回后缀最少还需引入的词数。
    private func minimumCost(index: Int64, used: BigInt): Int64 {
        if (index == path.size) {
            return 0
        }
        if (let Some(cost) <- memo[index].get(used)) {
            return cost
        }
        var best = graph.edges.size
        for (edge in graph.edges[index]) {
            let (extra, nextUsed) = advance(used, edge)
            best = min(best, extra + minimumCost(edge.end, nextUsed))
            if (best == 0) {
                break
            }
        }
        memo[index][used] = best
        return best
    }

    private func advance(used: BigInt, edge: WordMatch): (Int64, BigInt) {
        let bit = graph.wordBits[edge.wordId]
        let extra = if ((used & bit) == BigInt(0)) {
            1
        } else {
            0
        }
        // 越过某个词的最后匹配位置后，该词可以安全地从状态中遗忘。
        let nextUsed = (used | bit) & graph.futureBits[edge.end]
        return (extra, nextUsed)
    }

    private func collect(index: Int64, used: BigInt, depth: Int64): Unit {
        if (index == path.size) {
            answers.add(String.join(path[..depth], delimiter: " "))
            return
        }
        let best = minimumCost(index, used)
        for (edge in graph.edges[index]) {
            let (extra, nextUsed) = advance(used, edge)
            if (extra + minimumCost(edge.end, nextUsed) == best) {
                path[depth] = graph.words[edge.wordId]
                collect(edge.end, nextUsed, depth + 1)
            }
        }
    }
}
