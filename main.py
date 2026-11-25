"""Meeting-killer writer: the one line that replaces a whole pointless meeting."""

import os, string, sys

TEXT = "The project is cancelled, the deadline was a guess, and the only action item is to stop having this meeting."
LIMIT = 200
ENDERS = ".!?"

def fail(msg):
    sys.stderr.write("invalid: " + msg + "\n")
    raise SystemExit(1)

def validate(text):
    lowered = text.casefold()
    rules = [
        ("meeting" not in lowered, "must mention the meeting"),
        (bool(text) and not text[0].isupper(), "must start with a capital letter"),
        (not text.strip(), "blank entry"),
        (len(text) > LIMIT, "over 200 characters"),
        (any(ord(c) < 32 or ord(c) == 127 for c in text), "control character found"),
        (text != text.strip() or "  " in text or "\n" in text, "ragged edges, double space, or newline"),
        (bool(text) and text[-1] not in ENDERS, "must end with . ! or ?"),
        (all(c in string.punctuation for c in text), "punctuation only"),
        (text.isdigit(), "digits only"),
        (not any(c.isalpha() for c in text), "no letters"),
        ("---" in text, "triple hyphen"),
    ]
    for bad, msg in rules:
        if bad:
            fail(msg)

def write_out():
    validate(TEXT)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(TEXT + "\n")

if __name__ == "__main__":
    write_out()
