# Changelog

All notable changes to the skills in this repository are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and each skill uses [Semantic Versioning](https://semver.org/)
on its own. Entries up to 0.2.0 concern m3-design-review only (the repository then held one skill).

## 2026-11-17: m3-design-brief 0.1.0 and m3-design-review 0.3.0

References snapshot unchanged: 2026-05-21.

### m3-design-brief 0.1.0

#### Added

- New skill that writes self-contained Material Design 3 design briefs any AI assistant or developer can implement,
  in three modes: `system` (project design guidelines), `screen` (one screen, flow, feature or component) and
  `change` (accepted review findings or a list of changes as an implementation-ready change spec).
- `references/brief-method.md`: deciding from user tasks, navigation by destinations and window size class,
  components by function (CMP-01), layout and panes per window class, states for every interactive element and
  data view, copy, accessibility floor as acceptance criteria, motion with reduced-motion fallback, Expressive only
  on request.
- `references/brief-template.md`: common header, paste-ready handoff prompt, templates `system`, `screen` and
  `change`, closing sections (decisions `B-nn`, acceptance criteria `AC-nn`, open questions `Q-nn`, validation) and
  acceptance criteria rules.
- `scripts/m3tokens.py` (stdlib Python): `scheme` from a seed color (approximate tonal-spot, light and dark),
  `check` (contrast of required role pairs, exit 1 on failure), `export` (CSS, DTCG JSON, Jetpack Compose,
  Flutter, Tailwind; type and shape scales as CSS), with `references/color-scheme.md` and
  `references/platform-mapping.md`; tests in `test/brief/`.
- Shared references copied from m3-design-review (`adapter-protocol.md` and the seven rule files).
- From the end-to-end test: self-check for focus order that matches the specified layout and for named
  measurement references; acceptance-criteria rules separate page zoom (WCAG 2.2 SC 1.4.10) from text-only
  enlargement (SC 1.4.4); token exports no longer mention the skill's files and mark Expressive shape steps.

### m3-design-review 0.3.0

#### Added

- Design brief support: a brief given or found (from m3-design-brief or any brief with acceptance criteria) is used
  as project guidelines; its decisions count as recorded decisions within its scope; its tolerance, widths and
  themes set the review.
- Report section "Brief acceptance criteria": each AC with pass, fail or not checked and evidence; a failed AC that
  breaks a rule is also a finding or note, and its row points to it.
- Disabled fields: label and helper text are exempt from contrast; focus rings drawn with pseudo-elements or
  `box-shadow` are checked on a screenshot.

### Repository

- `examples/settings-screen/`: a brief, an implementation built from it by a different model, and its review.
- The repository is now a set of two skills ("Material 3 skills for Claude"); README rewritten.
- `maintenance/sync-shared.py` copies the shared references from the review skill to the brief skill; `--check`
  exits 1 when a copy is missing or differs.
- `maintenance/build-zip.py` builds `dist/m3-design-review.zip` and `dist/m3-design-brief.zip`, fails when the shared
  references are out of sync, checks both frontmatters and SKILL.md sizes (body at most 260 lines), and builds each
  ZIP twice to confirm it is reproducible.
- `NOTICE.md` covers the shared copies in the brief skill.

## [0.2.0] - 2026-11-15

Changes motivated by three pilot reviews of a real mobile web app. References snapshot unchanged: 2026-05-21.

### Added

- `measure.js` options `hitScan` (default on), `expectWidth` and `nonTextSelectors`.
- `measure.js` output: `viewport` (with `mismatch`), `warnings` (`viewport-meta-missing`, `viewport-width-mismatch`),
  effective hit areas on target items (`visualWidth`, `visualHeight`, `hitWidth`, `hitHeight`, `hitAreaVia`),
  `probe` and `covered`, `truncated`, `nonTextContrast`, `layoutOverflow`, `labelInName`, `ariaConflicts`,
  `document.headingCount`, `headingSkips` and `headingOutline`; option `maxProbe`.
- `measurement.md` sections "Setup check", "Effective hit areas", "Recipe: text at 200%" and "Recipe: focus flow".
- Evidence labels `measured-rendered`, `measured-code`, `measured-simulation` and `estimated`.
- Rules A11-29 (color is never the only cue in charts, data and status), A11-30 (minimum text size), A11-31
  (accessible name contains the visible label), A11-32 (arrow keys and roving tabindex in composite widgets),
  A11-33 (focus after a view or page change), A11-34 (focus in menus and popups, inert content behind modals),
  A11-35 (headings present), NVB-08 (no swiping between navigation bar destinations), NVB-09 (navigation bar color
  roles), BSH-06 (bottom sheet dismissal) and CMP-01 (classify a control by its function), in a new section
  "Cross-component rules".
- Rule sources `WCAG 2.2 SC x.y.z`, `WAI-ARIA APG <pattern>` and `heuristic` where Material Design 3 does not state a
  requirement.
- Report section "Project and WCAG notes" (`N-01`...) for project-guideline and WCAG items that are not M3 rules.
- Decision candidates may use Rule ID `none (project convention)`; these are recorded in a new project conventions
  list, not in the M3 deviation ledger.
- Grouping instruction: a problem repeated across places or coming from a shared component is reported once with
  all occurrences.
- Adapter "Review setup": optional widths, themes and text-size settings to test, production viewport meta tag and
  minimum text size.
- Freshness note in `maintenance/UPDATING.md`; this changelog.

### Changed

- SKILL.md Step 3 starts with a setup check: stop and fix the setup when `measure.js` reports viewport warnings.
- Target size is judged on the effective hit area, not on the visual box.
- Report header "Evidence" line counts each of the four labels.
- Freshness rule: when the references snapshot is more than 6 months old, the report warns and recommends refreshing
  the references before implementing tier C changes.
- Tier F findings and rejected WCAG notes can only be recorded as `accepted risk`, which does not suppress them.
- A11-15 (motion reduction) now repeats MOT-06 and takes its source; A11-22 (heading hierarchy) keeps tier F for
  skipped levels, and "single H1" becomes advisory.
- Overlapping rules clarified (chips versus segmented buttons, outlined button color roles, decorative bottom sheet
  handle, pressed state inheritance, menu focus return, modal surfaces other than dialogs).
- `document.h1Count` counts only visible h1 elements (`h1CountAll` keeps the old count).
- A11-32 recommends a roving tabindex rather than requiring it, since M3 sets one Tab stop per item for segmented
  buttons and the navigation bar; BSH-06 is tier C (its keyboard part lives in A11-11 and A11-34).
- v0.1 ignored hit areas enlarged by `::before`/`::after` and reported the visual size; v0.2 measures them on the
  padding box, so a 36 px chip with `inset: -6px` and a 1 px border is reported at its real 46 px, not 36 or 48.

### Deprecated

- The bare evidence label `measured`; it is read as `measured-rendered`.

## [0.1.0] - 2026-11-15

### Added

- First release: SKILL.md workflow (precedence of floor rules, project guidelines, M3 core and Expressive),
  tolerance modes `strict` and `inspired`, evidence labels `measured` and `estimated`.
- Distilled M3 references (snapshot 2026-05-21) with rule IDs, tiers and `path@lastmod` sources.
- `scripts/measure.js`, seeded test page and runner.
- Report template, adapter protocol (project guidelines, decisions ledger, change-list format), update procedure and
  ZIP build script.

[0.2.0]: https://github.com/sbk-jdm/m3-skills/releases/tag/v0.2.0
[0.1.0]: https://github.com/sbk-jdm/m3-skills/releases/tag/v0.1.0
