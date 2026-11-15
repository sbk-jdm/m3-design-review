#!/usr/bin/env python3
"""Build dist/m3-design-review.zip for upload (claude.ai "Upload a skill") or a GitHub Release.

The ZIP root is the folder m3-design-review/ with SKILL.md, references/, scripts/, plus copies of LICENSE and
NOTICE.md. Tests, maintenance files and the repository README are excluded. Python standard library only.

Usage: python3 maintenance/build-zip.py [--out dist/m3-design-review.zip]
"""
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "m3-design-review"
NAME = "m3-design-review"
INCLUDE_DIRS = ["references", "scripts"]
EXTRA = [ROOT / "LICENSE", ROOT / "NOTICE.md"]
FIXED_TIME = (2026, 1, 1, 0, 0, 0)  # stable timestamps make the ZIP reproducible
SKIP = re.compile(r"(^|/)(\.|__pycache__|.*~$|.*\.swp$)")


def check_skill():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        sys.exit("SKILL.md: missing frontmatter")
    front = dict(
        (k.strip(), v.strip()) for k, v in (line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
    )
    name, desc = front.get("name", ""), front.get("description", "")
    if name != NAME or not re.fullmatch(r"[a-z0-9-]+", name):
        sys.exit("SKILL.md: name must be '%s' (lowercase letters, digits, hyphens)" % NAME)
    if not desc or len(desc) > 200 or "<" in desc or ">" in desc:
        sys.exit("SKILL.md: description must be 1-200 characters without angle brackets (now %d)" % len(desc))
    body_lines = text[m.end():].count("\n")
    if body_lines > 450:
        sys.exit("SKILL.md: body has %d lines (max 450)" % body_lines)
    expected = ["color.md", "styles.md", "layout-interaction-a11y.md", "components-1.md", "components-2.md",
                "components-3.md", "expressive.md", "report-template.md", "adapter-protocol.md", "measurement.md"]
    missing = [f for f in expected if not (SKILL / "references" / f).is_file()]
    if missing:
        sys.exit("references missing: " + ", ".join(missing))
    if not (SKILL / "scripts" / "measure.js").is_file():
        sys.exit("scripts/measure.js missing")


def add(zf, src, arc):
    info = zipfile.ZipInfo(arc, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, src.read_bytes())


def main():
    out = ROOT / "dist" / (NAME + ".zip")
    if "--out" in sys.argv:
        out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1]).resolve()
    check_skill()
    files = [SKILL / "SKILL.md"]
    for d in INCLUDE_DIRS:
        files += sorted(p for p in (SKILL / d).rglob("*") if p.is_file() and not SKIP.search(p.relative_to(SKILL).as_posix()))
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w") as zf:
        for f in files:
            add(zf, f, NAME + "/" + f.relative_to(SKILL).as_posix())
        for f in EXTRA:
            add(zf, f, NAME + "/" + f.name)
    with zipfile.ZipFile(out) as zf:
        names = zf.namelist()
    print("%s: %d files, %.1f KB" % (out.relative_to(ROOT) if out.is_relative_to(ROOT) else out, len(names), out.stat().st_size / 1024))
    for n in names:
        print("  " + n)


if __name__ == "__main__":
    main()
