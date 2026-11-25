#!/usr/bin/env bash
# Run every check that does not need a C compiler.
set -euo pipefail
cd "$(dirname "$0")"

echo "== 1/6 original verification program =="
python3 verify_three_row_ant.py

echo
echo "== 2/6 transcript cross-check (coordinate replay) =="
python3 ant_transcript_crosscheck.py

echo
echo "== 3/6 independent enumeration =="
python3 independent_enumeration.py

echo
echo "== 4/6 certificate replay =="
python3 check_certificate.py

echo
echo "== 5/6 four-column -> two-column replacement test =="
python3 replacement_test.py

echo
echo "== 6/6 base cases 1..7 by exact search =="
python3 exact_search.py 7

echo
echo "ALL CHECKS PASSED"
