"""朗顿蚂蚁三行棋盘的精确逃逸时间。用 Python 3.8 或更高版本直接运行即可。

设 S(n) 为 3 行 n 列棋盘对所有染色、起点、朝向的最大首次出界步数，
包含迈出棋盘的一步。S(1)=2，S(2)=12。对 n>=3，偶数宽为 10n-12，
奇数宽为 10n-13。

Etse 在 MFCS 2026 论文第 4.3.2 节和图 12 已给出达到上述值的构造。
论文链接为 https://doi.org/10.4230/LIPIcs.MFCS.2026.49 。
本文件核验上界证明所需的两个有限命题。完整归纳如下。

一、从棋盘端部取出一块，蚂蚁的起点在块外。用 (进入行, 回应) 记录每次
访问。回应为原侧返回行或 -1（从其他三边之一逃出整盘）。朝向的横竖
和所在格的棋盘格奇偶每步同时翻转，所以同一条接口的所有进入行同奇偶。
一个记录可在任意一次返回后结束，也可以终止于逃逸。每次访问都继承前次
留下的颜色。P(w,r) 是在宽 w 的端块上实现整条记录 r 的最大累计步数，
只计从块内格子出发的步。空记录取 0。

二、profiles 重建宽 2 和宽 4 的全部记录。这两个宽度恰有同样的 34 条
记录，对每条记录 r 均有 P(4,r)<=P(2,r)+20。核验中没有按时间或深度
截去分支。检查深度的语句如被违反，程序会报错。入口默认在左侧；
把整个棋盘旋转 180 度即得另一侧的结论。

三、宽 n>=8 时，起点两侧至少一侧有 4 列。取该侧最末 4 列，设实际
轨迹在上面的记录为 r。以能实现 P(2,r) 的两列替换端块。第一次进入前，
外部运动相同。每次返回的行和朝向相同，且外部染色在一次块内访问期间
不变。按访问次数归纳，替换后的外部轨迹与原来逐段相同；如在块内逃逸，
两者均终止。新轨迹至多比原轨迹少 20 步，故 S(n)<=S(n-2)+20。
exact_small 给出宽 1 到 7 的精确基例。对奇偶宽分别归纳，再用 Etse 的
下界即得等号。证明只对三行成立。

For the implementation the headings are east, south, west, north (0 through 3).
Bit 1 means a right-turn cell. Row 0 is the top row.
"""

from collections import Counter


def moves(width):
    """Next cell after moving in each heading. -1 denotes a board exit."""
    result = []
    for cell in range(3 * width):
        row, col = divmod(cell, width)
        result.append((
            cell + 1 if col + 1 < width else -1,
            cell + width if row < 2 else -1,
            cell - 1 if col else -1,
            cell - width if row else -1,
        ))
    return result


def profiles(width):
    """Maximum local time for each complete or partial entry/response record."""
    next_cell = moves(width)
    maxima = {(): 0}

    def enumerate_records(board, rows, prefix, previous_steps):
        if len(prefix) >= 4:
            raise AssertionError("A fourth return would permit a fifth entry")
        for entry in rows:
            colors = board
            cell = entry * width
            heading = 0
            steps = previous_steps
            while cell >= 0:
                last = cell
                bit = 1 << cell
                heading = (heading + (1 if colors & bit else -1)) % 4
                colors ^= bit
                cell = next_cell[cell][heading]
                steps += 1
            # Returning through the entry face makes a further entry possible.
            returned = heading == 2
            reply = last // width if returned else -1
            record = prefix + ((entry, reply),)
            maxima[record] = max(steps, maxima.get(record, 0))
            if returned:
                enumerate_records(colors, rows, record, steps)

    for board in range(1 << (3 * width)):
        for rows in ((0, 2), (1,)):
            enumerate_records(board, rows, (), 0)
    return maxima


def exact_small(width):
    """Direct search from all 12*width poses, branching on first cell visits."""
    next_cell = moves(width)

    def walk(cell, heading, known, colors):
        if cell < 0:
            return 0
        bit = 1 << cell
        if known & bit:
            new_heading = (heading + (1 if colors & bit else -1)) % 4
            return 1 + walk(next_cell[cell][new_heading], new_heading,
                            known, colors ^ bit)
        left = (heading - 1) % 4
        right = (heading + 1) % 4
        # A first left turn leaves a right-turn cell and vice versa.
        return 1 + max(walk(next_cell[cell][left], left, known | bit, colors | bit),
                       walk(next_cell[cell][right], right, known | bit, colors))

    return max(walk(cell, heading, 0, 0)
               for cell in range(3 * width) for heading in range(4))


def main():
    small, large = profiles(2), profiles(4)
    if small.keys() != large.keys() or len(large) != 34:
        raise AssertionError("The two transcript sets should agree and have size 34")
    gains = Counter(large[key] - small[key] for key in large)
    expected = {0: 3, 8: 20, 15: 1, 16: 2, 20: 8}
    if gains != expected:
        raise AssertionError(f"Unexpected differences: {gains}")

    print("Entry>reply (X = escape) | width 2 | width 4 | difference")
    for record in sorted(small):
        pairs = [f"{entry}>{'X' if reply < 0 else reply}" for entry, reply in record]
        label = " ".join(pairs) or "(no entry)"
        print(f"{label:24s} {small[record]:8d} {large[record]:9d}"
              f" {large[record] - small[record]:12d}")
    base = [exact_small(n) for n in range(1, 8)]
    if base != [2, 12, 17, 28, 37, 48, 57]:
        raise AssertionError(f"Unexpected base cases: {base}")
    print(f"Widths 1 to 7: {base}")
    print("PASS: 34 transcripts, maximum difference 20, all seven base cases.")


if __name__ == "__main__":
    main()
