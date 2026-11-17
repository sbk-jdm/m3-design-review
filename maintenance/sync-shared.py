#!/usr/bin/env python3
"""Copy the shared reference files from the review skill into the brief skill.

skills/m3-design-review/references/ holds the canonical copies. The brief skill ships identical copies so each skill
ZIP is self-contained. Edit the review skill's files, then run this script.

Usage:
  python3 maintenance/sync-shared.py           copy the shared files (prints what changed)
  python3 maintenance/sync-shared.py --check   compare only; exit 1 if any copy is missing or differs
Python standard library only.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "skills" / "m3-design-review" / "references"
TARGET = ROOT / "skills" / "m3-design-brief" / "references"
SHARED = [
    "adapter-protocol.md",
    "color.md",
    "styles.md",
    "layout-interaction-a11y.md",
    "components-1.md",
    "components-2.md",
    "components-3.md",
    "expressive.md",
]


def main():
    check = "--check" in sys.argv[1:]
    unknown = [a for a in sys.argv[1:] if a != "--check"]
    if unknown:
        print("unknown argument: " + " ".join(unknown), file=sys.stderr)
        sys.exit(2)
    missing_src = [n for n in SHARED if not (SOURCE / n).is_file()]
    if missing_src:
        print("missing in the review skill: " + ", ".join(missing_src), file=sys.stderr)
        sys.exit(2)
    differ = []
    for name in SHARED:
        src, dst = SOURCE / name, TARGET / name
        if dst.is_file() and dst.read_bytes() == src.read_bytes():
            continue
        differ.append((name, "missing" if not dst.is_file() else "differs"))
        if not check:
            TARGET.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(src.read_bytes())
    if check:
        for name, why in differ:
            print("%s: %s" % (name, why))
        print("shared references: %d checked, %d out of sync" % (len(SHARED), len(differ)))
        sys.exit(1 if differ else 0)
    for name, why in differ:
        print("copied %s (%s)" % (name, why))
    print("shared references: %d checked, %d copied" % (len(SHARED), len(differ)))


if __name__ == "__main__":
    main()
