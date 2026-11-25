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


def main():
    validate(JOKE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(JOKE)
    print("Wrote %d characters to %s" % (len(JOKE), OUTPUT_PATH))
    print(JOKE)


if __name__ == "__main__":
    main()
