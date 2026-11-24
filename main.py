#!/usr/bin/env python3
"""The Funniest Toaster Error Message -- make.fun entry.

Writes a single line of text to /output/entry.txt: the error message a
kitchen toaster shows its owner when something goes wrong. Pure
standard library only.

The line: the toaster toasted the bread, the owner walked away and
never came back, and the toaster is still sitting there warm, holding
the same message. Deadpan, quietly dramatic, no toaster pun anywhere --
the joke is a small appliance that remembers being forgotten, and the
repeated "ready" is the toaster stuck on its one line of dialogue.
"""

import os
import sys

ENTRY = "ERROR: Your toast is ready. It has been ready since Tuesday. You forgot me again."

MIN_CHARS = 1
MAX_CHARS = 120


def check_gates(text):
    """Refuse to write unless every kit gate passes. Returns a list of failures."""
    failures = []
    if not isinstance(text, str):
        failures.append("entry is not text")
        return failures
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        failures.append("entry is not valid UTF-8")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        failures.append(
            "entry is %d characters, outside the 1-120 gate" % len(text)
        )
    if text.strip() == "":
        failures.append("entry is only whitespace")
    if "\n" in text or "\r" in text:
        failures.append("entry is not one line")
    return failures


def main():
    failures = check_gates(ENTRY)
    if failures:
        for failure in failures:
            print("GATE FAILED: %s" % failure, file=sys.stderr)
        return 1

    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    os.chmod(out_path, 0o644)

    # Read it back and verify what is on disk, byte for byte.
    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != ENTRY:
        print("GATE FAILED: read-back differs from the entry", file=sys.stderr)
        return 1
    if check_gates(written):
        print("GATE FAILED: written file fails the gates", file=sys.stderr)
        return 1

    print("OK: wrote %s (%d characters, 1 line)" % (out_path, len(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
