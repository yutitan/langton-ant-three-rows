"""Independent coordinate-based replay for every prescribed word of entry rows."""
from itertools import product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_three_row_ant import profiles


def word_profiles(width, from_right):
    maxima = {(): 0}
    cells = list(product(range(width), range(3)))
    for layout in product((False, True), repeat=len(cells)):
        initial = dict(zip(cells, layout))
        for word in [*product((0, 2), repeat=4), (1, 1, 1, 1)]:
            board = initial.copy()
            elapsed = 0
            record = ()
            for y in word:
                entry = y
                x = width - 1 if from_right else 0
                dx, dy = (-1, 0) if from_right else (1, 0)
                while (x, y) in board:
                    right = board[x,y]
                    board[x,y] = not right
                    dx, dy = (-dy, dx) if right else (dy, -dx)
                    x += dx
                    y += dy
                    elapsed += 1
                returned = x == (width if from_right else -1)
                record += ((entry, y if returned else -1),)
                maxima[record] = max(elapsed, maxima.get(record, 0))
                if not returned:
                    break
            else:
                raise ValueError("Four returns; longer words need checking")
    return maxima


if __name__ == "__main__":
    for width in (2, 4):
        target = profiles(width)
        for side in (False, True):
            observed = word_profiles(width, side)
            if observed != target:
                raise AssertionError((width, side, observed, target))
            print("All entries and times agree:", width, "R" if side else "L")
