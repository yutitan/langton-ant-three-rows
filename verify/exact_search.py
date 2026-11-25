"""Exact maximum escape time for three-row boards of small width.

The search below branches on the first visit to each cell: on a first visit
the turn direction determines the cell colour, and on later visits the colour
is the one stored in the bit mask.  This is the same strategy as in the
program written by GPT 6.2 Astra (verify/verify_three_row_ant.py); it is
validated here against the exhaustive C search verify/brute.c for widths
1-7 and used to compute widths 8-14.

Usage:
    python3 exact_search.py 7       # fast, widths 1..7 (base cases)
    python3 exact_search.py 14      # slow, adds widths 8..14 (about 2 minutes)

Rows are 0,1,2; headings 0,1,2,3 are E,S,W,N.  Bit 1 is a right-turn cell.
"""

import sys
import time


def moves(width):
    result = []
    for cell in range(3 * width):
        row, col = divmod(cell, width)
        result.append(
            (
                cell + 1 if col + 1 < width else -1,
                cell + width if row < 2 else -1,
                cell - 1 if col else -1,
                cell - width if row else -1,
            )
        )
    return result


def exact_small(width):
    next_cell = moves(width)

    def walk(cell, heading, known, colours):
        if cell < 0:
            return 0
        bit = 1 << cell
        if known & bit:
            new_heading = (heading + (1 if colours & bit else -1)) % 4
            return 1 + walk(next_cell[cell][new_heading], new_heading, known, colours ^ bit)
        left = (heading - 1) % 4
        right = (heading + 1) % 4
        return 1 + max(
            walk(next_cell[cell][left], left, known | bit, colours | bit),
            walk(next_cell[cell][right], right, known | bit, colours),
        )

    return max(
        walk(cell, heading, 0, 0)
        for cell in range(3 * width)
        for heading in range(4)
    )


def formula(width):
    if width == 1:
        return 2
    if width == 2:
        return 12
    return 10 * width - 12 if width % 2 == 0 else 10 * width - 13


def main(max_width=7):
    print("width  S(3,n)  formula  match  seconds")
    for width in range(1, max_width + 1):
        start = time.time()
        value = exact_small(width)
        elapsed = time.time() - start
        expected = formula(width)
        print("%5d  %6d  %7d  %5s  %6.1f" % (width, value, expected, value == expected, elapsed))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
