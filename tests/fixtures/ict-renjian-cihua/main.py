import sys


# 批量输入：用例数；每组依次给诗句、词数及逐行排列的词。
def main():
    lines = sys.stdin.buffer.read().decode("utf-8").split("\n")
    position = 0
    cases = int(lines[position].strip())
    position += 1
    output = []
    for _ in range(cases):
        verse = lines[position].strip()
        position += 1
        count = int(lines[position].strip())
        position += 1
        words = [lines[position + i].strip() for i in range(count)]
        position += count
        answers = solve(verse, words)
        output.append(str(len(answers)))
        output.extend(answers)
    sys.stdout.write("\n".join(output) + ("\n" if output else ""))


main()
