"""Till Firmware Do Us Part — make.fun text bounty entry.

Writes one funny, heartfelt wedding vow spoken by a robot to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The vow itself (141 characters, one sentence, one line):

    I vow to love you through every update, every crash, and every low
    battery, and to reboot beside you every morning, till firmware do
    us part.

Deterministic, Python standard library only. Self-verifies the entry
twice: once in memory before writing, and once after reading the file
back from disk, with the same rule set both times. The gate's rules
are UTF-8 text, 1-200 characters, a single line, not whitespace-only.
Exits non-zero on any failure.
"""

import os
import sys

ENTRY = (
    "I vow to love you through every update, every crash, and every low "
    "battery, and to reboot beside you every morning, till firmware do "
    "us part."
)

MIN_CHARS = 1
MAX_CHARS = 200


def verify_entry(text: str) -> list[str]:
    """Check one entry text against every gate rule, all at once.

    Returns a list of human-readable problem descriptions. An empty
    list means the text is valid. Unlike a fail-fast chain of `if`
    statements that stops at the first problem, every check here runs
    even when an earlier one failed, so a single run reports the whole
    diagnosis instead of one symptom at a time.
    """
    problems = []

    # Rule 1: the text must be encodable as UTF-8. A lone surrogate
    # (for example "\\ud800" on its own) is a valid Python str that
    # cannot be encoded, and would otherwise blow up only at write
    # time; catching it here names the problem instead.
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"entry is not valid UTF-8: {exc}")

    # Rule 2: length in characters, 1 to 200 inclusive. len() counts
    # Unicode code points, which is the gate's character count; the
    # entry is plain ASCII, so code points and bytes agree here.
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        problems.append(
            f"entry is {len(text)} chars, must be {MIN_CHARS}-{MAX_CHARS}"
        )

    # Rule 3: a single line — no line feed and no carriage return.
    # Checking "\\r" as well as "\\n" matters because a "\\r\\n" pair
    # smuggled in would otherwise slip past a "\\n"-only test on
    # systems that translate newlines.
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")

    # Rule 4: not whitespace-only. A string of spaces or tabs would
    # pass the length rule, so this check has to stand on its own.
    if not text.strip():
        problems.append("entry must not be whitespace-only")

    return problems


def report_problems(problems: list[str], context: str) -> None:
    """Print every problem found, one FAIL line each, to stderr.

    `context` says where the problems were found — "entry" for the
    in-memory check, "written file" for the read-back re-check — so a
    failure message always says which phase failed, not just that
    something failed somewhere.
    """
    for problem in problems:
        print(f"FAIL: {context}: {problem}", file=sys.stderr)


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    output_path = os.path.join(output_dir, "entry.txt")

    # Phase 1: verify the entry in memory, before touching the disk.
    # Verifying first means a bad entry never produces a partial or
    # stale file for the grader to mistake for a real entry, and all
    # problems are reported at once — nothing to fix one at a time
    # and re-run for.
    problems = verify_entry(ENTRY)
    if problems:
        report_problems(problems, "entry")
        return 1

    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY + "\n")

    # Phase 2: read the file back and check it with the SAME rules.
    # Two things are proven here, and they catch different faults:
    #   * byte equality with ENTRY + "\\n" catches truncation, a
    #     partial write, or a newline translated on the way out;
    #   * re-running verify_entry on the read-back text proves the
    #     file on disk is itself a valid entry by the gate's rules,
    #     and names the exact rule it breaks instead of only saying
    #     "does not match".
    # The read itself is guarded: a missing file or a file that is no
    # longer decodable UTF-8 used to raise an unhandled traceback;
    # now it is a clean FAIL with exit code 1.
    try:
        with open(output_path, "r", encoding="utf-8") as fh:
            written = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        print(f"FAIL: could not read back {output_path}: {exc}", file=sys.stderr)
        return 1

    if written != ENTRY + "\n":
        print("FAIL: written file does not match the entry", file=sys.stderr)
        return 1

    # The file holds ENTRY plus exactly one trailing newline, which is
    # the file format, not part of the entry: strip that one newline
    # and re-check the text itself, so the single-line rule is applied
    # to the entry rather than to the file's terminator.
    read_back = written[:-1] if written.endswith("\n") else written
    problems = verify_entry(read_back)
    if problems:
        report_problems(problems, "written file")
        return 1

    print(f"OK: wrote {len(ENTRY)}-char entry to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
