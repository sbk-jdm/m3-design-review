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

Label every finding:
- `measured`: read from computed styles, the DOM, or source code (selector and value given).
- `estimated`: inferred from an image.

Never state an exact dp or px value from a screenshot unless the scale is known (viewport width in CSS px and
devicePixelRatio, or a known reference element). Ask for the scale once, or give a range and label it `estimated`.
Never give an exact contrast ratio from a compressed image; give an approximate ratio and label it `estimated`.

## Workflow

### Step 0. Identify the surface

Determine, from the material given or by asking once:
- what is reviewed: screenshot(s), source files, a URL or local page, a design-tool export
- platform: web, Android (Compose or Views), Flutter, iOS, cross-platform
- form factor and window size class: compact (< 600), medium (600-839), expanded (840-1199), large or extra-large
- light, dark, or both; whether a high-contrast or reduced-motion variant exists

If the surface shows personal data (names, amounts, addresses, messages, health or account data), say so at the top
of the reply and suggest reviewing a redacted or demo state. Do not store screenshots or page data in files, memory or
the ledger. Quote only the minimum text needed to identify an element.

### Step 1. Load the adapter

Follow `references/adapter-protocol.md`: look for project design guidelines, a decisions ledger and a change-list
format. If none is found, ask once with a single short question; if the user does not answer or says there are none,
continue with M3 only and the default formats.

### Step 2. Choose the tolerance

`strict` or `inspired` (see Tolerance). Do not ask if the user or the guidelines already decided.

### Step 3. Measure

Prefer measurement over estimation. In this order:

1. Rendered page available (Playwright, a browser automation tool, DevTools): evaluate `scripts/measure.js` in the
   page and use its JSON. See `references/measurement.md` for how to run it, the meaning of each field and its limits.
   Measure each relevant viewport (for example 390 px and 1280 px) and theme (light and dark) separately.
2. Only source code available: read the CSS/HTML/JS or component code; compute sizes, colors and radii from it.
3. Only images available: estimate, label `estimated`, and ask for the scale if exact numbers matter.

Treat the script output as candidates, not verdicts: confirm each one against the rule before reporting it.
The script cannot see everything (pseudo-element hit areas, state styles, motion); check those in code or by
interaction when it matters.

When the script reports a contrast it could not resolve (gradient, image or semi-transparent background), compute the
worst case by hand: take the darkest and lightest stop under the text, or composite the alpha color over the actual
background; report the result as `estimated` with the stops used. For `color-mix()` or alpha text colors, use the
final composited color, not the declared one. If the page has no dark variant, say so once as a single finding
(rule on theme parity in `references/color.md`) and do not repeat it per element.

### Step 4. Load only the relevant references

Progressive disclosure: never load all reference files. Pick by what is on screen.

| Surface contains | Load |
| --- | --- |
| Any surface (always) | `references/layout-interaction-a11y.md`, section "Accessibility floor" first |
| Colors, themes, dark mode, tokens, contrast | `references/color.md` |
| Typography, corners, elevation, spacing, motion, icons | `references/styles.md` |
| App bars, badges, bottom sheets, button groups, buttons, cards, carousel, checkbox, chips, date pickers, dialogs, divider | `references/components-1.md` |
| Extended FAB, FAB menu, FAB, icon buttons, lists, loading indicator, menus, navigation bar / drawer / rail, progress indicators, radio button | `references/components-2.md` |
| Search, segmented buttons, side sheets, sliders, snackbar, split button, switch, tabs, text fields, time pickers, toolbars, tooltips | `references/components-3.md` |
| Expressive features, spring motion, shape morph, or the user asks about Expressive | `references/expressive.md` |
| Writing the report | `references/report-template.md` |
| Recording decisions, change list | `references/adapter-protocol.md` |

Inside a large file, read only the sections for the components on screen. List the headings first
(`grep -n '^## ' references/components-1.md`), then read just those line ranges (`sed -n 'START,ENDp' file`).
If a reference file is missing, say so and continue with the others; do not invent rules to fill the gap.

### Step 5. Check, classify, merge

For each candidate:
1. Find the rule. Cite its ID and its `Source` exactly as in the reference file (`path@lastmod`). When several
   rules overlap (a component rule and a floor rule for the same target size), cite the most specific one as the
   rule and list the other IDs after it ("also A11-01"). If no rule in the references supports it, do not report it
   as an M3 finding; at most mention it as a general usability note, labelled "not an M3 rule" (typical cases: missing
   `lang` attribute, viewport meta that disables zoom).
2. Check the ledger: a recorded deviation is not reported again (mention the count of suppressed items in one line).
3. Check the project guidelines: a conflict with tier C or E goes to "Decision candidates", not to findings.
4. Classify: tier (F, C, E) and kind (issue or suggestion) according to the tolerance. In `inspired` mode, a tier C
   mismatch "harms usability" (so it is an issue) only if it makes content hard to read, hard to operate, or
   ambiguous for a typical user: text under 12 px, a control whose purpose or state is unclear, a layout that
   breaks at a supported width. Otherwise it is a suggestion.
5. Merge repeats: one finding per root cause, with the count and two or three example selectors or regions
   ("14 icon buttons at 32 x 32 px, e.g. `.toolbar button`, `#close`").

Sort by impact: tier F issues first, then issues that affect task completion, then tier C issues, then suggestions.
Within a group, sort by reach (how many elements or screens). Cap the report at about 25 findings; if more exist, say
how many were left out and offer a second pass.

If there are few or no issues, say so plainly. Do not add filler praise. Do not invent problems to fill the report.

### Step 6. Present

Use `references/report-template.md` exactly. Each finding carries:
- ID `F-01`, `F-02`... (a running number for the finding; not the tier)
- area (component or foundation: Buttons, Color, Typography, Layout...)
- tier (F, C or E) and kind (issue or suggestion)
- evidence: selector or image region, the measured or estimated value, and the label `measured` / `estimated`
- rule: rule ID plus `source@lastmod`
- why it matters: one line, user impact first
- proposed change: concrete token, role or value (`min-height: 48px`, `color: var(--md-sys-color-on-surface-variant)`,
  "corner extra-large, 28dp"), not "improve contrast"
- effort: S (one property or token), M (one component or several files), L (structural or cross-screen)
- decision boxes: `[ ] accept  [ ] reject  [ ] deviation`

The report header states: the surface and viewports reviewed, the tolerance, the references snapshot date (the oldest
"snapshot" date in the headers of the reference files loaded), whether project guidelines and a ledger were found, and the evidence
mix (how many findings are measured vs estimated).

Freshness: if the snapshot date is more than 6 months before today, or the user mentions a newer Material release,
say so in the header and offer to verify the affected rules against https://m3.material.io/ before acting on them.

### Step 7. Apply the decisions

When the user answers (for example "accept F-01 to F-05, F-07 deviation: brand pill buttons, reject the rest"):

1. For each `deviation`: append one entry to the decisions ledger (date, rule ID, scope, one-line rationale, finding
   ID) in the format of `references/adapter-protocol.md`. If no ledger exists, propose its path and create it only
   after the user agrees.
2. For each `accept`: emit a change list in the project's format (or the default in the adapter protocol): target
   file or component, change, token or value, rule ID, effort.
3. For each `reject`: record nothing unless the user asks; mention that it may reappear in the next review.
4. Do not implement the changes unless the user asks.

If the user gives no decision for an item, leave it open and list open items at the end.

## Judgement rules

- Review by role and purpose, not by exact hex value: a color is right if its role fits the element and its pair is
  respected.
- Baseline M3 is not wrong for lacking Expressive features. Never report the absence of an Expressive feature as an
  issue.
- Do not require components the platform cannot ship (see availability notes in `references/expressive.md`); a custom
  build is the implementer's choice.
- A visible element may be smaller than its hit area: check the hit area (padding, min sizes, pseudo-elements) before
  reporting a target-size issue.
- Disabled elements are exempt from contrast minimums.
- Distinguish touch targets (48 x 48dp) from pointer-only targets (44 x 44dp): use the touch value unless the surface
  is clearly desktop-only with no touch input.
- Do not report the same root cause under two areas. Pick the area where the fix lives.
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

- `references/report-template.md`: report layout, finding block, decision candidates, change-list section.
- `references/adapter-protocol.md`: where to find project guidelines, the ledger format, the change-list format.
- `references/measurement.md`: how to run `scripts/measure.js`, field meanings, rule mapping, limits.
- `scripts/measure.js`: dependency-free measurement function to evaluate in the page.
- `references/color.md`, `references/styles.md`, `references/layout-interaction-a11y.md`,
  `references/components-1.md`, `references/components-2.md`, `references/components-3.md`,
  `references/expressive.md`: distilled M3 rules. Rule IDs are unique across files (prefixes such as A11, LAY, INT,
  WRT, COL, TOK, TYP, SHP, ELV, SPC, MOT, ICO, EXP and one prefix per component), each with a tier and a
  `path@lastmod` source that maps to `https://m3.material.io/<path>`.
