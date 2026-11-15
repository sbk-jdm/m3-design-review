# m3-design-review

A skill for Claude that reviews an existing user interface against Material Design 3 (M3) and returns a numbered,
decision-ready report. You decide on each finding (accept, reject, or record as a deliberate deviation); the skill then
records the deviations and gives you the accepted items as a change list.

It reviews screenshots, HTML/CSS/JS, rendered pages (through a browser tool) and design-tool exports.

## What it is not

- Not a UI generator. It does not build screens, themes or components from scratch.
- Not an automated linter. A bundled script measures what can be measured in a browser; the rest is a reasoned review.
- Not affiliated with, endorsed by, or sponsored by Google. "Material Design" is used only to name the guidelines
  the review is based on.

## How it differs from build-oriented Material 3 skills

| | Build-oriented skills | m3-design-review |
| --- | --- | --- |
| Goal | Produce M3 code or designs | Audit an existing UI and support decisions |
| Output | Code | Numbered findings with accept / reject / deviation boxes, then a change list |
| Evidence | Not the focus | Every finding labelled `measured` (computed styles or code) or `estimated` (image) |
| Traceability | Sources are typically listed for the skill as a whole | Every finding cites a rule ID and the source page with its last-modified date |
| Priorities | Applying M3 faithfully | Floor rules first: accessibility and usability minimums are never negotiable |
| Project fit | Focus on pure M3 | Reads your project's guidelines and decisions ledger; conflicts become "decision candidates", not violations |

This table describes the focus of this skill, not a judgement of other skills; they are complementary and can be
installed together.

## Features

- Layered precedence: floor rules (tier F) > your project guidelines and recorded decisions > M3 core (tier C) >
  M3 Expressive and optional items (tier E).
- Two tolerance modes: `strict` and `inspired` (default). In `inspired`, core mismatches are suggestions unless they
  harm usability.
- `scripts/measure.js`: a dependency-free function you evaluate in the page (Playwright, a browser-automation tool or
  DevTools). It reports small touch targets, small text, failing text contrast, unnamed controls, images without
  alt, missing focus indication, `:root` custom properties, font families, a corner-radius histogram and whether a
  reduced-motion query exists. It sends nothing anywhere and does not modify the page.
- Progressive disclosure: only the reference files relevant to the surface are loaded.
- Decisions ledger: accepted deviations are recorded once and not reported again.
- Freshness check: the report states the snapshot date of the references and warns when it is older than six months.
- Privacy: no screenshots or page data are stored; if personal data is visible, the report says so and suggests a
  redacted state.

## Install

Download `m3-design-review.zip` from the latest GitHub Release of `<USER>/<REPO>`, or build it yourself
(see `maintenance/UPDATING.md`). The ZIP's root is the folder `m3-design-review/`, which contains `SKILL.md`.

### claude.ai

1. Make sure code execution is enabled in your settings (skills require it).
2. Go to Customize > Skills, click "+", choose "Create skill", then "Upload a skill".
3. Upload `m3-design-review.zip`.

Skills enabled in a claude.ai account are also available in Claude Code when you are signed in with the same account
(listed under "claude.ai sync").

### Claude Code (manual)

Copy the skill folder:

```
# personal, all projects
cp -r skills/m3-design-review ~/.claude/skills/

# one project only
cp -r skills/m3-design-review .claude/skills/
```

If the skill does not appear, start a new session.

## Usage examples

- "Review this screen against Material 3." (attach a screenshot, and say the viewport width if you know it)
- "Run an M3 design review of http://localhost:5173/settings at 390 px and 1280 px, light and dark."
- "Audit `src/components/` for Material 3 issues, strict mode."
- "Accept F-01 to F-06, F-08 is a deviation: our brand uses 8dp button corners. Reject the rest."

For exact measurements, give the assistant a browser tool (for example Playwright) so it can run
`scripts/measure.js`. With screenshots only, findings are labelled `estimated`.

## Repository layout

```
skills/m3-design-review/
  SKILL.md                         workflow, precedence, tolerance, evidence rules
  scripts/measure.js               in-page measurement function
  references/
    report-template.md             report layout and finding block
    adapter-protocol.md            project guidelines, decisions ledger, change-list format
    measurement.md                 how to run measure.js, field meanings, limits
    color.md  styles.md  layout-interaction-a11y.md
    components-1.md  components-2.md  components-3.md  expressive.md
test/                              seeded test page, expected results, runner
maintenance/                       update procedure and ZIP build script
```

## How the references are structured

The reference files are distilled from the Material Design 3 documentation. Each starts with a header stating the
snapshot date and base URL, followed by rule tables:

```
| ID | Rule | Value / criterion | Tier | Source |
```

- ID: area prefix and number (for example `A11-01`, `COL-05`, `BTN-03`), unique across the skill.
- Tier: `F` floor (accessibility/usability minimum), `C` core M3 (a deviation needs an explicit decision),
  `E` Expressive-only, optional or platform-specific.
- Source: `path@lastmod`, where `path` maps to `https://m3.material.io/<path>` and `lastmod` is that page's
  last-modified date at snapshot time.

Component files use the same subsections for every component: Use, Dimensions & shape, Color roles, Do / Don't,
Accessibility, Review checks, and the rules table.

## Testing

```
python3 test/check.py            # requires Python Playwright and a Chromium-based browser
```

It loads `test/seeded-violations.html`, runs `measure.js` and checks every seeded violation and negative control
listed in `test/EXPECTED.md`, plus that the page was not modified.

## Updating the references

See `maintenance/UPDATING.md`: re-sync a mirror of the official docs, diff `lastmod` dates, re-distill only the
changed pages, bump the snapshot date, run the tests and rebuild the ZIP.

## License and attribution

Code and original text: MIT (see `LICENSE`). The reference files are distilled and modified from the Material Design 3
documentation, which its site states is available under Apache 2.0 or CC BY 4.0; see `NOTICE.md`. No images or
videos from the documentation are included.

This project is not affiliated with Google.
