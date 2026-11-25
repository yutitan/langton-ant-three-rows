"""Independent enumeration of the 34 end-block records.

This file deliberately does not import verify_three_row_ant.py.  It re-derives
from the Langton-ant rule alone the two finite facts used by the upper-bound
proof:

  * widths 2 and 4 realise exactly the same 34 entry/response records, and
  * for every such record  P4(r) - P2(r) <= 20.

The enumeration explores the block alone, with no time cut-off and no depth
cut-off below six visits; it reports if any record would need a fifth visit.
The values are compared against verify/certificate.json (which is produced by
verify/make_certificate.py, an independent generator).

Rows 0,1,2 are top, middle, bottom.  Headings 0,1,2,3 are E,S,W,N.  Bit 1 is
a right-turn cell.
"""

import json
from collections import Counter
from pathlib import Path

MAX_VISITS = 6
EXPECTED_DISTRIBUTION = {"0": 3, "8": 20, "15": 1, "16": 2, "20": 8}

DX = (1, 0, -1, 0)
DY = (0, 1, 0, -1)


def run_visit(board, width, entry):
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
    """Return ({record: max_steps}, too_deep)."""
    maxima = {(): 0}
    too_deep = []
    for mask in range(1 << (3 * width)):
        board = [(mask >> i) & 1 for i in range(3 * width)]

        def dfs(current, prefix, total, visits, parity):
            allowed = range(3) if parity is None else ((0, 2) if parity == 0 else (1,))
            for entry in allowed:
                after, reply, steps = run_visit(current, width, entry)
                record = prefix + ((entry, reply),)
                if total + steps > maxima.get(record, -1):
                    maxima[record] = total + steps
                if reply >= 0:
                    if visits + 1 >= MAX_VISITS:
                        too_deep.append(record)
                    else:
                        dfs(after, record, total + steps, visits + 1, entry % 2)

        dfs(board, (), 0, 0, None)
    return maxima, too_deep


def main():
    certificate = json.loads(
        (Path(__file__).resolve().parent / "certificate.json").read_text(encoding="utf-8")
    )
    expected = {
        tuple(tuple(pair) for pair in item["record"]): (item["P2"], item["P4"])
        for item in certificate["records"]
    }

    tables = {}
    for width in (2, 4):
        maxima, too_deep = enumerate_records(width)
        if too_deep:
            raise AssertionError("width %d needs a deeper search: %s" % (width, too_deep[:3]))
        longest = max(len(record) for record in maxima)
        if longest > 4:
            raise AssertionError("width %d: record with %d visits" % (width, longest))
        tables[width] = maxima
        print("width %d: %d records, longest record %d visits" % (width, len(maxima), longest))

    small, large = tables[2], tables[4]
    if set(small) != set(large):
        raise AssertionError(
            "record sets differ: extra in width 2 %r, extra in width 4 %r"
            % (sorted(set(small) - set(large))[:3], sorted(set(large) - set(small))[:3])
        )

    if set(expected) != set(small):
        raise AssertionError(
            "certificate mismatch: extra in certificate %r, missing from certificate %r"
            % (sorted(set(expected) - set(small))[:3], sorted(set(small) - set(expected))[:3])
        )

    for record in small:
        if (small[record], large[record]) != expected[record]:
            raise AssertionError(
                "record %r: independent (%d, %d) vs certificate %r"
                % (record, small[record], large[record], expected[record])
            )
        parities = {entry % 2 for entry, _ in record}
        if len(parities) > 1:
            raise AssertionError("record %r mixes entry-row parities" % (record,))

    diffs = Counter(large[r] - small[r] for r in small)
    distribution = {str(k): v for k, v in sorted(diffs.items())}
    if distribution != EXPECTED_DISTRIBUTION:
        raise AssertionError("unexpected difference distribution: %r" % (distribution,))
    if max(diffs) != 20:
        raise AssertionError("expected maximum difference 20, got %d" % max(diffs))
    if small[()] != 0 or large[()] != 0:
        raise AssertionError("empty record must have maximum 0")

    print("34 records; every entry row has a fixed parity inside its record")
    print("difference distribution:", EXPECTED_DISTRIBUTION, "maximum 20")
    print("independent values agree with certificate.json")
    print("PASS")


if __name__ == "__main__":
    main()
