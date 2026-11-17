# Updating the skills

The repository holds two skills, `m3-design-review` and `m3-design-brief`. The rule references and the adapter
protocol are shared: the canonical copies live in `skills/m3-design-review/references/`, and
`maintenance/sync-shared.py` copies them into `skills/m3-design-brief/references/`. Edit only the canonical copies.

## When to update

- The Material Design 3 site publishes changes (new components, changed specs, a new Expressive release).
- The snapshot date in the reference headers is more than six months old (the skill warns users in its reports).
- A user reports a rule that no longer matches the official page.

## Freshness

- Current references snapshot: 2026-11-17 (mirror: `sbk-jdm/m3-mirror`, workflow `fetch-cited`). It becomes six months old on 2027-05-17; from then on the skill warns in
  every report and recommends refreshing before implementing tier C changes.
- To refresh, run the mirror's `tools/sync.js` (for example in the md3-reference-hub mirror: `npm install`, then
  `node tools/sync.js`, which needs Node 22 or later; `node tools/validate.js` checks the result) on a machine with
  network access. The review environment usually has no network.
- Then follow steps 2 to 5 below, and re-verify the `@lastmod` part of every rule row whose cited page changed. Do not
  bump a lastmod you have not checked against the mirror's frontmatter.

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
- Update the `@lastmod` part of the Source to the new date. Rules sourced as `WCAG 2.2 SC x.y.z`,
  `WAI-ARIA APG <pattern>` or `heuristic` have no lastmod; check whether M3 now states them and, if so, switch the
  source to the M3 page.
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
verified as unchanged. If only some files were refreshed, each file keeps its own date; the report and brief headers
show the oldest one. Update the snapshot date in `README.md` and, if role names, tones or token names changed, in
`skills/m3-design-brief/references/color-scheme.md`, `platform-mapping.md` and `scripts/m3tokens.py`.

## 4b. Sync the shared references

```
python3 maintenance/sync-shared.py           # copies adapter-protocol.md and the seven rule files to the brief skill
python3 maintenance/sync-shared.py --check   # exits 1 if any copy is missing or differs
```

Run it after every change to a shared file (adapter-protocol.md, color.md, styles.md, layout-interaction-a11y.md,
components-1.md, components-2.md, components-3.md, expressive.md). Never edit the copies in the brief skill. If a
rule ID that the brief skill cites (`brief-method.md`, `brief-template.md`, `SKILL.md`) is removed or renumbered,
update those citations too:

```
grep -rhoE '\b[A-Z][A-Z0-9]{1,3}-[0-9]{2}\b' skills/m3-design-brief/SKILL.md skills/m3-design-brief/references/brief-*.md | grep -v '^AC-' | sort -u
```

Each ID listed must exist in a shared reference file.

## 5. Test and build

```
python3 test/check.py                              # measure.js against the seeded page; all checks must pass
python3 -m unittest discover -s test/brief -v      # m3tokens.py; all tests must pass
python3 maintenance/sync-shared.py --check         # shared references in sync
python3 maintenance/build-zip.py                   # writes dist/m3-design-review.zip and dist/m3-design-brief.zip
```

`build-zip.py` first runs `sync-shared.py --check` and stops if the shared references differ. For each skill it
validates the `SKILL.md` frontmatter (name equal to the folder name, description up to 200 characters, no angle
brackets), the body length (up to 260 lines) and the presence of all reference files and scripts, then writes a ZIP
whose root is the skill's folder with `SKILL.md`, `references/`, `scripts/`, `LICENSE` and `NOTICE.md`. Tests,
maintenance files and the repository README are not included. Timestamps and order are fixed, and each ZIP is built
twice and compared, so the same input gives the same bytes. `--only <skill>` builds one of them.

## 6. Release

- Add an entry to `CHANGELOG.md` (one subsection per skill that changed) and update the version table in `README.md`.
- Note in the release text: snapshot date, mirror used, pages re-distilled, IDs added or removed.
- Attach `dist/m3-design-review.zip` and `dist/m3-design-brief.zip` as release assets.
- Do not commit `dist/`.

## Changing measure.js

- Keep it one function expression with no imports, no network access and no page mutation (other than transient
  focus that is restored).
- Add a seeded violation and a negative control to `test/seeded-violations.html` for every new check, document it in
  `test/EXPECTED.md` and `test/check.py`, and document the field and its limits in `references/measurement.md`.


## Releasing a new version

1. Change the skill, add a `### <skill> <version>` section to `CHANGELOG.md`, and bump `skills/<skill>/VERSION`
   (also the README table and `m3tokens.py` `VERSION` when they apply).
2. Run the tests and `python3 maintenance/build-zip.py`.
3. Push to `main`. The `release` workflow (`.github/workflows/release.yml`) tags `<skill>/vX.Y.Z` and publishes a
   Release with the ZIP and the CHANGELOG section for every skill whose version has no tag yet. Existing tags are
   skipped, never moved or deleted. It also keeps one rolling release per skill (`latest-<skill>`, pre-release) whose
   ZIP is replaced on every new version, so the README download links never change, and opens an issue
   "Update <skill> in Claude: <version>" (GitHub emails you) with the upload steps; close it once uploaded.
   It needs Settings > Actions > General > Workflow permissions: Read and write.
