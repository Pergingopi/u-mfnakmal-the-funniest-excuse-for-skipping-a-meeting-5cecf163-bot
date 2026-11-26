#!/usr/bin/env python3
"""One excuse for skipping a meeting, written out as a program.

The program is pure Python 3.13 standard library, needs no network, and
is fully deterministic: every run writes exactly the same bytes.

The line it writes (115 characters, plus a trailing newline):
    Can't make it - my calendar auto-declined this meeting out of
    self-respect, and I've decided to trust its judgment.

What makes the line work: the calendar is given the dignity, so the joke
turns the usual excuse upside down. It is not the worker shirking; it is
the calendar refusing on principle. "Out of self-respect" is the twist,
and "I've decided to trust its judgment" ends it with a deadpan surrender
that anyone drowning in pointless meetings recognises at once.

The gate for this competition is UTF-8 text of 1 to 200 characters, not
only whitespace. The line is measured against that gate before anything
touches the output directory, so a line that would fail the gate can
never reach /output/entry.txt.

Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

# The single line the entry is judged on.
LINE = (
    "Can't make it - my calendar auto-declined this meeting out of "
    "self-respect, and I've decided to trust its judgment."
)

# Upper bound from the competition gate (entry.txt: 1 to 200 characters).
LIMIT = 200


def check_gate(text):
    """Measure a candidate line against the competition gate."""
    if not isinstance(text, str):
        raise TypeError("line must be str")
    if not 1 <= len(text) <= LIMIT:
        raise ValueError("line must be 1-200 characters, got %d" % len(text))
    if not text.strip():
        raise ValueError("line must not be only whitespace")
    text.encode("utf-8")  # the gate reads UTF-8 text


def resolve_output_dir():
    """Where entry.txt goes: the harness dir, or /output by default."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def write_entry(directory, text):
    """Write text atomically into directory/entry.txt, mode 0644.

    The file is staged next to its destination inside the output
    directory itself, then renamed into place, so the output directory
    is never removed and the grader (a different user) can read the file.
    """
    os.makedirs(directory, exist_ok=True)
    payload = (text + "\n").encode("utf-8")
    staging = os.path.join(directory, ".entry.txt.tmp")
    target = os.path.join(directory, "entry.txt")
    with open(staging, "wb") as handle:
        handle.write(payload)
    os.chmod(staging, 0o644)
    os.replace(staging, target)
    os.chmod(target, 0o644)


def main():
    check_gate(LINE)
    write_entry(resolve_output_dir(), LINE)


if __name__ == "__main__":
    main()
