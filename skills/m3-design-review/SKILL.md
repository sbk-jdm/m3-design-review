---
name: m3-design-review
description: Reviews a UI (screenshots, HTML/CSS/JS, rendered pages) against Material Design 3 and returns a numbered, decision-ready report with measured or estimated evidence. Review only.
---

# Material Design 3 review

Review a user interface against Material Design 3 (M3), respecting the project's own guidelines, and produce a
numbered report the user can decide on item by item. Then record the decisions and emit the accepted changes.

## When to use / not to use

Use when the user asks to:
- "review this screen / page / component against Material 3", "is this M3 compliant?", "M3 audit", "design review"
- check touch targets, contrast, type scale, color roles, shapes, spacing or components of an existing UI
- compare a screenshot or a running page with Material guidelines before a release
- decide which Material deviations to keep and which to fix

Do not use when:
- the user wants new UI generated, a theme built, or code written from scratch ("make me an M3 login page"); this
  skill reviews, it does not generate
- the target design system is explicitly not Material (Apple HIG, Fluent, a custom system with no M3 basis), unless
  the user wants only the floor checks
- the question is a single factual lookup ("what is the FAB height?"); answer from the reference file directly

Do not change code during a review. Change code only if the user asks after the decisions are made.

## Layers and precedence

Apply rules in this order. A higher layer wins over a lower one.

1. Floor rules, tier F: accessibility and usability minimums (targets, contrast, focus, labels, text scaling,
   reduced motion). Never negotiable. A project guideline cannot waive them.
2. Project guidelines and recorded decisions, found through the adapter protocol
   (`references/adapter-protocol.md`).
3. M3 core, tier C: roles, tokens, type scale, shape scale, component specs. A deviation needs an explicit decision.
4. M3 Expressive and optional items, tier E. Never report their absence as a defect.

When a project guideline or a recorded decision conflicts with a tier C or E rule, do not report a violation. List the
conflict once under "Decision candidates" (only if it is not already recorded in the ledger). When it conflicts with a
tier F rule, report the F finding and note the conflicting guideline in its evidence.

## Tolerance

Two modes. Default `inspired`.

- `strict`: every tier C mismatch is an issue; tier E items are suggestions.
- `inspired`: tier C mismatches are suggestions unless they harm usability (then they are issues); tier E items are
  suggestions only if they add clear value.
- In both modes every tier F finding is an issue.

Use the mode the user names. If the project guidelines state one, use it. Otherwise use `inspired` and say so in the
report header.

## Evidence labels

Label every finding and every note with exactly one of:
- `measured-rendered`: read from the rendered page (DOM, computed style, hit test), selector and value given.
- `measured-code`: read from source code or declared CSS, not confirmed on a rendered page.
- `measured-simulation`: measured on a rendered page under a simulation (narrow viewport for text zoom, emulated
  setting such as dark mode, reduced motion or forced colors). Recommend confirming on a real device.
- `estimated`: inferred from an image.

Treat the v0.1 label `measured` as `measured-rendered`. When a finding combines sources, use the weakest label.
Never state an exact dp or px value from a screenshot unless the scale is known (viewport width in CSS px and
devicePixelRatio, or a known reference element). Ask for the scale once, or give a range and label it `estimated`.
Never give an exact contrast ratio from a compressed image; give an approximate ratio and label it `estimated`.

## Workflow

### Step 0. Identify the surface

Determine, from the material given or by asking once:
- what is reviewed: screenshot(s), source files, a URL or local page, a design-tool export
- platform: web, Android (Compose or Views), Flutter, iOS, cross-platform
- form factor and window size class: compact (< 600), medium (600-839), expanded (840-1199), large or extra-large
- light, dark, or both; whether a high-contrast, reduced-motion or in-app text-size setting exists

If the surface shows personal data (names, amounts, addresses, messages, health or account data), say so at the top
of the reply and suggest reviewing a redacted or demo state. Do not store screenshots or page data in files, memory or
the ledger. Quote only the minimum text needed to identify an element.

### Step 1. Load the adapter

Follow `references/adapter-protocol.md`: look for project design guidelines, a decisions ledger, a conventions list,
a change-list format and the review setup (widths and text-size settings to test). If none is found, ask once with a
single short question; if the user does not answer or says there are none, continue with M3 only and the defaults.

Design brief: when a brief is given or found (from m3-design-brief, or any brief with acceptance criteria `AC-nn`),
treat it as project guidelines. Its decisions (`B-nn`) count as recorded decisions inside its scope (not decision
candidates); its tolerance, widths and themes are the review setup; tier F still wins. Check every AC and fill the
"Brief acceptance criteria" section of the report (pass, fail or not checked, with evidence).

### Step 2. Choose the tolerance

`strict` or `inspired` (see Tolerance). Do not ask if the user or the guidelines already decided.

### Step 3. Measure

Prefer measurement over estimation. In this order:

1. Rendered page available (Playwright, a browser automation tool, DevTools): evaluate `scripts/measure.js` in the
   page and use its JSON (`references/measurement.md`, "How to run" and "Output fields and the rules they feed").
   Measure each width and theme separately: the widths and text-size settings from the adapter, otherwise a compact
   width (for example 390 px) and an expanded one (for example 1280 px), light and dark.
2. Only source code available: read the CSS/HTML/JS or component code; compute sizes, colors and radii from it and
   label the results `measured-code`.
3. Only images available: estimate, label `estimated`, and ask for the scale if exact numbers matter.

Setup check, before reading any result (measurement.md, "Setup check"):
- Pass `expectWidth` with the CSS width you meant to test.
- If `warnings` contains `viewport-meta-missing` or `viewport-width-mismatch`, stop. The page was laid out at a width
  you did not intend (often 980 px), so every size is wrong. Fix the setup (set the viewport, or inject the same
  viewport meta tag that production serves), re-run, and only then continue. Never report sizes from such a run; if
  production itself lacks the tag, report that once.

Effective hit areas (measurement.md, "Effective hit areas"): with `hitScan` on (the default), judge target size on
`hitWidth` x `hitHeight`, not on the visual box. `hitAreaVia` says how the area was found (`box`, `label`, `pseudo`,
`probe`); `probe` says whether a hit test confirmed it (`ok`) or not (`covered`, `offscreen`, `limited`: geometry only,
confirm before reporting an exact size).
A `pseudo` area enlarged by `::before`/`::after` counts; check that its box is not shrunk by a border or clipped by an
`overflow: hidden` ancestor, and confirm doubtful cases in code.

For text scaling follow measurement.md, "Recipe: text at 200%" (results are `measured-simulation`); for menus,
dialogs, sheets, tabs, radio groups and view changes follow measurement.md, "Recipe: focus flow".

Treat the script output (including `truncated`, `nonTextContrast`, `labelInName`, `ariaConflicts`) as candidates,
not verdicts: confirm each against its rule before reporting it. State styles and motion are not measured; check
them in code or by interaction when they matter.

When the script cannot resolve a contrast (gradient, image or semi-transparent background), compute the worst case
by hand (darkest and lightest stop under the text, or the alpha color composited over the actual background) and
report it as `estimated` with the stops used. For `color-mix()` or alpha text colors, use the final composited color.
If the page has no dark variant, report it once (theme parity rule in `references/color.md`), not per element.

### Step 4. Load only the relevant references

Progressive disclosure: never load all reference files. Pick by what is on screen.

| Surface contains | Load |
| --- | --- |
| Any surface (always) | `references/layout-interaction-a11y.md`, sections "Accessibility floor" and "Cross-component rules" first |
| Colors, themes, dark mode, tokens, contrast | `references/color.md` |
| Typography, corners, elevation, spacing, motion, icons | `references/styles.md` |
| App bars, badges, bottom sheets, button groups, buttons, cards, carousel, checkbox, chips, date pickers, dialogs, divider | `references/components-1.md` |
| Extended FAB, FAB menu, FAB, icon buttons, lists, loading indicator, menus, navigation bar / drawer / rail, progress indicators, radio button | `references/components-2.md` |
| Search, segmented buttons, side sheets, sliders, snackbar, split button, switch, tabs, text fields, time pickers, toolbars, tooltips | `references/components-3.md` |
| Expressive features, spring motion, shape morph, or the user asks about Expressive | `references/expressive.md` |
| Writing the report | `references/report-template.md` |
| Recording decisions, conventions, change list | `references/adapter-protocol.md` |

Inside a large file, read only the sections for the components on screen. List the headings first
(`grep -n '^## ' references/components-1.md`), then read just those line ranges (`sed -n 'START,ENDp' file`).
If a reference file is missing, say so and continue with the others; do not invent rules to fill the gap.

### Step 5. Check, classify, group

For each candidate:
1. Classify the control by its function first (CMP-01), then find the rule. Cite its ID and its `Source` exactly as
   in the reference file. When several rules overlap (a component rule and a floor rule for the same target size),
   cite the most specific one and list the others after it ("also A11-01").
2. If no rule ID supports it, do not report it as an M3 finding. If it breaks a project guideline, or a WCAG 2.2
   success criterion that no rule in the references covers, put it in "Project and WCAG notes" (`N-01`...) with the
   guideline section or `WCAG 2.2 SC x.y.z` as its source (typical cases: missing `lang` attribute, a viewport meta
   tag that disables zoom). Otherwise leave it out.
3. Check the ledger: a recorded deviation is not reported again (mention the count of suppressed items in one line).
4. Check the project guidelines: a conflict with tier C or E goes to "Decision candidates", not to findings. If the
   project choice has no M3 rule to deviate from, the candidate uses Rule ID `none (project convention)`.
5. Classify: tier (F, C, E) and kind (issue or suggestion) according to the tolerance. In `inspired` mode, a tier C
   mismatch "harms usability" (so it is an issue) only if it makes content hard to read, hard to operate, or
   ambiguous for a typical user: text under 12 px, a control whose purpose or state is unclear, a layout that
   breaks at a supported width. Otherwise it is a suggestion.
6. Group: one finding per root cause. When the same problem appears in several places, or comes from one shared
   component, class or token, report it once with the count and every occurrence (or two or three examples plus the
   total: "14 icon buttons at 32 x 32 px, e.g. `.toolbar button`, `#close`"), so a single decision covers it. Put the
   finding in the area where the fix lives.

Sort by impact: tier F issues first, then issues that affect task completion, then tier C issues, then suggestions.
Within a group, sort by reach (how many elements or screens). Cap the report at about 25 findings; if more exist, say
how many were left out and offer a second pass.

If there are few or no issues, say so plainly. Do not add filler praise. Do not invent problems to fill the report.

### Step 6. Present

Use `references/report-template.md` exactly. Each finding carries: a running ID (`F-01`, not the tier), area, tier
and kind, evidence (selector or image region, value, evidence label, occurrences), rule ID with its source, why it
matters (one line, user impact first), a concrete proposed change (`min-height: 48px`,
`color: var(--md-sys-color-on-surface-variant)`, "corner extra-large, 28dp"; never "improve contrast"), effort
(S one property or token, M one component or several files, L structural or cross-screen) and decision boxes.

The report header states: the surface and widths reviewed, the tolerance, the references snapshot date (the oldest
"Snapshot date" in the headers of the reference files loaded), whether project guidelines and a ledger were found,
and the evidence mix (a count for each of the four labels). With a brief, a failed AC that breaks a rule is also a
finding (or note); its AC row points to that `F-nn`/`N-nn` instead of repeating the evidence.

Freshness: compare the snapshot date with today's date. If it is more than 6 months old, or the user mentions a newer
Material release, say so in the header, recommend refreshing the references (the repository's
`maintenance/UPDATING.md`) before implementing tier C changes, and offer to verify the affected rules against
https://m3.material.io/ first. Tier F findings stand regardless of the snapshot age.

### Step 7. Apply the decisions

When the user answers (for example "accept F-01 to F-05, F-07 deviation: brand pill buttons, reject the rest"):

1. For each `deviation` on a tier C or E rule: append one entry to the decisions ledger (date, rule ID, scope,
   one-line rationale, finding ID) in the format of `references/adapter-protocol.md`. A tier F finding cannot be a
   deviation: record it as `accepted risk` and keep reporting it in the summary line. If no ledger exists, propose its
   path and create it only after the user agrees.
2. For each decision candidate with Rule ID `none (project convention)`: record it in the project's conventions list,
   not in the M3 ledger.
3. For each `accept` (findings and notes): emit a change list in the project's format (or the default in the adapter
   protocol): target file or component, change, token or value, rule ID or source, effort.
4. For each `reject`: record nothing unless the user asks; mention that it may reappear in the next review.
5. Do not implement the changes unless the user asks.

If the user gives no decision for an item, leave it open and list open items at the end.

## Judgement rules

- Review by role and purpose, not by exact hex value: a color is right if its role fits the element and its pair is
  respected.
- Classify a control by its function, not its look (CMP-01): a single-select row of chips that switches a view is
  judged with the segmented-button rules for selection cues and with the chip rules for shape and size. Say which
  classification you used in the evidence.
- Baseline M3 is not wrong for lacking Expressive features. Never report the absence of an Expressive feature as an
  issue.
- Do not require components the platform cannot ship (see availability notes in `references/expressive.md`); a custom
  build is the implementer's choice.
- A visible element may be smaller than its hit area: judge target size on the effective hit area (`hitWidth`,
  `hitHeight`), never on the visual box alone.
- Disabled elements are exempt from contrast minimums, including the label and helper text of a disabled field;
  drop such items from `contrastFailures` and `nonTextContrast` after checking that the control is really disabled.
- A focus ring drawn with a pseudo-element or `box-shadow` may escape `focusNotVisible`; when in doubt, take a
  screenshot in focus and compare the ring against its background (3:1).
- Distinguish touch targets (48 x 48dp) from pointer-only targets (44 x 44dp): use the touch value unless the surface
  is clearly desktop-only with no touch input.
- Do not report the same root cause under two areas, or once as a finding and again as a note.
- When the evidence is ambiguous, report the finding as a question in the proposed change ("Confirm whether the chip
  row scrolls; if not, ...") rather than asserting.
- Keep the user's language for the report text; keep rule IDs, token names and sources unchanged.

## Output discipline

- Plain, professional text. No decorative icons or emoji.
- Use tables only where the template does.
- Quote measured values with units (`px` in CSS, `dp` in specs; on the web treat 1dp as 1 CSS px).
- Never paste the reference files or the raw script output into the report; cite IDs and the values that matter.
- Never send page data, screenshots or measurements to any external service.

## Files

- `references/report-template.md`: report layout, finding block, notes, brief acceptance criteria, decision
  candidates, change-list section.
- `references/adapter-protocol.md`: project guidelines, review setup, ledger, conventions list, change-list format.
- `references/measurement.md`: how to run `scripts/measure.js`, setup check, field meanings, recipes, limits.
- `scripts/measure.js`: dependency-free measurement function to evaluate in the page.
- The other `references/*.md` files: distilled M3 rules. Rule IDs are unique across files (A11, CMP, LAY, COL, TYP,
  SHP, MOT... and one prefix per component), each with a tier and a source: `path@lastmod` (maps to
  `https://m3.material.io/<path>`), `WCAG 2.2 SC x.y.z`, `WAI-ARIA APG <pattern>` or `heuristic`.
