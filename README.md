# Material 3 skills for Claude

Two complementary skills for designing and checking user interfaces with Material Design 3 (M3):

| Skill | Version | What it does |
| --- | --- | --- |
| `m3-design-brief` | 0.2.0 | Writes self-contained design briefs (project guidelines, screen specs, change specs) that any AI assistant or developer can implement. Design only: it does not write or edit code. |
| `m3-design-review` | 0.4.0 | Reviews an existing UI against M3 and returns a numbered, decision-ready report with measured or estimated evidence. Review only. |

See `CHANGELOG.md`. References snapshot: 2026-11-17.

## How they work together

```
m3-design-brief            any AI tool or developer          m3-design-review
write the brief     ->     implement the brief         ->    review against the brief
(values inline,            (handoff prompt + brief,          (brief = project guidelines;
 acceptance criteria)       no skill needed)                  each AC: pass / fail / not checked)
        ^                                                             |
        +------------- mode "change": accepted findings --------------+
```

1. Write a brief with `m3-design-brief`: `system` for project guidelines, `screen` for one screen, flow or
   component. The brief carries the actual values (hex per theme, dp, type roles, component specs), a paste-ready
   handoff prompt and numbered acceptance criteria (`AC-01`...), each tied to a rule ID, `project` or a WCAG 2.2
   success criterion.
2. Implement it with any AI tool or by hand: paste the handoff prompt and the brief. The implementer does not need
   either skill.
3. Review the result with `m3-design-review`, giving it the brief. The brief counts as project guidelines, its
   decisions (`B-nn`) are respected, and the report adds a "Brief acceptance criteria" section with pass, fail or not
   checked per AC.
4. Turn the accepted findings into a change spec with `m3-design-brief` mode `change`, and repeat.

Both skills share the same rule references (rule IDs, tiers, `path@lastmod` sources) and the same adapter protocol
for project guidelines and the decisions ledger, so a deviation recorded once is respected by both.

## m3-design-brief

- Three modes: `system` (foundations, tokens, component rules, project exceptions, do/don't, accessibility floor,
  review setup), `screen` (purpose, content inventory, layout per window size class, components with specs, states
  including loading, empty and error, interactions, motion with reduced-motion fallback, copy, accessibility, tokens)
  and `change` (per change: location, before, after with exact values, rule, how to verify, effort, grouped by
  shared component or token).
- Every value is marked `M3 <RULE-ID>`, `project` or `decision B-nn`; nothing is invented.
- At most three short questions, only when the answer changes the brief; other assumptions become numbered decisions.
- `scripts/m3tokens.py` (Python 3 standard library): `scheme` builds an approximate M3 tonal-spot color scheme from a
  seed color (light and dark, 26 core roles plus fixed roles), `check` tests the contrast of the required role
  pairs, and `export` writes CSS custom properties, W3C design tokens (JSON), Jetpack Compose, Flutter or Tailwind,
  plus the type and shape scales. The export is pasted into the brief, so the implementer does not need the script.
  For exact color values, regenerate from the same seed with Material Theme Builder or material-color-utilities.

## m3-design-review

- Layered precedence: floor rules (tier F) > your project guidelines and recorded decisions > M3 core (tier C) >
  M3 Expressive and optional items (tier E). Two tolerance modes: `strict` and `inspired` (default).
- `scripts/measure.js`: a dependency-free function you evaluate in the page (Playwright, a browser-automation tool or
  DevTools). It checks the viewport setup and reports small effective touch targets, small text, failing text and
  non-text contrast, truncated text, overflow, unnamed controls, label-in-name mismatches, ARIA conflicts, images
  without alt, missing focus indication, headings, custom properties, fonts, corner radii and reduced-motion support.
  It sends nothing anywhere and does not modify the page.
- Four evidence labels: `measured-rendered`, `measured-code`, `measured-simulation`, `estimated`.
- Decisions ledger: accepted deviations are recorded once and not reported again; decision candidates for project
  choices; a change list for accepted items.
- With a design brief: checks every acceptance criterion and reports pass, fail or not checked with evidence.
- Freshness check and privacy rules (no screenshots or page data stored; personal data flagged).

## What they are not

- Not code generators: the brief skill specifies, the review skill audits. Neither edits code unless you ask after
  the decisions are made (review) or you hand the brief to an implementer (brief).
- Not an automated linter: the scripts measure and compute what they can; the rest is reasoned and labelled.
- Not affiliated with, endorsed by, or sponsored by Google. "Material Design" is used only to name the guidelines
  the skills are based on.

## Install

Download the newest ZIPs (stable links, always the latest version):

- [m3-design-review.zip](https://github.com/sbk-jdm/m3-skills/releases/download/latest-m3-design-review/m3-design-review.zip)
- [m3-design-brief.zip](https://github.com/sbk-jdm/m3-skills/releases/download/latest-m3-design-brief/m3-design-brief.zip)

Or take a specific version from [Releases](https://github.com/sbk-jdm/m3-skills/releases) (tags `<skill>/vX.Y.Z`), or build
them yourself (`python3 maintenance/build-zip.py`, see `maintenance/UPDATING.md`). Each ZIP's root is the skill's
folder (`m3-design-brief/` or `m3-design-review/`), which contains `SKILL.md`. Install one or both.

### claude.ai

1. Make sure code execution is enabled in your settings (skills require it).
2. Go to Customize > Skills, click "+", choose "Create skill", then "Upload a skill".
3. Upload `m3-design-brief.zip`; repeat for `m3-design-review.zip`.

Skills enabled in a claude.ai account are also available in Claude Code when you are signed in with the same account
(listed under "claude.ai sync").

### Claude Code (manual)

Copy the skill folders:

```
# personal, all projects
cp -r skills/m3-design-brief skills/m3-design-review ~/.claude/skills/

# one project only
cp -r skills/m3-design-brief skills/m3-design-review .claude/skills/
```

If a skill does not appear, start a new session.

## Usage examples

m3-design-brief, mode `system`:
- "Write Material 3 design guidelines for our web app. Brand color #1B6EF3, light and dark, phones and desktop."
- "We have tokens in `src/theme.css`: turn them into project design guidelines for M3, inspired mode."

m3-design-brief, mode `screen`:
- "Write an M3 brief for a settings screen of an Android app in Jetpack Compose, compact and expanded."
- "Spec the checkout flow so another AI can build it in React with CSS custom properties. Follow `DESIGN.md`."

m3-design-brief, mode `change`:
- "Turn the accepted findings of this review (accept F-01 to F-06, N-01) into a change spec for the developers."
- "Write a change spec: the filter row must become a segmented button and all icon buttons need 48dp targets."

m3-design-review:
- "Review this screen against Material 3." (attach a screenshot, and say the viewport width if you know it)
- "Run an M3 design review of http://localhost:5173/settings at 390 px and 1280 px, light and dark."
- "Review the settings page against `docs/design/briefs/2026-11-17-settings.md` and report the acceptance criteria."
- "Accept F-01 to F-06, F-08 is a deviation: our brand uses 8dp button corners. Reject the rest."

For exact measurements in a review, give the assistant a browser tool (for example Playwright) so it can run
`scripts/measure.js`. With screenshots only, findings are labelled `estimated`.

## Repository layout

```
skills/m3-design-review/           review skill (canonical copy of the shared references)
  SKILL.md
  scripts/measure.js
  references/  report-template.md  measurement.md  + shared files
skills/m3-design-brief/            brief skill
  SKILL.md
  scripts/m3tokens.py
  references/  brief-method.md  brief-template.md  color-scheme.md  platform-mapping.md  + shared files
shared references (identical in both skills):
  adapter-protocol.md  color.md  styles.md  layout-interaction-a11y.md
  components-1.md  components-2.md  components-3.md  expressive.md
test/                              review: seeded page and runner; brief/: tests for m3tokens.py
maintenance/                       update procedure, sync-shared.py, build-zip.py
CHANGELOG.md                       version history
```

Edit shared references only in `skills/m3-design-review/references/`, then run
`python3 maintenance/sync-shared.py`; the ZIP build fails if the copies differ.

## How the references are structured

The reference files are distilled from the Material Design 3 documentation. Each starts with a header stating the
snapshot date and base URL, followed by rule tables:

```
| ID | Rule | Value / criterion | Tier | Source |
```

- ID: area prefix and number (for example `A11-01`, `COL-05`, `BTN-03`), unique across the references.
- Tier: `F` floor (accessibility/usability minimum), `C` core M3 (a deviation needs an explicit decision),
  `E` Expressive-only, optional or platform-specific.
- Source: `path@lastmod`, where `path` maps to `https://m3.material.io/<path>` and `lastmod` is that page's
  last-modified date at snapshot time; or `WCAG 2.2 SC x.y.z`, `WAI-ARIA APG <pattern>`, `heuristic`.

Component files use the same subsections for every component: Use, Dimensions & shape, Color roles, Do / Don't,
Accessibility, Review checks, and the rules table.

## Testing

```
python3 test/check.py                                    # review: measure.js on the seeded page (Playwright)
python3 -m unittest discover -s test/brief -v            # brief: m3tokens.py
python3 maintenance/sync-shared.py --check               # shared references in sync
python3 maintenance/build-zip.py                         # both ZIPs, with frontmatter and reproducibility checks
```

## Updating the references

See `maintenance/UPDATING.md`: re-sync a mirror of the official docs, diff `lastmod` dates, re-distill only the
changed pages, bump the snapshot date, sync the shared copies, run the tests and rebuild the ZIPs.

## License and attribution

Code and original text: MIT (see `LICENSE`). The reference files are distilled and modified from the Material Design 3
documentation, which its site states is available under Apache 2.0 or CC BY 4.0; see `NOTICE.md`. No images or
videos from the documentation are included. WCAG 2.2 and the WAI-ARIA Authoring Practices Guide are cited by
reference only.

This project is not affiliated with Google.
