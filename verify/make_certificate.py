"""Generate verify/certificate.json: the finite 34-record certificate.

Conventions shared by every script in this directory:

  * the board has three rows (0 = top, 1 = middle, 2 = bottom) and 'width'
    columns; a cell is addressed by  row * width + col;
  * in a board mask, bit (row * width + col) is the cell colour:
    bit 1 = right-turn cell (white in the usual convention), bit 0 = left-turn;
  * headings 0,1,2,3 are east, south, west, north;
  * the block is the rightmost 'width' columns and the ant enters it through
    the left face at (entry, 0), heading east.

A record is a sequence of (entry row, reply) pairs.  The reply is the row in
which the ant leaves the block again through the same (left) face, or -1 when
it escapes through the top, bottom or right side of the board.  P_w(r) is the
largest number of steps the ant can spend inside a w-column right-end block
while realising the complete record r.

The certificate stores every realisable record together with P2, P4 and one
witness (initial board mask, entry word) for each width.  Run this file to
regenerate certificate.json.
"""

import json
from collections import Counter
from pathlib import Path

MAX_VISITS = 6  # only used to detect a hypothetical fifth/sixth visit

DX = (1, 0, -1, 0)
DY = (0, 1, 0, -1)


def run_visit(board, width, entry):
    """Run one visit to the block; return (mutated board, reply, steps)."""
    b = board[:]
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
            return b, row, steps
        if col >= width or row < 0 or row >= 3:
            return b, -1, steps


def enumerate_records(width):
    """Return ({record: (max_steps, initial_mask, entry_word)}, too_deep)."""
    best = {(): (0, None, ())}
    too_deep = []

    for mask in range(1 << (3 * width)):
        board = [(mask >> i) & 1 for i in range(3 * width)]

        def dfs(current, prefix, total, entries, visits, parity):
            allowed = range(3) if parity is None else ((0, 2) if parity == 0 else (1,))
            for entry in allowed:
                after, reply, steps = run_visit(current, width, entry)
                record = prefix + ((entry, reply),)
                here = total + steps
                if here > best.get(record, (-1,))[0]:
                    best[record] = (here, mask, entries + (entry,))
                if reply >= 0:
                    if visits + 1 >= MAX_VISITS:
                        too_deep.append(record)
                    else:
                        dfs(after, record, here, entries + (entry,), visits + 1,
                            entry % 2)

        dfs(board, (), 0, (), 0, None)

    return best, too_deep


def main():
    tables = {}
    for width in (2, 4):
        best, too_deep = enumerate_records(width)
        if too_deep:
            raise AssertionError(
                "width %d: a record returns at depth %d, deeper search needed: %s"
                % (width, MAX_VISITS, too_deep[:3])
            )
        longest = max(len(record) for record in best)
        if longest > 4:
            raise AssertionError("width %d: record with %d visits" % (width, longest))
        tables[width] = best
        print(
            "width %d: %d records from %d initial boards; longest record %d visits"
            % (width, len(best), 1 << (3 * width), longest)
        )

    small, large = tables[2], tables[4]
    if set(small) != set(large):
        raise AssertionError("the two widths do not have the same record set")

    rows = []
    for record in sorted(set(small), key=lambda r: (len(r), r)):
        p2, mask2, entries2 = small[record]
        p4, mask4, entries4 = large[record]
        rows.append(
            {
                "record": [list(pair) for pair in record],
                "P2": p2,
                "P4": p4,
                "diff": p4 - p2,
                "witness2": None
                if mask2 is None
                else {"board": mask2, "entries": list(entries2)},
                "witness4": None
                if mask4 is None
                else {"board": mask4, "entries": list(entries4)},
            }
        )

    diffs = Counter(row["diff"] for row in rows)
    certificate = {
        "description": (
            "Finite certificate for the upper-bound proof of the exact escape "
            "time of Langton's ant on three-row boards: for every realisable "
            "end-block record P4(r) - P2(r) <= 20."
        ),
        "conventions": (
            "3 rows x width columns; cell = row*width+col; board mask bit 1 = "
            "right-turn cell; headings 0,1,2,3 = E,S,W,N; entry from the left "
            "face at (entry,0) heading east; reply = exit row through the left "
            "face, or -1 for escape through another side."
        ),
        "generated_by": "verify/make_certificate.py",
        "widths": [2, 4],
        "max_visits": 4,
        "records": rows,
        "count": len(rows),
        "max_diff": max(row["diff"] for row in rows),
        "diff_distribution": {str(k): v for k, v in sorted(diffs.items())},
        "base_cases": {"1": 2, "2": 12, "3": 17, "4": 28, "5": 37, "6": 48, "7": 57},
    }

    out = Path(__file__).resolve().parent / "certificate.json"
    out.write_text(json.dumps(certificate, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", out.name)
    print(
        "records %d, diff distribution %s, max diff %d"
        % (certificate["count"], certificate["diff_distribution"], certificate["max_diff"])
    )


if __name__ == "__main__":
    main()
