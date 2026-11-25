"""One-Line Office Joke Laugh-Off entry.

Writes a single original one-line office joke to /output/entry.txt.
Pure Python standard library only.
"""

import os

JOKE = "Our printer only jams on deadline day, which is how I know it reads my calendar."

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def validate(text):
    """Check the entry against the competition gate."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if "\n" in text.rstrip("\n") or "\r" in text:
        raise ValueError("entry must be a single line")
    return True


def validate_entry(text):
    """Strict guard: single line, 1-200 chars, non-whitespace, valid UTF-8.

    Extends validate() with an explicit UTF-8 round-trip check so an
    entry that cannot be encoded exactly is rejected before writing.
    """
    validate(text)
    # Must be exactly one line with no embedded newline or carriage return.
    if text != text.strip() or "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line with no leading/trailing whitespace")
    # Must survive a UTF-8 encode/decode round-trip byte-for-byte.
    decoded = text.encode("utf-8").decode("utf-8")
    if decoded != text:
        raise ValueError("entry must be valid UTF-8")
    return True


def verify_written(path, expected_text):
    """Re-read the file from disk and re-validate its exact bytes.

    Guards against a truncated or altered write: the bytes on disk must
    decode as UTF-8 and equal the validated entry exactly.
    """
    with open(path, "rb") as handle:
        raw = handle.read()
    try:
        on_disk = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("entry.txt on disk is not valid UTF-8") from exc
    if on_disk != expected_text:
        raise ValueError(
            "entry.txt on disk does not match the validated entry "
            "(%d bytes on disk, expected %d characters)"
            % (len(raw), len(expected_text))
        )
    validate_entry(on_disk)
    return on_disk


def main():
    validate_entry(JOKE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(JOKE)
    verify_written(OUTPUT_PATH, JOKE)
    print("Wrote %d characters to %s" % (len(JOKE), OUTPUT_PATH))
    print(JOKE)


if __name__ == "__main__":
    main()
