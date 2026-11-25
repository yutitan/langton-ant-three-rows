"""End-to-end test of the four-column -> two-column replacement.

For a random 3 x n board (n in {8,9,10}) and a random starting pose outside
the right-end four-column block:

  1. run the actual trajectory and extract its end-block record r;
  2. find a two-column block that realises r and maximises the number of
     steps spent inside the block (P2(r));
  3. build the width n-2 board: the old outside columns plus the new
     two-column block;
  4. run the new trajectory.

The proof claims that the new trajectory keeps the same record and loses at
most 20 steps, so T_new >= T_old - 20.  This test checks that claim directly
on 400 random instances.

Rows 0,1,2 are top, middle, bottom.  Headings 0,1,2,3 are E,S,W,N.  Bit 1 is
a right-turn cell.
"""

import random

DX = (1, 0, -1, 0)
DY = (0, 1, 0, -1)


def run(board, width, row, col, heading, block_width):
    """Return (steps, record, internal_steps) for the right-end block."""
    b = board[:]
    block_start = width - block_width
    steps = 0
    internal = 0
    record = []
    entry = None
    while True:
        cell = row * width + col
        bit = b[cell]
        heading = (heading + (1 if bit else 3)) & 3
        b[cell] = 1 - bit
        new_row = row + DY[heading]
        new_col = col + DX[heading]
        inside = col >= block_start
        steps += 1
        if inside:
            internal += 1
        if col == block_start - 1 and new_col == block_start and 0 <= new_row < 3:
            entry = new_row
        if inside and not (0 <= new_row < 3 and 0 <= new_col < width):
            record.append((entry, -1))
            return steps, tuple(record), internal
        if inside and new_col == block_start - 1:
            record.append((entry, new_row))
            entry = None
        row, col = new_row, new_col
        if not (0 <= row < 3 and 0 <= col < width):
            return steps, tuple(record), internal


def block_profile(width):
    """Maximum steps inside a w-column end block for every record."""
    maxima = {(): 0}
    for mask in range(1 << (3 * width)):
        board = [(mask >> i) & 1 for i in range(3 * width)]

        def dfs(current, prefix, total, parity):
            if len(prefix) >= 6:
                raise AssertionError("unexpected sixth visit")
            allowed = range(3) if parity is None else ((0, 2) if parity == 0 else (1,))
            for entry in allowed:
                b = current[:]
                row, col, heading = entry, 0, 0
                steps = 0
                while True:
                    cell = row * width + col
                    bit = b[cell]
                    heading = (heading + (1 if bit else 3)) & 3
                    b[cell] = 1 - bit
                    row += DY[heading]
                    col += DX[heading]
                    steps += 1
                    if col < 0:
                        record = prefix + ((entry, row),)
                        maxima[record] = max(maxima.get(record, -1), total + steps)
                        dfs(b, record, total + steps, entry % 2)
                        break
                    if col >= width or row < 0 or row >= 3:
                        record = prefix + ((entry, -1),)
                        maxima[record] = max(maxima.get(record, -1), total + steps)
                        break

        dfs(board, (), 0, None)
    return maxima


def two_column_realisation(record):
    """Best two-column witness for a given record (board mask, steps)."""
    if not record:
        # The ant never entered the block, so its colouring is irrelevant.
        return 0, 0
    best_mask, best_steps = None, -1
    for mask in range(1 << 6):
        board = [(mask >> i) & 1 for i in range(6)]
        ok = True
        total = 0
        current = board
        for entry, reply in record:
            b = current[:]
            row, col, heading = entry, 0, 0
            steps = 0
            while True:
                cell = row * 2 + col
                bit = b[cell]
                heading = (heading + (1 if bit else 3)) & 3
                b[cell] = 1 - bit
                row += DY[heading]
                col += DX[heading]
                steps += 1
                if col < 0:
                    got = row
                    break
                if col >= 2 or row < 0 or row >= 3:
                    got = -1
                    break
            if got != reply:
                ok = False
                break
            total += steps
            current = b
        if ok and total > best_steps:
            best_mask, best_steps = mask, total
    return best_mask, best_steps


def main(trials=400, seed=42):
    random.seed(seed)
    profile2 = block_profile(2)
    checked = 0
    failures = []
    gains = []
    for _ in range(trials):
        width = random.choice([8, 9, 10])
        mask = random.getrandbits(3 * width)
        board = [(mask >> i) & 1 for i in range(3 * width)]
        start_col = random.randrange(0, width - 4)
        start_row = random.randrange(0, 3)
        start_heading = random.randrange(0, 4)

        old_steps, record, _ = run(board, width, start_row, start_col, start_heading, 4)
        block2, block_steps = two_column_realisation(record)
        if block2 is None:
            failures.append(("no two-column realisation", width, record))
            continue

        new_width = width - 2
        new_board = [0] * (3 * new_width)
        for row in range(3):
            for col in range(width - 4):
                new_board[row * new_width + col] = board[row * width + col]
            for col in range(2):
                new_board[row * new_width + (width - 4 + col)] = (block2 >> (row * 2 + col)) & 1

        new_steps, new_record, _ = run(
            new_board, new_width, start_row, start_col, start_heading, 2
        )
        checked += 1
        gains.append(old_steps - new_steps)
        if new_record != record or new_steps < old_steps - 20:
            failures.append((width, old_steps, new_steps, record, new_record))

    print("trials:", checked, "failures:", len(failures))
    if checked:
        print(
            "steps lost: min %d, max %d, mean %.1f"
            % (min(gains), max(gains), sum(gains) / len(gains))
        )
    for failure in failures[:5]:
        print("FAILURE:", failure)
    if failures:
        raise AssertionError("replacement test failed")
    print("PASS: every replacement keeps the record and loses at most 20 steps")


if __name__ == "__main__":
    main()
