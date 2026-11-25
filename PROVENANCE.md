# Provenance and AI disclosure

[Back to the README](README.md)

This repository is published as a **public record of a personal AI-assisted
exploration** and as the second entry of the *大模型的小练习* (LLM Exercises)
series. It makes **no priority claim**: the argument is short enough that
others may well have found it independently, and the conclusion was already
known numerically (Etse's lower-bound constructions and simulations up to
n ≤ 20).

## Series

* （一）[Counterexamples to *Written on the Wall II* conjecture #138](https://github.com/yutitan/wowii-conjecture-138)
* （二）this repository, *三行朗顿蚂蚁的精确逃逸时间*

## Timeline (UTC, 2026-11-25 / 2026-11-26)

| time | event | evidence |
| --- | --- | --- |
| 13:06:14 | Codex session 01a212d0-4743-7213-8b9e-22a59d508eac opened (also used for series (一)) | rollout on the author's machine; sha256 below |
| 17:44:27 | the three-row ant turn starts in the same session | turn id 01a213cf-fa3d-7121-9d0f-02cb4373512c |
| 17:54 | GPT 6.2 Astra writes/updates outputs/verify_three_row_ant.py | original file retained; sha256 below |
| 17:55:34 | GPT 6.2 Astra returns the result and proof sketch | saved answer; sha256 below |
| 17:59–18:10 | DeepSeek Harness verifies: literature, independent enumeration, C brute force, exact search to width 14, 400-case replacement test | raw scripts in [provenance/](provenance/); file times 2026-11-26 01:59–02:10 (+08) |
| 2026-11-26 | repository assembled and published | this repository |

(2026-11-26 is the local date in UTC+8; the corresponding UTC instants are on
2026-11-25 evening.)

## What the AI systems did

* **GPT 6.2 Astra** (OpenAI Codex, model gpt-6.2-astra): derived the
  finite-record argument, wrote the first verification program, and produced
  the answer saved in [provenance/gpt-6.2-astra-answer.md](provenance/gpt-6.2-astra-answer.md).
* **DeepSeek Harness**: independently re-derived the 34 records with a separate
  implementation, wrote the exhaustive C search, the exact branch search to
  width 14, the certificate generator/replayer and the 400-case end-to-end
  test; assembled and published the repository.
* The **human author** ([@yutitan](https://github.com/yutitan)) initiated and
  directed both sessions, reviewed the output, and takes responsibility for
  the content. AI systems are not legal authors.

## Hashes

    verify/verify_three_row_ant.py       e5baa078a4d626eeba4583ec5feceaebe9f5a82baded65eb50f64778bac95be1
    verify/ant_transcript_crosscheck.py  fd5395774d9c12447e89423af16c258c7cbfe893502e967d34aa860d10b6caad
    verify/make_certificate.py           b8d9ce6174f74103b081d77f81549fe4e1904918f09d6bdeb2dd3f368419c5b6
    verify/check_certificate.py          1ba9cc543da6bdc5453e4682491a089bc1885aabd2f1c2cdc9dc6ac2132a8929
    verify/independent_enumeration.py    793d38b54a6caf8b5b06dea7306aa3b92096a5f826678add76e735c6d255600b
    verify/replacement_test.py           7ac256a6a375e6221d669b9a460e7f31d15487eb806e73a141f87396a9086b87
    verify/exact_search.py               23db68c274c2bda0403c6ab6de447d720e39a982552d3dea898f0cd2c61a7a58
    verify/brute.c                       ea3351a9915a4e31828c576e9dc4548f54d315d8de33d44b61fa2d54cec33d3e
    verify/certificate.json              91828fd8d635148c789190cd2dc9f9c55f10335a37cb644ac35ad3e6ff7f42dd
    verify/results.txt                   7b12fa8bafa18229ba5c6cd831acf21a6fd4e01deafe2bb8fedf1c1eb350b92f
    provenance/gpt-6.2-astra-answer.md   cafe837a73e8ab1fa79ba9219fbf87ede7a69ba3b976539bb479dc9df4cd89e4

Codex rollout (retained on the author's machine, not redistributed):

    rollout sha256: fc09b5cb34777813b5906c1d8e5ae45b932a3eaa0c6f9752b3bd7e8d216f4c98
    original GPT programs:
      outputs/verify_three_row_ant.py       e5baa078...95be1   (identical to verify/)
      work/ant_transcript_crosscheck.py     3f6fc7fc...a8cd    (only the import path was adapted here)

The rollout file contains the full Codex session; the ant answer is the
assistant message at 0-based line 528 of the JSONL, timestamped
17:55:34.101Z.

## What was checked independently

* The 34 records and all P2, P4 values: recomputed by a second implementation
  ([verify/independent_enumeration.py](verify/independent_enumeration.py)) that
  does not import the original program; the two agree entry by entry.
* The base cases 1–7: exhaustive C enumeration of all colourings and poses
  ([verify/brute.c](verify/brute.c)).
* Widths 8–14: exact branch search; all values equal the formula
  ([data/exact_search_1_14.txt](data/exact_search_1_14.txt)).
* The replacement construction: 400 random boards of widths 8, 9, 10; the new
  board always keeps the record and loses at most 4 steps in the test (the
  proof only needs 20).
* The certificate witnesses: replayed by
  [verify/check_certificate.py](verify/check_certificate.py).

## Caveats

* The proof is computer-assisted; the finite certificate is exhaustive but the
  induction itself is a human-readable argument (Section 3 of the note).
* Etse's lower-bound construction is used as published and is not re-proved
  here.
* The parity/HV-partition fact and the rotation/mirror symmetries are standard;
  they are stated, not formalised.
* No systematic priority search beyond the sources listed in
  [literature/notes.md](literature/notes.md).
