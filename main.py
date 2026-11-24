#!/usr/bin/env python3
"""Write the single judged text artifact for Charm the Commuter.

The deliverable is /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt): one
UTF-8 text of 1-140 characters, not whitespace-only, with no trailing newline.
Bytes are staged in a temporary file in the destination directory and moved
into place with os.replace, so the grader never sees a partially written file.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

# Named invented city, weather as the point, broadcast-forecast rhythm, one
# concrete commute detail, and a dry one-reading joke. 102 ASCII characters.
FORECAST = (
    "Nimbusleigh: overcast with sunny spells, and a 30% chance of arriving "
    "at work having enjoyed the walk."
)


def checked_bytes() -> bytes:
    """Return the exact artifact bytes, refusing anything the gate would refuse."""
    if not 1 <= len(FORECAST) <= 140:
        raise ValueError("forecast must be 1-140 characters")
    if not FORECAST.strip():
        raise ValueError("forecast must not be whitespace-only")
    if FORECAST.startswith("\ufeff"):
        raise ValueError("forecast must not begin with a BOM")
    if FORECAST.endswith(("\n", "\r")):
        raise ValueError("forecast must not end with a newline")
    data = FORECAST.encode("utf-8", errors="strict")
    if data.decode("utf-8", errors="strict") != FORECAST:
        raise ValueError("forecast must round-trip through strict UTF-8")
    return data


def write_atomically(target: Path, data: bytes) -> None:
    """Stage beside the target, flush, then replace it in one atomic operation."""
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, staged = tempfile.mkstemp(prefix=".entry-", suffix=".tmp", dir=target.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staged, target)
    except BaseException:
        try:
            os.unlink(staged)
        except FileNotFoundError:
            pass
        raise


def main() -> None:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    write_atomically(output_dir / "entry.txt", checked_bytes())


if __name__ == "__main__":
    main()
