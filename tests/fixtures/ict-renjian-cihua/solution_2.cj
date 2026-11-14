package ict02

import std.collection.{ArrayList, HashMap}
import std.math.numeric.BigInt

private class TrieNode {
    let children = HashMap<Rune, TrieNode>()
    var wordId = -1
}

struct WordMatch {
    WordMatch(let end: Int64, let wordId: Int64) {}
}

// 顶点是汉字边界；边表示一个词，并且只保留能继续到达诗句末尾的匹配。
class WordGraph {
    let words: ArrayList<String>
    let edges: Array<ArrayList<WordMatch>>
    let wordBits: Array<BigInt>
    let futureBits: Array<BigInt>

    init(verse: String, dictionary: Array<String>) {
        let text = verse.toRuneArray()
        let (root, tokens) = buildTrie(dictionary, text.size)
        words = tokens
        edges = buildEdges(root, text)
        wordBits = buildWordBits(edges, words.size)
        futureBits = buildFutureBits(edges, wordBits)
    }
}

private func buildTrie(dictionary: Array<String>, length: Int64): (TrieNode, ArrayList<String>) {
    let root = TrieNode()
    let words = ArrayList<String>()
    for (word in dictionary) {
        let letters = word.toRuneArray()
        // 原始词表含连续逗号；忽略空词，保证每条边都向前推进。
        if (letters.isEmpty() || letters.size > length) {
            continue
        }
        var node = root
        for (letter in letters) {
            if (let Some(child) <- node.children.get(letter)) {
                node = child
            } else {
                let newChild = TrieNode()
                node.children[letter] = newChild
                node = newChild
            }
        }
        if (node.wordId < 0) {
            node.wordId = words.size
            words.add(word)
        }
    }
    return (root, words)
}

private func buildEdges(root: TrieNode, text: Array<Rune>): Array<ArrayList<WordMatch>> {
    let edges = Array(text.size + 1) {_ => ArrayList<WordMatch>()}
    let reachable = Array<Bool>(text.size + 1, repeat: false)
    reachable[text.size] = true
    var start = text.size
    while (start > 0) {
        start -= 1
        var node = root
        for (end in start..text.size) {
            if (let Some(child) <- node.children.get(text[end])) {
                node = child
            } else {
                break
            }
            if (node.wordId >= 0 && reachable[end + 1]) {
                edges[start].add(WordMatch(end + 1, node.wordId))
                reachable[start] = true
            }
        }
    }
    return edges
}

private func buildWordBits(edges: Array<ArrayList<WordMatch>>, wordCount: Int64): Array<BigInt> {
    let occurrences = Array<Int64>(wordCount, repeat: 0)
    for (matches in edges) {
        for (edge in matches) {
            occurrences[edge.wordId] += 1
        }
    }
    let bits = Array<BigInt>(wordCount, repeat: BigInt(0))
    var bitIndex = 0
    for (id in 0..wordCount) {
        // 只出现一次的词不可能复用，无需占据集合状态的一位。
        if (occurrences[id] > 1) {
            bits[id] = BigInt(0).setBit(bitIndex)
            bitIndex += 1
        }
    }
    return bits
}

private func buildFutureBits(edges: Array<ArrayList<WordMatch>>, wordBits: Array<BigInt>): Array<BigInt> {
    let future = Array<BigInt>(edges.size, repeat: BigInt(0))
    var index = edges.size - 1
    while (index > 0) {
        index -= 1
        var mask = future[index + 1]
        for (edge in edges[index]) {
            mask = mask | wordBits[edge.wordId]
        }
        future[index] = mask
    }
    return future
}
