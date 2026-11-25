"""Replay the witnesses in verify/certificate.json.

For every record the checker runs the ant on the stored width-2 and width-4
witness boards and checks that the observed entry/reply sequence equals the
recorded one and that the number of steps equals P2 / P4.  The checker does
not recompute the enumeration; verify/independent_enumeration.py does that.
"""

import json
from collections import Counter
from pathlib import Path

DX = (1, 0, -1, 0)
DY = (0, 1, 0, -1)

EXPECTED_DISTRIBUTION = {"0": 3, "8": 20, "15": 1, "16": 2, "20": 8}


def replay(width, mask, record):
    """Replay one witnessed record; return total steps or None on mismatch."""
    board = [(mask >> i) & 1 for i in range(3 * width)]
    total = 0
    for entry, expected_reply in record:
        row, col, heading = entry, 0, 0
        while True:
            cell = row * width + col
            bit = board[cell]
            heading = (heading + (1 if bit else 3)) & 3
            board[cell] = 1 - bit
            row += DY[heading]
            col += DX[heading]
            total += 1
            if col < 0:
                reply = row
                break
            if col >= width or row < 0 or row >= 3:
                reply = -1
                break
        if reply != expected_reply:
            return None
    return total


def main():
    path = Path(__file__).resolve().parent / "certificate.json"
    certificate = json.loads(path.read_text(encoding="utf-8"))
    rows = certificate["records"]
    assert certificate["count"] == len(rows) == 34, "expected 34 records"
    assert certificate["max_visits"] == 4, "expected at most 4 visits"

    diffs = Counter()
    for item in rows:
        record = [tuple(pair) for pair in item["record"]]
        entries = [entry for entry, _ in record]
        if record:
            for width, key, board_key in ((2, "P2", "witness2"), (4, "P4", "witness4")):
                witness = item[board_key]
                if witness is None:
                    raise AssertionError("missing witness for %s at width %d" % (record, width))
                if witness["entries"] != entries:
                    raise AssertionError("entry word mismatch for %s at width %d" % (record, width))
                steps = replay(width, witness["board"], record)
                if steps != item[key]:
                    raise AssertionError(
                        "%s: width %d replay gives %r, certificate says %d"
                        % (record, width, steps, item[key])
                    )
        else:
            if item["P2"] != 0 or item["P4"] != 0:
                raise AssertionError("empty record must have P2 = P4 = 0")
        if item["diff"] != item["P4"] - item["P2"]:
            raise AssertionError("diff field inconsistent for %s" % (record,))
        diffs[str(item["diff"])] += 1

    if dict(sorted(diffs.items())) != EXPECTED_DISTRIBUTION:
        raise AssertionError("unexpected difference distribution: %r" % (dict(diffs),))
    if max(item["diff"] for item in rows) != 20:
        raise AssertionError("expected maximum difference 20")

    print("certificate replay: 34 records, all witnesses reproduce their P2 / P4")
    print("difference distribution:", EXPECTED_DISTRIBUTION, "maximum 20")
    print("PASS")


if __name__ == "__main__":
    main()
