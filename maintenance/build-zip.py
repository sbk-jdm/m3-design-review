#!/usr/bin/env python3
"""Build dist/m3-design-review.zip and dist/m3-design-brief.zip for upload (claude.ai "Upload a skill") or a GitHub
Release.

Each ZIP root is the skill's folder (m3-design-review/ or m3-design-brief/) with SKILL.md, references/, scripts/, plus
copies of LICENSE and NOTICE.md. Tests, maintenance files and the repository README are excluded. Before building,
the shared references must be in sync (maintenance/sync-shared.py --check) and each SKILL.md must pass the
frontmatter and size checks. Timestamps and file order are fixed, so the same input gives the same bytes; the script
builds each ZIP twice and fails if the two builds differ. Python standard library only.

Usage: python3 maintenance/build-zip.py [--only m3-design-review|m3-design-brief] [--out-dir dist]
"""
import hashlib
import io
import pathlib
import re
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXTRA = [ROOT / "LICENSE", ROOT / "NOTICE.md"]
INCLUDE_DIRS = ["references", "scripts"]
FIXED_TIME = (2026, 1, 1, 0, 0, 0)  # stable timestamps make the ZIP reproducible
SKIP = re.compile(r"(^|/)(\.|__pycache__|.*~$|.*\.swp$|.*\.pyc$)")
SHARED = ["adapter-protocol.md", "color.md", "styles.md", "layout-interaction-a11y.md", "components-1.md",
          "components-2.md", "components-3.md", "expressive.md"]

SKILLS = {
    "m3-design-review": {
        "references": SHARED + ["report-template.md", "measurement.md"],
        "scripts": ["measure.js"],
        "max_body_lines": 260,
    },
    "m3-design-brief": {
        "references": SHARED + ["brief-method.md", "brief-template.md", "platform-mapping.md", "color-scheme.md"],
        "scripts": ["m3tokens.py"],
        "max_body_lines": 260,
    },
}


def fail(msg):
    sys.exit("build-zip: " + msg)


def check_shared():
    r = subprocess.run([sys.executable, str(ROOT / "maintenance" / "sync-shared.py"), "--check"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        fail("shared references out of sync; run python3 maintenance/sync-shared.py\n" + r.stdout + r.stderr)


def check_skill(name, spec):
    skill = ROOT / "skills" / name
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail("%s/SKILL.md: missing frontmatter" % name)
    front = dict(
        (k.strip(), v.strip()) for k, v in (line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
    )
    fname, desc = front.get("name", ""), front.get("description", "")
    if fname != name or not re.fullmatch(r"[a-z0-9-]+", fname):
        fail("%s/SKILL.md: name must be '%s' (lowercase letters, digits, hyphens)" % (name, name))
    if not desc or len(desc) > 200 or "<" in desc or ">" in desc:
        fail("%s/SKILL.md: description must be 1-200 characters without angle brackets (now %d)" % (name, len(desc)))
    body_lines = text[m.end():].count("\n")
    if body_lines > spec["max_body_lines"]:
        fail("%s/SKILL.md: body has %d lines (max %d)" % (name, body_lines, spec["max_body_lines"]))
    missing = [f for f in spec["references"] if not (skill / "references" / f).is_file()]
    missing += ["scripts/" + f for f in spec["scripts"] if not (skill / "scripts" / f).is_file()]
    if missing:
        fail("%s: missing %s" % (name, ", ".join(missing)))
    return skill


def add(zf, src, arc):
    info = zipfile.ZipInfo(arc, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, src.read_bytes())


def build_bytes(name, skill):
    files = [skill / "SKILL.md"]
    for d in INCLUDE_DIRS:
        if (skill / d).is_dir():
            files += sorted(p for p in (skill / d).rglob("*")
                            if p.is_file() and not SKIP.search(p.relative_to(skill).as_posix()))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for f in files:
            add(zf, f, name + "/" + f.relative_to(skill).as_posix())
        for f in EXTRA:
            add(zf, f, name + "/" + f.name)
    return buf.getvalue()


def main():
    args = sys.argv[1:]
    out_dir = ROOT / "dist"
    names = list(SKILLS)
    if "--out-dir" in args:
        out_dir = pathlib.Path(args[args.index("--out-dir") + 1]).resolve()
    if "--only" in args:
        only = args[args.index("--only") + 1]
        if only not in SKILLS:
            fail("unknown skill '%s' (choose %s)" % (only, ", ".join(SKILLS)))
        names = [only]
    check_shared()
    for f in EXTRA:
        if not f.is_file():
            fail("missing " + f.name)
    for name in names:
        skill = check_skill(name, SKILLS[name])
        data = build_bytes(name, skill)
        if build_bytes(name, skill) != data:
            fail("%s: two builds differ; the ZIP is not reproducible" % name)
        out = out_dir / (name + ".zip")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        with zipfile.ZipFile(out) as zf:
            entries = zf.namelist()
        shown = out.relative_to(ROOT) if str(out).startswith(str(ROOT)) else out
        print("%s: %d files, %.1f KB, sha256 %s" % (shown, len(entries), len(data) / 1024,
                                                  hashlib.sha256(data).hexdigest()[:16]))
        for n in entries:
            print("  " + n)


if __name__ == "__main__":
    main()
