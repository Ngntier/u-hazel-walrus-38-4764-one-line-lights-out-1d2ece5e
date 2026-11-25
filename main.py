"""One-line entry: lights out mid-sentence.

The program holds a single fixed line of text, checks it against a
handful of sanity rules, and then writes it verbatim to entry.txt
inside the output directory chosen by the environment.
"""

import os
import sys


ENTRY = "Lid closed mid-sentence. My reply is still half-typed, and the cursor just keeps blinking at nobody."

MAX_CHARS = 200
MAX_UTF8_BYTES = 400


def fail(message):
    """Print a validation failure to stderr and exit non-zero."""
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def check_blank(text):
    """Fail if the entry is empty or only whitespace."""
    if not text or text.strip() == "":
        fail("entry is empty or whitespace only")


def check_edges(text):
    """Fail if the entry starts or ends with whitespace."""
    if text != text.strip():
        fail("entry starts or ends with whitespace")


def check_controls(text):
    """Fail if the entry holds any control character."""
    for ch in text:
        code = ord(ch)
        if code < 0x20 or code == 0x7F:
            fail("entry contains a control character U+%04X" % code)


def check_sizes(text, encoded):
    """Fail if the entry exceeds the character or byte limits."""
    if len(text) > MAX_CHARS:
        fail("entry is %d characters, over the %d limit" % (len(text), MAX_CHARS))
    if len(encoded) > MAX_UTF8_BYTES:
        fail("entry is %d UTF-8 bytes, over the %d limit" % (len(encoded), MAX_UTF8_BYTES))


def check_entry(text):
    """Run every validation helper, then return the UTF-8 bytes."""
    check_blank(text)
    check_edges(text)
    check_controls(text)
    encoded = text.encode("utf-8")
    check_sizes(text, encoded)
    return encoded


def output_path():
    """Resolve the entry.txt path from the environment, default /output."""
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(base, "entry.txt")


def run():
    payload = check_entry(ENTRY)
    target = output_path()
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(payload)


if __name__ == "__main__":
    run()
