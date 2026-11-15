# Updating the skill

## When to update

- The Material Design 3 site publishes changes (new components, changed specs, a new Expressive release).
- The snapshot date in the reference headers is more than six months old (the skill warns users in its reports).
- A user reports a rule that no longer matches the official page.

## 1. Re-sync a local mirror

Work from a local Markdown mirror of https://m3.material.io/ in which every page has frontmatter with at least
`source_url` and `lastmod`. Any mirror that preserves those two fields works; record which one you used in the
release notes. Keep the mirror outside this repository (it is not redistributed).

## 2. Find what changed

Every rule cites `path@lastmod`. List the cited pages and compare their dates with the mirror:

```
grep -rhoE '[a-z0-9/_-]+@[0-9]{4}-[0-9]{2}-[0-9]{2}' skills/m3-design-review/references | sort -u > /tmp/cited.txt
```

For each `path@date` in `cited.txt`, read `lastmod` of `<mirror>/<path>.md`. A page needs re-distilling when the
mirror date is newer. Also list mirror pages that are not cited at all and check whether they add rules a reviewer
needs (new components, new accessibility pages).

## 3. Re-distill only the changed pages

For each changed page, update only the rules that cite it, following the same conventions:

- Table rows `| ID | Rule | Value / criterion | Tier | Source |`; keep existing IDs stable. Never reuse a removed ID
  for a different rule; append new IDs at the end of the prefix's range.
- Tiers: F floor (accessibility/usability minimum), C core M3, E Expressive-only, optional or platform-specific.
- Where the docs give baseline and Expressive values, write "M3: X / Expressive: Y" and use tier E for
  Expressive-only items.
- Update the `@lastmod` part of the Source to the new date.
- Write your own wording. Numbers, token names and values may be copied; no quotation longer than about ten words.
- Keep dp as in the source (on the web 1dp = 1 CSS px). No images or videos.
- Component files keep the fixed subsections: Use, Dimensions & shape, Color roles, Do / Don't, Accessibility,
  Review checks, rules table (about 1.6 KB per component).
- Nothing about a specific product, company or person.

Check that IDs are unique across all files:

```
grep -rhoE '^\| [A-Z0-9]+-[0-9]+ ' skills/m3-design-review/references | sort | uniq -d
```

The output must be empty. Check that every table row has the same number of columns as its header.

## 4. Bump the snapshot date

Set the new snapshot date in the header of every reference file you touched, and in any file whose rules you
verified as unchanged. If only some files were refreshed, each file keeps its own date; the report header shows the
oldest one.

## 5. Test and build

```
python3 test/check.py                # measure.js against the seeded page; all checks must pass
python3 maintenance/build-zip.py     # writes dist/m3-design-review.zip
```

`build-zip.py` validates the `SKILL.md` frontmatter (name, description length up to 200 characters, no angle
brackets), the body length (up to 450 lines) and the presence of all reference files, then writes a ZIP whose root is
the folder `m3-design-review/` with `SKILL.md`, `references/`, `scripts/`, `LICENSE` and `NOTICE.md`. Tests,
maintenance files and the repository README are not included. Timestamps are fixed so the same input gives the same
ZIP.

## 6. Release

- Note in the release text: snapshot date, mirror used, pages re-distilled, IDs added or removed.
- Attach `dist/m3-design-review.zip` as a release asset.
- Do not commit `dist/`.

## Changing measure.js

- Keep it one function expression with no imports, no network access and no page mutation (other than transient
  focus that is restored).
- Add a seeded violation and a negative control to `test/seeded-violations.html` for every new check, document it in
  `test/EXPECTED.md` and `test/check.py`, and document the field and its limits in `references/measurement.md`.
